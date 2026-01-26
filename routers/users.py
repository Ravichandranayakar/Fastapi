# routers/users.py
from fastapi import APIRouter, Path

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
        examples=123
    )
):
    """
    Get user by ID
    
    Returns user information based on the provided user ID.
    """
    return {
        "user_id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@baro.ai",
        "role": "lawyer"
    }
