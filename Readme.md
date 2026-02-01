```markdown
DAY 1
[✓] Created venv and activated it
[✓] Installed FastAPI and Uvicorn
[✓] Got the server running with --reload
[✓] Tested the endpoints and they work!

DAY 2

[✓] Pydantic models created (request + response)
[✓] Validation works (try invalid data)
[✓] Path parameters implemented
[✓] Query parameters implemented
[✓] Request body (POST) works
[✓] Response structured with response_model
[✓] Status codes understood
[✓] Error handling with HTTPException
[✓] Tested in /docs

DAy 3

[✓] Created routers/ folder
[✓] Created schemas/ folder
[✓] Organized models by domain (schemas/legal.py)
[✓] Created APIRouter instances
[✓] Used prefix and tags
[✓] Included routers in main.py
[✓] main.py has NO endpoint logic (only includes)
[✓] Tested all endpoints still work
[✓] /docs shows organized structure
[✓] Code is scalable and clean

DAY 4

[✓] Created dependencies/Request.py (request ID)
[✓] Created dependencies/config.py (settings)
[✓] Created dependencies/models.py (ML model)
[✓] Created dependencies/auth.py (API key validation)
[✓] Used Depends() in endpoints
[✓] Used @lru_cache() for expensive operations
[✓] Tested model loads once and caches
[✓] Tested authentication with valid/invalid keys
[✓] No repeated code in endpoints

DAy 5

[✓] Created utils/logger.py (structured logging)
[✓] Created utils/exceptions.py(customexceptions)
[✓] Created utils/error_handlers.py (exception handlers)
[✓] Created middleware/logging.py (request logging)
[✓] Registered middleware in main.py
[✓] Registered exception handlers in main.py
[✓] Updated dependencies to use logger
[✓] Updated dependencies to use custom exceptions
[✓] Tested all components individually
[✓] Tested everything together
[✓] No Unicode errors (Windows-friendly symbols)
[✓] Clean error responses (no tracebacks to users)
[✓] Full error details in logs (for developers)
[✓] Request timing working (X-Process-Time header)

DAY 6

[✓] Added `startup_event` to load resources when the app starts  
[✓] Added `shutdown_event` to clean up resources when the app stops  
[✓] Imported and used `FakeLegalModel` in `main.py`  
[✓] Created a single `FakeLegalModel` instance in `startup_event`  
[✓] Stored the model in `app.state.legal_model` for global access   
[✓] Updated `/legal/analyze` to accept `Request` and use `request.app.state.legal_model`  
[✓] Confirmed model is not re-created per request (no “Loading Legal AI Model…” in request logs)  
[✓] Verified `/legal/analyze` runs in milliseconds (~0.02s) instead of ~2 seconds  
[✓] Kept using the existing dummy `FakeLegalModel` (no real ML model yet)  
[✓] Confirmed startup logs show model loading once with version info  
[✓] Confirmed shutdown logs show model unload/cleanup

```
