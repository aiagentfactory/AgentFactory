from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter(prefix="/compute", tags=["Compute Factory"])

class ResourceRequest(BaseModel):
    gpu_type: str
    count: int

@router.post("/allocate")
def allocate_resources(req: ResourceRequest):
    return {
        "status": "allocated",
        "resource_id": "res-12345",
        "details": f"Allocated {req.count} x {req.gpu_type}"
    }

@router.get("/usage")
def get_usage():
    return {
        "gpu_util": "45%",
        "memory_util": "60%",
        "active_nodes": 3
    }
