from datetime import datetime, timezone
from typing import Optional, Any

from pydantic import BaseModel
from starlette.authentication import BaseUser

from boaviztapi.dto import BaseDTO

class GoogleJwtPayload(BaseDTO):
    iss: str = None
    azp: str = None
    aud: str = None
    sub: str = None
    email: str = None
    email_verified: bool = None
    nonce: str = None
    nbf: int = None
    name: str = None
    picture: str = None
    given_name: str = None
    family_name: str = None
    iat: int = None
    exp: int = None
    jti: str = None

class UserPublicDTO(BaseModel, BaseUser):
    sub: str = None
    email: Optional[str] = None
    picture: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None

    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)


    @property
    def is_authenticated(self) -> bool:
        if self.sub is None:
            return False
        return True

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def identity(self) -> str:
        return self.sub

    def __str__(self):
        return f"{self.name} ({self.email})"

    @classmethod
    def from_google_jwt(cls, jwt_payload: GoogleJwtPayload) -> "UserPublicDTO":
        """Create UserPublicDTO from Google JWT payload"""
        return cls(
            sub=jwt_payload.sub,
            email=jwt_payload.email,
            picture=jwt_payload.picture,
            name=jwt_payload.name,
            given_name=jwt_payload.given_name,
            family_name=jwt_payload.family_name
        )
