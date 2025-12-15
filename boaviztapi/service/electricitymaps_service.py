import logging

import requests

from boaviztapi.application_context import get_app_context
from boaviztapi.service.base import BaseService
from boaviztapi.service.exceptions import APIAuthenticationError, APIError, APIMissingValueError

_log = logging.getLogger(__name__)

class ElectricityMapsService(BaseService):

    base_url = "https://api.electricitymaps.com/v3"

    @staticmethod
    def _get_api_key():
        ctx = get_app_context()
        api_token = ctx.ELECTRICITYMAPS_API_KEY
        if not api_token:
            raise APIAuthenticationError("No ElectricityMaps API key found!")
        return api_token

    @staticmethod
    def _perform_request(url: str):
        api_token = ElectricityMapsService._get_api_key()
        r = requests.get(url, headers={"auth-token": api_token})
        if r.status_code == 401:
            raise APIAuthenticationError(msg="Invalid ElectricityMaps API key.", logger=_log)
        if r.status_code == 404:
            raise APIMissingValueError(msg="No data was found for the requested zone.", logger=_log)
        elif r.status_code != 200:
            raise APIError(msg="Unexpected response from ElectricityMaps API.", status_code=r.status_code, logger=_log)
        return r.json()