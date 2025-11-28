from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import models, database
from pydantic import BaseModel
import time
import random

router = APIRouter(prefix="/algo", tags=["Algorithm Factory"])

class TrainingConfig(BaseModel):
    model_base: str
    algorithm: str
    hyperparams: dict

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def mock_training_process(job_id: int):
    db = database.SessionLocal()
    job = db.query(models.TrainingJob).filter(models.TrainingJob.id == job_id).first()
    
    # Simulate training steps
    for i in range(1, 6):
        time.sleep(2) # Simulate work
        job.progress = i * 20.0
        job.metrics = {"loss": random.random(), "step": i}
        db.commit()
    
    job.status = "completed"
    db.commit()
    db.close()

@router.post("/train/jobs")
def create_training_job(config: TrainingConfig, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    job = models.TrainingJob(model_base=config.model_base, status="pending", progress=0.0, metrics={})
    db.add(job)
    db.commit()
    db.refresh(job)
    
    job.status = "training"
    db.commit()
    
    background_tasks.add_task(mock_training_process, job.id)
    
    return job

@router.get("/train/jobs/{job_id}")
def get_job_status(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.TrainingJob).filter(models.TrainingJob.id == job_id).first()
    return job
