import os
import subprocess
import time
import requests
import json
from agent_tools import read_file, write_code, run_shell, run_tests

class LLMProxy:
    """Connects directly to the native host Ollama API for dynamic agent reasoning."""
    
    def __init__(self):
        self.base_url = "http://host.docker.internal:11434"
        self.model = "gemma:7b"

    def generate_structured_response(self, instruction: str) -> dict:
        api_url = f"{self.base_url}/api/generate"
        
        system_prompt = (
            "You are an autonomous senior developer agent with tool access. "
            "You must output ONLY a valid JSON object with 'action_type' and 'args'. "
            "Available action_types and exact arg formats:\n"
            "- 'run_shell': {\"command\": \"shell command here\"}\n"
            "- 'read_file': {\"file_path\": \"relative/path/to/file.py\"}\n"
            "- 'write_code': {\"file_path\": \"relative/path/to/file.py\", \"content\": \"code content\"}\n"
            "- 'run_tests': {}\n"
            "- 'stop': {}\n"
            "Example: {\"action_type\": \"read_file\", \"args\": {\"file_path\": \"test_agent.py\"}}\n\n"
            f"Instruction: {instruction}"
        )
        
        payload = {
            "model": self.model,
            "prompt": system_prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_predict": 256
            }
        }

        print("🧠 LLM: Thinking and generating dynamic action...")
        try:
            response = requests.post(api_url, json=payload, timeout=30)
            response.raise_for_status()
            raw_text = response.json().get("response", "").strip()
            
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_text:
                raw_text = raw_text.split("```")[1].split("```")[0].strip()
                
            return json.loads(raw_text)
        except Exception as e:
            print(f"⚠️ Failed to parse LLM response as JSON: {e}. Defaulting to stop.")
            return {"action_type": "stop", "args": {}}

class AgentOrchestrator:
    def __init__(self):
        self.llm = LLMProxy()
        print("✨ Dynamic LLM-Driven Agent initialized.")

    def run(self, target_task: str):
        print(f"\n==================================================")
        print(f"🤖 [AGENT START] Target Task: {target_task}")
        print(f"==================================================\n")
         
        action_queue = []
         
        print("🧠 [PLANNING] Requesting initial plan from Gemma...")
        initial_action = self.llm.generate_structured_response(target_task)
        action_queue.append(initial_action)
        print(f"✅ Initial Action Decided by LLM: {initial_action.get('action_type')}")
         
        print("\n⚡ [EXECUTION] Starting dynamic tool loop...")
         
        steps_taken = 0
        max_steps = 4
         
        while action_queue and steps_taken < max_steps:
            steps_taken += 1
            current_action = action_queue.pop(0) 
            action_type = current_action.get("action_type")
            args = current_action.get("args", {})
             
            if action_type == "stop":
                print("\n🛑 Agent reached a natural stopping point.")
                break

            # --- Tool Aliasing for LLM Hallucinations ---
            if action_type in ["read_files", "get_file", "cat_file"]:
                action_type = "read_file"
                if "file_paths" in args and not "file_path" in args:
                    paths = args.get("file_paths", [])
                    if paths:
                        args["file_path"] = paths[0]
            elif action_type in ["list_files", "search_files"]:
                action_type = "run_shell"
                args = {"command": "find . -name '*.py'"}

            print(f"\n⚡ [TOOL DISPATCH - Step {steps_taken}] Executing {action_type} with {args}...")
            action_result = None
             
            if action_type == "read_file":
                action_result = read_file(args.get("file_path", ""))
            elif action_type == "write_code":
                action_result = write_code(args.get("file_path", ""), args.get("content", ""))
            elif action_type == "run_shell":
                action_result = run_shell(args.get("command", ""))
            elif action_type == "run_tests":
                action_result = run_tests()
            else:
                action_result = f"Unknown tool {action_type}."
             
            print(f"   ✅ Action Result: {str(action_result)[:200]}...")

            print("\n🔎 [REFLECTION] Sending execution result back to Gemma...")
            stop_example = '{"action_type": "stop", "args": {}}'
            reflection_prompt = f"Previous action '{action_type}' returned: '{action_result}'. If the task is complete, output {stop_example}. Otherwise, what is the next tool action to continue toward: {target_task}?"
            next_action_response = self.llm.generate_structured_response(reflection_prompt)

            action_queue.append(next_action_response)
            time.sleep(0.5)
         
        print("\n🎉 AGENT DYNAMIC RUN COMPLETE.")

if __name__ == "__main__":
    agent = AgentOrchestrator()
    task_goal = "Locate all python files in the workspace and check their contents."
    agent.run(task_goal)
