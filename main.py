# main.py
from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Import routers
from routers import legal, users, search

from utils.logger import logger # import logger

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title=os.getenv("API_NAME", "BARO AI"),
    version="v1",
    description="Legal AI Assistant - Organized with Routers"
)

@app.on_event("startup")
async def stratup():
    logger.info("="*50)
    logger.info("BARO AI API Starting...")
    logger.info("Testing Logger module")
    logger.info("=" * 50)


@app.get("/")
def test_logger():
    """ Test all log levels"""
    logger.dubug("this is DEBUG (wont show - level too low )")
    logger.info("this is info")
    logger.warning(" This is warning")
    logger.error(":this is ERROR")
    return {"message" : "chcek terminal and logs/app.log"}

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
            "search": "/search?q=query"
        }
    }


@app.get("/health", tags=["Main"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": os.getenv("API_NAME"),
        "version": "v1"
    }
