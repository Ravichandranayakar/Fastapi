# importing reuired libraries
from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv() # To load  environment variable from.env file 

app = FastAPI(
    title = os.getenv("API_NAME" , "FastAPI APP"),
    debug  = os.getenv("DEBUG" , False)
    )

# health check endpoint  weather app is live or not
@app.get("/health")

# function that returns the health check in json format 
def health_check():
    """
    Health endpoint to verify API is running 
    """ 
    return {
        "status" : "healty",
        "App_name" : os.getenv("API_NAME"),
        "message"  : "API is running successfully"
    }

# Root endpoint  for user to provide links to find interactive docs 
@app.get("/")
def read_root():
    return {
        "message" : "welcome to BARO AI API",
        "docs" : "/docs" ,
        "health" : "/health"
    }

# to activate the venv = .\venv\Scripts\activate

