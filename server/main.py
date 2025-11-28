from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import models, database
from .routers import data_factory, env_factory, algo_factory, reward_factory, compute_factory, runtime_factory, pipeline_factory

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Agent Factory API", version="1.0")

# CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(data_factory.router)
app.include_router(env_factory.router)
app.include_router(algo_factory.router)
app.include_router(reward_factory.router)
app.include_router(compute_factory.router)
app.include_router(runtime_factory.router)
app.include_router(pipeline_factory.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Agent Factory API"}
