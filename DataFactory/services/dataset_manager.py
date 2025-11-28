"""
Dataset Manager for Data Factory
Manages dataset creation, versioning, and lifecycle.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class DatasetType(str, Enum):
    """Types of datasets"""
    SFT = "sft"  # Supervised Fine-Tuning
    RFT = "rft"  # Reinforcement Fine-Tuning
    RM = "rm"    # Reward Model
    EVAL = "eval"  # Evaluation


class DatasetStatus(str, Enum):
    """Dataset lifecycle status"""
    BUILDING = "building"
    READY = "ready"
    DEPRECATED = "deprecated"


class Dataset(BaseModel):
    """Dataset definition"""
    dataset_id: str
    name: str
    dataset_type: DatasetType
    version: str
    status: DatasetStatus = DatasetStatus.BUILDING
    event_ids: List[str] = []
    size: int = 0
    created_at: datetime
    metadata: Optional[Dict] = None
    
    class Config:
        use_enum_values = True


class DatasetManager:
    """Manages datasets and versions"""
    
    def __init__(self):
        self.datasets: Dict[str, Dataset] = {}
        self.version_counter: Dict[str, int] = {}
    
    def create_dataset(
        self,
        name: str,
        dataset_type: DatasetType,
        event_ids: List[str],
        metadata: Optional[Dict] = None
    ) -> Dataset:
        """
        Create a new dataset.
        
        Args:
            name: Dataset  name
            dataset_type: Type of dataset
            event_ids: List of event IDs to include
            metadata: Optional metadata
            
        Returns:
            Created Dataset
        """
        # Generate version
        if name not in self.version_counter:
            self.version_counter[name] = 0
        self.version_counter[name] += 1
        version = f"v{self.version_counter[name]}"
        
        dataset_id = f"ds_{name}_{version}_{datetime.now().timestamp()}"
        dataset = Dataset(
            dataset_id=dataset_id,
            name=name,
            dataset_type=dataset_type,
            version=version,
            event_ids=event_ids,
            size=len(event_ids),
            created_at=datetime.now(),
            metadata=metadata
        )
        
        self.datasets[dataset_id] = dataset
        return dataset
    
    def finalize_dataset(self, dataset_id: str) -> bool:
        """
        Mark dataset as ready for use.
        
        Args:
            dataset_id: ID of dataset to finalize
            
        Returns:
            True if successfully finalized
        """
        if dataset_id in self.datasets:
            self.datasets[dataset_id].status = DatasetStatus.READY
            return True
        return False
    
    def deprecate_dataset(self, dataset_id: str) -> bool:
        """
        Deprecate an old dataset version.
        
        Args:
            dataset_id: ID of dataset to deprecate
            
        Returns:
            True if successfully deprecated
        """
        if dataset_id in self.datasets:
            self.datasets[dataset_id].status = DatasetStatus.DEPRECATED
            return True
        return False
    
    def get_dataset(self, dataset_id: str) -> Optional[Dataset]:
        """Get dataset by ID"""
        return self.datasets.get(dataset_id)
    
    def list_datasets(
        self,
        dataset_type: Optional[DatasetType] = None,
        status: Optional[DatasetStatus] = None
    ) -> List[Dataset]:
        """
        List datasets with filters.
        
        Args:
            dataset_type: Filter by dataset type
            status: Filter by status
            
        Returns:
            List of matching datasets
        """
        datasets = list(self.datasets.values())
        
        if dataset_type:
            datasets = [d for d in datasets if d.dataset_type == dataset_type]
        
        if status:
            datasets = [d for d in datasets if d.status == status]
        
        return datasets
    
    def get_versions(self, name: str) -> List[Dataset]:
        """
        Get all versions of a dataset.
        
        Args:
            name: Dataset name
            
        Returns:
            List of dataset versions
        """
        return [d for d in self.datasets.values() if d.name == name]
    
    def get_latest_version(
        self,
        name: str,
        dataset_type: Optional[DatasetType] = None
    ) -> Optional[Dataset]:
        """
        Get the latest version of a dataset.
        
        Args:
            name: Dataset name
            dataset_type: Optional filter by type
            
        Returns:
            Latest dataset version or None
        """
        versions = self.get_versions(name)
        
        if dataset_type:
            versions = [d for d in versions if d.dataset_type == dataset_type]
        
        if not versions:
            return None
        
        # Sort by version number
        versions.sort(key=lambda d: int(d.version[1:]), reverse=True)
        return versions[0]
    
    def get_statistics(self) -> Dict:
        """Get dataset statistics"""
        by_type = {}
        by_status = {}
        
        for dataset in self.datasets.values():
            by_type[dataset.dataset_type] = by_type.get(dataset.dataset_type, 0) + 1
            by_status[dataset.status] = by_status.get(dataset.status, 0) + 1
        
        total_events = sum(d.size for d in self.datasets.values())
        
        return {
            "total_datasets": len(self.datasets),
            "total_events": total_events,
            "by_type": by_type,
            "by_status": by_status
        }
