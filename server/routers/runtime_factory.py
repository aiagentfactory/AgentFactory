from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import models, database
from pydantic import BaseModel

router = APIRouter(prefix="/runtime", tags=["Runtime Factory"])

class AgentCreate(BaseModel):
    name: str
    version: str
    config: dict

class ChatMessage(BaseModel):
    agent_id: int
    message: str
    session_id: str

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/agents")
def deploy_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    db_agent = models.Agent(
        name=agent.name,
        version=agent.version,
        status="active",
        config=agent.config
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

@router.get("/agents")
def list_agents(db: Session = Depends(get_db)):
    return db.query(models.Agent).all()

@router.post("/chat")
def chat_with_agent(chat: ChatMessage, db: Session = Depends(get_db)):
    agent = db.query(models.Agent).filter(models.Agent.id == chat.agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Mock Agent Response
    response_text = f"I am Agent {agent.name} (v{agent.version}). I received: {chat.message}"
    
    # Log event automatically to Data Factory (simulated internal call)
    db_event = models.Event(
        event_type="chat_turn",
        content={"input": chat.message, "output": response_text, "agent_id": agent.id},
        session_id=chat.session_id
    )
    db.add(db_event)
    db.commit()
    
    return {"response": response_text}
