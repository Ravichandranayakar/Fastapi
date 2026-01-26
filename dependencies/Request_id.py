import uuid
from fastapi import Request
# uuid = Universally Unique Identifier

def get_request_id() -> str:
    """
    Generate unique request ID for tracking
    
    WHY: Every request needs unique ID for logging/debugging
    HOW: Generate UUID4 (random unique string)
    WHEN: Called automatically before every endpoint
    """
    request_id = str(uuid.uuid4()) # (UUID version 4) 
    print(f"Request ID --> '{request_id}' ") # it will appear in termianl
    return request_id # to send to fastapi

