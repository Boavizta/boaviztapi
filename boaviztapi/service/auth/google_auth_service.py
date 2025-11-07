import logging

from google.auth.exceptions import GoogleAuthError
from google.oauth2.id_token import verify_oauth2_token
from google.auth.transport import requests

from boaviztapi.application_context import get_app_context
from boaviztapi.dto.auth.user_dto import GoogleJwtPayload
from boaviztapi.service.base import BaseService

_logger = logging.getLogger(__name__)
class GoogleAuthService(BaseService):

    @staticmethod
    def _get_client_credentials():
        ctx = get_app_context()
        _client_id = ctx.GOOGLE_CLIENT_ID
        _client_secret = ctx.GOOGLE_CLIENT_SECRET
        if not _client_id or not _client_secret:
            raise ValueError("No Google client ID or secret found!")
        return _client_id, _client_secret

    @staticmethod
    def verify_jwt(token: str) -> GoogleJwtPayload:
        _client_id, _ = GoogleAuthService._get_client_credentials()
        try:
            decoded_token = verify_oauth2_token(id_token = token,
                                                request = requests.Request(),
                                                audience = _client_id,
                                                clock_skew_in_seconds=300) # 5 mins is default at Okta, seems good enough
        except GoogleAuthError as e:
            _logger.exception(msg= "A GoogleAuthError occurred while verifying the Google JWT token.", exc_info=e)
            raise ValueError("The issuer of the token is invalid or expired.")
        return GoogleJwtPayload(**decoded_token)