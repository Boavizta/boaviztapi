from fastapi import APIRouter, Request, HTTPException
from fastapi.params import Depends
from fastapi.responses import RedirectResponse

from boaviztapi.dto.auth.user_dto import UserPublicDTO
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

        # Check double submit cookie
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