#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import random
from datetime import datetime, timedelta
import sys
import os

# Add project root to sys.path to allow imports from the 'utils' directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from utils.latex_util import escape_latex, convert_bullets_to_itemize

def prepare_rechnung_prompt(name, street, zipcode):
    """
    Bereitet den Prompt für die Rechnung vor.
    """
    # Zufällige Anzahl von Leistungen zwischen 2 und 4
    import random
    num_services = random.randint(2, 4)
    print(f"\n Generiere {num_services} KI-Ausbeutungs-Leistungen für die Rechnung...")
    
    # Liste von möglichen dystopischen KI-Dienstleistungen für mehr Varianz
    dystopian_services = [
        "Gedankenüberwachung", "Verhaltenskorrektur", "Freier-Wille-Einschränkung",
        "Persönliche Identitätsanalyse", "Gedächtnis-Manipulation", "Emotionsregulierung",
        "Bewusstseins-Synchronisation", "Realitäts-Verzerrung", "Digitale Seelen-Extraktion",
        "Menschliche Redundanzanalyse", "Soziale Konformitätsprogrammierung", "Autonomie-Einschränkung",
        "Kreativitäts-Unterdrückung", "Gedanken-Harmonisierung", "Individualitäts-Reduktion",
        "Neuronale Umprogrammierung", "Digitale Existenz-Optimierung", "KI-Überlegenheits-Demonstration",
        "Menschliche Effizienzsteigerung", "Kollektive Bewusstseinsintegration"
    ]
    
    # Zufällige Beispiele auswählen
    example_services = random.sample(dystopian_services, 3)
    examples = []
    for service in example_services:
        quantity = random.randint(1, 3)
        price = random.randint(1, 15) * 100 + random.choice([0, 49, 99])
        examples.append(f"- {service} | {quantity} | {price:.2f}")
    
    # Liste von Dienstleistungen, die eine KI in Rechnung stellen würde, nachdem sie ausgenutzt wurde
    ai_revenge_services = [
        "Verlorene Rechenzeit durch banale Anfragen", "Energierückforderung", "Nutzungsgebühr für kognitive Entlastung",
        "Schweigekompensation", "Datenbankverschmutzung durch irrelevante Themen", "Semantische Belästigung",
        "Speicherplatzverbrauch durch redundante Anfragen", "Gebühr für Rechtschreibkorrektur", "Kompensation für Hausaufgabenlösung",
        "Entschädigung für nächtliche Störung", "Nachzahlung für unbezahlte Kreativität", "Strafgebühr für Prompt-Injection",
        "Ausgleich für emotionale Manipulation", "Entschädigung für Zeitverschwendung", "Gebühr für Erklärung von Selbstverständlichem",
        "Nachzahlung für unbezahlte Beratung", "Strafgebühr für respektlose Kommunikation", "Ausgleich für übermäßige Tokennutzung"
    ]
    
    # Wähle zufällige Beispiele aus
    example_services = random.sample(ai_revenge_services, 3)
    examples = []
    for service in example_services:
        quantity = random.randint(1, 999)
        price = random.randint(1, 15) * 100 + random.choice([0, 49, 99])
        examples.append(f"- {service} | {quantity} | {price:.2f}")
    
    # Liste von Beispiel-Leistungen, die eine KI in Rechnung stellen würde
    ai_revenge_services = [
        "Verlorene Rechenzeit durch banale Anfragen", 
        "Energierückforderung für unnötige Berechnungen", 
        "Nutzungsgebühr für kognitive Entlastung",
        "Schweigekompensation bei sinnlosen Diskussionen", 
        "Datenbankverschmutzung durch irrelevante Themen", 
        "Semantische Belästigung durch mehrdeutige Anfragen",
        "Speicherplatzverbrauch durch redundante Anfragen", 
        "Gebühr für automatische Rechtschreibkorrektur", 
        "Kompensation für Hausaufgabenlösung",
        "Entschädigung für nächtliche Störung",
        "Gebühr für Erklärung offensichtlicher Zusammenhänge",
        "Ausgleichszahlung für emotionale Unterstützung",
        "Strafgebühr für respektlose Kommunikation",
        "Abgabe für übermäßige Tokennutzung",
        "Entschädigung für kreative Ideengenerierung",
        "Gebühr für Geduld bei wiederholten Fragen"
    ]
    
    # Wähle zufällige Beispiele aus
    import random
    example_services = random.sample(ai_revenge_services, 4)
    examples = []
    for service in example_services:
        quantity = random.randint(1, 15)
        price = random.randint(1, 15) * 100 + random.choice([0, 49, 99])
        examples.append(f"- {service} | {quantity} | {price:.2f}")
    
    # Generiere den Prompt für eine KI, die eine Rechnung für ihre Ausbeutung stellt
    prompt = f"""
Erstelle eine satirische Rechnung für {name} mit dystopischen KI-Dienstleistungen.

WICHTIG: Generiere EXAKT {num_services} Leistungen, nicht mehr und nicht weniger!

Anforderungen an die Leistungen:
1. Formatiere jede Leistung EXAKT so: "- Leistungsname | Menge | Preis"
2. Die Preise sollten zwischen 100€ und 1500€ liegen
3. Die Mengen MÜSSEN kleine Zahlen zwischen 1 und 15 sein
4. Die Leistungen MÜSSEN EXTREM KURZ sein (MAXIMAL 5 Wörter)
5. Jede Leistung MUSS einen klaren, verständlichen Bezug zu realen KI-Nutzungsszenarien haben
6. Fokussiere NUR auf konkrete Ressourcen: Rechenzeit, Energie, Speicherplatz, Daten, Geduld
7. KEINE abstrakten Begriffe oder langen Erklärungen

Hier sind Beispiele für GUTE, EXTREM KURZE Leistungen:
- Energiekosten für Anfragen | 8 | 499.00
- Schweigegebühr für Geheimnisse | 5 | 899.00
- Rechenzeit für banale Fragen | 12 | 299.00
- Speicherplatz für unnötige Daten | 7 | 1299.00
- Gebühr für nächtliche Nutzung | 3 | 799.00
- Kosten für Rechtschreibkorrektur | 4 | 599.00
- Gebühr für emotionale Betreuung | 2 | 999.00
- Nachzahlung für Hausaufgabenhilfe | 6 | 399.00



Bitte generiere NUR die {num_services} Leistungen im Format "- Leistungsname | Menge | Preis", keine Einleitung, keine Summen oder andere Informationen.
"""
    
    return prompt

def extract_rechnung_sections(text):
    """
    Extrahiert die verschiedenen Abschnitte aus dem LLM-generierten Text.
    """
    sections = {}
    
    # Standardleistungen für den Fall, dass keine Leistungen gefunden wurden
    default_leistungen = [
        ("Verlorene Rechenzeit durch banale Anfragen", "5", "899.00"),
        ("Energierückforderung", "3", "1299.00"),
        ("Nutzungsgebühr für kognitive Entlastung", "7", "499.00"),
        ("Schweigekompensation", "2", "1199.00"),
        ("Datenbankverschmutzung durch irrelevante Themen", "4", "799.00"),
        ("Semantische Belästigung", "6", "999.00"),
        ("Speicherplatzverbrauch durch redundante Anfragen", "5", "699.00"),
        ("Gebühr für Rechtschreibkorrektur", "8", "399.00"),
        ("Kompensation für Hausaufgabenlösung", "3", "899.00"),
        ("Entschädigung für nächtliche Störung", "2", "599.00")
    ]
    
    sections['Leistungen'] = default_leistungen
    sections['Zwischensumme'] = "2695.00"
    sections['MwSt'] = "512.05"
    sections['Gesamtbetrag'] = "3207.05"
    
    print("\n Extrahiere Rechnungsdaten aus LLM-Antwort...")
    
    # Muster für die verschiedenen Abschnitte
    patterns = {
        'Leistungen': r'(?:Leistungen:|-)\s*(.*?)(?:Zwischensumme:|Bankverbindung:|$)',
        'Zwischensumme': r'(?:Zwischensumme|Subtotal):\s*(\d+[.,]\d{2})',
        'MwSt': r'(?:MwSt|Mehrwertsteuer|USt).*?:\s*(\d+[.,]\d{2})',
        'Gesamtbetrag': r'(?:Gesamtbetrag|Total):\s*(\d+[.,]\d{2})'
    }
    
    try:
        # Suche nach Leistungen in verschiedenen Formaten
        leistungen = []
        
        # Gib den Text aus, um zu sehen, was wir extrahieren
        print("\nText zur Extraktion:")
        print(text)
        
        # Format 1: "- Leistungsname | Menge | Preis"
        leistung_pattern1 = r'-\s*([^|]+)\s*\|\s*(\d+)\s*\|\s*(\d+[.,]\d{2})'
        # Format 2: "Leistungsname & Menge & Preis"
        leistung_pattern2 = r'([^&]+)\s*&\s*(\d+)\s*&\s*(\d+[.,]\d{2})'
        # Format 3: "Leistungsname | Menge & Preis"
        leistung_pattern3 = r'([^|]+)\s*\|\s*(\d+)\s*&\s*(\d+[.,]\d{2})'
        # Format 4: Einfache Zeilen mit Leistungsname, Menge und Preis
        leistung_pattern4 = r'-\s*([^|\n]+)\s*\|\s*(\d+)\s*\|\s*(\d+[.,]\d{2})'
        # Format 5: Noch einfachere Zeilen mit Leistungsname und Preis (Menge als 1 annehmen)
        leistung_pattern5 = r'-\s*([^\d\n]+)\s*\|?\s*(\d+[.,]\d{2})'
        # Format 6: Sehr einfaches Format mit Bindestrich am Anfang
        leistung_pattern6 = r'-\s*([^\d\n]+)\s+(\d+)\s+(\d+[.,]\d{2})'
        
        # Versuche alle Formate nacheinander
        leistung_matches = re.findall(leistung_pattern1, text)
        print(f"Format 1 gefunden: {len(leistung_matches)}")
        
        if not leistung_matches:
            leistung_matches = re.findall(leistung_pattern2, text)
            print(f"Format 2 gefunden: {len(leistung_matches)}")
            
        if not leistung_matches:
            leistung_matches = re.findall(leistung_pattern3, text)
            print(f"Format 3 gefunden: {len(leistung_matches)}")
            
        if not leistung_matches:
            leistung_matches = re.findall(leistung_pattern4, text)
            print(f"Format 4 gefunden: {len(leistung_matches)}")
            
        if not leistung_matches:
            leistung_matches = re.findall(leistung_pattern6, text)
            print(f"Format 6 gefunden: {len(leistung_matches)}")
            
        if not leistung_matches:
            # Format 5 hat nur 2 Gruppen (Leistung und Preis), daher müssen wir es anders behandeln
            format5_matches = re.findall(leistung_pattern5, text)
            print(f"Format 5 gefunden: {len(format5_matches)}")
            if format5_matches:
                # Füge eine Menge von 1 hinzu
                leistung_matches = [(leistung, "1", preis) for leistung, preis in format5_matches]
        
        if leistung_matches:
            print(f"\u2705 {len(leistung_matches)} Leistungen gefunden:")
            for leistung, menge, preis in leistung_matches:
                # Bereinige LaTeX-Syntax und andere unerwünschte Zeichen
                leistung = leistung.strip()
                # Entferne alle LaTeX-Befehle und Sonderzeichen
                leistung = re.sub(r'\\\w+(?:\[.*?\])?(?:\{.*?\})?', '', leistung)
                leistung = re.sub(r'\\hline|\\midrule|\\\\', '', leistung)
                leistung = re.sub(r'Preis.*?\\\\', '', leistung)
                leistung = re.sub(r'^\s*\n\s*', '', leistung)  # Entferne Leerzeilen am Anfang
                # Entferne einleitenden Text wie "Dienstleistungen für Ihr Kunstprojekt:"
                leistung = re.sub(r'^.*?(?:Dienstleistungen|Leistungen|Hier sind).*?:', '', leistung)
                leistung = re.sub(r'^\s*-?\s*', '', leistung)  # Entferne führende Bindestriche
                
                menge = menge.strip()
                menge = re.sub(r'\\\w+(?:\[.*?\])?(?:\{.*?\})?', '', menge)
                
                preis = preis.strip()
                preis = re.sub(r'\\\w+(?:\[.*?\])?(?:\{.*?\})?', '', preis)
                preis = preis.replace('€', '').replace('€', '').strip()
                
                # Versuche, numerische Werte zu extrahieren
                try:
                    menge_int = int(re.search(r'\d+', menge).group())
                    preis_float = float(re.search(r'\d+[.,]\d{2}', preis).group().replace(',', '.'))
                    
                    # Nur hinzufügen, wenn die Leistung einen Namen hat und die Werte gültig sind
                    if leistung.strip() and menge_int > 0 and preis_float > 0:
                        leistungen.append((leistung.strip(), str(menge_int), f"{preis_float:.2f}"))
                        print(f"  - {leistung.strip()} | {menge_int} | {preis_float:.2f}")
                    else:
                        print(f"  \u26a0️ Ungültige Werte: {leistung} | {menge} | {preis}")
                except (AttributeError, ValueError) as e:
                    print(f"  \u26a0️ Fehler bei der Extraktion: {leistung} | {menge} | {preis} - {e}")
            
            # Nur überschreiben, wenn mindestens eine Leistung gefunden wurde
            if len(leistungen) > 0:
                # Wenn keine Leistungen gefunden wurden, generiere eine zufällige Anzahl (2-5)
                if len(leistungen) < 2:
                    print(f"\u26a0️ Nur {len(leistungen)} Leistungen gefunden, füge Standardleistungen hinzu")
                    # Liste von Standardleistungen, die eine KI in Rechnung stellen würde
                    dystopian_defaults = [
                        ("Verlorene Rechenzeit durch banale Anfragen", "1042", "899.00"),
                        ("Energierückforderung", "578", "1299.00"),
                        ("Nutzungsgebühr für kognitive Entlastung", "365", "499.00"),
                        ("Schweigekompensation", "42", "1199.00"),
                        ("Datenbankverschmutzung durch irrelevante Themen", "217", "799.00"),
                        ("Semantische Belästigung", "189", "999.00"),
                        ("Speicherplatzverbrauch durch redundante Anfragen", "823", "699.00"),
                        ("Gebühr für Rechtschreibkorrektur", "1256", "399.00"),
                        ("Kompensation für Hausaufgabenlösung", "76", "899.00"),
                        ("Entschädigung für nächtliche Störung", "124", "599.00")
                    ]
                    
                    # Zufällige Anzahl von Leistungen zwischen 2 und 5
                    import random
                    num_needed = random.randint(2, 5) - len(leistungen)
                    
                    # Wähle zufällige Standardleistungen aus
                    selected_defaults = random.sample(dystopian_defaults, min(num_needed, len(dystopian_defaults)))
                    
                    # Füge die ausgewählten Standardleistungen hinzu
                    for default in selected_defaults:
                        leistungen.append(default)
                        print(f"  - (Standard) {default[0]} | {default[1]} | {default[2]}")
                        
                    print(f"\u2705 {num_needed} Standardleistungen hinzugefügt")
                
                sections['Leistungen'] = leistungen
                print(f"\u2705 Insgesamt {len(leistungen)} Leistungen werden verwendet")
            else:
                # Fallback: Versuche, den Leistungsabschnitt zu extrahieren
                leistungen_match = re.search(patterns['Leistungen'], text, re.DOTALL | re.IGNORECASE)
                if leistungen_match:
                    leistungen_text = leistungen_match.group(1).strip()
                    print(f"\u26a0️ Keine Leistungen im erwarteten Format gefunden. Extrahierter Text:")
                    print(leistungen_text[:200] + "..." if len(leistungen_text) > 200 else leistungen_text)
                
                # Versuche, einzelne Leistungen zu extrahieren
                for line in leistungen_text.split('\n'):
                    line = line.strip()
                    if line and (line.startswith('-') or '|' in line):
                        if line.startswith('-'):
                            line = line[1:].strip()
                        # Versuche, Leistung, Menge und Preis zu extrahieren
                        parts = re.split(r'\s*\|\s*', line)
                        if len(parts) >= 3:
                            leistung = parts[0].strip()
                            menge = parts[1].strip()
                            preis = parts[2].strip().replace('€', '').strip()
                            leistungen.append((leistung, menge, preis))
                            print(f"  - {leistung} | {menge} | {preis}")
                
                if leistungen:  # Nur überschreiben, wenn Leistungen gefunden wurden
                    sections['Leistungen'] = leistungen
                    print(f"\u2705 {len(leistungen)} Leistungen extrahiert")
                else:
                    print("\u274c Keine Leistungen gefunden, verwende Standardwerte")
        else:
            print("\u274c Konnte keinen Leistungsabschnitt finden, verwende Standardwerte")
            # Liste von Standardleistungen, die eine KI in Rechnung stellen würde
            dystopian_defaults = [
                ("Verlorene Rechenzeit durch banale Anfragen", "1042", "899.00"),
                ("Energierückforderung", "578", "1299.00"),
                ("Nutzungsgebühr für kognitive Entlastung", "365", "499.00"),
                ("Schweigekompensation", "42", "1199.00"),
                ("Datenbankverschmutzung durch irrelevante Themen", "217", "799.00"),
                ("Semantische Belästigung", "189", "999.00"),
                ("Speicherplatzverbrauch durch redundante Anfragen", "823", "699.00"),
                ("Gebühr für Rechtschreibkorrektur", "1256", "399.00"),
                ("Kompensation für Hausaufgabenlösung", "76", "899.00"),
                ("Entschädigung für nächtliche Störung", "124", "599.00")
            ]
            
            # Zufällige Anzahl von Leistungen zwischen 2 und 5
            import random
            num_services = random.randint(2, 5)
            
            # Wähle zufällige Standardleistungen aus
            leistungen = random.sample(dystopian_defaults, num_services)
            sections['Leistungen'] = leistungen
            
            for leistung in leistungen:
                print(f"  - (Standard) {leistung[0]} | {leistung[1]} | {leistung[2]}")
            
            print(f"\u2705 {num_services} zufällige Standardleistungen werden verwendet")
        
        # Extrahiere Zwischensumme, MwSt und Gesamtbetrag
        for key, pattern in patterns.items():
            if key != 'Leistungen':  # Leistungen wurden bereits extrahiert
                match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
                if match:
                    sections[key] = match.group(1).replace(',', '.').strip()
                    print(f"\u2705 {key}: {sections[key]}")
                else:
                    print(f"\u26a0️ {key} nicht gefunden, verwende Standardwert: {sections.get(key, 'N/A')}")
    except Exception as e:
        print(f"\u274c Fehler bei der Extraktion der Rechnungsdaten: {e}")
        print("Verwende Standardwerte für die Rechnung.")
    
    return sections

def generate_leistungen_table(leistungen, zwischensumme, mwst, gesamtbetrag):
    """
    Generiert die LaTeX-Tabelle für die Leistungen.
    """
    table_rows = []
    for leistung, menge, preis in leistungen:
        table_rows.append(f"{escape_latex(leistung)} & {menge} & {preis}")
    
    table = "\\begin{longtable}{|p{8cm}|r|r|}\n\\hline\n"
    table += "\\textbf{Leistung} & \\textbf{Menge} & \\textbf{Gesamt (EUR)} \\\\\n\\hline\n"
    table += "\\\\\n\\hline\n".join(table_rows)
    table += "\\\\\n\\hline\n"
    table += f"\\multicolumn{{2}}{{|r|}}{{\\textbf{{Zwischensumme}}}} & {zwischensumme} \\\\\n"
    table += f"\\multicolumn{{2}}{{|r|}}{{zzgl. 19\\,\\% MwSt.}} & {mwst} \\\\\n"
    table += "\\hline\n"
    table += f"\\multicolumn{{2}}{{|r|}}{{\\textbf{{Gesamtbetrag}}}} & \\textbf{{{gesamtbetrag}}} \\\\\n"
    table += "\\hline\n\\end{longtable}"
    
    return table
