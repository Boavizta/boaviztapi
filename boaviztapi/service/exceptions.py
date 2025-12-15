import logging

from fastapi import HTTPException

_log = logging.getLogger(__name__)

class APIError(HTTPException):
    """Base exception for API errors"""
    def __init__(self,
                 detail: str = "No further details were given.",
                 msg: str = "No further details were given.",
                 status_code: int = 500,
                 logger: logging.Logger = _log):
        self.detail = f"""
        {detail}
        {msg}
        Please try again later or contact a system administrator.
        """
        self.msg = msg
        self.status_code = status_code
        logger.error(msg=detail, exc_info=True, extra={"status_code": self.status_code})
        super().__init__(detail=self.detail, status_code=self.status_code)

class APIAuthenticationError(APIError):
    """Raised when there's an authentication error in the API call"""
    def __init__(self, msg: str = None, logger: logging.Logger = _log):
        self.detail = "This request could not be authenticated due to missing or invalid credentials."
        self.msg = msg
        self.status_code = 401
        super().__init__(detail=self.detail, msg=self.msg, status_code=self.status_code)

class APIResponseParsingError(APIError):
    """Raised when there's an error in the API response format, or the API response schema is unexpected"""
    def __init__(self, msg: str = None, logger: logging.Logger = _log):
        self.detail = "This request could not be parsed due to an unexpected response format from the API."
        self.msg = msg
        self.status_code = 422
        super().__init__(detail=self.detail, msg=self.msg, status_code=self.status_code)

class APIMissingValueError(APIError):
    """Raised when there's a missing value in the API call"""
    def __init__(self, msg: str = None, logger: logging.Logger = _log):
        self.detail = "This request could not be parsed due to a missing value in the response format from the API."
        self.msg = msg
        self.status_code = 422
        super().__init__(detail=self.detail, msg=self.msg, status_code=self.status_code)
