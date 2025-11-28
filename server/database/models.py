from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String) # agent_action, env_obs, user_feedback
    content = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    session_id = Column(String, index=True)

class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    event_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Scenario(Base):
    __tablename__ = "scenarios"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(String) # browser, api, text
    config = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ModelArtifact(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    version = Column(String)
    source_job_id = Column(Integer, nullable=True)
    metrics = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class TrainingJob(Base):
    __tablename__ = "training_jobs"
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=True)
    model_base = Column(String)
    algorithm = Column(String)
    status = Column(String) # pending, training, completed, failed
    progress = Column(Float, default=0.0)
    metrics = Column(JSON)
    output_model_id = Column(Integer, ForeignKey("models.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Evaluation(Base):
    __tablename__ = "evaluations"
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("models.id"))
    scenario_id = Column(Integer, ForeignKey("scenarios.id"))
    score = Column(Float)
    status = Column(String) # running, completed
    report = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Agent(Base):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    model_id = Column(Integer, ForeignKey("models.id"))
    status = Column(String) # active, stopped
    endpoint = Column(String)
    config = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ComputeNode(Base):
    __tablename__ = "compute_nodes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    type = Column(String) # gpu, cpu
    status = Column(String) # idle, busy, offline
    specs = Column(JSON) # {"gpu": "A100", "vram": "80GB"}
