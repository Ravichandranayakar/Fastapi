# main.py
from fastapi import FastAPI , Request
from dotenv import load_dotenv
import os

# Import routers
from routers import legal, users, search

# import logger 
from utils.logger import logger 

#importing exception handler
from utils.exceptions import (InvalidAPIKeyException , 
                              ModelNotLoadedException,
                              PredictionException,
                              RateLimitException,
                              BaroException)


# importing error handler 
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field

from utils.error_handlers import (
     baro_exception_handler,
     validation_exception_handler,
     generic_exception_handler
     
 )

from middleware.logging import LoggingMiddleware

from dependencies.models import FakeLegalModel

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title=os.getenv("API_NAME", "BARO AI"),
    version="v1",
    description="Legal AI Assistant - Organized with Routers"
)

# ================= Register middleware =================
app.add_middleware(LoggingMiddleware) 

#================ Exception handler ======================
app.add_exception_handler(BaroException ,baro_exception_handler)
app.add_exception_handler(RequestValidationError,validation_exception_handler)
app.add_exception_handler(Exception , generic_exception_handler)

#============== Lifespan events =====================================
@app.on_event("startup")

async def startup_event():
    """
    Runs ONCE when server starts
    
    WHY: Load heavy resources before first request
    WHAT: ML models, database connections, caches
    WHEN: Server startup (before accepting requests)
    """
    logger.info("=" * 60)
    logger.info(">> BARO AI API Starting...")
    logger.info("   Version: v1.0")
    logger.info(f"  Environment: {os.getenv('DEBUG', 'production')}")
    logger.info("=" * 60)
    
    # Load ML Model
    logger.info(">> Loading ML Model...")
    try:
        app.state.legal_model = FakeLegalModel()
        logger.info(f"OK Model loaded! Version: {app.state.legal_model.model_version}")
    except Exception as e:
        logger.error(f"XX Failed to load model: {str(e)}")
        raise  # Stop server if model fails to load
    
    logger.info("=" * 60)
    logger.info("OK BARO AI API Ready!")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs ONCE when server stops
    
    WHY: Cleanup resources gracefully
    WHAT: Close connections, save state, log shutdown
    WHEN: Server shutdown (Ctrl+C or crash)
    """
    logger.info("=" * 80)
    logger.info("XX BARO AI API Shutting Down...")
    logger.info("Cleaning up resources...")
    
    # Cleanup model (if needed)
    if hasattr(app.state, "legal_model"):
        logger.info("   Unloading ML model...")
        del app.state.legal_model
    
    logger.info("OK Shutdown complete!")
    logger.info("=" * 80)


#=====================================================================
#This code defines a startup hook in FastAPI that runs once when 
#API starts and just prints some log lines using your global
# @app.on_event("startup")
# async def stratup():
#     logger.info("="*50)
#     logger.info("BARO AI API Starting...")
#     logger.info("Testing Logger module")
#     logger.info("=" * 50)

#Async means Python can pause this function 
# at await points and do other work while it waits.

# ============ INCLUDE ROUTERS ============
app.include_router(legal.router)
app.include_router(users.router)
app.include_router(search.router)


# ============ ROOT & HEALTH ENDPOINTS ============
@app.get("/", tags=["Main"])
def root():
    """Welcome endpoint with API information"""
    return {
        "message": "Welcome to BARO AI API",
        "version": "v1",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "legal_analysis": "/legal/analyze",
            "fir_classification": "/legal/fir-classify",
            "user_info": "/users/{user_id}",
            "search": "/search?q=query",
            "Logging test" :"/logging",
            "exception" : "/exception",
            "error handler" : "/use each functions path"
        }
    }
 

@app.get("/health", tags=["Main"])
def health_check(request : Request):
    """Health check endpoint"""
    model_loaded = hasattr(request.app.state , "legal_model")
    model_version = request.app.state.legal_model.model_version if model_loaded  else "N/A"
    return {
        "status": "healthy",
        "app": os.getenv("API_NAME"),
        "Model loaded": True,
        "Model version" : "v1.2.3"
    }


#========= Logging and exceptions ============================
@app.get("/Logging", tags={"Logging Test"})
def test_logger():
    """ Test all log levels"""
    logger.debug("this is DEBUG (wont show - level too low )")
    logger.info("this is info")
    logger.warning(" This is warning")
    logger.error(":this is ERROR")
    return {"message" : "chcek terminal and logs/app.log"}

# Test endpoint 1: Invalid API key

@app.get("/test-invalid-key" , tags=["Exceptions"])
def test_invalid_key():
    """Test Invalidkeyexception"""
    logger.warning("testing invalide = API key exception")
    raise InvalidAPIKeyException()

# Test endpoint 2: Model not loaded

@app.get("/test-model-error" ,  tags=["Exceptions"])

def model_error():
    """Test ModelLoadedException"""
    logger.error("testing model loading exception")
    raise ModelNotLoadedException( detail= "Legal AI model to initialize")


# Test endpoint 3: Prediction failed
@app.get("/test-prediction-error" ,  tags=["Exceptions"])
def test_prediction_error():
    """Test PredictionException"""
    logger.error("Testing prediction exception")
    raise PredictionException(detail="Could not classify the legal document")


# Test endpoint 4: Rate limit
@app.get("/test-rate-limit", tags=["Exceptions"])
def test_rate_limit():
    """Test RateLimitException"""
    logger.warning("Testing rate limit exception")
    raise RateLimitException()


# Test endpoint 5: Custom message
@app.get("/test-custom-message" ,  tags=["Exceptions"])
def test_custom_message():
    """Test exception with custom message"""
    logger.warning("Testing custom error message")
    raise InvalidAPIKeyException(detail="API key 'test-123' is not valid for this endpoint")

#================== with error handler ==============================

# Test 1: Custom exception (InvalidAPIKey)
@app.get("/test-invalid-key" , tags=["Using Error handler"])
def test_invalid_key():
    """Test InvalidAPIKeyException with handler"""
    logger.warning("Testing invalid API key exception")
    raise InvalidAPIKeyException()


# Test 2: Custom exception with custom message
@app.get("/test-model-error" ,tags=["Using Error handler"])
def test_model_error():
    """Test ModelNotLoadedException with handler"""
    logger.error("Testing model loading exception")
    raise ModelNotLoadedException(detail="Legal AI model failed to initialize")


# Test 3: Validation error (Pydantic)
class TestRequest(BaseModel):
    case_text: str = Field(..., min_length=20, max_length=100)
    urgency: str = Field(..., pattern="^(low|medium|high)$")

@app.post("/test-validation" ,tags=["Using Error handler"])
def test_validation(data: TestRequest):
    """Test validation error with handler"""
    return {"message": "Validation passed!", "data": data}


# Test 4: Unhandled exception (division by zero)
@app.get("/test-crash" , tags=["Using Error handler"])
def test_crash():
    """Test unhandled exception (should be caught by generic handler)"""
    logger.info("About to crash...") # stores all logs what message printed in terminal in app.log
    result = 1 / 0  # ZeroDivisionError
    return {"result": result}
