from pydantic import BaseModel , Field , field_validator

from typing import Optional

# creating request model 
class CaseRequest(BaseModel):
    case_text:str = Field(
        ...,
        min_length= 1,
        max_length= 500,
        description= "ADd Description here"
    ),
    urgency :str = Field(
        default="medium",
        description="chose the level",
        pattern="^(low|medium|high)$"
    )
    
    class config():
        json_shema_structure = {
            "example" :{
                "case_text" :"Property dispute between two parties regarding boundary lines",
            "urgency" : "high"}
        }
        
        
#creating response model 

class CaseResponse(BaseModel):
    
    success :bool
    category : str  = Field(description = "legal")
    confidence :float = Field(ge=0.0 , le = 1.0)
    urgency : str
    
    class cofig:
        json_shema_extra = {
            "Example" :{
                "success" : True,
                "category" : "proparity",
                "confidence" : 1.0,
                "urgency" : "high"
            }
        }
    