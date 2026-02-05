# routers/legal.py
from fastapi import APIRouter, status , Request
from schemas.legal import CaseRequest, CaseResponse, FIRRequest, FIRResponse


from fastapi import Depends
from dependencies.Request_id import get_request_id # import dependecies

from dependencies.config import get_settings , Settings # import Config

from dependencies.models import get_legal_model , FakeLegalModel # importing model

from dependencies.auth import verify_api_key

from utils.logger import logger
from pydantic import BaseModel , Field

from fastapi.concurrency import run_in_threadpool
# Create a router instance
router = APIRouter(
    prefix="/legal",      # All routes will start with /legal
    tags=["Legal Analysis"],  # Tag for /docs grouping
)

 # prifix =  Group related endpoints under one path

      # Legal: /legal/analyze, /legal/fir-classify

      # Users: /users/{user_id}

      # Search: /search
      # Instead of everything directly under /analyze, /fir-classify, /users,
      

class CaseAnalysisRequest(BaseModel):
    case_text: str = Field(..., min_length=10, max_length=5000)
    urgency: str = Field(..., pattern="^(low|medium|high)$")
    
@router.post("/analyze", response_model=CaseResponse, 
             dependencies=[Depends(verify_api_key)]) # Protect this endpoint
async def case_analyze(request: CaseRequest ,
                        body: CaseAnalysisRequest,
                 request_M : Request,
                 request_id : str = Depends(get_request_id),
                 settings: Settings =  Depends(get_settings),
                 model: FakeLegalModel = Depends(get_legal_model)):
    
                # Get model from app.state (loaded at startup)
                model = request_M.app.state.legal_model
                 
                logger.info(f">> processing case analysis for request : {request_id}")
                logger.info(f"   [BARO AI] Request: {request_id}")
                logger.info(f"   Model version: {model.model_version}")
                
                # use the model
                #category , confidence = model.predict_category(request_body.case_text)
                
                # Run blocking prediction in threadpool 
                # so it doesn't block the event loop
                category, confidence = await run_in_threadpool(
                model.predict_category,
                body.case_text,
                 )
#---------------------------------------------------------------------#    
#settings: Settings =  Depends(get_settings),
#"This line defines a settings variable that takes the shape of the
# Settings class, then tells FastAPI to 'go find and run' 
# the get_settings function to fill that variable with data."
#----------------------------------------------------------------------#

                """
                Analyze legal case and predict category
    
                This endpoint accepts a case description and returns the predicted
                legal category with confidence score.
                """
                """
                Analyze legal case with request id tracking
                """
                print(f"processing case analsis for request {request_id}")
    
                """
                Analyze legal case with configurable settings
                """
                print(f"[{settings.API_NAME}] processing request: {request_id}") # Just for  my refference i am printing this line 
    
                print(f"Using model version: {model.model_version}")
               
                # Dummy logic (replace with ML model later)
                
                case_lower = request.case_text.lower()
    
                # Use settings in logic 
                if len(request.case_text) > settings.max_prediction_length:
                    print(f" Case text too long! MAX: {settings.max_prediction_length}")
        
                if "property" in case_lower or "land" in case_lower:
                    category = "Property Law"
                    confidence = 0.89
                elif "contract" in case_lower or "agreement" in case_lower:
                    category = "Contract Law"
                    confidence = 0.85
                elif "divorce" in case_lower or "marriage" in case_lower:
                    category = "Family Law"
                    confidence = 0.82
                else:
                    category = "General Law"
                    confidence = settings.default_confidence_threshold
    
                print(f"Completed request {request_id}") # prints request id
    
                return CaseResponse(
                    success=True,
                    category=category,
                    confidence=confidence,
                    urgency=request.urgency
                    )


@router.post("/fir-classify", response_model=FIRResponse, 
             dependencies=[Depends(verify_api_key)]) # Protect this endpoint
def classify_fir(request: FIRRequest ,
                 request_id:str = Depends(get_request_id),
                 settings:Settings = Depends(get_settings),
                 model : FakeLegalModel = Depends(get_legal_model)):
    """
    Classify FIR and predict IPC section
    
    Analyzes crime description and suggests relevant IPC sections.
    """
    """
    Classify FIR with request id tracking
    """
    
    print(f"processing FIR classification for request {request_id}")
    
    print(f"Using model version: {model.model_version}")
    
    crime_type, confidence = model.predict_crime(request.description)
    
    # use teh settings logic 
    if len(request.description)>settings.max_prediction_length:
        print(f"Fir text too long! MAX:{settings.max_prediction_length}")
    # Dummy logic (replace with ML model later)
    desc_lower = request.description.lower()
    
    if "theft" in desc_lower or "stolen" in desc_lower:
        crime_type = "IPC 379 - Theft"
        confidence = 0.92
    elif "assault" in desc_lower or "attack" in desc_lower:
        crime_type = "IPC 323 - Assault"
        confidence = 0.88
    elif "fraud" in desc_lower or "cheating" in desc_lower:
        crime_type = "IPC 420 - Cheating"
        confidence = 0.85
    else: 
        crime_type = "IPC General Section"
        confidence = settings.default_confidence_threshold
    
    print(f"Completed request {request_id}") # prints request id
    
    return FIRResponse(
        success=True,
        crime_type=crime_type,
        confidence=confidence,
        severity=request.severity
    )
