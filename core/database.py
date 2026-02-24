from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv() 

DATABSE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABSE_URL)
sessionlocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base = declarative_base() #parent class that all your ORM models inherit from.
