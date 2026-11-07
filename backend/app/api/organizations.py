from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

try:
    from backend.app.core.dependencies import AuthenticatedUser, get_current_membership, get_current_user, get_db
    from backend.app.database import commit_or_rollback
    from backend.app.models.tenant import Membership, Organization
    from backend.app.schemas.organizations import OrganizationResponse, OrganizationSummary, OrganizationUpdate
except ModuleNotFoundError:  # pragma: no cover - supports running from backend/ directly
    from app.core.dependencies import AuthenticatedUser, get_current_membership, get_current_user, get_db
    from app.database import commit_or_rollback
    from app.models.tenant import Membership, Organization
    from app.schemas.organizations import OrganizationResponse, OrganizationSummary, OrganizationUpdate

router = APIRouter(prefix="/api", tags=["organisations"])


@router.get("/organizations", response_model=list[OrganizationSummary])
def list_organizations(
    current_user: AuthenticatedUser = Depends(get_current_user), db: Session = Depends(get_db)
) -> list[OrganizationSummary]:
    rows = db.execute(
        select(Organization, Membership.role)
        .join(Membership, Membership.organization_id == Organization.id)
        .where(Membership.user_id == current_user.id)
        .order_by(Organization.name, Organization.id)
    ).all()
    return [OrganizationSummary(id=organization.id, name=organization.name, role=role) for organization, role in rows]


@router.get("/organization", response_model=OrganizationResponse)
def get_organization(
    membership: Membership = Depends(get_current_membership), db: Session = Depends(get_db)
) -> OrganizationResponse:
    organization = db.get(Organization, membership.organization_id)
    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organisation not found")
    return OrganizationResponse(id=organization.id, name=organization.name, role=membership.role)


@router.patch("/organization", response_model=OrganizationResponse)
def update_organization(
    payload: OrganizationUpdate,
    membership: Membership = Depends(get_current_membership),
    db: Session = Depends(get_db),
) -> OrganizationResponse:
    if membership.role not in {"owner", "admin"}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient organisation role")
    organization = db.get(Organization, membership.organization_id)
    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organisation not found")
    organization.name = payload.name
    commit_or_rollback(db)
    db.refresh(organization)
    return OrganizationResponse(id=organization.id, name=organization.name, role=membership.role)