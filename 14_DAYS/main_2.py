# importing reuired libraries
from fastapi import FastAPI
from dotenv import load_dotenv
import os

from fastapi import Query , Path , HTTPException , status
from fastapi.responses import JSONResponse

# import shema
from schemas import PredictionRequest , PredictionResponse

load_dotenv() # To load  environment variable from.env file 

# need fastapi for all endpoints
app = FastAPI(
    title = os.getenv("API_NAME" , "FastAPI APP"),
    version="1.0.0",
    description="AI-Powered leagal prediction API"
    )

# ==========Path parameters=======

@app.get('/user/{user_id}')

def get_user(
    user_id: int = Path(
        ...,
        description="user ID to fetch",
        gt=0 ,# must be positive and geaterthan 0
        example = 123
    )
):
    """
    Example of PATH parameter
    URL: /user/123
    """
    return {
        "user_id" : user_id,
        "name" : f"User{user_id}", # type: ignore
        "message" : "this is a path parameter example"
    }
    
# ======== Query parameter =======

@app.get("/Search")

def search(
    q: str = Query(
        ...,
        min_length=1 ,
        max_length=100,
        description="Search query"
    ),
    page: int  = Query(
        default=1,
        ge=1,
        description="page number"
    ),
    limit: int  =Query(
        default=10,
        ge=1,
        description="item per page"
    )
):
    """
    Example of QUERY parameters
    URL: /search?q=fastapi&page=1&limit=10
    """
    return {
        "query" :q,
        "page" : page,
        "limit": limit,
        "results" : [f"results {i} for '{q}' " for i in range(1, limit+1)]
        
    }
    
    
# =========== Request Body (POSt) =============
# health check endpoint  weather app is live or not

@app.post("/predict", response_model = PredictionResponse, status_code = status.HTTP_200_OK)
def predict(request: PredictionRequest):
    """
    Main prediction endpoint with REQUEST BODY
    
    - Accepts JSON in POST body
    - Validates using Pydantic
    - Returns structured response
    """
    #Dummy prediction logic (replace with our existing models)
    prediction = "spam" if "buy" in request.text.lower() else "ham"
    confidence = 0.90 if prediction == "spam" else 0.65
    
    # return responce matching PredictionResponse shema
    return PredictionResponse(
        success = True,
        prediction = prediction,
        confidence = confidence,
        model_version = request.model_version
    )


# ============ MIXED PARAMETERS ============
@app.post("/predict/{model_name}")
def predict_with_path_and_body(
    model_name: str = Path(..., description="Model to use"),
    threshold: float = Query(default=0.5, ge=0.0, le=1.0),
    request: PredictionRequest = None
):
    """
    Example combining PATH, QUERY, and BODY
    URL: /predict/bert?threshold=0.7
    BODY: {"text": "...", "model_version": "v2"}
    """
    return {
        "model_name": model_name,
        "threshold": threshold,
        "text": request.text if request else None,
        "message": "This combines all three input types!"
    }

# ============ Error handling ========
@app.get("/error-demo")
def error_demo(Should_fail : bool = Query(default=False)):
    """
    Demonstrates custom error handling
    """
    if Should_fail:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="you set should_fail = True , so here's an error!"
       )
    return{"message" : "No error occurred"}
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
        "health" : "/health",
        "endpoints" : {
            "predict" :"/predict (POST)",
            "search" : "/search?q=test",
            "user": "/user/123"
        }
    }

# to activate the venv = .\venv\Scripts\activate

