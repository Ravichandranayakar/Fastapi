from fastapi import Header , HTTPException , status

def verify_api_key(x_api_key: str = Header(...)) -> str:
    """
    Verify API key from request header
    
    WHY: Protect endpoints from unauthorized access
    HOW: Check X-API-Key header against valid keys
    WHEN: Every protected endpoint calls this
    
    Usage in endpoint:
        @router.post("/analyze", dependencies=[Depends(verify_api_key)])
    """
    
    valid_keys = ["secret-key-123" , "dev-key=456"] # in real app we are going to use database
    if x_api_key not in valid_keys:
        print(f"invalid API key attempted: {x_api_key}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "INvalid API key"
        )
    print(f"valid API key ->{x_api_key}")
    return x_api_key

