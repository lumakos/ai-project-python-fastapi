from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from .db import SessionLocal, engine, Base
from . import crud, models
from app.db import get_connection

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"msg": "FastAPI + Postgres 🚀"}

@app.get("/db-test")
def db_test():
    with get_connection() as conn:
        result = conn.execute(text("SELECT NOW()"))
        return {"db_time": str(result.scalar_one())}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.post("/users")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    return crud.create_user(db, name, email)