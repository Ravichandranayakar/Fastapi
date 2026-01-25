from pydantic_settings import BaseSettings
from functools import lru_cache

#-----------------------------------------------------------------#
#BaseSettings: Helps you create a Settings class that 
# automatically reads values from .env / environment
# and converts them to correct types.

#lru_cache: Makes sure get_settings() runs only once
# and then returns the same settings object every time 
# (fast, no repeated .env reading).
#-----------------------------------------------------------------#
class Settings(BaseSettings):
    """
    Application settings from environment variables
    
    WHY: Centralize all config in one place
    HOW: Pydantic reads from .env automatically
    """
    API_NAME : str = "BARO API"
    app_version :str = "v1"
    debug : bool = False
    max_prediction_length : int  = 1000
    default_confidence_threshold : float = 0.5
    
    class Config:
        env_file = ".env"
    
@lru_cache()  ## "(Least Recently Used)" Cache the settings (load once, reuse forever)

# Settings = “how to build the object”
# get_settings() = “give me the one shared object for the whole app”.

def get_settings() -> Settings: #this function returns a Settings object”
    """
    Get application settings
    
    WHY: Avoid reading .env file on every request
    HOW: @lru_cache decorator caches the result
    WHEN: First request loads settings, subsequent requests use cache
    """
    return Settings()
