#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import random
from pathlib import Path
import datetime
import argparse
import shutil
import json

# Füge das Projektverzeichnis zum Pfad hinzu
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.latex_util import load_template, build_latex, save_latex, compile_pdf, escape_latex
from utils.ollama_util import call_ollama
from utils.frontend_data_util import get_user_data_for_document
from Skripte.Gedicht import gedicht_util

# Konstanten
TEMPLATE_PATH = project_root / "templates" / "Gedicht_template.tex"
OUTPUT_DIR = project_root / "out"

def main():
    parser = argparse.ArgumentParser(description="Generiert ein personalisiertes Gedicht")
    parser.add_argument("name", help="Name der Person", nargs='?')
    parser.add_argument("birthdate", help="Geburtsdatum der Person", nargs='?')
    
    # Hole Benutzerdaten aus dem Frontend oder über Eingabe
    user_data = get_user_data_for_document()
    
    # Verwende Kommandozeilenargumente, falls vorhanden und keine Frontend-Daten gefunden wurden
    if len(sys.argv) > 1 and ('firstname' not in user_data or not user_data['firstname']):
        args = parser.parse_args()
        if args.name:
            parts = args.name.split()
            user_data['firstname'] = parts[0]
            if len(parts) > 1:
                user_data['lastname'] = ' '.join(parts[1:])
            user_data['full_name'] = args.name
        if args.birthdate:
            user_data['birthdate_german'] = args.birthdate
    
    # Extrahiere die benötigten Daten
    firstname = user_data.get('firstname', '')
    birthdate = user_data.get('birthdate_german', '')
    full_name = user_data.get('full_name', firstname)
    
    # Erzeuge Zeitstempel für Dateinamen
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Gedicht generieren - verwende nur den Vornamen für die Personalisierung
    gedicht_titel = gedicht_util.generate_gedicht_title(firstname)
    gedicht_text = gedicht_util.generate_gedicht_text(firstname, birthdate)
    
    # Format poem for LaTeX while preserving exact structure
    formatted_text = ""
    lines = gedicht_text.split('\n')
    for i, line in enumerate(lines):
        if line.strip():
            # Escape special LaTeX characters in the line content
            escaped_line = escape_latex(line)
            # For non-empty lines, add a line break (not escaped)
            formatted_text += escaped_line
            if i < len(lines) - 1:  # Don't add line break after the last line
                formatted_text += r" \\" + "\n"  # Raw string for LaTeX command
        else:
            # For empty lines (stanza breaks), add vertical space (not escaped)
            if i < len(lines) - 1:  # Don't add space after the last line if it's empty
                formatted_text += r"\vspace{1em}" + "\n"  # Raw string for LaTeX command
    
    # Lade und fülle Template
    template = load_template(TEMPLATE_PATH)
    latex_content = build_latex(template, {
        "GEDICHT_TITEL": escape_latex(gedicht_titel),
        "BENUTZER_NAME": escape_latex(firstname),  # Verwende nur den Vornamen im Template
        "GEDICHT_TEXT": formatted_text  # Already escaped, don't escape again
    })
    
    # Erstelle Ausgabeverzeichnis, falls es nicht existiert
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Speichere und kompiliere LaTeX - verwende den vollen Namen für die Datei
    output_filename = f"{full_name.replace(' ', '_')}_Gedicht_{timestamp}"
    latex_path = save_latex(latex_content, OUTPUT_DIR, output_filename)
    
    try:
        # Übergebe den richtigen template_dir Parameter
        template_dir = project_root / "templates"
        compile_pdf(latex_path, template_dir)
        pdf_path = latex_path.with_suffix('.pdf')
        print(f"📄 PDF erfolgreich erstellt: {pdf_path}")
        
        # Drucken simulieren
        print("🖨️  Datei drucken ...")
        return True
    except Exception as e:
        print(f"🚨 Fehler beim Kompilieren von LaTeX zu PDF: {e}")
        return False

if __name__ == "__main__":
    main()
