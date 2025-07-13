# KI-Dokumentengenerator

Dieses Projekt generiert automatisch verschiedene Dokumente wie Testament, Patientenverfügung, Kündigungsschreiben und mehr mit Hilfe von KI (llama3.2).

## 🚀 Quickstart

### 1️⃣ Abhängigkeiten installieren

Python-Abhängigkeiten:
```bash
pip install -r requirements.txt
```

System-Abhängigkeiten (einmalig über Homebrew):
```bash
brew install --cask mactex-no-gui
brew install --cask ollama
brew install ngrok  # Für Remote-Zugriff
```

### 2️⃣ Ollama starten

In separatem Terminal:
```bash
ollama run llama3.2
```

### 3️⃣ Ngrok konfigurieren

Ngrok wird benötigt, um den lokalen Server über das Internet zugänglich zu machen.

```bash
# Einmalig: Authentifizierung einrichten
ngrok config add-authtoken 2zKW5K8FNEkO4XRpA0ytd0oXajc_3Ga3yvc2Qq6FTuTDbgMTU

# Server starten (in separatem Terminal)
ngrok http --url=guiding-orca-powerful.ngrok-free.app 9000
```

### 4️⃣ Frontend-Server starten

In separatem Terminal:
```bash
cd frontend
python server.py
```

Der Server läuft standardmäßig auf Port 9000 und ist über http://localhost:9000 erreichbar.

### 5️⃣ Dokumente generieren

Über die Weboberfläche können Sie Ihre Daten eingeben und Dokumente generieren lassen. Die generierten Dokumente werden automatisch gedruckt und anschließend aus dem System gelöscht.

## 📁 Projektstruktur

- `/frontend` - Enthält den Webserver und die Benutzeroberfläche
- `/backend` - Enthält die Skripte zur Dokumentengenerierung
  - `/Skripte` - Spezifische Skripte für verschiedene Dokumenttypen
  - `/out` - Temporäres Verzeichnis für generierte Dokumente
  - `/utils` - Hilfsfunktionen für LaTeX, Ollama, etc.
- `/templates` - LaTeX-Vorlagen für die Dokumente

## 🔧 Hinweise

- Alle generierten Dokumente werden nach dem Drucken automatisch gelöscht
- Das System verwendet ausschließlich das llama3.2-Modell für alle Skripte
- Die Ausgabedateien werden im `/backend/out`-Verzeichnis gespeichert
