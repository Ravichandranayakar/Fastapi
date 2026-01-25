from fastapi import FastAPI
from dotenv import load_dotenv
import os
load_dotenv()

# create app instence for endpoints 

app = FastAPI(
    title= "BARO AI",
    version = "v1",
    description= " leagal ai baro"
)

@app.get("/" , tags=["MAIN ROOT"])

def root_point():
    return {
        "name" :" BARO AI",
        "api_name" : os.getenv("API_NAME" , "FastAPI"),
          "message": "Welcome to BARO API" 
    } 
@app.get("/health" ,tags=["health"])
def health_check():
    return{
        "health " : "Good"
    }

from fastapi.responses import  JSONResponse
from fastapi import Query , Path

# path parameter 

@app.get("/user/{user_id}" , tags=["User"])

def user_id(user_id :int = Path(
        ...,
        description="user ID to fetch",
        gt =0 ,
        example= 198
    )
):
    return {
        "user" : user_id,
        "name" : f"you name is {user_id}",
        "Gmail" : f"your Gmail is {user_id}@baro.ai"
    }
    
# Query parameter

@app.get("/search" , tags=["Search"])
def search(
    q:str = Query(
        ...,
        min_length=1,
        max_length= 100,
        description="wellcome to baro ai"
    ),
    page:int = Query(
        default=1,
        ge=1,
        le=100,
        description= "Page number"
    ),
    limit:int =  Query(
        default=10,
        ge=1,
        le=100,
        description="Results per page"
    )
):
    return{
        "Query" : q,
        "page" : page,
        "limits" : limit,
        "results" : [f"results {i} matching '{q}' " for i in range(1, 4)]
    }
    
from shemas2 import CaseResponse , CaseRequest
from fastapi import HTTPException , status
# POST endpoint with request body 
@app.post("/analyze", response_model=CaseResponse ,status_code = status.HTTP_200_OK , tags=["Analyse"])
def analyze_case(request: CaseRequest):
    """
    Analyze legal case and predict category
    
    This endpoint accepts a case description and returns the predicted
    legal category with confidence score.
    """
    # Dummy logic (replacing with real ml modle logic)
    if "property" in request.case_text.lower():
        category = "Property Law"
        confidence = 0.89
    elif "contract" in request.case_text.lower():
        category = "Contract Law"
        confidence = 0.85
    else:
        category = "General Law"
        confidence = 0.60
    
    return CaseResponse(
        success=True,
        category=category,
        confidence=confidence,
        urgency=request.urgency
    )

   
# Your Homework: Build One Endpoint
# Goal: Create this endpoint from scratch and watch /docs:

# text
# POST /fir-classify
# - Input: {"description": "theft case...", "location": "Karnataka"}
# - Output: {"crime_type": "IPC 379", "severity": "medium"}
# - Tag: "FIR Analysis"
# - Description: "Classify FIR based on description"
# Steps:

# Create Pydantic models in schemas.py

# Add endpoint in main.py

# Run server

# Check /docs

# Test with "Try it out"

# Test validation with bad data

@app.post("/FIR-clasify" , tags=["FIR Analysis"] , response_model=CaseResponse , status_code=status.HTTP_200_OK  )
def fir_analyse(request:CaseRequest):
    """
     Analyze the description, location and predicts crime type
    
    This endpoint accepts a case description and returns the predicted
    legal Crime type with confidence score.
    """
    if "theft" in request.description.lower():
        Criem_type = "IPC 379"
        confidence = 0.89
        if "karanataka" in request.location.lower():
            Criem_type = "IPC 379"
            confidence = 0.90
    else:
        Criem_type = "general IPc"
        confidence = 0.60
    
    return CaseResponse(
        success=True,
        Criem_type=Criem_type,
        confidence=confidence,
        serverity=request.serverity
    )

# error handling 
@app.get("/error-demo" , tags=["Error handling"])
def error_demo(Should_fail : bool = Query(default=False)):
    """
    Demonstrates custom error handling
    """
    if Should_fail:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="you set should_fail = True , so here's an error!")
    return{"message" : "No error occurred"}
