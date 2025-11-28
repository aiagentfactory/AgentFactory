from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import models, database
from pydantic import BaseModel
import time
import random

router = APIRouter(prefix="/reward", tags=["Reward Factory"])

class EvalRequest(BaseModel):
    model_id: int
    scenario_id: int

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def mock_eval_process(eval_id: int):
    db = database.SessionLocal()
    eval_task = db.query(models.Evaluation).filter(models.Evaluation.id == eval_id).first()
    time.sleep(3) # Simulate processing
    
    score = random.uniform(0.6, 0.99)
    eval_task.score = score
    eval_task.status = "completed"
    eval_task.report = {
        "safety_score": 0.95,
        "helpfulness": score,
        "details": "Agent performed well in scenario."
    }
    db.commit()
    db.close()

@router.post("/evaluations")
def run_evaluation(req: EvalRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    eval_task = models.Evaluation(
        model_id=req.model_id,
        scenario_id=req.scenario_id,
        score=0.0,
        status="running",
        report={}
    )
    db.add(eval_task)
    db.commit()
    db.refresh(eval_task)
    
    background_tasks.add_task(mock_eval_process, eval_task.id)
    return eval_task

@router.get("/evaluations")
def list_evaluations(db: Session = Depends(get_db)):
    return db.query(models.Evaluation).order_by(models.Evaluation.id.desc()).all()
