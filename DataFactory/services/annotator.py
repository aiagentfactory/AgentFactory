"""
Data Annotator for Data Factory
Handles human annotation and LLM-based auto-annotation.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class AnnotationType(str, Enum):
    """Types of annotations"""
    HUMAN_RATING = "human_rating"
    HUMAN_PREFERENCE = "human_preference"
    LLM_SCORE = "llm_score"
    LLM_SUMMARY = "llm_summary"
    LLM_JUDGE = "llm_judge"


class Annotation(BaseModel):
    """Annotation record"""
    annotation_id: str
    event_id: str
    annotation_type: AnnotationType
    value: Optional[float] = None  # For ratings/scores
    text: Optional[str] = None  # For summaries/comments
    metadata: Optional[Dict] = None
    annotator_id: Optional[str] = None
    created_at: datetime
    
    class Config:
        use_enum_values = True


class DataAnnotator:
    """Manages data annotation tasks"""
    
    def __init__(self):
        self.annotations: Dict[str, List[Annotation]] = {}
    
    def add_human_rating(
        self,
        event_id: str,
        rating: float,
        annotator_id: str,
        comments: Optional[str] = None
    ) -> Annotation:
        """
        Add human rating annotation.
        
        Args:
            event_id: ID of event being annotated
            rating: Rating value (e.g., 1-5)
            annotator_id: ID of human annotator
            comments: Optional comments
            
        Returns:
            Created Annotation
        """
        annotation_id = f"anno_{datetime.now().timestamp()}"
        annotation = Annotation(
            annotation_id=annotation_id,
            event_id=event_id,
            annotation_type=AnnotationType.HUMAN_RATING,
            value=rating,
            text=comments,
            annotator_id=annotator_id,
            created_at=datetime.now()
        )
        
        if event_id not in self.annotations:
            self.annotations[event_id] = []
        self.annotations[event_id].append(annotation)
        
        return annotation
    
    def add_preference_comparison(
        self,
        response_a_id: str,
        response_b_id: str,
        preferred: str,  # "a" or "b"
        annotator_id: str
    ) -> Annotation:
        """
        Add preference comparison (for RLHF).
        
        Args:
            response_a_id: ID of first response
            response_b_id: ID of second response
            preferred: Which response was preferred ("a" or "b")
            annotator_id: ID of human annotator
            
        Returns:
            Created Annotation
        """
        annotation_id = f"anno_{datetime.now().timestamp()}"
        annotation = Annotation(
            annotation_id=annotation_id,
            event_id=f"{response_a_id}_{response_b_id}",
            annotation_type=AnnotationType.HUMAN_PREFERENCE,
            metadata={
                "response_a": response_a_id,
                "response_b": response_b_id,
                "preferred": preferred
            },
            annotator_id=annotator_id,
            created_at=datetime.now()
        )
        
        event_id = annotation.event_id
        if event_id not in self.annotations:
            self.annotations[event_id] = []
        self.annotations[event_id].append(annotation)
        
        return annotation
    
    def llm_auto_score(
        self,
        event_id: str,
        prompt: str,
        response: str,
        model: str = "gpt-4"
    ) -> Annotation:
        """
        Use LLM to automatically score a response.
        
        Args:
            event_id: ID of event being annotated
            prompt: Original prompt
            response: Response to score
            model: LLM model to use for scoring
            
        Returns:
            Created Annotation
        """
        # Mock LLM scoring - in real implementation, call actual LLM API
        mock_score = 0.75  # Score between 0-1
        
        annotation_id = f"anno_{datetime.now().timestamp()}"
        annotation = Annotation(
            annotation_id=annotation_id,
            event_id=event_id,
            annotation_type=AnnotationType.LLM_SCORE,
            value=mock_score,
            metadata={
                "model": model,
                "prompt": prompt[:100],  # Store truncated prompt
                "response": response[:100]
            },
            annotator_id=f"llm_{model}",
            created_at=datetime.now()
        )
        
        if event_id not in self.annotations:
            self.annotations[event_id] = []
        self.annotations[event_id].append(annotation)
        
        return annotation
    
    def llm_judge(
        self,
        event_id: str,
        criteria: List[str],
        response: str,
        model: str = "gpt-4"
    ) -> Annotation:
        """
        Use LLM as a judge based on criteria.
        
        Args:
            event_id: ID of event being judged
            criteria: List of evaluation criteria
            response: Response to evaluate
            model: LLM model to use
            
        Returns:
            Created Annotation
        """
        # Mock LLM judge - in real implementation, call actual LLM API
        mock_judgment = {
            "overall_score": 0.8,
            "criteria_scores": {c: 0.7 + (i * 0.05) for i, c in enumerate(criteria)},
            "reasoning": "Mock LLM judgment reasoning"
        }
        
        annotation_id = f"anno_{datetime.now().timestamp()}"
        annotation = Annotation(
            annotation_id=annotation_id,
            event_id=event_id,
            annotation_type=AnnotationType.LLM_JUDGE,
            value=mock_judgment["overall_score"],
            text=mock_judgment["reasoning"],
            metadata={
                "model": model,
                "criteria": criteria,
                "criteria_scores": mock_judgment["criteria_scores"]
            },
            annotator_id=f"llm_judge_{model}",
            created_at=datetime.now()
        )
        
        if event_id not in self.annotations:
            self.annotations[event_id] = []
        self.annotations[event_id].append(annotation)
        
        return annotation
    
    def get_annotations(
        self,
        event_id: Optional[str] = None,
        annotation_type: Optional[AnnotationType] = None
    ) -> List[Annotation]:
        """
        Retrieve annotations with filters.
        
        Args:
            event_id: Filter by event ID
            annotation_type: Filter by annotation type
            
        Returns:
            List of matching annotations
        """
        if event_id:
            annotations = self.annotations.get(event_id, [])
        else:
            annotations = [a for annos in self.annotations.values() for a in annos]
        
        if annotation_type:
            annotations = [a for a in annotations if a.annotation_type == annotation_type]
        
        return annotations
    
    def get_statistics(self) -> Dict:
        """Get annotation statistics"""
        all_annotations = [a for annos in self.annotations.values() for a in annos]
        
        by_type = {}
        for anno in all_annotations:
            by_type[anno.annotation_type] = by_type.get(anno.annotation_type, 0) + 1
        
        return {
            "total_annotations": len(all_annotations),
            "events_annotated": len(self.annotations),
            "by_type": by_type
        }
