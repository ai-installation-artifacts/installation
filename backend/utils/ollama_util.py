import requests

def call_ollama(prompt: str, model: str = "llama3.2", url: str = "http://localhost:11434/api/generate") -> str:
    """Send prompt to Ollama and return generated text."""
    try:
        resp = requests.post(
            url,
            json={"model": model, "prompt": prompt, "stream": False, "temperature": 0.8, "seed": -1}
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get('response', '')
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}")
        return ""
