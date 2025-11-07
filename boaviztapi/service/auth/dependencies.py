from fastapi import Request, HTTPException, status, Depends
from fastapi.security import APIKeyCookie
from boaviztapi.dto.auth.user_dto import UserPublicDTO

# Document in OpenAPI
session_cookie = APIKeyCookie(name="session", auto_error=False)

async def get_current_user(
        request: Request,
        session_id: str = Depends(session_cookie)  # Documents in OpenAPI
) -> UserPublicDTO:
    """
    Documented session authentication.
    Uses middleware's request.user if available.
    """
    # Middleware already authenticated
    if hasattr(request, 'user') and request.user.is_authenticated:
        user_data = request.session.get('user')
        if user_data:
            return UserPublicDTO.model_validate_json(user_data)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated"
    )


async def get_current_user_optional(request: Request) -> UserPublicDTO | None:
    """Optional authentication - doesn't raise exception"""
    if hasattr(request, 'user') and request.user.is_authenticated:
        user_data = request.session.get('user')
        if user_data:
            return UserPublicDTO.model_validate_json(user_data)
    return None