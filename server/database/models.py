from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String)
    content = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    session_id = Column(String, index=True)

class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    event_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Scenario(Base):
    __tablename__ = "scenarios"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(String) 
    config = Column(JSON)

class Run(Base):
    __tablename__ = "runs"
    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"))
    status = Column(String) 
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    logs = Column(JSON)

class TrainingJob(Base):
    __tablename__ = "training_jobs"
    id = Column(Integer, primary_key=True, index=True)
    model_base = Column(String)
    algorithm = Column(String) # Added field
    dataset_id = Column(Integer, ForeignKey("datasets.id")) # Added field
    status = Column(String)
    progress = Column(Float, default=0.0)
    metrics = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Model(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    version = Column(String)
    source_job_id = Column(Integer, ForeignKey("training_jobs.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Evaluation(Base):
    __tablename__ = "evaluations"
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("models.id"))
    scenario_id = Column(Integer, ForeignKey("scenarios.id"))
    score = Column(Float)
    status = Column(String)
    report = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ComputeNode(Base):
    __tablename__ = "compute_nodes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    type = Column(String) # 'gpu' or 'cpu'
    status = Column(String) # 'active', 'busy', 'offline'
    specs = Column(JSON)

class Agent(Base):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    model_id = Column(Integer, ForeignKey("models.id")) # Link to model
    version = Column(String)
    status = Column(String)
    config = Column(JSON)

class PipelineRun(Base):
    __tablename__ = "pipeline_runs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    status = Column(String) # 'running', 'completed', 'failed'
    current_stage = Column(String) # 'training', 'evaluation', 'deployment'
    config = Column(JSON) # {dataset_id, algo, scenario_id}
    artifacts = Column(JSON) # {job_id, model_id, eval_id, agent_id}
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class PipelineRun(BaseModel): # Oops, SQLAlchemy models should inherit from Base, not Pydantic BaseModel. But wait, the user is asking to ADD it.
# Let me fix the inheritance in the instruction string.
    pass

# Correcting the logic:
# I will write the full class definition for PipelineRun inheriting from Base.
