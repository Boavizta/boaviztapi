class APIError(Exception):
    """Base exception for API errors"""
    pass

class APIAuthenticationError(APIError):
    """Raised when there's an authentication error in the API call"""
    pass

class APIResponseParsingError(APIError):
    """Raised when there's an error in the API response format, or the API response schema is unexpected"""
    pass

class APIMissingValueError(APIError):
    """Raised when there's a missing value in the API call"""
    pass