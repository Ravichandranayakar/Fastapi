from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    titel = os.getenv("API_NAME" , "FastAPI APP"),
    debug = os.getenv("DEBUG" , False)
)

@app.get("/health")

def health_check():
    return {
        "status" :"healthy",
        "app_name" : os.getenv("API_NAME" , "FastAPI APP"),
        "message" : " API is successfully running"
    }

@app.get("/")
def root_endpoint():
    return {
        "message" : "wellcome to baro ai",
        "docs" : "/docs",
       "health" : "/health"
    }



