from fastapi import FastAPI
from sqlalchemy import text
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database import engine, Base, SessionLocal
from backend import models
from backend.routes import auth_routes, ticket_routes

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)
app.include_router(ticket_routes.router)


@app.get("/")
def home():
    return {"message": "Backend is running"}


@app.get("/test_db")
def test_db():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"message": "Database connected successfully"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()