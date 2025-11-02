from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from .db import SessionLocal, engine, Base
from . import crud, models, schemas
from app.db import get_connection
from openai import OpenAI
import os

app = FastAPI()

Base.metadata.create_all(bind=engine)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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

@app.post("/summarize", response_model=schemas.SummaryResponse)
def create_summary(request: schemas.SummaryCreate, db: Session = Depends(get_db)):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful text summarizer."},
                {"role": "user", "content": f"Summarize this text: {request.text}"}
            ],
            max_tokens=150,
        )
        summary_text = response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    summary = models.Summary(input_text=request.text, summary_text=summary_text)
    db.add(summary)
    db.commit()
    db.refresh(summary)

    return summary


@app.get("/results/{summary_id}", response_model=schemas.SummaryResponse)
def get_summary(summary_id: int, db: Session = Depends(get_db)):
    summary = db.query(models.Summary).filter(models.Summary.id == summary_id).first()
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary


@app.get("/history", response_model=list[schemas.SummaryResponse])
def get_history(db: Session = Depends(get_db)):
    return db.query(models.Summary).order_by(models.Summary.created_at.desc()).all()