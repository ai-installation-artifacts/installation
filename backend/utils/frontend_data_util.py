#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from pathlib import Path
import shutil

# Pfad zum Projektverzeichnis
project_root = Path(__file__).resolve().parent.parent
frontend_data_dir = project_root.parent / "frontend" / "data"

# Pfade zu den Frontend-Dateien
USER_DATA_PATH = frontend_data_dir / "temp_user_data.json"
SIGNATURE_PATH = frontend_data_dir / "unterschrift.png"

# Standard-Ausgabeverzeichnis für die Signatur
SIGNATURE_DIR = project_root / "out" / "Signature"

def get_frontend_user_data():
    """
    Liest die Benutzerdaten aus der Frontend-JSON-Datei.
    
    Returns:
        dict: Ein Dictionary mit den Schlüsseln 'firstname', 'lastname', 'birthdate', 
              'full_name', 'birthdate_german' und 'timestamp'
    """
    if not USER_DATA_PATH.exists():
        return None
    
    try:
        with open(USER_DATA_PATH, 'r') as f:
            user_data = json.load(f)
            
        # Extrahiere die Daten
        firstname = user_data.get('firstname', '')
        lastname = user_data.get('lastname', '')
        full_name = f"{firstname} {lastname}".strip()
        
        # Konvertiere das ISO-Format in deutsches Datumsformat (TT.MM.JJJJ)
        birthdate_german = None
        if 'birthdate' in user_data:
            iso_date = user_data['birthdate']
            # Konvertiere YYYY-MM-DD zu TT.MM.JJJJ
            parts = iso_date.split('-')
            if len(parts) == 3:
                birthdate_german = f"{parts[2]}.{parts[1]}.{parts[0]}"
        
        # Erstelle ein erweitertes Dictionary mit allen nötigen Informationen
        result = {
            'firstname': firstname,
            'lastname': lastname,
            'full_name': full_name,
            'birthdate': user_data.get('birthdate', ''),  # Original ISO-Format
            'birthdate_german': birthdate_german,  # Deutsches Format
            'timestamp': user_data.get('timestamp', '')
        }
        
        return result
    except Exception as e:
        print(f"Fehler beim Lesen der Frontend-Benutzerdaten: {e}")
        return None

def ensure_signature_copied():
    """
    Stellt sicher, dass die Unterschriftsdatei in das Standard-Signaturverzeichnis kopiert wird.
    Dieses Verzeichnis wird von allen LaTeX-Templates verwendet.
    
    Returns:
        bool: True, wenn die Signatur erfolgreich kopiert wurde oder bereits existiert, sonst False
    """
    # Stelle sicher, dass das Signaturverzeichnis existiert, auch wenn keine Unterschrift vorhanden ist
    os.makedirs(SIGNATURE_DIR, exist_ok=True)
    
    if not SIGNATURE_PATH.exists():
        print("Keine Unterschriftsdatei gefunden.")
        return False
    
    try:
        # Zieldatei im Signaturverzeichnis
        target_path = SIGNATURE_DIR / "unterschrift.png"
        
        # Kopiere die Datei, wenn sie nicht bereits existiert oder aktualisiert werden muss
        if not target_path.exists() or os.path.getmtime(SIGNATURE_PATH) > os.path.getmtime(target_path):
            shutil.copy2(SIGNATURE_PATH, target_path)
            print(f"Unterschrift kopiert nach: {target_path}")
        
        return True
    except Exception as e:
        print(f"Fehler beim Kopieren der Unterschrift: {e}")
        return False

def get_user_data_for_document():
    """
    Bereitet die Benutzerdaten für die Dokumentgenerierung vor.
    Kombiniert die Frontend-Daten oder fragt nach Eingaben, wenn keine Daten gefunden wurden.
    Kopiert auch die Unterschrift in das Standard-Signaturverzeichnis.
    
    Returns:
        dict: Ein Dictionary mit den Schlüsseln 'firstname', 'lastname', 'full_name', 
              'birthdate_german' und 'has_signature'
    """
    # Versuche, Daten aus dem Frontend zu lesen
    user_data = get_frontend_user_data()
    
    # Wenn keine Frontend-Daten gefunden wurden, frage nach Eingaben
    if not user_data:
        print("Keine Frontend-Daten gefunden. Bitte geben Sie die Daten manuell ein.")
        firstname = input("Vorname: ").strip()
        lastname = input("Nachname: ").strip()
        birthdate = input("Geburtsdatum (TT.MM.JJJJ): ").strip()
        
        user_data = {
            'firstname': firstname,
            'lastname': lastname,
            'full_name': f"{firstname} {lastname}".strip(),
            'birthdate_german': birthdate
        }
    
    # Kopiere die Unterschrift in das Standard-Verzeichnis
    has_signature = ensure_signature_copied()
    user_data['has_signature'] = has_signature
    
    return user_data
