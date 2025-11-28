from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import models, database
from pydantic import BaseModel

router = APIRouter(prefix="/reward", tags=["Reward Factory"])

class EvalRequest(BaseModel):
    model_id: str
    scenario_id: int

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/evaluations")
def run_evaluation(request: EvalRequest, db: Session = Depends(get_db)):
    # Mock evaluation logic
    score = 0.85
    passed = True
    report = {"safety_score": 95, "performance_score": 85, "details": "Passed all safety checks."}
    
    db_eval = models.Evaluation(
        model_id=int(request.model_id) if request.model_id else None,
        scenario_id=request.scenario_id,
        score=score,
        status="completed",
        report=report
    )
    db.add(db_eval)
    db.commit()
    db.refresh(db_eval)
    return db_eval

@router.get("/evaluations")
def list_evaluations(db: Session = Depends(get_db)):
    return db.query(models.Evaluation).order_by(models.Evaluation.id.desc()).all()
