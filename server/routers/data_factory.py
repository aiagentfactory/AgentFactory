from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import models, database
from pydantic import BaseModel
from typing import Dict, Any, List

router = APIRouter(prefix="/data", tags=["Data Factory"])

class EventCreate(BaseModel):
    event_type: str
    content: Dict[str, Any]
    session_id: str

class DatasetCreate(BaseModel):
    name: str
    description: str

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/events")
def ingest_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = models.Event(
        event_type=event.event_type,
        content=event.content,
        session_id=event.session_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return {"status": "success", "event_id": db_event.id}

@router.get("/events")
def list_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = db.query(models.Event).offset(skip).limit(limit).all()
    return events

@router.post("/datasets")
def create_dataset(dataset: DatasetCreate, db: Session = Depends(get_db)):
    # Snapshot logic: Count current events
    count = db.query(models.Event).count()
    db_dataset = models.Dataset(
        name=dataset.name,
        description=dataset.description,
        event_count=count
    )
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset

@router.get("/datasets")
def list_datasets(db: Session = Depends(get_db)):
    return db.query(models.Dataset).all()
