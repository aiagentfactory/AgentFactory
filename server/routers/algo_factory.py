from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import models, database
from pydantic import BaseModel
import time
import random
import uuid

router = APIRouter(prefix="/algo", tags=["Algorithm Factory"])

class TrainingConfig(BaseModel):
    model_base: str
    algorithm: str
    dataset_id: str # Frontend sends string or int
    epochs: int

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
    
    # Create a Model artifact
    new_model = models.Model(
        name=f"Model_{job.algorithm}_{str(uuid.uuid4())[:5]}",
        version="1.0",
        source_job_id=job.id
    )
    db.add(new_model)
    
    db.commit()
    db.close()

@router.post("/train/jobs")
def create_training_job(config: TrainingConfig, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    dataset_id_int = int(config.dataset_id) if config.dataset_id else None
    job = models.TrainingJob(
        model_base=config.model_base,
        algorithm=config.algorithm,
        dataset_id=dataset_id_int,
        status="pending", 
        progress=0.0, 
        metrics={}
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    
    job.status = "training"
    db.commit()
    
    background_tasks.add_task(mock_training_process, job.id)
    
    return job

@router.get("/train/jobs")
def list_training_jobs(db: Session = Depends(get_db)):
    return db.query(models.TrainingJob).order_by(models.TrainingJob.id.desc()).all()

@router.get("/train/jobs/{job_id}")
def get_job_status(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.TrainingJob).filter(models.TrainingJob.id == job_id).first()
    return job

@router.get("/models")
def list_models(db: Session = Depends(get_db)):
    return db.query(models.Model).all()
