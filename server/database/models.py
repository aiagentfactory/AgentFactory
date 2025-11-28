from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String) # agent_action, env_obs, etc.
    content = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    session_id = Column(String, index=True)

class Scenario(Base):
    __tablename__ = "scenarios"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(String) # browser, api, text
    config = Column(JSON)

class Run(Base):
    __tablename__ = "runs"
    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"))
    status = Column(String) # running, completed, failed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    logs = Column(JSON)

class TrainingJob(Base):
    __tablename__ = "training_jobs"
    id = Column(Integer, primary_key=True, index=True)
    model_base = Column(String)
    status = Column(String) # pending, training, completed
    progress = Column(Float, default=0.0)
    metrics = Column(JSON)

class Agent(Base):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    version = Column(String)
    status = Column(String) # active, deprecated
    config = Column(JSON)
