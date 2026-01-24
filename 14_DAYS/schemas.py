from pydantic import BaseModel , Field , field_validator
from typing import Optional

# Requestmodel what user send
class PredictionRequest(BaseModel):
    """
   Schema for prediction input 
    """
    text : str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Text input for prediction"
    )
    model_version_threshold: Optional[str] = Field(
        default="v1",
        description="Model version to use"
    )
    
    confidence_threshold: Optional[float]  = Field(
        default=0.5,
        ge = 0.0,
        le = 1.0,
        description="Minimum confidence score"
    )
    # coustem validator
    @field_validator('text')
    @classmethod
    def text_must_not_be_empty(cls , v: str) -> str:
        """
        Validate that text is not just whitspace
        """
        if not v.strip():
            raise ValueError("Text cannot be empty or whitspace")
        return v.strip() # returns cleaned text
    
    # Responce model - what API returns
    
class PredictionResponse(BaseModel):
    """
    Schema for prediction output
    """
    success: bool = Field(description="whether prediction succeeded")
    prediction: str  = Field(description="Predicted class/label")
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score"
    )
        
    model_version: str = Field(description="Model version used")
        
    # Example for docs
        
    class config:
        json_schema_extra = {
            "example" :{
                "success": True,
                "prediction" : "Spam",
                "confidence" : 0.90,
                "model_version" :"v1"
            }
        }