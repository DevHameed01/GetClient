from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class OrganizationSummary(BaseModel):
    id: UUID
    name: str
    role: str


class OrganizationResponse(BaseModel):
    id: UUID
    name: str
    role: str


class OrganizationUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=200)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Organisation name cannot be blank")
        return normalized