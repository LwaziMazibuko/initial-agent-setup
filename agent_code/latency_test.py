import requests
import time
import json
import os

def measure_latency(prompt: str) -> float:
    """Sends a request to the host Mac's native Ollama API and measures response time."""
    
    # Pointing to the Mac host via Docker's bridge gateway
    API_URL = "http://host.docker.internal:11434/api/generate" 
    
    payload = {
        "model": "gemma:7b",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 256
        }
    }

    print(f"Sending request: '{prompt[:40]}...'")
    start_time = time.time()
    
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"--- ERROR --- Could not connect to host Ollama. Error: {e}")
        return 0.0

    end_time = time.time()
    latency = end_time - start_time
    
    print("--- Response Received ---")
    print(f"Full response size: {len(response.content)} bytes")
    print(f"Total Round Trip Time (Latency): {latency:.2f} seconds")
    
    return latency

if __name__ == "__main__":
    simple_prompt = "Explain the difference between agentic memory and tool use in two sentences."
    print("="*50)
    print(">>> STARTING HOST-ACCELERATED SIMPLE QUERY TEST")
    measure_latency(simple_prompt)
    print("="*50)
    
    complex_prompt = "Write a short story about a cosmic AI that decides to install a database."
    print("\n>>> STARTING HOST-ACCELERATED COMPLEX QUERY TEST")
    measure_latency(complex_prompt)
    print("="*50)
