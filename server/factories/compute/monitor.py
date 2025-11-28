"""
Resource Monitor for Compute Factory
Tracks resource usage, metrics, and cost.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime
import psutil


class UsageMetrics(BaseModel):
    """Resource usage metrics"""
    timestamp: datetime
    resource_id: str
    cpu_percent: float
    memory_percent: float
    gpu_utilization: Optional[float] = None
    gpu_memory_used: Optional[float] = None
    
    
class CostReport(BaseModel):
    """Cost calculation report"""
    period_start: datetime
    period_end: datetime
    total_compute_hours: float
    inference_cost: float
    training_cost: float
    total_cost: float


class ResourceMonitor:
    """Monitors resource usage and calculates costs"""
    
    def __init__(self):
        self.metrics_history: List[UsageMetrics] = []
        self.cost_per_gpu_hour = 1.0  # USD
        self.cost_per_cpu_hour = 0.1  # USD
    
    def collect_metrics(self, resource_id: str) -> UsageMetrics:
        """
        Collect current resource metrics.
        
        Args:
            resource_id: ID of resource to monitor
            
        Returns:
            UsageMetrics snapshot
        """
        metrics = UsageMetrics(
            timestamp=datetime.now(),
            resource_id=resource_id,
            cpu_percent=psutil.cpu_percent(interval=1),
            memory_percent=psutil.virtual_memory().percent
        )
        self.metrics_history.append(metrics)
        return metrics
    
    def get_current_usage(self) -> Dict:
        """Get current system resource usage"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "cpu_percent": cpu_percent,
            "memory_total_gb": memory.total / (1024**3),
            "memory_used_gb": memory.used / (1024**3),
            "memory_percent": memory.percent,
            "disk_total_gb": disk.total / (1024**3),
            "disk_used_gb": disk.used / (1024**3),
            "disk_percent": disk.percent
        }
    
    def calculate_cost(
        self, 
        start_time: datetime, 
        end_time: datetime,
        gpu_count: int = 0,
        cpu_count: int = 1
    ) -> float:
        """
        Calculate cost for resource usage.
        
        Args:
            start_time: Start of usage period
            end_time: End of usage period
            gpu_count: Number of GPUs used
            cpu_count: Number of CPUs used
            
        Returns:
            Total cost in USD
        """
        duration_hours = (end_time - start_time).total_seconds() / 3600
        gpu_cost = gpu_count * duration_hours * self.cost_per_gpu_hour
        cpu_cost = cpu_count * duration_hours * self.cost_per_cpu_hour
        return gpu_cost + cpu_cost
    
    def generate_cost_report(
        self, 
        start: datetime, 
        end: datetime
    ) -> CostReport:
        """
        Generate cost report for a time period.
        
        Args:
            start: Report period start
            end: Report period end
            
        Returns:
            CostReport with breakdown
        """
        duration_hours = (end - start).total_seconds() / 3600
        
        # Mock calculations - in real implementation, query actual usage
        inference_cost = duration_hours * 0.5
        training_cost = duration_hours * 2.0
        
        return CostReport(
            period_start=start,
            period_end=end,
            total_compute_hours=duration_hours,
            inference_cost=inference_cost,
            training_cost=training_cost,
            total_cost=inference_cost + training_cost
        )
    
    def get_metrics_summary(self, resource_id: Optional[str] = None) -> Dict:
        """
        Get summary of collected metrics.
        
        Args:
            resource_id: Optional filter by resource ID
            
        Returns:
            Metrics summary statistics
        """
        if resource_id:
            metrics = [m for m in self.metrics_history if m.resource_id == resource_id]
        else:
            metrics = self.metrics_history
        
        if not metrics:
            return {"message": "No metrics available"}
        
        avg_cpu = sum(m.cpu_percent for m in metrics) / len(metrics)
        avg_memory = sum(m.memory_percent for m in metrics) / len(metrics)
        
        return {
            "total_samples": len(metrics),
            "avg_cpu_percent": round(avg_cpu, 2),
            "avg_memory_percent": round(avg_memory, 2),
            "latest_timestamp": metrics[-1].timestamp.isoformat()
        }
