from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class BusinessProfileInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    business_name: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    industry: str = Field(min_length=1, max_length=160)
    website: HttpUrl
    location: str = Field(min_length=1, max_length=200)
    products_and_services: str = Field(min_length=1)
    target_market: str = Field(min_length=1)
    unique_value_proposition: str = Field(min_length=1)
    communication_style: str = Field(min_length=1, max_length=80)


class BusinessProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    business_name: str
    description: str
    industry: str
    website: str
    location: str
    products_and_services: str
    target_market: str
    unique_value_proposition: str
    communication_style: str
    created_at: datetime
    updated_at: datetime