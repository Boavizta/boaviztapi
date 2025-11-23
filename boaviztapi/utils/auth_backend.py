from datetime import timedelta, datetime, timezone

from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
    UnauthenticatedUser
)
from starlette.requests import HTTPConnection
import jwt
import os

from boaviztapi.dto.auth.user_dto import UserPublicDTO, GoogleJwtPayload

# Configuration (Same as your security.py)
SECRET_KEY = os.getenv("SESSION_MIDDLEWARE_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 Hours

class JWTAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection):
        if "Authorization" not in conn.headers:
            return

        auth = conn.headers["Authorization"]
        try:
            scheme, token = auth.split()
            if scheme.lower() != 'bearer':
                return
        except ValueError:
            return

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")

            if user_id is None:
                raise AuthenticationError("Invalid token payload")

        except jwt.PyJWTError as e:
            raise AuthenticationError(f"Invalid token: {e}")

        # 'authenticated' is a scope required by @requires('authenticated') decorator
        scopes = ["authenticated"]
        user = UserPublicDTO(**payload)

        return AuthCredentials(scopes), user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Creates a JSON Web Token (JWT) with an expiration time.
    """
    to_encode = data.copy()
    # Determine expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add 'exp' claim (Expiration)
    to_encode.update({"exp": expire})

    # Encode the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
