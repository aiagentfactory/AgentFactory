import requests
import json
import time
import sys
import os

# Configuration
BASE_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://localhost:5173"
REPORT_FILE = "Demo/test_report.log"

def log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(REPORT_FILE, "a") as f:
        f.write(line + "\n")

def run_test():
    # Clear previous report
    if os.path.exists(REPORT_FILE):
        os.remove(REPORT_FILE)
    
    log("=== Starting Agent Factory E2E Test ===")
    
    # 0. Check Frontend Health
    try:
        log(f"Checking Frontend at {FRONTEND_URL}...")
        res = requests.get(FRONTEND_URL)
        if res.status_code == 200:
            log("✅ Frontend is accessible.")
        else:
            log(f"⚠️ Frontend returned status code {res.status_code}")
    except Exception as e:
        log(f"❌ Frontend Check Failed: {e}")

    # 1. Environment Factory: Create Scenario
    try:
        log("Step 1: Creating Scenario...")
        with open("Demo/scenario_config.json") as f:
            scenario_data = json.load(f)
        
        res = requests.post(f"{BASE_URL}/env/scenarios", json=scenario_data)
        res.raise_for_status()
        scenario = res.json()
        log(f"✅ Scenario Created: ID={scenario['id']}, Name={scenario['name']}")
        scenario_id = scenario['id']
    except Exception as e:
        log(f"❌ Step 1 Failed: {e}")
        return

    # 2. Data Factory: Ingest Events
    try:
        log("Step 2: Ingesting Mock Events...")
        event_data = {
            "event_type": "user_feedback",
            "content": {"rating": 5, "comment": "Great job"},
            "session_id": "test-session-01"
        }
        res = requests.post(f"{BASE_URL}/data/events", json=event_data)
        res.raise_for_status()
        log("✅ Event Ingested.")
        
        # Verify listing
        res = requests.get(f"{BASE_URL}/data/events")
        events = res.json()
        log(f"✅ Verified: Found {len(events)} events in Data Factory.")
    except Exception as e:
        log(f"❌ Step 2 Failed: {e}")
        return

    # 3. Algorithm Factory: Start Training
    try:
        log("Step 3: Starting Training Job...")
        with open("Demo/training_config.json") as f:
            train_config = json.load(f)
            
        res = requests.post(f"{BASE_URL}/algo/train/jobs", json=train_config)
        res.raise_for_status()
        job = res.json()
        job_id = job['id']
        log(f"✅ Job Started: ID={job_id}, Status={job['status']}")
        
        # Wait for completion
        log("Waiting for training to complete...")
        for _ in range(10):
            time.sleep(2)
            res = requests.get(f"{BASE_URL}/algo/train/jobs/{job_id}")
            job = res.json()
            log(f"   ... Job Status: {job['status']} (Progress: {job['progress']}%) ")
            if job['status'] == 'completed':
                break
        
        if job['status'] != 'completed':
            raise Exception("Training job timed out.")
        log("✅ Training Completed Successfully.")
    except Exception as e:
        log(f"❌ Step 3 Failed: {e}")
        return

    # 4. Runtime Factory: Deploy Agent
    try:
        log("Step 4: Deploying Agent...")
        agent_config = {
            "name": "DemoBot_v1",
            "version": "1.0.0",
            "config": {"model_id": "trained-model-123"}
        }
        res = requests.post(f"{BASE_URL}/runtime/agents", json=agent_config)
        
        # Handle unique name constraint mock
        if res.status_code == 500 or res.status_code == 400:
             log("⚠️ Agent might already exist, fetching list...")
        else:
             res.raise_for_status()
             log(f"✅ Agent Deployed: {res.json()['name']}")

        # Get Agent ID
        res = requests.get(f"{BASE_URL}/runtime/agents")
        agents = res.json()
        target_agent = next((a for a in agents if a['name'] == "DemoBot_v1"), agents[0] if agents else None)
        
        if not target_agent:
            raise Exception("No agents found.")
            
        agent_id = target_agent['id']
        log(f"Using Agent ID: {agent_id}")

        # 5. Chat with Agent
        log("Step 5: Testing Chat...")
        chat_payload = {
            "agent_id": agent_id,
            "message": "Hello, testing 123",
            "session_id": "test-chat-01"
        }
        res = requests.post(f"{BASE_URL}/runtime/chat", json=chat_payload)
        res.raise_for_status()
        chat_resp = res.json()
        log(f"✅ Agent Response: {chat_resp['response']}")
        
    except Exception as e:
        log(f"❌ Step 4/5 Failed: {e}")
        return

    log("=== Test Completed Successfully ===")

if __name__ == "__main__":
    run_test()
