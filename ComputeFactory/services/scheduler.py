"""
Job Scheduler for Compute Factory
Handles job queue, priority scheduling, and autoscaling.
"""

from typing import Dict, List, Optional
from enum import Enum
from pydantic import BaseModel
from datetime import datetime
import asyncio


class JobPriority(str, Enum):
    """Job priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class JobStatus(str, Enum):
    """Job execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PREEMPTED = "preempted"


class ComputeJob(BaseModel):
    """Compute job definition"""
    job_id: str
    name: str
    priority: JobPriority = JobPriority.NORMAL
    status: JobStatus = JobStatus.PENDING
    preemptible: bool = False
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    allocation_id: Optional[str] = None
    
    class Config:
        use_enum_values = True


class JobScheduler:
    """Manages job scheduling and execution"""
    
    def __init__(self):
        self.job_queue: List[ComputeJob] = []
        self.running_jobs: Dict[str, ComputeJob] = {}
        self.completed_jobs: Dict[str, ComputeJob] = {}
    
    def submit_job(
        self, 
        name: str, 
        priority: JobPriority = JobPriority.NORMAL,
        preemptible: bool = False
    ) -> ComputeJob:
        """
        Submit a new job to the queue.
        
        Args:
            name: Job name
            priority: Job priority level
            preemptible: Whether job can be preempted
            
        Returns:
            Created ComputeJob
        """
        job_id = f"job_{datetime.now().timestamp()}"
        job = ComputeJob(
            job_id=job_id,
            name=name,
            priority=priority,
            preemptible=preemptible,
            created_at=datetime.now()
        )
        self.job_queue.append(job)
        self._sort_queue()
        return job
    
    def _sort_queue(self):
        """Sort job queue by priority"""
        priority_order = {
            JobPriority.CRITICAL: 0,
            JobPriority.HIGH: 1,
            JobPriority.NORMAL: 2,
            JobPriority.LOW: 3
        }
        self.job_queue.sort(key=lambda j: priority_order[j.priority])
    
    def start_job(self, job_id: str, allocation_id: str) -> bool:
        """
        Start a job with allocated resources.
        
        Args:
            job_id: ID of job to start
            allocation_id: ID of resource allocation
            
        Returns:
            True if job started successfully
        """
        job = next((j for j in self.job_queue if j.job_id == job_id), None)
        if job:
            job.status = JobStatus.RUNNING
            job.started_at = datetime.now()
            job.allocation_id = allocation_id
            self.job_queue.remove(job)
            self.running_jobs[job_id] = job
            return True
        return False
    
    def complete_job(self, job_id: str, success: bool = True) -> bool:
        """
        Mark a job as completed.
        
        Args:
            job_id: ID of job to complete
            success: Whether job completed successfully
            
        Returns:
            True if job marked as completed
        """
        if job_id in self.running_jobs:
            job = self.running_jobs[job_id]
            job.status = JobStatus.COMPLETED if success else JobStatus.FAILED
            job.completed_at = datetime.now()
            del self.running_jobs[job_id]
            self.completed_jobs[job_id] = job
            return True
        return False
    
    def preempt_job(self, job_id: str) -> bool:
        """
        Preempt a running job if it's preemptible.
        
        Args:
            job_id: ID of job to preempt
            
        Returns:
            True if job was preempted
        """
        if job_id in self.running_jobs:
            job = self.running_jobs[job_id]
            if job.preemptible:
                job.status = JobStatus.PREEMPTED
                del self.running_jobs[job_id]
                self.job_queue.insert(0, job)  # Re-queue at front
                return True
        return False
    
    def get_queue_status(self) -> Dict:
        """Get current queue statistics"""
        return {
            "pending_jobs": len(self.job_queue),
            "running_jobs": len(self.running_jobs),
            "completed_jobs": len(self.completed_jobs),
            "queue": [
                {
                    "job_id": j.job_id,
                    "name": j.name,
                    "priority": j.priority,
                    "status": j.status
                }
                for j in self.job_queue[:10]  # Show first 10
            ]
        }
