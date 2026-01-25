# routers/legal.py
from fastapi import APIRouter, status
from schemas.legal import CaseRequest, CaseResponse, FIRRequest, FIRResponse

# Create a router instance
router = APIRouter(
    prefix="/legal",      # All routes will start with /legal
    
      # Group related endpoints under one path

      # Legal: /legal/analyze, /legal/fir-classify

      # Users: /users/{user_id}

      # Search: /search
      # Instead of everything directly under /analyze, /fir-classify, /users,
    tags=["Legal Analysis"],  # Tag for /docs grouping
)


@router.post("/analyze", response_model=CaseResponse, status_code=status.HTTP_200_OK)
def case_analyze(request: CaseRequest):
    """
    Analyze legal case and predict category
    
    This endpoint accepts a case description and returns the predicted
    legal category with confidence score.
    """
    # Dummy logic (replace with ML model later)
    case_lower = request.case_text.lower()
    
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
        confidence = 0.60
    
    return CaseResponse(
        success=True,
        category=category,
        confidence=confidence,
        urgency=request.urgency
    )


@router.post("/fir-classify", response_model=FIRResponse, status_code=status.HTTP_200_OK)
def classify_fir(request: FIRRequest):
    """
    Classify FIR and predict IPC section
    
    Analyzes crime description and suggests relevant IPC sections.
    """
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
        confidence = 0.65
    
    return FIRResponse(
        success=True,
        crime_type=crime_type,
        confidence=confidence,
        severity=request.severity
    )
