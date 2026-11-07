from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

try:
    from backend.app.core.dependencies import get_current_membership, get_db
    from backend.app.database import commit_or_rollback
    from backend.app.models.business import BusinessProfile
    from backend.app.models.tenant import Membership
    from backend.app.schemas.business import BusinessProfileInput, BusinessProfileResponse
except ModuleNotFoundError:  # pragma: no cover - supports running from backend/ directly
    from app.core.dependencies import get_current_membership, get_db
    from app.database import commit_or_rollback
    from app.models.business import BusinessProfile
    from app.models.tenant import Membership
    from app.schemas.business import BusinessProfileInput, BusinessProfileResponse

router = APIRouter(prefix="/api/business-profile", tags=["business profile"])


@router.get("", response_model=BusinessProfileResponse)
def get_business_profile(
    membership: Membership = Depends(get_current_membership), db: Session = Depends(get_db)
) -> BusinessProfileResponse:
    profile = db.scalar(
        select(BusinessProfile).where(BusinessProfile.organization_id == membership.organization_id)
    )
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business profile not configured")
    return BusinessProfileResponse.model_validate(profile)


@router.put("", response_model=BusinessProfileResponse)
def save_business_profile(
    payload: BusinessProfileInput,
    membership: Membership = Depends(get_current_membership),
    db: Session = Depends(get_db),
) -> BusinessProfileResponse:
    profile = db.scalar(
        select(BusinessProfile).where(BusinessProfile.organization_id == membership.organization_id)
    )
    values = payload.model_dump(mode="json")
    if profile is None:
        profile = BusinessProfile(organization_id=membership.organization_id, **values)
        db.add(profile)
    else:
        for field, value in values.items():
            setattr(profile, field, value)
    commit_or_rollback(db)
    db.refresh(profile)
    return BusinessProfileResponse.model_validate(profile)