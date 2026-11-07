from collections.abc import Generator
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID

from fastapi import Cookie, Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import func, select
from sqlalchemy.orm import Session

try:
    from backend.app.config import settings
    from backend.app.core.security import decode_access_token
    from backend.app.database import SessionLocal
    from backend.app.models.tenant import AuthSession, Membership, User
except ModuleNotFoundError:  # pragma: no cover - supports running from backend/ directly
    from app.config import settings
    from app.core.security import decode_access_token
    from app.database import SessionLocal
    from app.models.tenant import AuthSession, Membership, User

bearer_scheme = HTTPBearer(auto_error=False)
ACCESS_COOKIE_NAME = "getclient_access_token"


@dataclass(frozen=True)
class AuthenticatedUser:
    id: UUID
    session_id: UUID
    user: User


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            if session.in_transaction():
                session.rollback()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
    access_cookie: Annotated[str | None, Cookie(alias=ACCESS_COOKIE_NAME)] = None,
) -> AuthenticatedUser:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing access token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = credentials.credentials if credentials is not None else access_cookie
    if token is None:
        raise unauthorized
    try:
        user_id, session_id = decode_access_token(
            token, settings.auth_token_secret.get_secret_value()
        )
    except ValueError:
        raise unauthorized from None

    user = db.get(User, user_id)
    auth_session = db.scalar(
        select(AuthSession).where(
            AuthSession.id == session_id,
            AuthSession.user_id == user_id,
            AuthSession.revoked_at.is_(None),
            AuthSession.expires_at > func.now(),
        )
    )
    if user is None or not user.is_active or auth_session is None:
        raise unauthorized
    return AuthenticatedUser(id=user.id, session_id=session_id, user=user)


def get_current_membership(
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    organization_id: Annotated[UUID | None, Header(alias="X-Organization-ID")] = None,
) -> Membership:
    query = select(Membership).where(Membership.user_id == current_user.id)
    if organization_id is not None:
        membership = db.scalar(query.where(Membership.organization_id == organization_id))
        if membership is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organisation access denied")
        return membership

    memberships = db.scalars(query.order_by(Membership.created_at, Membership.id)).all()
    if not memberships:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No organisation membership")
    if len(memberships) > 1:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Multiple organisation memberships require an explicit server-validated selection",
        )
    return memberships[0]