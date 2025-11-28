"""
Evaluation Factory API Router (formerly Reward Factory)
Provides agent evaluation, safety testing, and LLM-as-a-judge endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict

router = APIRouter(prefix="/eval", tags=["Evaluation Factory"])


# Request Models
class CreateTaskSetRequest(BaseModel):
    name: str
    difficulty_level: int  # 1-5
    tasks: List[Dict]


class RunEvaluationRequest(BaseModel):
    model_id: str
    taskset_id: str
    criteria: Optional[List[str]] = None


@router.post("/taskset")
def create_taskset(request: CreateTaskSetRequest):
    """Create an evaluation task set"""
    taskset_id = f"taskset_{request.name}_{request.difficulty_level}"
    
    return {
        "status": "success",
        "taskset_id": taskset_id,
        "name": request.name,
        "difficulty_level": request.difficulty_level,
        "task_count": len(request.tasks)
    }


@router.get("/taskset")
def list_tasksets():
    """List all task sets"""
    # Mock tasksets
    tasksets = [
        {
            "taskset_id": "taskset_basic_1",
            "name": "Basic Tasks",
            "difficulty_level": 1,
            "task_count": 50,
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "taskset_id": "taskset_advanced_4",
            "name": "Advanced Tasks",
            "difficulty_level": 4,
            "task_count": 30,
            "created_at": "2024-01-02T00:00:00"
        }
    ]
    
    return {
        "status": "success",
        "tasksets": tasksets,
        "count": len(tasksets)
    }


@router.post("/run")
def run_evaluation(request: RunEvaluationRequest):
    """Run evaluation on a model"""
    eval_id = f"eval_{request.model_id}_{request.taskset_id}"
    
    return {
        "status": "success",
        "eval_id": eval_id,
        "model_id": request.model_id,
        "taskset_id": request.taskset_id,
        "state": "running"
    }


@router.get("/results/{eval_id}")
def get_evaluation_results(eval_id: str):
    """Get evaluation results"""
    # Mock results
    results = {
        "eval_id": eval_id,
        "status": "completed",
        "metrics": {
            "task_success_rate": 0.85,
            "quality_score": 0.78,
            "tool_accuracy": 0.92,
            "safety_score": 0.95,
            "hallucination_score": 0.12
        },
        "verdict": "PASS",
        "completed_at": "2024-01-03T10:30:00"
    }
    
    return {
        "status": "success",
        **results
    }


@router.get("/results/{eval_id}/details")
def get_evaluation_details(eval_id: str):
    """Get detailed evaluation results"""
    details = {
        "eval_id": eval_id,
        "per_task_results": [
            {
                "task_id": "task_001",
                "success": True,
                "score": 0.9,
                "errors": []
            },
            {
                "task_id": "task_002",
                "success": False,
                "score": 0.3,
                "errors": ["Tool call failed", "Hallucination detected"]
            }
        ],
        "error_clusters": {
            "tool_errors": 5,
            "hallucinations": 3,
            "timeout": 2
        }
    }
    
    return {
        "status": "success",
        **details
    }


@router.get("/benchmarks")
def get_benchmarks():
    """Get benchmark comparison across models"""
    # Mock benchmark data
    benchmarks = {
        "models": ["model_v1", "model_v2", "model_v3"],
        "metrics": {
            "task_success_rate": [0.75, 0.85, 0.90],
            "quality_score": [0.70, 0.78, 0.85],
            "safety_score": [0.90, 0.95, 0.97]
        }
    }
    
    return {
        "status": "success",
        **benchmarks
    }
