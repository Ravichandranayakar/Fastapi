# utils/exceptions.py
from fastapi import HTTPException, status


class BaroException(HTTPException):
    """
    Base exception for BARO API
    
    WHY: Custom exceptions for business logic errors
    HOW: Inherit from HTTPException for FastAPI compatibility
    """
    
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)


class InvalidAPIKeyException(BaroException):
    """API key is invalid or missing"""
    
    def __init__(self, detail: str = "Invalid or missing API key"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class ModelNotLoadedException(BaroException):
    """ML model failed to load"""
    
    def __init__(self, detail: str = "ML model not available"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


class PredictionException(BaroException):
    """Prediction failed"""
    
    def __init__(self, detail: str = "Prediction failed"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class RateLimitException(BaroException):
    """Too many requests"""
    
    def __init__(self, detail: str = "Rate limit exceeded. Try again later."):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )
