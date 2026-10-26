import requests

class GemmaClient:
    def __init__(self, model="gemma:7b", base_url="http://host.docker.internal:11434"):
        self.model = model
        self.base_url = base_url

    def generate(self, prompt: str, temperature: float = 0.2, num_predict: int = 300) -> str:
        """Sends a prompt to native Ollama and returns the generated text."""
        api_url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": num_predict
            }
        }
        try:
            response = requests.post(api_url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except Exception as e:
            return f"Error communicating with Gemma API: {e}"
