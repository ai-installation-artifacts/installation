import requests

def generate_ollama_text(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False}
    )

    try:
        data = response.json()
    except Exception as e:
        print("Fehler beim Verarbeiten der Antwort:", e)
        print("Raw Response:", response.text)
        return "Fehler: keine gültige Antwort erhalten."

    if "response" not in data:
        print("Antwort enthält kein 'response'-Feld. Voller Inhalt:")
        print(data)
        return "Fehler: Modell hat keine Antwort erzeugt."

    return data["response"]
