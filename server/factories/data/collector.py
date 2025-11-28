"""
Data Collector for Data Factory
Collects Agent interaction logs, environment rollouts, and user data.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class EventType(str, Enum):
    """Types of data events"""
    INTERACTION = "interaction"
    ROLLOUT = "rollout"
    FEEDBACK = "feedback"
    ERROR = "error"


class DataEvent(BaseModel):
    """Data event record"""
    event_id: str
    event_type: EventType
    timestamp: datetime
    agent_id: Optional[str] = None
    session_id: Optional[str] = None
    prompt: Optional[str] = None
    response: Optional[str] = None
    trace: Optional[Dict] = None
    metadata: Optional[Dict] = None
    
    class Config:
        use_enum_values = True


class DataCollector:
    """Collects data from various sources"""
    
    def __init__(self):
        self.events: List[DataEvent] = []
    
    def collect_interaction(
        self,
        agent_id: str,
        session_id: str,
        prompt: str,
        response: str,
        metadata: Optional[Dict] = None
    ) -> DataEvent:
        """
        Collect an Agent interaction.
        
        Args:
            agent_id: ID of the Agent
            session_id: Session identifier
            prompt: User prompt
            response: Agent response
            metadata: Additional metadata
            
        Returns:
            Created DataEvent
        """
        event_id = f"evt_{datetime.now().timestamp()}"
        event = DataEvent(
            event_id=event_id,
            event_type=EventType.INTERACTION,
            timestamp=datetime.now(),
            agent_id=agent_id,
            session_id=session_id,
            prompt=prompt,
            response=response,
            metadata=metadata
        )
        self.events.append(event)
        return event
    
    def collect_rollout(
        self,
        agent_id: str,
        trace: Dict,
        metadata: Optional[Dict] = None
    ) -> DataEvent:
        """
        Collect environment rollout data.
        
        Args:
            agent_id: ID of the Agent
            trace: Execution trace (observations, actions, rewards)
            metadata: Additional metadata
            
        Returns:
            Created DataEvent
        """
        event_id = f"evt_{datetime.now().timestamp()}"
        event = DataEvent(
            event_id=event_id,
            event_type=EventType.ROLLOUT,
            timestamp=datetime.now(),
            agent_id=agent_id,
            trace=trace,
            metadata=metadata
        )
        self.events.append(event)
        return event
    
    def collect_feedback(
        self,
        event_id: str,
        feedback: Dict
    ) -> DataEvent:
        """
        Collect human feedback on an event.
        
        Args:
            event_id: ID of the original event
            feedback: Feedback data (rating, comments, etc.)
            
        Returns:
            Created DataEvent
        """
        fb_event_id = f"evt_fb_{datetime.now().timestamp()}"
        event = DataEvent(
            event_id=fb_event_id,
            event_type=EventType.FEEDBACK,
            timestamp=datetime.now(),
            metadata={"original_event_id": event_id, **feedback}
        )
        self.events.append(event)
        return event
    
    def get_events(
        self,
        event_type: Optional[EventType] = None,
        agent_id: Optional[str] = None,
        limit: int = 100
    ) -> List[DataEvent]:
        """
        Retrieve collected events with filters.
        
        Args:
            event_type: Filter by event type
            agent_id: Filter by agent ID
            limit: Maximum number of events to return
            
        Returns:
            List of matching events
        """
        filtered = self.events
        
        if event_type:
            filtered = [e for e in filtered if e.event_type == event_type]
        
        if agent_id:
            filtered = [e for e in filtered if e.agent_id == agent_id]
        
        return filtered[-limit:]
    
    def get_statistics(self) -> Dict:
        """Get collection statistics"""
        by_type = {}
        for event in self.events:
            by_type[event.event_type] = by_type.get(event.event_type, 0) + 1
        
        return {
            "total_events": len(self.events),
            "by_type": by_type,
            "latest_event": self.events[-1].timestamp.isoformat() if self.events else None
        }
