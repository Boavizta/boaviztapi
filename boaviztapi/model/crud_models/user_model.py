from datetime import datetime, UTC
from typing import Optional

from bson import ObjectId
from pydantic import Field, ConfigDict

from boaviztapi.dto.auth.user_dto import UserPublicDTO
from boaviztapi.model.crud_models.basemodel import BaseCRUDModel, BaseCRUDUpdateModel, BaseCRUDCollection


class UserModel(BaseCRUDModel):
    sub: str = Field(...)
    registration_date: datetime = Field(...)
    last_seen_date: datetime = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "sub": "1234567890",
                "registration_date": "2023-01-01T00:00:00.000Z",
                "last_seen_date": "2025-01-01T00:00:00.000Z"
            }
        }
    )

    @classmethod
    def from_user_dto(cls, user: UserPublicDTO):
        """Create UserModel from UserPublicDTO"""
        return cls(
            sub=user.sub,
            registration_date=datetime.now(UTC),
            last_seen_date=datetime.now(UTC)
        )


class UpdateUserModel(BaseCRUDUpdateModel):
    sub: Optional[str] = None
    registration_date: Optional[datetime] = None
    last_seen_date: Optional[datetime] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "sub": "1234567890",
                "registration_date": "2023-01-01T00:00:00.000Z",
                "last_seen_date": "2025-01-01T00:00:00.000Z"
            }
        }
    )

class UserCollection(BaseCRUDCollection[UserModel]):
    """
    A container holding a list of `UserModel` objects.
    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """