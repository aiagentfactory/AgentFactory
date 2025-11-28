"""
Training Factory API Router (formerly Algo Factory)
Provides model training, fine-tuning, and RL training endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List

router = APIRouter(prefix="/train", tags=["Training Factory"])


# Request Models
class CreateTrainingJobRequest(BaseModel):
    name: str
    model_base: str
    dataset_id: str
    training_type: str  # "sft", "rft", "ppo", "dpo"
    config: Optional[Dict] = None


class RewardConfigRequest(BaseModel):
    reward_model_id: Optional[str] = None
    reward_criteria: Optional[List[str]] = None


@router.post("/jobs")
def create_training_job(request: CreateTrainingJobRequest):
    """Create a new training job"""
    job_id = f"job_{request.name}_{hash(request.dataset_id)}"
    
    return {
        "status": "success",
        "job_id": job_id,
        "name": request.name,
        "training_type": request.training_type,
        "state": "pending"
    }


@router.get("/jobs")
def list_training_jobs():
    """List all training jobs"""
    # Mock data
    jobs = [
        {
            "job_id": "job_sft_001",
            "name": "SFT Training v1",
            "training_type": "sft",
            "status": "completed",
            "progress": 100,
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "job_id": "job_ppo_001",
            "name": "PPO Training v1",
            "training_type": "ppo",
            "status": "running",
            "progress": 45,
            "created_at": "2024-01-02T00:00:00"
        }
    ]
    
    return {
        "status": "success",
        "jobs": jobs,
        "count": len(jobs)
    }


@router.get("/jobs/{job_id}/status")
def get_job_status(job_id: str):
    """Get training job status"""
    # Mock status
    status = {
        "job_id": job_id,
        "status": "running",
        "progress": 65,
        "current_epoch": 3,
        "total_epochs": 5,
        "metrics": {
            "loss": 0.35,
            "accuracy": 0.87,
            "learning_rate": 0.0001
        }
    }
    
    return {
        "status": "success",
        **status
    }


@router.post("/jobs/{job_id}/reward-config")
def configure_reward(job_id: str, request: RewardConfigRequest):
    """Configure reward model for RL training"""
    return {
        "status": "success",
        "job_id": job_id,
        "reward_config": request.dict(),
        "message": "Reward configuration updated"
    }


@router.post("/models/promote")
def promote_model(model_id: str, environment: str = "production"):
    """Promote a trained model to production"""
    return {
        "status": "success",
        "model_id": model_id,
        "environment": environment,
        "message": f"Model promoted to {environment}"
    }


@router.get("/models")
def list_models():
    """List all trained models"""
    # Mock models
    models = [
        {
            "model_id": "model_v1",
            "name": "Agent Model v1",
            "base_model": "gpt-3.5-turbo",
            "training_job_id": "job_sft_001",
            "status": "ready",
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "model_id": "model_v2",
            "name": "Agent Model v2",
            "base_model": "gpt-4",
            "training_job_id": "job_ppo_001",
            "status": "training",
            "created_at": "2024-01-02T00:00:00"
        }
    ]
    
    return {
        "status": "success",
        "models": models,
        "count": len(models)
    }
