# routers/users.py
from fastapi import APIRouter, Path
from dependencies.Request_id import get_request_id
from fastapi import Depends
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/{user_id}")

def get_user(
    user_id: int = Path(
        ...,
        gt=0,
        description="User ID to fetch",
        examples=123 ,
    ),
    request_id: str = Depends(get_request_id)
):
    """
    Get user by ID
    
    Returns user information based on the provided user ID.
    """
    print(f" Users -> Request ID: {request_id}")
    return {
        "user_id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@baro.ai",
        "role": "lawyer"
    }
