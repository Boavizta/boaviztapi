import logging

import requests

from typing import Mapping, Any, Annotated
from datetime import datetime, timezone
from urllib.parse import urlencode

from fastapi import APIRouter, Request, HTTPException, Form, Query
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from pymongo.asynchronous.collection import AsyncCollection
from respx import router

import jwt

from boaviztapi.application_context import get_app_context
from boaviztapi.dto.auth.user_dto import UserPublicDTO, GoogleJwtPayload
from boaviztapi.model.crud_models.user_model import UserModel, UserCollection
from boaviztapi.routers.pydantic_based_router import GenericPydanticCRUDService
from boaviztapi.service.auth.dependencies import get_current_user
from boaviztapi.service.auth.google_auth_service import GoogleAuthService
from boaviztapi.utils.auth_backend import create_access_token

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

_log = logging.getLogger(__name__)

FRONTEND_URL = "http://localhost:3000"

@auth_router.post('/google/callback', description="TODO")
async def google_signin_callback(
        request: Request,
        credential: Annotated[str, Form()],
        next: Annotated[str, Query()] = "/",
        g_csrf_token: Annotated[str | None, Form()] = None
        ):

        # csrf_token_cookie = request.cookies.get('g_csrf_token')
        # csrf_token_body = form['g_csrf_token']
        # verify_double_submit_cookie(csrf_token_cookie, csrf_token_body)

        # Verify the ID token
        try:
            google_jwt_payload = GoogleAuthService.verify_jwt(credential)
            if not google_jwt_payload:
                raise HTTPException(status_code=401, detail="Google sign-in failed, missing credential!")
            access_token = create_access_token(data=google_jwt_payload.model_dump(exclude={"aud"}))
            params = urlencode({"token": access_token, "next": next})

            service = get_crud_service()
            try:
                if (
                    user := await service.get_one_by_filter({"sub": google_jwt_payload.sub})
                ) is not None:
                    # The user already exists, just update his/her last seen date
                    user_model = UserModel(sub=user.sub,
                                           registration_date=user.registration_date,
                                           last_seen_date=datetime.now(timezone.utc),
                                           **user.model_dump(exclude={"sub", "registration_date", "last_seen_date"}))
                    await service.update(user.id, user_model)
            except HTTPException as e:
                # The user does not exist, create a new one
                await service.create(UserModel.from_user_dto(UserPublicDTO.from_google_jwt(google_jwt_payload)))
        except Exception as e:
            _log.exception(e)
            error_params = urlencode({"error": str(e), "next": next})
            return RedirectResponse(f"{request.headers.get('origin')}?{error_params}", status_code=303)
        #TODO: add nonce verification by sending it to the frontend on nextjs startup
        return RedirectResponse(status_code=303, url=f"{request.headers.get('origin')}/#{params}")

@auth_router.get('/discord/callback', description="TODO")
async def discord_signin_callback(
        req: Request,
        code: str = Query(),
        next: Annotated[str, Query()] = "/"
        ):
    app = get_app_context()

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': app.DISCORD_REDIRECT_URL
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    token_response = requests.post("https://discord.com/api/v10/oauth2/token", data=data, headers=headers, auth=(app.DISCORD_CLIENT_ID, app.DISCORD_CLIENT_SECRET))
    token_response.raise_for_status()

    token_json = token_response.json()
    access_token = token_json['access_token']

    user_response = requests.get("https://discord.com/api/v10/users/@me", headers={
        'Authorization': 'Bearer ' + token_json['access_token']
    })
    user_response.raise_for_status()

    discord_user = user_response.json()

    discord_payload = {
        "sub": discord_user['id'],
        "email": discord_user.get('email'),
        "name": discord_user.get('global_name') or discord_user['username'],
        "picture": f"https://cdn.discordapp.com/avatars/{discord_user['id']}/{discord_user['avatar']}.png" if discord_user.get(
            'avatar') else None,
    }

    params = urlencode({"token": create_access_token(discord_payload), "next": next})

    service = get_crud_service()
    try:
        if (user := await service.get_one_by_filter({"sub": discord_payload["sub"]})) is not None:
            user_model = UserModel(
                sub=user.sub,
                registration_date=user.registration_date,
                last_seen_date=datetime.now(timezone.utc),
                **user.model_dump(exclude={"sub", "registration_date", "last_seen_date"})
            )
            await service.update(user.id, user_model)
        else:
            await service.create(UserModel.from_discord_user(discord_payload))
    except HTTPException:
        await service.create(UserModel.from_discord_user(discord_payload))

    return RedirectResponse(
        status_code=303,
        url=f"{FRONTEND_URL}/#{params}"
    )

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

    db = ctx.mongodb_client.get_database(ctx.database_name)
    return db.get_collection(name="users")

def get_crud_service() -> GenericPydanticCRUDService[UserModel]:
    return GenericPydanticCRUDService(
        model_class=UserModel,
        collection_class=UserCollection,
        mongo_collection=get_user_collection(),
        collection_name="users"
    )