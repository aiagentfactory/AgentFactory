from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import models, database
from pydantic import BaseModel
import time
import uuid
import random

router = APIRouter(prefix="/pipeline", tags=["Pipeline Factory"])

class PipelineConfig(BaseModel):
    name: str
    dataset_id: int
    algorithm: str
    scenario_id: int

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def run_pipeline_task(pipeline_id: int, config: PipelineConfig):
    db = database.SessionLocal()
    pipeline = db.query(models.PipelineRun).filter(models.PipelineRun.id == pipeline_id).first()
    
    artifacts = {}
    
    # Step 1: Training
    pipeline.current_stage = "Training Model..."
    db.commit()
    
    job = models.TrainingJob(
        model_base="llama-3-8b",
        algorithm=config.algorithm,
        dataset_id=config.dataset_id,
        status="training",
        progress=0.0,
        metrics={}
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    artifacts["job_id"] = job.id
    pipeline.artifacts = artifacts
    db.commit()
    
    # Simulate training wait
    for i in range(1, 4):
        time.sleep(2)
        job.progress = i * 33.3
        db.commit()
    
    job.status = "completed"
    job.progress = 100.0
    
    # Create Model
    model_name = f"PipeModel_{pipeline.name}_{str(uuid.uuid4())[:4]}"
    model = models.Model(
        name=model_name,
        version="1.0.0",
        source_job_id=job.id
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    artifacts["model_id"] = model.id
    pipeline.artifacts = artifacts
    db.commit()
    
    # Step 2: Evaluation
    pipeline.current_stage = "Evaluating Safety..."
    db.commit()
    time.sleep(2)
    
    eval_run = models.Evaluation(
        model_id=model.id,
        scenario_id=config.scenario_id,
        score=0.92,
        status="completed",
        report={"safety": "pass", "performance": "high"}
    )
    db.add(eval_run)
    db.commit()
    db.refresh(eval_run)
    artifacts["eval_id"] = eval_run.id
    pipeline.artifacts = artifacts
    db.commit()
    
    # Step 3: Deployment
    pipeline.current_stage = "Deploying Agent..."
    db.commit()
    time.sleep(1)
    
    agent = models.Agent(
        name=f"Agent_{pipeline.name}",
        model_id=model.id,
        version="v1",
        status="active",
        config={}
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    artifacts["agent_id"] = agent.id
    
    pipeline.status = "completed"
    pipeline.current_stage = "Ready"
    pipeline.artifacts = artifacts
    db.commit()
    db.close()

@router.post("/runs")
def create_pipeline_run(config: PipelineConfig, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    pipeline = models.PipelineRun(
        name=config.name,
        status="running",
        current_stage="Initializing...",
        config=config.dict(),
        artifacts={}
    )
    db.add(pipeline)
    db.commit()
    db.refresh(pipeline)
    
    background_tasks.add_task(run_pipeline_task, pipeline.id, config)
    
    return pipeline

@router.get("/runs")
def list_pipeline_runs(db: Session = Depends(get_db)):
    return db.query(models.PipelineRun).order_by(models.PipelineRun.id.desc()).all()
