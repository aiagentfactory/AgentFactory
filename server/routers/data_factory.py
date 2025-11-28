"""
Data Factory API Router
Provides data collection, cleaning, annotation, and dataset management endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict

# Import data factory modules
from ..factories.data import DataCollector, DataCleaner, DataAnnotator, DatasetManager
from ..factories.data.collector import EventType
from ..factories.data.annotator import AnnotationType
from ..factories.data.dataset_manager import DatasetType

router = APIRouter(prefix="/data", tags=["Data Factory"])

# Initialize singletons  
data_collector = DataCollector()
data_cleaner = DataCleaner()
data_annotator = DataAnnotator()
dataset_manager = DatasetManager()


# Request Models
class CollectInteractionRequest(BaseModel):
    agent_id: str
    session_id: str
    prompt: str
    response: str
    metadata: Optional[Dict] = None


class AddAnnotationRequest(BaseModel):
    event_id: str
    rating: float
    annotator_id: str
    comments: Optional[str] = None


class CreateDatasetRequest(BaseModel):
    name: str
    dataset_type: DatasetType
    event_ids: List[str]
    metadata: Optional[Dict] = None


@router.post("/events")
def collect_event(request: CollectInteractionRequest):
    """Collect an Agent interaction event"""
    event = data_collector.collect_interaction(
        agent_id=request.agent_id,
        session_id=request.session_id,
        prompt=request.prompt,
        response=request.response,
        metadata=request.metadata
    )
    
    return {
        "status": "success",
        "event": event.dict()
    }


@router.get("/events")
def get_events(
    event_type: Optional[EventType] = None,
    agent_id: Optional[str] = None,
    limit: int = 100
):
    """Get collected events"""
    events = data_collector.get_events(
        event_type=event_type,
        agent_id=agent_id,
        limit=limit
    )
    
    return {
        "status": "success",
        "events": [e.dict() for e in events],
        "count": len(events)
    }


@router.get("/events/statistics")
def get_event_statistics():
    """Get event collection statistics"""
    stats = data_collector.get_statistics()
    return {
        "status": "success",
        **stats
    }


@router.post("/label")
def add_annotation(request: AddAnnotationRequest):
    """Add human annotation to an event"""
    annotation = data_annotator.add_human_rating(
        event_id=request.event_id,
        rating=request.rating,
        annotator_id=request.annotator_id,
        comments=request.comments
    )
    
    return {
        "status": "success",
        "annotation": annotation.dict()
    }


@router.get("/annotations/{event_id}")
def get_annotations(event_id: str):
    """Get annotations for an event"""
    annotations = data_annotator.get_annotations(event_id=event_id)
    
    return {
        "status": "success",
        "annotations": [a.dict() for a in annotations],
        "count": len(annotations)
    }


@router.post("/datasets/create")
def create_dataset(request: CreateDatasetRequest):
    """Create a new dataset"""
    dataset = dataset_manager.create_dataset(
        name=request.name,
        dataset_type=request.dataset_type,
        event_ids=request.event_ids,
        metadata=request.metadata
    )
    
    return {
        "status": "success",
        "dataset": dataset.dict()
    }


@router.get("/datasets/{dataset_id}")
def get_dataset(dataset_id: str):
    """Get dataset by ID"""
    dataset = dataset_manager.get_dataset(dataset_id)
    
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    return {
        "status": "success",
        "dataset": dataset.dict()
    }


@router.get("/datasets")
def list_datasets(
    dataset_type: Optional[DatasetType] = None
):
    """List all datasets"""
    datasets = dataset_manager.list_datasets(dataset_type=dataset_type)
    
    return {
        "status": "success",
        "datasets": [d.dict() for d in datasets],
        "count": len(datasets)
    }


@router.post("/datasets/{dataset_id}/finalize")
def finalize_dataset(dataset_id: str):
    """Mark dataset as ready"""
    success = dataset_manager.finalize_dataset(dataset_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    return {
        "status": "success",
        "dataset_id": dataset_id,
        "message": "Dataset finalized"
    }
