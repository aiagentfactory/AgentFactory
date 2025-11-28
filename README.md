# Agent Factory

A complete "Agent Training and Deployment Factory" prototype.

## Architecture
- **Backend:** Python (FastAPI, SQLAlchemy, SQLite) - Implements the 6 Factories (Data, Environment, Algo, Reward, Compute, Runtime).
- **Frontend:** React (Vite, Tailwind CSS) - Provides a Dashboard and interfaces for each factory.

## Prerequisites
- Python 3.8+
- Node.js 16+

## Setup
Run the automated setup script to install dependencies:
```bash
./setup.sh
```

## Running the Application
Start both the Backend and Frontend with:
```bash
./run.sh
```

- **Frontend Dashboard:** [http://localhost:5173](http://localhost:5173)
- **Backend API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

## Testing
To run the backend tests:
```bash
python3 run_tests.py
```

## Features (MVP)
- **Data Factory:** View ingested events.
- **Environment Factory:** Create scenarios and run simulations.
- **Algorithm Factory:** Start mock training jobs and track progress.
- **Runtime Factory:** Chat with a deployed mock agent.