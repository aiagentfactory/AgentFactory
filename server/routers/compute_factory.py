from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Import compute factory modules
from ..factories.compute import ResourceManager, JobScheduler, ResourceMonitor
from ..factories.compute.resource_manager import ResourceSpec, ResourceType, PoolType
from ..factories.compute.scheduler import JobPriority

router = APIRouter(prefix="/compute", tags=["Compute Factory"])

# Initialize singletons
resource_manager = ResourceManager()
job_scheduler = JobScheduler()
resource_monitor = ResourceMonitor()


# Request/Response Models
class AllocateResourceRequest(BaseModel):
    pool_type: PoolType
    resource_type: ResourceType
    count: int
    memory_gb: Optional[int] = None
    job_id: Optional[str] = None


class ReleaseResourceRequest(BaseModel):
    allocation_id: str


class SubmitJobRequest(BaseModel):
    name: str
    priority: JobPriority = JobPriority.NORMAL
    preemptible: bool = False


@router.post("/allocate")
def allocate_resource(request: AllocateResourceRequest):
    """Allocate compute resources from a pool"""
    resource_spec = ResourceSpec(
        resource_type=request.resource_type,
        count=request.count,
        memory_gb=request.memory_gb
    )
    
    allocation = resource_manager.allocate_resource(
        pool_type=request.pool_type,
        resource_spec=resource_spec,
        job_id=request.job_id
    )
    
    return {
        "status": "success",
        "allocation": allocation.dict()
    }


@router.post("/release")
def release_resource(request: ReleaseResourceRequest):
    """Release allocated resources"""
    success = resource_manager.release_resource(request.allocation_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Allocation not found")
    
    return {
        "status": "success",
        "allocation_id": request.allocation_id
    }


@router.get("/pools")
def get_pools():
    """Get status of all resource pools"""
    pools = resource_manager.get_all_pools()
    return {
        "status": "success",
        "pools": pools
    }


@router.get("/pools/{pool_type}")
def get_pool_status(pool_type: PoolType):
    """Get status of a specific resource pool"""
    status = resource_manager.get_pool_status(pool_type)
    return {
        "status": "success",
        "pool": status
    }


@router.get("/usage")
def get_usage():
    return {
        "gpu_util": "45%",
        "memory_util": "60%",
        "active_nodes": 3
    }
