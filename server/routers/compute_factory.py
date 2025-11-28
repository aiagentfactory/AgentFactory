from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import models, database
from pydantic import BaseModel

router = APIRouter(prefix="/compute", tags=["Compute Factory"])

class NodeCreate(BaseModel):
    name: str
    type: str # gpu, cpu

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/nodes")
def list_nodes(db: Session = Depends(get_db)):
    return db.query(models.ComputeNode).all()

@router.post("/nodes")
def add_node(node: NodeCreate, db: Session = Depends(get_db)):
    specs = {"vram": "24GB"} if node.type == "gpu" else {"cores": 16}
    db_node = models.ComputeNode(
        name=node.name,
        type=node.type,
        status="idle",
        specs=specs
    )
    db.add(db_node)
    db.commit()
    db.refresh(db_node)
    return db_node
