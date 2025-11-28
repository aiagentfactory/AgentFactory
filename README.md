# 🏭 Agent Factory

> **The Industrial-Grade Platform for Building, Training, and Deploying AI Agents.**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-MVP-orange.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![React](https://img.shields.io/badge/react-18-blue.svg)

**Agent Factory** is a modular, end-to-end platform designed to industrialize the lifecycle of AI Agents. Unlike ad-hoc scripts or scattered notebooks, Agent Factory standardizes the process into 6 distinct "Production Lines" (Factories), decoupling data ingestion, environment simulation, algorithm training, and deployment.

---

## 🏗️ System Architecture

The platform follows a clean, separated architecture ensuring scalability and ease of development:
*   **Frontend:** A modern React dashboard interacting via REST.
*   **Backend:** FastAPI serving as the central orchestrator.
*   **Factories:** 6 Isolated modules handling distinct domain logic.

![System Architecture](docs/images/architecture.svg)

---

## 🌟 Key Advantages

### 1. Modular "Factory" Architecture
We move beyond monolithic agent scripts. By separating concerns into 6 dedicated factories, developers can upgrade a specific component (e.g., switching from PPO to DPO in the *Algo Factory*) without breaking the environment or data pipelines.

### 2. Visual & API-First
*   **Frontend Dashboard:** A React-based control center to visualize training progress, manage clusters, and chat with agents.
*   **REST API:** Every action available in the UI is backed by a fully documented FastAPI backend, allowing for programmatic automation and CI/CD integration.

### 3. Extensible & Open
Built on standard stacks (FastAPI + React). The codebase is designed for easy extension—add your own custom Environments, Reward Functions, or Model Architectures with minimal boilerplate.

---

## 📸 Factory Tour (Features & Advantages)

The platform is divided into 6 integrated modules, each with its own dashboard and specialized capability.

### 📊 Data Factory
*Ingest, clean, and version control your datasets.*
![Data Factory](docs/images/factory_data.svg)
- **Advantage:** **Visual Data Engineering.** Decouple raw data streams from model inputs. Monitor real-time event logs (as shown in the bottom pane) and create snapshots without writing a single SQL query.
- **Capability:** Real-time event stream monitoring and dataset management.


### 🌍 Environment Factory
*Define the world your agents live in.*
![Environment Factory](docs/images/factory_env.svg)
- **Advantage:** **Scenario-Based Simulation.** Stop hardcoding environments. Create reusable scenarios (e.g., "Customer Support Sim" vs "Trading Bot") and switch between text-chat or browser automation modes instantly.
- **Capability:** Create text-based, browser-based, or grid-world simulation scenarios.


### 🧠 Algorithm Factory
*The brain of the operation.*
![Algorithm Factory](docs/images/factory_algo.svg)
- **Advantage:** **One-Click Training.**  Abstracts away complex training loops. Select your dataset, pick an algorithm (SFT/PPO), and watch loss curves update in real-time without needing to SSH into a training cluster.
- **Capability:** Configure training runs, select baselines (SFT, PPO, DQN), and track loss curves.


### ⚖️ Reward Factory
*Align agents with human intent.*
![Reward Factory](docs/images/factory_reward.svg)
- **Advantage:** **Safety First.**  Dedicated pipeline for "Constitutional AI". Run safety evaluations against defined criteria and get a clear "Pass/Fail" report before any model is allowed to deploy.
- **Capability:** Define objective functions, run safety evaluations, and manage safety rules.


### 🖥️ Compute Factory
*Manage the engine room.*
![Compute Factory](docs/images/factory_compute.svg)
- **Advantage:** **Resource Transparency.**  No more guessing if GPU nodes are idle. View cluster health, provision H100s or CPUs on demand, and optimize resource allocation visually.
- **Capability:** Provision and monitor GPU/CPU resources, manage clusters, and view utilization.


### 💬 Runtime Factory
*Where agents go to work.*
![Runtime Factory](docs/images/factory_runtime.svg)
- **Advantage:** **Human-in-the-Loop Verification.**  Instantly deploy trained models to a chat sandbox. Test edge cases manually and compare agent versions side-by-side before pushing to production.
- **Capability:** One-click deployment of trained models to inference endpoints with a chat sandbox.

### 🔄 Pipeline Automation
*The Assembly Line.*
- **Advantage:** **End-to-End Automation.** Connect the factories into a seamless workflow. Select a dataset, train a model, run safety evaluations, and deploy successful agents automatically without manual intervention.
- **Capability:** Design and execute multi-stage workflows (Data -> Algo -> Eval -> Deploy).

---

## 🚀 Roadmap

We are building towards **v1.0**. Here is the plan:

### Phase 1: The Foundation (Current - MVP)
- [x] Core Architecture (6 Factories)
- [x] Basic UI/UX Dashboard
- [x] Mock Simulation & Training Loops
- [x] End-to-End Flow Validation

### Phase 2: Integration (Next Steps)
- [ ] **Real Model Integration:** Support for HuggingFace Transformers & PyTorch training loops.
- [ ] **Dockerized Environments:** Sandboxed execution for dangerous agent tools (Code Interpreter).
- [ ] **Vector Database:** Integration with Chroma/Pinecone for Agent Memory (RAG).

### Phase 3: Scale & Production
- [ ] **Kubernetes Operator:** Native K8s support for scaling training jobs.
- [ ] **Multi-Agent Orchestration:** Swarm protocols (agents talking to agents).
- [ ] **Plugin Marketplace:** Community-contributed environments and reward functions.

---

## 🤝 Contributing & Sharing

We welcome contributions! This project aims to be the standard shared infrastructure for Agent developers.

### How to Develop
1. **Fork & Clone** the repository.
2. **Setup:** Run `./setup.sh` to install Python & Node dependencies.
3. **Run:** Execute `./run.sh` to start the dev servers.
    - Backend: `http://localhost:8000/docs` (Swagger UI)
    - Frontend: `http://localhost:5173`

### Development Standards
- **Backend:** Follow PEP 8. Use `pydantic` for data validation.
- **Frontend:** Functional React components with Hooks. Tailwind CSS for styling.
- **Tests:** Run `python3 run_tests.py` before submitting PRs.

### License
This project is open-sourced under the MIT License.

---

*Built with ❤️ by the Agent Factory Team.*