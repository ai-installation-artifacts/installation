import sys
import random
import os
import importlib.util
from pathlib import Path
import tempfile
import json
import subprocess

# Add project root to sys.path to allow imports from the 'utils' directory
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Import the frontend data utility
from utils.frontend_data_util import get_user_data_for_document

# Pfade zu den Skripten
KUENDIGUNG_PATH = project_root / "Skripte" / "Kuendigung" / "kuendigung.py"
TESTAMENT_PATH = project_root / "Skripte" / "Testament" / "testament.py"
PATIENTENVERFUEGUNG_PATH = project_root / "Skripte" / "Patientenverfuegung" / "patientenverfuegung.py"
VOLLMACHT_PATH = project_root / "Skripte" / "Vollmacht" / "vollmacht.py"
RECHNUNG_PATH = project_root / "Skripte" / "Rechnung" / "rechnung.py"
GEDICHT_PATH = project_root / "Skripte" / "Gedicht" / "gedicht.py"

def run_script_in_subprocess(script_path, user_data, script_type=None):
    """Führt ein Skript als separaten Prozess aus und übergibt die Benutzerdaten als Argumente."""
    try:
        # Wechsle in das Verzeichnis des Skripts, um relative Imports zu ermöglichen
        script_dir = script_path.parent
        
        # Extrahiere die benötigten Daten
        full_name = user_data.get('full_name', '')
        birthdate = user_data.get('birthdate_german', '')
        
        # Bereite die Kommandozeile basierend auf dem Skripttyp vor
        if script_type in ["kuendigung", "vollmacht"]:
            # Kündigungs- und Vollmachtsskript verwenden interaktive Eingabe
            cmd = [sys.executable, str(script_path)]
            cmd.append("--no_print")  # Für alle Skripte das Drucken deaktivieren
            # Wir werden input() mit einem Pipe-Trick überschreiben
            input_data = f"{full_name}\n{birthdate}\n"
        elif script_type == "patientenverfuegung":
            # Patientenverfügung verwendet jetzt argparse
            cmd = [sys.executable, str(script_path), "--no_print"]
            input_data = f"{full_name}\n{birthdate}\n"
        elif script_type == "rechnung":
            # Rechnung verwendet argparse
            cmd = [sys.executable, str(script_path), "--no_print"]
            input_data = f"{full_name}\n{birthdate}\n"
        else:
            # Testament und andere verwenden positionelle Argumente
            cmd = [sys.executable, str(script_path), full_name, birthdate, "--no_print"]
            input_data = None
        
        # Führe das Skript im Unterverzeichnis aus
        if input_data:
            # Wenn wir Eingaben über stdin senden müssen
            process = subprocess.Popen(
                cmd,
                cwd=str(script_dir),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Sende die Eingabedaten
            stdout, stderr = process.communicate(input=input_data)
            
            # Ausgabe anzeigen
            if stdout:
                print(stdout.strip())
            
            # Prüfe, ob es Fehler gab
            if process.returncode != 0:
                if stderr:
                    print(f"Fehler beim Ausführen des Skripts (Exit-Code {process.returncode}):")
                    print(stderr.strip())
                return False, None
                
            # Extrahiere den PDF-Pfad aus der Ausgabe
            pdf_path = None
            for line in stdout.splitlines():
                if "PDF erfolgreich erstellt:" in line:
                    pdf_path = line.split("PDF erfolgreich erstellt:")[-1].strip()
                    break
            
            return True, pdf_path
        else:
            # Normale Ausführung ohne stdin-Eingabe
            process = subprocess.Popen(
                cmd,
                cwd=str(script_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Ausgabe sammeln und in Echtzeit anzeigen
            stdout_lines = []
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
                    stdout_lines.append(output.strip())
            
            # Prüfe, ob es Fehler gab
            return_code = process.poll()
            if return_code != 0:
                error = process.stderr.read()
                print(f"Fehler beim Ausführen des Skripts (Exit-Code {return_code}):")
                print(error)
                return False, None
            
            # Extrahiere den PDF-Pfad aus der Ausgabe
            pdf_path = None
            for line in stdout_lines:
                if "PDF erfolgreich erstellt:" in line:
                    pdf_path = line.split("PDF erfolgreich erstellt:")[-1].strip()
                    break
            
            return True, pdf_path
    
    except Exception as e:
        print(f"Fehler beim Ausführen des Skripts: {e}")
        return False, None

def run_kuendigung(user_data):
    """Führt das Kündigungsskript aus."""
    print("\n=== Generiere Kündigungsschreiben ===")
    return run_script_in_subprocess(KUENDIGUNG_PATH, user_data, script_type="kuendigung")

def run_testament(user_data):
    """Führt das Testamentsskript aus."""
    print("\n=== Generiere Testament ===")
    return run_script_in_subprocess(TESTAMENT_PATH, user_data)

def run_patientenverfuegung(user_data):
    """Führt das Patientenverfügungsskript aus."""
    print("\n=== Generiere Patientenverfügung ===")
    return run_script_in_subprocess(PATIENTENVERFUEGUNG_PATH, user_data)

def run_vollmacht(user_data):
    """Führt das Vollmachtsskript aus."""
    print("\n=== Generiere Vollmacht ===")
    return run_script_in_subprocess(VOLLMACHT_PATH, user_data, script_type="vollmacht")

def run_rechnung(user_data):
    """Führt das Rechnungsskript aus."""
    print("\n=== Generiere Rechnung ===")
    return run_script_in_subprocess(RECHNUNG_PATH, user_data, script_type="rechnung")

def run_gedicht(user_data):
    """Führt das Gedicht-Skript aus."""
    print("\n=== Generiere personalisiertes Gedicht ===")
    return run_script_in_subprocess(GEDICHT_PATH, user_data)

def main():
    try:
        # Hole Benutzerdaten aus dem Frontend oder über Eingabe
        user_data = get_user_data_for_document()
        
        # Prüfe, ob die notwendigen Daten vorhanden sind
        if not user_data.get('firstname') or not user_data.get('birthdate_german'):
            print("Fehler: Vorname und Geburtsdatum sind erforderlich.")
            return
        
        # Liste zum Sammeln der PDF-Pfade
        pdf_paths = []
        
        # 1. Immer zuerst ein Gedicht generieren
        print("\nGeneriere personalisiertes Gedicht als erstes Dokument...")
        gedicht_success, gedicht_pdf = run_gedicht(user_data)
        if gedicht_pdf:
            pdf_paths.append(gedicht_pdf)
        
        # 2. Zwei zufällige weitere Skripte auswählen
        available_scripts = [
            ("Kündigung", run_kuendigung),
            ("Testament", run_testament),
            ("Patientenverfügung", run_patientenverfuegung),
            ("Vollmacht", run_vollmacht),
            ("Rechnung", run_rechnung)
        ]
        
        selected_scripts = random.sample(available_scripts, 2)
        
        print(f"\nAls weitere Dokumente wurden zufällig ausgewählt:")
        for i, (script_name, _) in enumerate(selected_scripts, 1):
            print(f"{i}. {script_name}")
        
        # 3. Die ausgewählten Skripte ausführen
        success_count = 0
        for _, script_func in selected_scripts:
            success, pdf_path = script_func(user_data)
            if success:
                success_count += 1
                if pdf_path:
                    pdf_paths.append(pdf_path)
        
        # 4. Erfolgsmeldung ausgeben
        total_success = (gedicht_success + success_count)
        if total_success == 3:
            print("\n✅ Alle drei Dokumente wurden erfolgreich generiert.")
        else:
            print(f"\n⚠️ {total_success} von 3 Dokumenten wurden generiert.")
        
        print("Die generierten Dokumente finden Sie im 'out'-Verzeichnis.")
        
        # 5. Alle generierten PDFs zusammen drucken
        if pdf_paths:
            print(f"\n🖨️ Drucke {len(pdf_paths)} Dokumente...")
            # Importiere die print_file Funktion
            from utils.latex_util import print_file
            for pdf_path in pdf_paths:
                print(f"Drucke: {pdf_path}")
                print_file(pdf_path)
            print("✅ Druckaufträge abgeschlossen.")
        
    except Exception as e:
        print(f"Fehler bei der Ausführung: {e}")

if __name__ == "__main__":
    main()
