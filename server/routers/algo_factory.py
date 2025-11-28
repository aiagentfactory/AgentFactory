from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import models, database
from pydantic import BaseModel
import time
import random
import uuid

router = APIRouter(prefix="/algo", tags=["Algorithm Factory"])

class TrainingConfig(BaseModel):
    dataset_id: int
    model_base: str
    algorithm: str
    epochs: int = 3

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def mock_training_process(job_id: int):
    db = database.SessionLocal()
    job = db.query(models.TrainingJob).filter(models.TrainingJob.id == job_id).first()
    
    # Simulate training
    steps = 5
    for i in range(1, steps + 1):
        time.sleep(2)
        job.progress = (i / steps) * 100.0
        job.metrics = {"loss": random.random(), "step": i}
        db.commit()
    
    # Create Model Artifact
    model_name = f"Model_{job.algorithm}_{uuid.uuid4().hex[:6]}"
    new_model = models.ModelArtifact(
        name=model_name,
        version="v1.0",
        source_job_id=job.id,
        metrics=job.metrics
    )
    db.add(new_model)
    db.commit()
    db.refresh(new_model)
    
    job.status = "completed"
    job.output_model_id = new_model.id
    db.commit()
    db.close()

@router.post("/train/jobs")
def create_training_job(config: TrainingConfig, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    job = models.TrainingJob(
        dataset_id=config.dataset_id,
        model_base=config.model_base,
        algorithm=config.algorithm,
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
def list_jobs(db: Session = Depends(get_db)):
    return db.query(models.TrainingJob).order_by(models.TrainingJob.id.desc()).all()

@router.get("/models")
def list_models(db: Session = Depends(get_db)):
    return db.query(models.ModelArtifact).all()
