from fastapi import Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer

from boaviztapi.dto.auth.user_dto import UserPublicDTO
from boaviztapi.model.services.user_service import UserService

security = HTTPBearer(auto_error=False)


async def get_current_user(
        request: Request,
        token: str = Depends(security)
) -> UserPublicDTO:
    if not request.user.is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = request.user.identity
    service = UserService.get_crud_service()
    user_model = await service.get_one_by_filter({"sub": user_id})

    if not user_model:
        raise HTTPException(status_code=401, detail="User not found")

    return UserPublicDTO.model_validate(user_model)


async def get_current_user_optional(
        request: Request,
        token: str = Depends(security)
) -> UserPublicDTO | None:
    if not request.user.is_authenticated:
        return None

    try:
        user_id = request.user.identity
        service = UserService.get_crud_service()
        user_model = await service.get_one_by_filter({"sub": user_id})

        if user_model:
            return UserPublicDTO.model_validate(user_model)
    except Exception:
        pass

    return None