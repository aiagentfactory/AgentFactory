from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import models, database
from pydantic import BaseModel

router = APIRouter(prefix="/runtime", tags=["Runtime Factory"])

class DeployRequest(BaseModel):
    name: str
    model_id: int

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
def deploy_agent(req: DeployRequest, db: Session = Depends(get_db)):
    # Check if model exists
    model = db.query(models.ModelArtifact).filter(models.ModelArtifact.id == req.model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
        
    db_agent = models.Agent(
        name=req.name,
        model_id=req.model_id,
        status="active",
        endpoint=f"/runtime/chat",
        config={"deployed_at": "now"}
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
    
    model = db.query(models.ModelArtifact).filter(models.ModelArtifact.id == agent.model_id).first()
    model_name = model.name if model else "Unknown"

    response_text = f"[{agent.name} using {model_name}]: I processed '{chat.message}'."
    
    # Log event
    db_event = models.Event(
        event_type="chat_turn",
        content={"input": chat.message, "output": response_text, "agent_id": agent.id},
        session_id=chat.session_id
    )
    db.add(db_event)
    db.commit()
    
    return {"response": response_text}
