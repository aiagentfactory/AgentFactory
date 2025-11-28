from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import models, database
from pydantic import BaseModel
from typing import Dict, Any, Optional

router = APIRouter(prefix="/env", tags=["Environment Factory"])

class ScenarioCreate(BaseModel):
    name: str
    type: str
    config: Dict[str, Any]

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/scenarios")
def create_scenario(scenario: ScenarioCreate, db: Session = Depends(get_db)):
    db_scenario = models.Scenario(name=scenario.name, type=scenario.type, config=scenario.config)
    db.add(db_scenario)
    db.commit()
    db.refresh(db_scenario)
    return db_scenario

@router.get("/scenarios")
def list_scenarios(db: Session = Depends(get_db)):
    return db.query(models.Scenario).all()

@router.post("/runs")
def start_run(scenario_id: int, db: Session = Depends(get_db)):
    # Mocking a run start
    db_run = models.Run(scenario_id=scenario_id, status="running", logs=[])
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run

@router.post("/runs/{run_id}/step")
def step_run(run_id: int, action: Dict[str, Any], db: Session = Depends(get_db)):
    run = db.query(models.Run).filter(models.Run.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    # Mock logic: If action contains 'finish', complete the run
    observation = {"obs": f"Processed action: {action}", "status": "ongoing"}
    
    if "finish" in str(action).lower():
         run.status = "completed"
         observation["status"] = "done"
    
    # Update logs (simple append mock)
    current_logs = list(run.logs) if run.logs else []
    current_logs.append({"action": action, "observation": observation})
    run.logs = current_logs
    
    db.commit()
    return observation
