# middleware/logging.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
from utils.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all requests and responses
    
    WHY: Track every API call for debugging and monitoring
    HOW: Intercepts all requests, logs details, measures time
    WHEN: Every single request passes through this
    """
    
    async def dispatch(self, request: Request, call_next):
        # Start timer
        start_time = time.time()
        
        # Get request details
        method = request.method
        path = request.url.path
        client_ip = request.client.host if request.client else "unknown"
        
        # Log incoming request
        logger.info(f" {method} {path} | Client: {client_ip}")
        
        # Process request
        try:
            response = await call_next(request)
        except Exception as e:
            # Log if request crashes
            logger.error(f" Request failed: {method} {path} | Error: {str(e)}")
            raise
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        status_code = response.status_code
        
        # Color-code by status
        if status_code < 400:
            Symbol = "OK"
            level = "info"
        elif status_code < 500:
            Symbol = "!!"
            level = "warning"
        else:
            Symbol = "XX"
            level = "error"
        
        log_message = (
            f"{Symbol} {method} {path} | "
            f"Status: {status_code} | "
            f"Time: {process_time:.3f}s"
        )
        
        getattr(logger, level)(log_message)
        
        # Add custom header with processing time
        response.headers["X-Process-Time"] = str(process_time)
        
        return response

