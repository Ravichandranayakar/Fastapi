from sqlalchemy import Column , Integer , String , Float , DateTime
from sqlalchemy.sql import func
from core.database import Base

class Prediction(Base):
    __tablename__ = "predictions"
    id  = Column(Integer ,primary_key=True , index=True)
    case_text = Column(String, nullable=False)
    category = Column(String(100),nullable=False)
    confidence = Column(Float, nullable=False)  
    model_version = Column(String(20), nullable=False) 
    created_at = Column(DateTime(timezone=True),server_default=func.now())
