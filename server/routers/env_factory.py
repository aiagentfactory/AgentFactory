"""
Environment Factory API Router
Provides environment definition, scenario building, and rollout execution endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict

router = APIRouter(prefix="/env", tags=["Environment Factory"])


# Mock implementations for MVP
class CreateScenarioRequest(BaseModel):
    name: str
    env_type: str  # "http_api", "browser", "rpa"
    config: Dict


class RunEnvironmentRequest(BaseModel):
    scenario_id: str
    agent_id: str
    max_steps: int = 100


@router.post("/scenarios")
def create_scenario(request: CreateScenarioRequest):
    """Create a new environment scenario"""
    scenario_id = f"scenario_{request.name}_{hash(str(request.config))}"
    
    return {
        "status": "success",
        "scenario_id": scenario_id,
        "name": request.name,
        "env_type": request.env_type
    }


@router.get("/scenarios")
def list_scenarios():
    """List all scenarios"""
    # Mock data
    scenarios = [
        {
            "scenario_id": "scenario_customer_support",
            "name": "Customer Support Simulation",
            "env_type": "http_api",
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "scenario_id": "scenario_web_navigation",
            "name": "Web Navigation Task",
            "env_type": "browser",
            "created_at": "2024-01-02T00:00:00"
        }
    ]
    
    return {
        "status": "success",
        "scenarios": scenarios,
        "count": len(scenarios)
    }
 

@router.post("/run")
def run_environment(request: RunEnvironmentRequest):
    """Execute an agent in an environment"""
    run_id = f"run_{request.scenario_id}_{request.agent_id}"
    
    # Mock rollout execution
    return {
        "status": "success",
        "run_id": run_id,
        "scenario_id": request.scenario_id,
        "agent_id": request.agent_id,
        "state": "running"
    }


@router.get("/run/{run_id}/trace")
def get_trace(run_id: str):
    """Get execution trace for a run"""
    # Mock trace data
    trace = {
        "run_id": run_id,
        "steps": [
            {
                "step": 1,
                "observation": "Welcome to the environment",
                "action": "analyze_situation",
                "reward": 0.1
            },
            {
                "step": 2,
                "observation": "Situation analyzed",
                "action": "take_action_1",
                "reward": 0.5
            }
        ],
        "total_reward": 0.6,
        "completed": True
    }
    
    return {
        "status": "success",
        "trace": trace
    }


@router.get("/run/{run_id}/replay")
def replay_run(run_id: str):
    """Get timeline for replay"""
    timeline = {
        "run_id": run_id,
        "timeline": [
            {"timestamp": "00:00:01", "event": "Environment initialized"},
            {"timestamp": "00:00:02", "event": "Agent started"},
            {"timestamp": "00:00:05", "event": "Action executed"},
            {"timestamp": "00:00:08", "event": "Task completed"}
        ]
    }
    
    return {
        "status": "success",
        **timeline
    }
