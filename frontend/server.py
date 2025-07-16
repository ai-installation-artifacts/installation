#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import subprocess
from urllib.parse import parse_qs, urlparse
from pathlib import Path
import threading
import time

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

# Status-Datei für den Druckvorgang
PRINT_STATUS_FILE = os.path.join(DATA_DIR, "print_status.json")

# Funktion zum Speichern des Druckstatus
def save_print_status(status, message):
    """Speichert den Druckstatus in einer JSON-Datei"""
    status_data = {
        'type': 'print_status',
        'status': status,
        'message': message,
        'timestamp': time.time()
    }
    
    try:
        with open(PRINT_STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(status_data, f, ensure_ascii=False, indent=2)
        print(f"Druckstatus gespeichert: {status} - {message}")
    except Exception as e:
        print(f"Fehler beim Speichern des Druckstatus: {e}")

# Funktion zum Überprüfen des Druckwarteschlangenstatus
def check_print_queue_status():
    """Überprüft den Druckwarteschlangenstatus und setzt den Status auf 'completed', wenn keine Druckaufträge mehr in der Warteschlange sind"""
    print("Überprüfe Druckwarteschlange...")
    try:
        # Auf macOS: lpstat -o zeigt alle aktiven Druckaufträge
        result = subprocess.run(['lpstat', '-o'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wenn der Befehl erfolgreich war und keine Ausgabe hat, sind keine Druckaufträge in der Warteschlange
        if result.returncode == 0 and not result.stdout.strip():
            print("Keine Druckaufträge in der Warteschlange. Druckvorgang abgeschlossen.")
            save_print_status('completed', 'Druckvorgang erfolgreich abgeschlossen')
            return True
        elif result.returncode == 0:
            # Es sind noch Druckaufträge in der Warteschlange
            print(f"Druckaufträge in der Warteschlange: {result.stdout}")
            save_print_status('printing', 'Dokumente werden gedruckt...')
            
            # Starte einen Timer, um die Druckwarteschlange nach 5 Sekunden erneut zu überprüfen
            threading.Timer(5.0, check_print_queue_status).start()
            return False
        else:
            # Fehler beim Ausführen des Befehls
            print(f"Fehler beim Überprüfen der Druckwarteschlange: {result.stderr}")
            save_print_status('completed', 'Druckvorgang wahrscheinlich abgeschlossen (Status konnte nicht überprüft werden)')
            return True
    except Exception as e:
        print(f"Fehler beim Überprüfen der Druckwarteschlange: {e}")
        save_print_status('completed', 'Druckvorgang wahrscheinlich abgeschlossen (Status konnte nicht überprüft werden)')
        return True

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
                print(f"Benutzerdaten gespeichert in: {USER_DATA_FILE}")
                
                # Signatur als PNG-Datei speichern, wenn vorhanden
                if signature_base64:
                    import base64
                    signature_bytes = base64.b64decode(signature_base64)
                    with open(SIGNATURE_FILE, 'wb') as f:
                        f.write(signature_bytes)
                    print(f"Unterschrift gespeichert in: {SIGNATURE_FILE}")
                
                # Starte den random_generator.py im Hintergrund
                if os.path.exists(RANDOM_GENERATOR_SCRIPT):
                    print(f"Starte Dokumentengenerierung mit {RANDOM_GENERATOR_SCRIPT}...")
                    try:
                        # Status auf "generating" setzen
                        save_print_status('generating', 'Dokumente werden generiert und gedruckt...')
                        
                        # Starte den Prozess und überwache ihn
                        process = subprocess.Popen(
                            ["python3", str(RANDOM_GENERATOR_SCRIPT)],
                            cwd=str(BACKEND_DIR),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True
                        )
                        
                        # Überwache den Prozess in einem separaten Thread
                        def monitor_process():
                            _, stderr = process.communicate()
                            if process.returncode == 0:
                                print("Dokumentengenerierung erfolgreich abgeschlossen.")
                                # Überprüfe die Druckwarteschlange
                                check_print_queue_status()
                            else:
                                print(f"Fehler bei der Dokumentengenerierung: {stderr}")
                                # Status auf "error" setzen
                                save_print_status('error', f'Fehler beim Druckvorgang: {stderr}')
                        
                        # Starte den Überwachungsthread
                        threading.Thread(target=monitor_process, daemon=True).start()
                        
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
    
    def do_GET(self):
        """Behandelt GET-Anfragen"""
        # Prüfe, ob es eine Anfrage für den Druckstatus ist
        if self.path == '/print-status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Prüfe, ob die Statusdatei existiert
            if os.path.exists(PRINT_STATUS_FILE):
                try:
                    with open(PRINT_STATUS_FILE, 'r', encoding='utf-8') as f:
                        status_data = json.load(f)
                    self.wfile.write(json.dumps(status_data).encode('utf-8'))
                except Exception as e:
                    print(f"Fehler beim Lesen des Druckstatus: {e}")
                    error_response = {'status': 'error', 'message': 'Fehler beim Lesen des Druckstatus'}
                    self.wfile.write(json.dumps(error_response).encode('utf-8'))
            else:
                # Wenn keine Statusdatei existiert, sende einen Standardstatus
                default_status = {'type': 'print_status', 'status': 'unknown', 'message': 'Kein Druckstatus verfügbar'}
                self.wfile.write(json.dumps(default_status).encode('utf-8'))
        else:
            # Für alle anderen GET-Anfragen, verwende die Standard-Implementierung
            super().do_GET()
    
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
