from core.database import sessionlocal
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db():
    db = sessionlocal()
    try:
        yield db 
    finally:
        db.close()