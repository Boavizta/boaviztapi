import os
from typing import Mapping, Any
from datetime import datetime, UTC
from fastapi import APIRouter, Request, HTTPException
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from pymongo.asynchronous.collection import AsyncCollection

from boaviztapi.application_context import get_app_context
from boaviztapi.dto.auth.user_dto import UserPublicDTO
from boaviztapi.model.crud_models.user_model import UserModel, UserCollection
from boaviztapi.routers.pydantic_based_router import GenericPydanticCRUDService
from boaviztapi.service.auth.dependencies import get_current_user
from boaviztapi.service.auth.google_auth_service import GoogleAuthService

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@auth_router.post('/google/callback', description="TODO")
async def google_signin_callback(request: Request):
    async with request.form() as form:
        request_origin = request.headers.get('origin')
        if not form:
            raise HTTPException(status_code=400, detail="Google sign-in failed, missing request body!")

        # Check double submit cookie only in development environment (prone to CSRF attacks)
        # For prod environments, we verify the token using google's public key only (cookies can get deleted
        # due to domain mismatch)
        if (os.getenv("PROD_ENVIRONMENT", 0)) == 0:
            csrf_token_cookie = request.cookies.get('g_csrf_token')
            csrf_token_body = form['g_csrf_token']
            verify_double_submit_cookie(csrf_token_cookie, csrf_token_body)

        # Verify the ID token
        try:
            google_jwt_payload = GoogleAuthService.verify_jwt(form['credential'])
            if not google_jwt_payload:
                raise HTTPException(status_code=401, detail="Google sign-in failed, missing credential!")
            request.session['user'] = UserPublicDTO.from_google_jwt(google_jwt_payload).model_dump_json()
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e)) from e

        service = get_crud_service()
        try:
            if (
                user := await service.get_one_by_filter({"sub": google_jwt_payload.sub})
            ) is not None:
                # The user already exists, just update his/her last seen date
                user_model = UserModel(sub=user.sub, registration_date=user.registration_date,
                                       last_seen_date=datetime.now(UTC))
                await service.update(user.id, user_model)
        except HTTPException as e:
            # The user does not exist, create a new one
            await service.create(UserModel.from_user_dto(await get_current_user(request)))

        #TODO: add nonce verification by sending it to the frontend on nextjs startup
        return RedirectResponse(status_code=303, url=request_origin)

@auth_router.post('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(status_code=303, url='/')

@auth_router.get('/user',
    response_model=UserPublicDTO,
    summary="Get current user",
    responses={
        401: {"description": "Not authenticated"}
    }
)
async def get_me(current_user: UserPublicDTO = Depends(get_current_user)):
    """
    Get the current authenticated user from the HTTPS session.
    Requires a valid session cookie.
    """
    return current_user

def verify_double_submit_cookie(csrf_token_cookie: str, csrf_token_body: str):
    if not csrf_token_cookie:
        raise HTTPException(status_code=400, detail="Google CSRF token not found in cookies")
    if not csrf_token_body:
        raise HTTPException(status_code=400, detail="Google CSRF token not found in body")
    if csrf_token_cookie != csrf_token_body:
        raise HTTPException(status_code=400,
                            detail="Google CSRF token mismatch. Failed to verify double submit cookie.")

def get_user_collection() -> AsyncCollection[Mapping[str, Any] | Any]:
    ctx = get_app_context()
    if ctx.mongodb_client is None:
        raise HTTPException(status_code=503, detail="MongoDB is not available!")

    db = ctx.mongodb_client.get_database(name="development")
    return db.get_collection(name="users")

def get_crud_service() -> GenericPydanticCRUDService[UserModel]:
    return GenericPydanticCRUDService(
        model_class=UserModel,
        collection_class=UserCollection,
        mongo_collection=get_user_collection(),
        collection_name="users"
    )