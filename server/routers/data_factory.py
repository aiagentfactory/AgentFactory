from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import models, database
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

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
    return db.query(models.Event).offset(skip).limit(limit).all()

@router.post("/datasets")
def create_dataset(ds: DatasetCreate, db: Session = Depends(get_db)):
    # In a real system, this would filter and aggregate events. 
    # Here we just snapshot the current event count.
    count = db.query(models.Event).count()
    db_ds = models.Dataset(
        name=ds.name,
        description=ds.description,
        event_count=count
    )
    db.add(db_ds)
    db.commit()
    db.refresh(db_ds)
    return db_ds

@router.get("/datasets")
def list_datasets(db: Session = Depends(get_db)):
    return db.query(models.Dataset).all()
