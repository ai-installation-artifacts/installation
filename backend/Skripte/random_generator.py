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

# Pfade zu den Skripten
KUENDIGUNG_PATH = project_root / "Skripte" / "Kuendigung" / "kuendigung.py"
TESTAMENT_PATH = project_root / "Skripte" / "Testament" / "testament.py"
PATIENTENVERFUEGUNG_PATH = project_root / "Skripte" / "Patientenverfuegung" / "patientenverfuegung.py"
VOLLMACHT_PATH = project_root / "Skripte" / "Vollmacht" / "vollmacht.py"
RECHNUNG_PATH = project_root / "Skripte" / "Rechnung" / "rechnung.py"

# Temporäre Datei für die Zwischenspeicherung der Eingabedaten
TEMP_DATA_FILE = project_root / "temp_user_data.json"

def collect_user_input():
    """Sammelt Benutzereingaben und speichert sie temporär."""
    
    name = input("Name: ").strip()
    birthdate = input("Geburtsdatum (TT.MM.JJJJ): ").strip()
    
    # Validierung der Eingaben
    if not name or not birthdate:
        print("Fehler: Name und Geburtsdatum dürfen nicht leer sein.")
        sys.exit(1)
    
    # Speichern der Daten in einer temporären Datei
    user_data = {
        "name": name,
        "birthdate": birthdate
    }
    
    with open(TEMP_DATA_FILE, 'w') as f:
        json.dump(user_data, f)
    
    return user_data

def run_script_in_subprocess(script_path, name, birthdate, script_type=None):
    """Führt ein Skript als separaten Prozess aus und übergibt die Benutzerdaten als Argumente."""
    try:
        # Wechsle in das Verzeichnis des Skripts, um relative Imports zu ermöglichen
        script_dir = script_path.parent
        
        # Bereite die Kommandozeile basierend auf dem Skripttyp vor
        if script_type in ["kuendigung", "vollmacht"]:
            # Kündigungs- und Vollmachtsskript verwenden interaktive Eingabe
            cmd = [sys.executable, str(script_path)]
            if script_type == "kuendigung":
                cmd.append("--no_print")  # Nur für Kündigung
            # Wir werden input() mit einem Pipe-Trick überschreiben
            input_data = f"{name}\n{birthdate}\n"
        else:
            # Testament und Patientenverfügung verwenden positionelle Argumente
            cmd = [sys.executable, str(script_path), name, birthdate]
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
                return False
        else:
            # Normale Ausführung ohne stdin-Eingabe
            process = subprocess.Popen(
                cmd,
                cwd=str(script_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Ausgabe in Echtzeit anzeigen
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
            
            # Prüfe, ob es Fehler gab
            return_code = process.poll()
            if return_code != 0:
                error = process.stderr.read()
                print(f"Fehler beim Ausführen des Skripts (Exit-Code {return_code}):")
                print(error)
                return False
        
        return True
    
    except Exception as e:
        print(f"Fehler beim Ausführen des Skripts: {e}")
        return False

def run_kuendigung(name, birthdate):
    """Führt das Kündigungsskript aus."""
    print("\n=== Generiere Kündigungsschreiben ===")
    return run_script_in_subprocess(KUENDIGUNG_PATH, name, birthdate, script_type="kuendigung")

def run_testament(name, birthdate):
    """Führt das Testamentsskript aus."""
    print("\n=== Generiere Testament ===")
    return run_script_in_subprocess(TESTAMENT_PATH, name, birthdate)

def run_patientenverfuegung(name, birthdate):
    """Führt das Patientenverfügungsskript aus."""
    print("\n=== Generiere Patientenverfügung ===")
    return run_script_in_subprocess(PATIENTENVERFUEGUNG_PATH, name, birthdate)

def run_vollmacht(name, birthdate):
    """Führt das Vollmachtsskript aus."""
    print("\n=== Generiere Vollmacht ===")
    return run_script_in_subprocess(VOLLMACHT_PATH, name, birthdate, script_type="vollmacht")

def run_rechnung(name, birthdate):
    """Führt das Rechnungsskript aus."""
    print("\n=== Generiere Rechnung ===")
    return run_script_in_subprocess(RECHNUNG_PATH, name, birthdate, script_type="vollmacht")

def cleanup():
    """Löscht die temporären Daten."""
    if TEMP_DATA_FILE.exists():
        TEMP_DATA_FILE.unlink()
        print("\nBenutzerinformationen wurden gelöscht.")

def main():
    try:
        # 1. Benutzereingaben sammeln
        user_data = collect_user_input()
        name = user_data["name"]
        birthdate = user_data["birthdate"]
        
        # 2. Zwei zufällige Skripte auswählen
        available_scripts = [
            ("Kündigung", run_kuendigung),
            ("Testament", run_testament),
            ("Patientenverfügung", run_patientenverfuegung),
            ("Vollmacht", run_vollmacht),
            ("Rechnung", run_rechnung)
        ]
        
        selected_scripts = random.sample(available_scripts, 2)
        
        print(f"\nEs wurden folgende Dokumente zufällig ausgewählt:")
        for i, (script_name, _) in enumerate(selected_scripts, 1):
            print(f"{i}. {script_name}")
        
        # 3. Die ausgewählten Skripte ausführen
        success_count = 0
        for _, script_func in selected_scripts:
            if script_func(name, birthdate):
                success_count += 1
        
        if success_count == 2:
            print("\n✅ Alle Dokumente wurden erfolgreich generiert.")
        else:
            print(f"\n⚠️ {success_count} von 2 Dokumenten wurden generiert.")
        
        print("Die generierten Dokumente finden Sie im 'out'-Verzeichnis.")
        
    except Exception as e:
        print(f"Fehler bei der Ausführung: {e}")
    finally:
        # 4. Aufräumen
        cleanup()

if __name__ == "__main__":
    main()
