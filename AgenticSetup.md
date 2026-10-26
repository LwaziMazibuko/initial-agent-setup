# Master Agentic Setup & Architecture Spec

## 🎯 Objective
To establish a modular, production-grade, local AI coding agent infrastructure running on Apple Silicon (M4) with Metal acceleration, isolated via Docker, and structured for multi-project workflows and plug-and-play model swapping.

---

## 🏛️ System Architecture Overview

1. **Inference Layer (The Brain)**: 
   - Powered by **Ollama** running natively on the macOS host (leveraging M4 Metal GPU acceleration).
   - Endpoint: `http://host.docker.internal:11434`
   - Active Model: `gemma:7b` (Swappable via configuration).

2. **Infrastructure Layer (The Containers)**:
   - Managed via `docker-compose.yml`.
   - **`agent_db`**: PostgreSQL container providing long-term execution and run memory logging (`agent_memory` database).
   - **`agent_orchestrator`**: Python container executing the core loop, tool dispatch, and LLM communication.

3. **Application & Tool Layer (The Body)**:
   - Custom tools located in `agent_code/agent_tools.py` (`read_file`, `write_code`, `run_shell`, `run_tests`).
   - Dynamic ReAct (Reasoning and Acting) orchestration loop handled by `agent_orchestrator.py` and `LLMProxy`.

---

## 🔌 How to Swap Models
To swap from `gemma:7b` to another model (e.g., `llama3` or `qwen2.5-coder`):
1. Pull the model on your host: `ollama pull <model_name>`
2. Update the `model` parameter inside `agent_code/agent_orchestrator.py` (`self.model = "<model_name>"`).
3. Restart the orchestrator container: `docker-compose restart agent_orchestrator`

---

## 🛠️ Reusing This Setup for Other Projects
To point this agent infrastructure to a new project (e.g., `/Users/lwazi/Downloads/projects/another-project`):
1. Mount the target project directory into the `agent_orchestrator` container via `docker-compose.yml` volumes.
2. Ensure the project contains a local copy or symbolic link to `agent_tools.py` and the execution scripts.
EOF
