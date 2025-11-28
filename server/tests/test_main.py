from fastapi.testclient import TestClient
from server.main import app
from server.database import models, database
import pytest

client = TestClient(app)

# Reset DB for testing
models.Base.metadata.drop_all(bind=database.engine)
models.Base.metadata.create_all(bind=database.engine)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Agent Factory API"}

def test_create_scenario_and_run():
    # 1. Create Scenario
    res_scenario = client.post("/env/scenarios", json={"name": "TestScenario", "type": "text", "config": {}})
    assert res_scenario.status_code == 200
    scenario_id = res_scenario.json()["id"]

    # 2. Start Run
    res_run = client.post(f"/env/runs?scenario_id={scenario_id}")
    assert res_run.status_code == 200
    run_id = res_run.json()["id"]

    # 3. Step Run
    res_step = client.post(f"/env/runs/{run_id}/step", json={"action": "hello"})
    assert res_step.status_code == 200
    assert res_step.json()["status"] == "ongoing"

def test_agent_chat_flow():
    # 1. Deploy Agent
    res_agent = client.post("/runtime/agents", json={"name": "ChatBot", "version": "1.0", "config": {}})
    assert res_agent.status_code == 200
    agent_id = res_agent.json()["id"]

    # 2. Chat
    res_chat = client.post("/runtime/chat", json={"agent_id": agent_id, "message": "Hello", "session_id": "sess-1"})
    assert res_chat.status_code == 200
    assert "response" in res_chat.json()

    # 3. Verify Event Logged
    res_events = client.get("/data/events")
    assert res_events.status_code == 200
    assert len(res_events.json()) > 0
