```markdown
# 💻 Project Setup: The Gemma Agentic Ecosystem
**Goal:** To establish a robust, scalable, and modular development environment that allows a Large Language Model (Gemma) to act as an advanced coding agent, tightly integrated with the development 
workflow.
**Version:** 0.1.0
**Date:** 2026-10-26

## 🚀 I. Infrastructure (Phase 1)
*   **Status:** PENDING / STARTED / COMPLETE
*   **Goal:** Establish isolated, reliable services (LLM API, Agent Engine, Database).
*   **Current State:** Docker setup initiated.
*   **Key Decisions:**
    *   **Container Strategy:** All services run in Docker containers via `docker-compose.yml`.
    *   **Data Isolation:** Gemma API, Agent Orchestrator, and Database are distinct services.
    *   **Project Location:** All projects are located under `/downloads/projects/`.
    *   **Testing Project:** [personal_website] is the current test target.

## 🧠 II. Core Services Mapping
| Service | Role | Technology | Container Name (Target) | Communication | Key Configs |
| :--- | :--- | :--- | :--- | :--- | :--- |

| **Gemma API** | The LLM "Brain." Converts weights into a queryable API endpoint. | vLLM / Ollama | `gemma_api` | Provides internal API (e.g., `http://gemma_api:8000/generate`) | Model path, GPU 
resource limits, Max Tokens |

| **Agent Engine** | The "Planner." Receives goals, interacts with tools, and manages the LLM loop. | Python (LangChain/AutoGen) | `agent_orchestrator` | Consumes Gemma API, utilizes `/agent_tools` | 

Agent prompt templates, Tool definitions, Database connection2 string |

| **Database** | Memory storage for long-term context, conversation history, and project state. | PostgreSQL / Vector DB (e.g., Qdrant) | `agent_db` | Provides a persistent storage layer | Connection 
pooling, Schema migration status |

## 🛠️ III. Development Environment Checklist
*   [ ] Git repository initialized for testing branch.
*   [ ] Python Virtual Environment created (`venv`).
*   [ ] Agent Tools implemented (`read_file`, `run_shell`, etc.).
*   [ ] API Latency benchmark established (Phase 2).
*   [ ] VS Code extension client configured.
