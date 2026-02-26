from fastapi import Header, HTTPException , status
import os

API_KEY = os.getenv("API_KEY")

async def verify_api_key(x_api_key : str = Header(...)):
    print("Recived:", x_api_key)
    print("Expected:" , API_KEY)
    if x_api_key !=API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key" )
    return x_api_key

print("Loaded API_KEY from env:", API_KEY)