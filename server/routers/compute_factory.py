from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import models, database
from pydantic import BaseModel

router = APIRouter(prefix="/compute", tags=["Compute Factory"])

class NodeCreate(BaseModel):
    name: str
    type: str

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/nodes")
def provision_node(node: NodeCreate, db: Session = Depends(get_db)):
    db_node = models.ComputeNode(
        name=node.name,
        type=node.type,
        status="active",
        specs={"memory": "80GB" if node.type == "gpu" else "32GB"}
    )
    db.add(db_node)
    db.commit()
    db.refresh(db_node)
    return db_node

@router.get("/nodes")
def list_nodes(db: Session = Depends(get_db)):
    return db.query(models.ComputeNode).all()

@router.get("/usage")
def get_usage():
    return {
        "gpu_util": "45%",
        "memory_util": "60%",
        "active_nodes": 3
    }
