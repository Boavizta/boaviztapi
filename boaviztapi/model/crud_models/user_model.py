from datetime import datetime, UTC
from typing import Optional

from bson import ObjectId
from pydantic import Field, ConfigDict

from boaviztapi.dto.auth.user_dto import UserPublicDTO
from boaviztapi.model.crud_models.basemodel import BaseCRUDModel, BaseCRUDUpdateModel, BaseCRUDCollection


class UserModel(BaseCRUDModel):
    sub: str = Field(...),
    email: Optional[str] = Field(...)
    picture: Optional[str] = Field(...)
    name: Optional[str] = Field(...)
    given_name: Optional[str] = Field(...)
    family_name: Optional[str] = Field(...)
    registration_date: datetime = Field(...)
    last_seen_date: datetime = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "sub": "1234567890",
                "email": "user@gmail.com",
                "picture": "https://example.com/picture.jpg",
                "name": "John Doe",
                "given_name": "John",
                "family_name": "Doe",
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
            email=user.email,
            picture=user.picture,
            name=user.name,
            given_name=user.given_name,
            family_name=user.family_name,
            registration_date=datetime.now(UTC),
            last_seen_date=datetime.now(UTC)
        )


class UpdateUserModel(BaseCRUDUpdateModel):
    sub: Optional[str] = None
    email: Optional[str] = None
    picture: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    registration_date: Optional[datetime] = None
    last_seen_date: Optional[datetime] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "sub": "1234567890",
                "email": "user@gmail.com",
                "picture": "https://example.com/picture.jpg",
                "name": "John Doe",
                "given_name": "John",
                "family_name": "Doe",
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