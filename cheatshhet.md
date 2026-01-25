```markdown
# My FastAPI Cheat Sheet

## 1. Basic Endpoint Patterns

### GET with Path Parameter
```python
@app.get("/user/{user_id}")
def get_user(user_id: int = Path(..., gt=0)):
    return {"user_id": user_id}
```

### GET with Query Parameters
```python
@app.get("/search")
def search(
    q: str = Query(...),
    page: int = Query(default=1)
):
    return {"query": q, "page": page}
```

### POST with Request Body
```python
@app.post("/predict", response_model=ResponseModel)
def predict(request: RequestModel):
    return ResponseModel(...)
```

## 2. Pydantic Model Template

```python
from pydantic import BaseModel, Field

class MyRequest(BaseModel):
    # Required field
    name: str = Field(..., min_length=1)
    
    # Optional field with default
    age: Optional[int] = Field(default=None, ge=0)
```

## 3. When to Use What?

- **Path (`/user/{id}`)**: Required identifiers
- **Query (`?page=1`)**: Optional filters
- **Body (JSON)**: Complex data in POST/PUT

## 4. Common Validation

- `min_length` / `max_length`: String length
- `ge` / `le`: Number range (greater/less equal)
- `gt` / `lt`: Number range (exclusive)
```

***

## Better Learning Approach: "Skeleton Method"

**Instead of memorizing full code, memorize small skeletons and fill them in.**

```python
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# REQUEST MODEL - Copy and modify
class MyRequest(BaseModel):
    text: str = Field(..., min_length=1)  # Required
    option: Optional[str] = Field(default="default")  # Optional

# RESPONSE MODEL - Copy and modify
class MyResponse(BaseModel):
    success: bool
    result: str

# ENDPOINT - Copy and modify
@app.post("/endpoint", response_model=MyResponse)
def my_endpoint(request: MyRequest):
    # Your logic here
    return MyResponse(success=True, result="done")
```

**Now when you need to build something:**
1. Copy this skeleton
2. Change names to match your use case
3. Add your logic
4. Done!

***

## Realistic Learning Plan 

### What You Should Actually Remember:

**Tier 1: Core Concepts (Must Know)**
- FastAPI uses decorators: `@app.get()`, `@app.post()`
- Pydantic validates data automatically
- Three input types: Path, Query, Body
- `response_model` filters output

**Tier 2: Patterns (Reference as needed)**
- How to write a Pydantic model (use template)
- Validation constraints (check cheatsheet)
- Status codes (Google when needed)

**Tier 3: Details (Always Google)**
- Exact syntax for validators
- All Field parameters
- HTTPException details

### Mini-Project: Legal Case Classifier API

```
Goal: Create ONE endpoint that accepts case description and returns category

Requirements:
1. POST /classify
2. Input: {"case_text": "...", "language": "en"}
3. Output: {"category": "civil", "confidence": 0.75}
4. Validation: case_text must be 10-500 chars
5. Language must be "en" or "hi"
```

**Rules:**
- Use your cheatsheet
- Google when stuck
- It's OK to look at old code, but TYPE it yourself
- Focus on ONE endpoint only

**Time limit:** 30 minutes (even if incomplete!)

***

## The  15-Minute Daily Practice" Method

Every morning, build this tiny FastAPI from memory (no looking!):

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Request(BaseModel):
    text: str

@app.post("/predict")
def predict(req: Request):
    return {"result": req.text.upper()}
```


***
###################################################################################

┌─────────────────────────────────────────────────────────┐
│ 1. BROWSER                                              │
│    User fills form and clicks "Execute"                 │
│    JavaScript creates HTTP POST request                 │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│ 2. NETWORK                                              │
│    HTTP POST http://127.0.0.1:8000/FIR-clasify          │
│    Headers: Content-Type: application/json              │
│    Body: {"description": "...", ...}                    │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│ 3. UVICORN (Server)                                     │
│    Receives HTTP request                                │
│    Passes to FastAPI application                        │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│ 4. FASTAPI ROUTING                                      │
│    Matches URL path: /FIR-clasify                       │
│    Finds endpoint function: fir_analyse()               │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│ 5. PYDANTIC VALIDATION                                  │
│    Tries to create FIRRequest from JSON                 │
│    Checks: types, lengths, patterns, etc.               │
│                                                         │
│    ✓ Valid → Continue                                   |  
│    ✗ Invalid → Return 422 error (STOP HERE)             │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼ (only if validation passed)
┌─────────────────────────────────────────────────────────┐
│ 6. YOUR FUNCTION                                        │
│    def fir_analyse(request: FIRRequest):                │
│        # Your business logic                            │
│        return FIRResponse(...)                          │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│ 7. RESPONSE MODEL VALIDATION                            │
│    FastAPI validates your return value                  │
│    Ensures it matches FIRResponse schema                │
│    Filters out extra fields (security!)                 │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│ 8. JSON SERIALIZATION                                   │
│    Pydantic model → Python dict → JSON string           │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│ 9. HTTP RESPONSE                                        │
│    Status: 200 OK                                       │
│    Headers: Content-Type: application/json              │
│    Body: {"success": true, "Criem_type": "IPC 379"...}  │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│ 10. BROWSER                                             │
│     Displays response in /docs interface                │
│     Syntax highlighting, formatting, etc.               │
└─────────────────────────────────────────────────────────┘

