from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

try:
    from backend.app.config import settings
    from backend.app.core.dependencies import ACCESS_COOKIE_NAME, AuthenticatedUser, get_current_user, get_db
    from backend.app.database import commit_or_rollback
    from backend.app.core.security import create_access_token, hash_password, verify_password
    from backend.app.models.tenant import AuthSession, Membership, Organization, User
    from backend.app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest
except ModuleNotFoundError:  # pragma: no cover - supports running from backend/ directly
    from app.config import settings
    from app.core.dependencies import ACCESS_COOKIE_NAME, AuthenticatedUser, get_current_user, get_db
    from app.database import commit_or_rollback
    from app.core.security import create_access_token, hash_password, verify_password
    from app.models.tenant import AuthSession, Membership, Organization, User
    from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _create_auth_session(user: User, db: Session) -> tuple[str, datetime]:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    auth_session = AuthSession(user_id=user.id, expires_at=expires_at)
    db.add(auth_session)
    db.flush()
    token = create_access_token(
        user.id,
        auth_session.id,
        settings.auth_token_secret.get_secret_value(),
        settings.access_token_expire_minutes,
    )
    return token, expires_at


def _set_auth_cookie(response: Response, token: str, expires_at: datetime) -> None:
    max_age = max(0, int((expires_at - datetime.now(timezone.utc)).total_seconds()))
    response.set_cookie(
        key=ACCESS_COOKIE_NAME,
        value=token,
        max_age=max_age,
        expires=max_age,
        httponly=True,
        secure=settings.environment.lower() == "production",
        samesite="lax",
        path="/api",
    )


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(
    payload: RegisterRequest, response: Response, db: Session = Depends(get_db)
) -> AuthResponse:
    user = User(email=str(payload.email).strip().lower(), password_hash=hash_password(payload.password))
    organization = Organization(name=payload.organization_name)
    try:
        db.add_all([user, organization])
        db.flush()
        db.add(Membership(user_id=user.id, organization_id=organization.id, role="owner"))
        token, expires_at = _create_auth_session(user, db)
        commit_or_rollback(db)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="An account with that email exists") from None
    _set_auth_cookie(response, token, expires_at)
    return AuthResponse(user_id=user.id)


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)) -> AuthResponse:
    user = db.scalar(select(User).where(func.lower(User.email) == str(payload.email).strip().lower()))
    if user is None or not user.is_active or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token, expires_at = _create_auth_session(user, db)
    commit_or_rollback(db)
    _set_auth_cookie(response, token, expires_at)
    return AuthResponse(user_id=user.id)


@router.get("/session", response_model=AuthResponse)
def current_session(current_user: AuthenticatedUser = Depends(get_current_user)) -> AuthResponse:
    return AuthResponse(user_id=current_user.id)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    auth_session = db.get(AuthSession, current_user.session_id)
    if auth_session is not None and auth_session.revoked_at is None:
        auth_session.revoked_at = datetime.now(timezone.utc)
        commit_or_rollback(db)
    response.delete_cookie(
        key=ACCESS_COOKIE_NAME,
        httponly=True,
        secure=settings.environment.lower() == "production",
        samesite="lax",
        path="/api",
    )
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get("/status")
async def auth_status() -> dict[str, str]:
    return {"status": "auth-module-ready", "provider": "local", "registration": "enabled"}
