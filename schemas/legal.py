# schemas/legal.py
from pydantic import BaseModel, Field
from typing import Optional


class CaseRequest(BaseModel):
    """Request model for case analysis"""
    case_text: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Legal case description"
    )
    urgency: str = Field(
        default="medium",
        description="Case urgency level",
        pattern="^(low|medium|high)$"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "case_text": "Property dispute between two parties regarding boundary lines",
                "urgency": "high"
            }
        }


class CaseResponse(BaseModel):
    """Response model for case analysis"""
    success: bool
    category: str = Field(description="Legal category")
    confidence: float = Field(ge=0.0, le=1.0)
    urgency: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "category": "Property Law",
                "confidence": 0.89,
                "urgency": "high"
            }
        }


class FIRRequest(BaseModel):
    """Request model for FIR classification"""
    description: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="Crime description"
    )
    location: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Location where crime occurred"
    )
    severity: str = Field(  # Fixed typo: serverity → severity
        default="medium",
        description="Crime severity level",
        pattern="^(low|medium|high)$"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "description": "Theft of mobile phone from public transport",
                "location": "Bangalore",
                "severity": "medium"
            }
        }


class FIRResponse(BaseModel):
    """Response model for FIR classification"""
    success: bool
    crime_type: str = Field(description="IPC section")  # Fixed typo: Criem_type
    confidence: float = Field(ge=0.0, le=1.0)
    severity: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "crime_type": "IPC 379 - Theft",
                "confidence": 0.92,
                "severity": "medium"
            }
        }
