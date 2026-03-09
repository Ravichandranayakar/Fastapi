# routers/legal.py
from fastapi import APIRouter, status , Request, HTTPException
from schemas.legal import CaseRequest, CaseResponse, FIRRequest, FIRResponse


from fastapi import Depends
from dependencies.Request_id import get_request_id # import dependecies

from dependencies.config import get_settings , Settings # import Config

from dependencies.models import get_legal_model , FakeLegalModel # importing model

from dependencies.auth import verify_api_key

from utils.logger import logger
from pydantic import BaseModel , Field
from fastapi.concurrency import run_in_threadpool

from fastapi import APIRouter, UploadFile,File,Request
from fastapi.concurrency import run_in_threadpool
import csv
from io import StringIO

# adding database for the Prediction model
from core.dependencies import get_db
from sqlalchemy.orm import Session
from models.predictions import Prediction


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.dependencies import get_db
from core.security import verify_api_key
from core.auth import get_current_user

from core.limiter import limiter
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request
import bleach

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
        confidence = 0.95
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

###########################################

@router.post("/legal/predict_batch")
async def predict_batch(
    file : UploadFile = File(...), request: Request = None):
    """
    TEMP: Dummy batch endpoint.
    - Echoes the crime text from CSV.
    - Returns a fixed 'General Law' label and 0.8 confidence as placeholders.
    """
    model = request.app.state.legal_model
    contents = await file.read()
    decoded = contents.decode("utf-8")
    
    reader = csv.DictReader(StringIO(decoded))
    
    results = []
    
    for row in reader:
        text = row.get("Crime Type")
        
        if not text:
            continue
        
        
        category, confidence = await run_in_threadpool(
            model.predict_category,
            text)
        
        results.append({
            "case__text" : text[:50] , 
            "category":category,
            "confidence" :confidence
        })
     
    return{
        "total_processed": len(results),
        "results" : results
    }   
######################################################################### 
# code for database

@router.post("/test-db")
def test_db( case_text:str , db:Session = Depends(get_db)):
    pred = Prediction(case_text = case_text,
                      category = "Test",
                      confidence = 0.95,
                      model_version = "v1.0")
    
    db.add(pred)
    db.commit()
    db.refresh(pred)
    return {"saved ID":pred.id}


# another type of code for databases only for understanding 
@router.post("/legal/predict")
@limiter.limit("5/minute")
async def predict_case(
    body: CaseAnalysisRequest,
    request: Request,
    db: Session = Depends(get_db),
    api_key : str = Depends(verify_api_key),
    current_user: dict = Depends(get_current_user),):
    clean_text = bleach.clean(body.case_text)
    model = request.app.state.legal_model

    category, confidence = await run_in_threadpool(
        model.predict_category,
        body.case_text
    )

    prediction = Prediction(
        case_text=body.case_text,
        category=category,
        confidence=confidence,
        model_version="v1.2.3"
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return {
        "category": category,
        "confidence": confidence
    }
    
    
# fecth the history 

@router.get("/legal/history")
def get_history(
    limit: int = 10,
    db: Session = Depends(get_db),
    api_key : str = Depends(verify_api_key),
    current_user : dict =  Depends(get_current_user)
):  # sourcery skip: inline-immediately-returned-variable
    records = db.query(Prediction)\
                .order_by(Prediction.created_at.desc())\
                .limit(limit)\
                .all()

    return records

# to delet endpoint 

@router.delete("/legal/history/{prediction_id}")
def delete_prediction(
    prediction_id: int,
    db: Session = Depends(get_db)
):
    record = db.query(Prediction)\
               .filter(Prediction.id == prediction_id)\
               .first()

    if not record:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(record)
    db.commit()

    return {"message": "Deleted"}

