# main.py
from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Import routers
from routers import legal, users, search

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title=os.getenv("APP_NAME", "BARO AI"),
    version="v1",
    description="Legal AI Assistant - Organized with Routers"
)


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
        "app": os.getenv("APP_NAME"),
        "version": "v1"
    }
