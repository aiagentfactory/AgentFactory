from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter(prefix="/reward", tags=["Reward Factory"])

class EvalRequest(BaseModel):
    trajectory: list
    criteria: str

@router.post("/eval/run")
def run_evaluation(request: EvalRequest):
    # Mock evaluation logic
    score = 0.0
    if len(request.trajectory) > 0:
        score = 0.8 # Mock high score for existing trajectory
    
    return {
        "score": score,
        "passed": score > 0.5,
        "report": "Evaluation complete. Agent performed adequately."
    }
