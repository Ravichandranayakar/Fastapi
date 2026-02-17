# routers/search.py
from fastapi import APIRouter, Query
from fastapi import Depends
from dependencies.Request_id import get_request_id

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.get("")  # Empty string means just /search
def search(
    q: str = Query(
        ...,
        min_length=1,
        max_length=100,
        description="Search query text"
    ),
    page: int = Query(default=1, ge=1, le=100),
    limit: int = Query(default=10, ge=1, le=100),
    request_id : str  = Depends(get_request_id)
):
    """
    Search cases, users, and legal documents
    
    Returns paginated search results matching the query.
    """
    print(f" Search -> Request ID: {request_id}")
    return {
        "query": q,
        "page": page,
        "limit": limit,
        "total_results": 42,
        "results": [
            {"id": i, "title": f"Result {i} matching '{q}'", "type": "case"}
            for i in range(1, 4)
        ]
    }
    