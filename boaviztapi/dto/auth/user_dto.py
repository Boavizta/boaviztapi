from typing import Optional

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

class UserPublicDTO(BaseDTO):
    sub: str = None
    email: str = None
    picture: str = None
    name: str = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None

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

