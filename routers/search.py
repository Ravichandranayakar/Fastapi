# routers/search.py
from fastapi import APIRouter, Query

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.get("")  # Empty string means just /search
def search(
    q: str = Query(
        ...,
        min_length=1,
        max_length=50,
        description="Search query text"
    ),
    page: int = Query(default=1, ge=1, le=100),
    limit: int = Query(default=10, ge=1, le=100)
):
    """
    Search cases, users, and legal documents
    
    Returns paginated search results matching the query.
    """
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
    