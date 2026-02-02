from pydantic import BaseModel , Field , field_validator

from typing import Optional

# creating request model 
class CaseRequest(BaseModel):
    description:str = Field(
        ...,
        min_length= 1,
        max_length= 500,
        description= "ADd Description here"
    ),
    location:str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="crime location"
    
    ),
    serverity:str = Field(
        default="medium",
        description="chose the level",
        pattern="^(low|medium|high)$" # Regex validation 
    )
    
    class config():
        json_shema_structure = {
            "example" :{
                "Description": "Classifies an FIR description and location into a predicted crime section (for example, IPC code) and a severity level for quick legal triage",
                 "location" :"karnataka",
                 "serverity" : "high"}
        }
        
        
#creating response model 

class CaseResponse(BaseModel):
    
    success :bool
    Criem_type : str  = Field(description = "IPC 379")
    confidence :float = Field(ge=0.0 , le = 1.0)
    serverity : str
    
    class cofig:
        json_shema_extra = {
            "Example" :{
                "success" : True,
                "Crime_type" : "IPC 379",
                "confidence" : 1.0,
                "Serverity" : "midium"
            }
        }
 