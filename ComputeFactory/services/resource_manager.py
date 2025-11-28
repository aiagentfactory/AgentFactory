"""
Resource Manager for Compute Factory
Handles resource abstraction, allocation, and pool management.
"""

from typing import Dict, Optional, List
from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class ResourceType(str, Enum):
    """Types of compute resources"""
    GPU = "gpu"
    CPU = "cpu"
    NPU = "npu"
    TPU = "tpu"


class PoolType(str, Enum):
    """Types of resource pools"""
    INFERENCE = "inference"
    TRAINING = "training"
    ENVIRONMENT = "environment"


class ResourceSpec(BaseModel):
    """Specification for compute resources"""
    resource_type: ResourceType
    count: int
    memory_gb: Optional[int] = None
    bandwidth_gbps: Optional[float] = None
    accelerator_model: Optional[str] = None
    
    class Config:
        use_enum_values = True


class ResourceAllocation(BaseModel):
    """Record of resource allocation"""
    allocation_id: str
    pool_type: PoolType
    resource_spec: ResourceSpec
    allocated_at: datetime
    released_at: Optional[datetime] = None
    job_id: Optional[str] = None
    
    class Config:
        use_enum_values = True


class ResourceManager:
    """Manages compute resource allocation and pools"""
    
    def __init__(self):
        self.pools: Dict[PoolType, List[ResourceSpec]] = {
            PoolType.INFERENCE: [],
            PoolType.TRAINING: [],
            PoolType.ENVIRONMENT: []
        }
        self.allocations: Dict[str, ResourceAllocation] = {}
    
    def allocate_resource(
        self, 
        pool_type: PoolType, 
        resource_spec: ResourceSpec,
        job_id: Optional[str] = None
    ) -> ResourceAllocation:
        """
        Allocate resources from a specific pool.
        
        Args:
            pool_type: Type of resource pool
            resource_spec: Specification of required resources
            job_id: Optional job identifier
            
        Returns:
            ResourceAllocation record
        """
        allocation_id = f"alloc_{datetime.now().timestamp()}"
        allocation = ResourceAllocation(
            allocation_id=allocation_id,
            pool_type=pool_type,
            resource_spec=resource_spec,
            allocated_at=datetime.now(),
            job_id=job_id
        )
        self.allocations[allocation_id] = allocation
        return allocation
    
    def release_resource(self, allocation_id: str) -> bool:
        """
        Release allocated resources.
        
        Args:
            allocation_id: ID of the allocation to release
            
        Returns:
            True if successfully released
        """
        if allocation_id in self.allocations:
            self.allocations[allocation_id].released_at = datetime.now()
            return True
        return False
    
    def get_pool_status(self, pool_type: PoolType) -> Dict:
        """
        Get status of a resource pool.
        
        Args:
            pool_type: Type of pool to query
            
        Returns:
            Dictionary with pool statistics
        """
        active_allocations = [
            a for a in self.allocations.values()
            if a.pool_type == pool_type and a.released_at is None
        ]
        
        return {
            "pool_type": pool_type,
            "total_resources": len(self.pools[pool_type]),
            "active_allocations": len(active_allocations),
            "available": len(self.pools[pool_type]) - len(active_allocations)
        }
    
    def get_all_pools(self) -> List[Dict]:
        """Get status of all resource pools"""
        return [self.get_pool_status(pt) for pt in PoolType]
