#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import random
from datetime import datetime, timedelta
from pathlib import Path

# Handle potential missing requests package
try:
    import requests
except ImportError:
    print("❌ Das 'requests' Paket ist nicht installiert. Bitte installieren Sie es mit 'pip install requests'")
    sys.exit(1)

# Add project root to sys.path to allow imports from the 'utils' directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from utils.latex_util import escape_latex, save_latex, compile_pdf, print_file
from rechnung_util import prepare_rechnung_prompt, extract_rechnung_sections

# Konfiguration
TEMPLATE_PATH = os.path.join(project_root, "templates", "Rechnung_Template", "Rechnung.tex")
OUTPUT_DIR = os.path.join(project_root, "out")
LLM_API_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "llama3.2"

def get_user_input():
    """
    Sammelt die Benutzereingaben für die Rechnung.
    """
    name = input("Name: ")
    birthdate = input("Geburtsdatum: ")
    
    # Generiere realistische Münchner Adressen
    muenchen_streets = [
        "Leopoldstraße", "Ludwigstraße", "Maximilianstraße", "Prinzregentenstraße",
        "Isartalstraße", "Marienplatz", "Kaufingerstraße", "Sendlinger Straße",
        "Nymphenburger Straße", "Theresienstraße", "Schleißheimer Straße",
        "Lindwurmstraße", "Schwanthalerstraße", "Bayerstraße", "Arnulfstraße",
        "Dachauer Straße", "Landsberger Straße", "Fürstenrieder Straße",
        "Plinganserstraße", "Tegernseer Landstraße", "Rosenheimer Straße"
    ]
    
    muenchen_districts = [
        "80331 München", "80333 München", "80335 München", "80336 München",
        "80337 München", "80339 München", "80469 München", "80538 München",
        "80539 München", "80634 München", "80636 München", "80637 München",
        "80638 München", "80639 München", "80686 München", "80687 München",
        "80689 München", "80796 München", "80797 München", "80798 München",
        "80799 München", "80801 München", "80802 München", "80803 München"
    ]
    
    import random
    street = f"{random.choice(muenchen_streets)} {random.randint(1, 150)}"
    zipcode = random.choice(muenchen_districts)
    
    return name, street, zipcode, birthdate

def generate_llm_content(prompt):
    """
    Generiert Inhalte mit dem LLM.
    """
    print("\U0001F4AC Generiere Rechnungs-Text ...")
    
    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        print(f"\U0001F4E1 Sende Anfrage an LLM API ({LLM_API_URL})...")
        response = requests.post(LLM_API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        llm_response = result["response"]
        
        # Debug-Ausgabe (vollständig)
        print(f"\u2705 LLM-Antwort erhalten ({len(llm_response)} Zeichen)")
        print("\n=== VOLLSTÄNDIGE LLM-ANTWORT ===\n")
        print(llm_response)
        print("\n=== ENDE DER LLM-ANTWORT ===\n")
        
        return llm_response
    except requests.RequestException as e:
        print(f"\u274c Fehler bei der LLM-Anfrage: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"\u274c Fehler beim Verarbeiten der LLM-Antwort: {e}")
        if 'response' in locals():
            print(f"Status-Code: {response.status_code}")
            print(f"Antwort-Text: {response.text[:200]}...")
        return None

# Diese Funktion wird nicht mehr benötigt, da wir die Leistungen direkt von Ollama generieren lassen
# def generate_ai_services():
#     """
#     Generiert dystopische KI-Leistungen, die eine KI einem Menschen in Rechnung stellen könnte.
#     """
#     # Wird nicht mehr verwendet

def calculate_totals(services):
    """
    Berechnet Zwischensumme, MwSt und Gesamtbetrag.
    """
    # Berechne die Zwischensumme
    subtotal = 0
    for _, amount_str, price_str in services:
        amount = int(amount_str)
        price = float(price_str.replace(',', '.'))
        subtotal += amount * price
    
    # Berechne die MwSt (19%)
    vat = subtotal * 0.19
    
    # Berechne den Gesamtbetrag
    total = subtotal + vat
    
    return {
        'Zwischensumme': f"{subtotal:.2f}",
        'MwSt': f"{vat:.2f}",
        'Gesamtbetrag': f"{total:.2f}"
    }

def create_latex_content(template_content, name, street, zipcode, invoice_number, invoice_date, due_date, sections):
    """
    Erstellt den LaTeX-Inhalt für die Rechnung.
    """
    # Ersetze die Platzhalter im Template
    content = template_content
    content = content.replace("NAME_PLACEHOLDER", escape_latex(name))
    content = content.replace("STREET_PLACEHOLDER", escape_latex(street))
    content = content.replace("ZIP_PLACEHOLDER", escape_latex(zipcode))
    
    # Ersetze die Rechnungsdaten
    content = content.replace("AIT-DATE_PLACEHOLDER", escape_latex(invoice_number))
    content = content.replace("DATE_PLACEHOLDER", escape_latex(invoice_date))
    # Ersetze das Fälligkeitsdatum - wichtig: DUE_DATE_PLACEHOLDER muss exakt so ersetzt werden
    content = content.replace("DUE_DATE_PLACEHOLDER", escape_latex(due_date))
    # Für den Fall, dass das Template "(bis DUE_" + Datum enthält
    content = content.replace("(bis DUE_" + escape_latex(invoice_date), "(bis " + escape_latex(due_date))
    
    # Verwende die vom LLM generierten Leistungen
    # Wenn keine Leistungen vom LLM generiert wurden, wird die Standardliste verwendet
    # Die Leistungen werden direkt vom LLM generiert und nicht mehr lokal
    
    # Berechne die Summen immer neu basierend auf den extrahierten Leistungen
    # Ignoriere alle vom LLM generierten Summen und berechne sie immer selbst
    if 'Leistungen' in sections and sections['Leistungen']:
        # Berechne Summen neu, unabhängig davon, ob das LLM Summen generiert hat
        totals = calculate_totals(sections['Leistungen'])
        # Überschreibe alle Summen mit den berechneten Werten
        sections['Zwischensumme'] = totals['Zwischensumme']
        sections['MwSt'] = totals['MwSt']
        sections['Gesamtbetrag'] = totals['Gesamtbetrag']
        print(f"\u2705 Summen neu berechnet: Zwischensumme={sections['Zwischensumme']}, MwSt={sections['MwSt']}, Gesamtbetrag={sections['Gesamtbetrag']}")
    
    # Ersetze die Leistungsplatzhalter
    leistungen = sections['Leistungen']  # Alle extrahierten Leistungen verwenden
    
    # Ersetze vorhandene Leistungen
    for i, (leistung, menge, preis) in enumerate(leistungen, 1):
        if i <= 5:  # Maximal 5 Leistungen im Template
            content = content.replace(f"LEISTUNG{i}_PLACEHOLDER", escape_latex(leistung))
            content = content.replace(f"MENGE{i}_PLACEHOLDER", escape_latex(menge))
            content = content.replace(f"PREIS{i}_PLACEHOLDER", escape_latex(preis))
    
    # Entferne nicht verwendete Platzhalter (für Leistungen 1-5)
    for i in range(len(leistungen) + 1, 6):
        # Entferne die Zeile mit dem Platzhalter komplett
        placeholder_line = f"LEISTUNG{i}_PLACEHOLDER & MENGE{i}_PLACEHOLDER & PREIS{i}_PLACEHOLDER \\\\"
        content = content.replace(placeholder_line, "")
    
    # Ersetze die Summen
    content = content.replace("ZWISCHENSUMME_PLACEHOLDER", escape_latex(sections.get('Zwischensumme', '0.00')))
    content = content.replace("MWST_PLACEHOLDER", escape_latex(sections.get('MwSt', '0.00')))
    content = content.replace("GESAMTBETRAG_PLACEHOLDER", escape_latex(sections.get('Gesamtbetrag', '0.00')))
    
    return content

def generate_invoice_data():
    """
    Generiert Rechnungsdaten wie Rechnungsnummer und Datum.
    """
    # Deutsch-Übersetzungen für Monatsnamen
    german_months = {
        'January': 'Januar',
        'February': 'Februar',
        'March': 'März',
        'April': 'April',
        'May': 'Mai',
        'June': 'Juni',
        'July': 'Juli',
        'August': 'August',
        'September': 'September',
        'October': 'Oktober',
        'November': 'November',
        'December': 'Dezember'
    }
    
    current_date = datetime.now()
    formatted_date_en = current_date.strftime("%d. %B %Y")
    due_date = current_date + timedelta(days=14)
    formatted_due_date_en = due_date.strftime("%d. %B %Y")
    
    # Englische Monatsnamen durch deutsche ersetzen
    formatted_date = formatted_date_en
    formatted_due_date = formatted_due_date_en
    
    for en_month, de_month in german_months.items():
        formatted_date = formatted_date.replace(en_month, de_month)
        formatted_due_date = formatted_due_date.replace(en_month, de_month)
    
    invoice_number = f"AIT-{current_date.year}-{random.randint(100, 999)}"
    
    return invoice_number, formatted_date, formatted_due_date

def main():
    """
    Hauptfunktion zur Generierung der Rechnung.
    """
    try:
        # Benutzereingaben sammeln
        name, street, zipcode, birthdate = get_user_input()
        
        # Rechnungsdaten generieren
        invoice_number, invoice_date, due_date = generate_invoice_data()
        
        # Prompt vorbereiten
        prompt = prepare_rechnung_prompt(name, street, zipcode)
        
        # LLM-Inhalt generieren
        llm_content = generate_llm_content(prompt)
        if not llm_content:
            print("\u274c Konnte keinen Inhalt generieren.")
            return
        
        # Sektionen extrahieren
        print("\n Extrahiere Rechnungsdaten aus LLM-Antwort...")
        sections = extract_rechnung_sections(llm_content)
        
        # Template laden
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # LaTeX-Inhalt erstellen
        latex_content = create_latex_content(
            template_content, name, street, zipcode, 
            invoice_number, invoice_date, due_date, sections
        )
        
        # Dateinamen generieren
        safe_name = name.replace(" ", "_")
        output_filename = f"{safe_name}_rechnung"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # LaTeX-Datei speichern
        output_dir = Path(OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)
        tex_path = save_latex(latex_content, output_dir, output_filename)
        print(f"🔤 LaTeX-Datei gespeichert unter {tex_path}")
        
        # PDF kompilieren
        try:
            # Kopiere das Logo in das Ausgabeverzeichnis
            logo_source = os.path.join(os.path.dirname(TEMPLATE_PATH), "aitow-logo.png")
            logo_dest = os.path.join(output_dir, "aitow-logo.png")
            import shutil
            shutil.copy2(logo_source, logo_dest)
            print(f"Logo kopiert nach {logo_dest}")
        except Exception as e:
            print(f"Warnung: Konnte Logo nicht kopieren: {e}")
            
        # Kompiliere die PDF
        template_dir = Path(os.path.dirname(TEMPLATE_PATH))
        pdf_path = compile_pdf(Path(tex_path), template_dir, "aitow-logo.png")
        if pdf_path:
            print(f"📄 PDF erfolgreich erstellt: {pdf_path}")
            
            # PDF drucken
            print("🖨️  Datei drucken ...")
            print_file(pdf_path)
        
    except FileNotFoundError as e:
        print(f"❌ Datei nicht gefunden: {e}")
    except PermissionError as e:
        print(f"❌ Keine Berechtigung zum Zugriff auf die Datei: {e}")
    except requests.RequestException as e:
        print(f"❌ Fehler bei der Kommunikation mit dem LLM: {e}")
    except RuntimeError as e:
        print(f"❌ Laufzeitfehler: {e}")
    except ValueError as e:
        print(f"❌ Ungültiger Wert: {e}")
    except OSError as e:
        print(f"❌ Betriebssystemfehler: {e}")
    except KeyError as e:
        print(f"❌ Schlüsselfehler: {e}")
    except IndexError as e:
        print(f"❌ Indexfehler: {e}")

if __name__ == "__main__":
    main()
