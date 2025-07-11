#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import subprocess
from urllib.parse import parse_qs, urlparse
from pathlib import Path

# Verzeichnis für die Datenspeicherung
DATA_DIR = "data"
USER_DATA_FILE = os.path.join(DATA_DIR, "temp_user_data.json")
SIGNATURE_FILE = os.path.join(DATA_DIR, "unterschrift.png")

# Pfad zum Backend-Skript
FRONTEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = FRONTEND_DIR.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
RANDOM_GENERATOR_SCRIPT = BACKEND_DIR / "Skripte" / "random_generator.py"

# Stellen Sie sicher, dass das Datenverzeichnis existiert
os.makedirs(DATA_DIR, exist_ok=True)

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        """Behandelt POST-Anfragen zum Speichern von Benutzerdaten"""
        if self.path == '/save-user-data':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # JSON-Daten parsen
                request_data = json.loads(post_data.decode('utf-8'))
                user_data = request_data.get('userData', {})
                signature_base64 = request_data.get('signature')
                
                # Benutzerdaten in JSON-Datei speichern
                with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, ensure_ascii=False, indent=2)
                
                # Signatur als PNG-Datei speichern, wenn vorhanden
                if signature_base64:
                    import base64
                    signature_bytes = base64.b64decode(signature_base64)
                    with open(SIGNATURE_FILE, 'wb') as f:
                        f.write(signature_bytes)
                    print(f"Unterschrift gespeichert in: {SIGNATURE_FILE}")
                
                # Erfolgsantwort senden
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                # Starte den random_generator.py im Hintergrund
                if os.path.exists(RANDOM_GENERATOR_SCRIPT):
                    print(f"Starte Dokumentengenerierung mit {RANDOM_GENERATOR_SCRIPT}...")
                    try:
                        # Führe das Skript im Hintergrund aus
                        subprocess.Popen(
                            ["python3", str(RANDOM_GENERATOR_SCRIPT)],
                            cwd=str(BACKEND_DIR),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                        print("Dokumentengenerierung erfolgreich gestartet.")
                        response_message = 'Daten und Unterschrift gespeichert, Dokumentengenerierung gestartet'
                    except Exception as e:
                        print(f"Fehler beim Starten der Dokumentengenerierung: {e}")
                        response_message = 'Daten und Unterschrift gespeichert, aber Dokumentengenerierung fehlgeschlagen'
                else:
                    print(f"Skript nicht gefunden: {RANDOM_GENERATOR_SCRIPT}")
                    response_message = 'Daten und Unterschrift gespeichert, aber Generierungsskript nicht gefunden'
                
                self.wfile.write(json.dumps({
                    'status': 'success',
                    'message': response_message
                }).encode('utf-8'))
                print(f"Benutzerdaten gespeichert in: {USER_DATA_FILE}")
            except Exception as e:
                # Fehlerantwort senden
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode('utf-8'))
                print(f"Fehler beim Speichern der Daten: {e}")
        else:
            # Für alle anderen POST-Anfragen 404 zurückgeben
            self.send_response(404)
            self.end_headers()
    
    def do_DELETE(self):
        """Behandelt DELETE-Anfragen zum Löschen von Benutzerdaten"""
        if self.path == '/delete-user-data':
            try:
                # Lösche alle Dateien im data-Ordner
                files_deleted = 0
                for filename in os.listdir(DATA_DIR):
                    file_path = os.path.join(DATA_DIR, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Datei gelöscht: {file_path}")
                        files_deleted += 1
                
                # Erfolgsantwort senden
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'status': 'success',
                    'message': f'Alle {files_deleted} Dateien im data-Ordner wurden gelöscht'
                }).encode('utf-8'))
                print(f"Alle {files_deleted} Dateien im data-Ordner wurden gelöscht")
            except Exception as e:
                # Fehlerantwort senden
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode('utf-8'))
                print(f"Fehler beim Löschen der Daten: {e}")
        else:
            # Für alle anderen DELETE-Anfragen 404 zurückgeben
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        """Behandelt OPTIONS-Anfragen für CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == "__main__":
    PORT = 9000  # Port auf 9000 gesetzt
    Handler = CustomHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler, bind_and_activate=False) as httpd:
        httpd.allow_reuse_address = True
        httpd.server_bind()
        httpd.server_activate()
        print(f"Server läuft auf Port {PORT}")
        print(f"Daten werden in {DATA_DIR} gespeichert")
        print(f"Bei Datenempfang wird automatisch {RANDOM_GENERATOR_SCRIPT} gestartet")
        httpd.serve_forever()
