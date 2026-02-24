from core.database import SessionLocal
from models.predictions import Prediction

db = SessionLocal() # converstaion what we are going to perform on database
print("Tables:", db.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';").fetchall())
print("Predictions:", db.query(Prediction).count())
db.close()
