from starlette.authentication import (
    AuthenticationBackend,
    SimpleUser,
    AuthCredentials
)
from starlette.requests import HTTPConnection

from boaviztapi.dto.auth.user_dto import UserPublicDTO


class SessionAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection):
        if "user" not in conn.session:
            return None

        user_data = UserPublicDTO.model_validate_json(conn.session["user"])
        return AuthCredentials(["authenticated"]), SimpleUser(user_data.sub)