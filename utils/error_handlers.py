# utils/error_handlers.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from utils.logger import logger
from utils.exceptions import BaroException
import traceback


async def baro_exception_handler(request: Request, exc: BaroException):
    """
    Handle custom BARO exceptions
    
    WHY: Consistent error format for business logic errors
    WHEN: Any BaroException is raised
    """
    logger.warning(f"BaroException: {exc.detail} | Path: {request.url.path}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "path": str(request.url.path)
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle Pydantic validation errors
    
    WHY: Make validation errors more user-friendly
    WHEN: Request body/params fail Pydantic validation
    """
    errors = [
        {
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        }
        for error in exc.errors()
    ]
    
    logger.warning(f"Validation Error: {errors} | Path: {request.url.path}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": True,
            "message": "Validation failed",
            "details": errors,
            "path": str(request.url.path)
        }
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """
    Catch-all handler for unhandled exceptions
    
    WHY: Never show raw Python tracebacks to users (security!)
    HOW: Log full error, return clean message
    WHEN: Any unhandled exception occurs
    """
    # Log full traceback for debugging
    logger.error(f"Unhandled Exception: {str(exc)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "Internal server error. Please contact support.",
            "path": str(request.url.path)
        }
    )
