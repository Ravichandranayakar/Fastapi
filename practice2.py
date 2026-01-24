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

@app.get("/")

def root_point():
    return {
        "name" :" BARO AI",
        "api_name" : os.getenv("API_NAME" , "FastAPI"),
          "message": "Welcome to BARO API" 
    } 
@app.get("/health")
def health_check():
    return{
        "health " : "Good"
    }

from fastapi.responses import  JSONResponse
from fastapi import Query , Path

# path parameter 

@app.get("/user/{user_id}")

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

@app.get("/search")
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
@app.post("/analyze", response_model=CaseResponse ,status_code = status.HTTP_200_OK)
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

