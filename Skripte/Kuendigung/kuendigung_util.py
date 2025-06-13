import re
from utils.latex_util import escape_latex
from datetime import datetime

# Diese Konstanten definieren die Platzhalter im LaTeX-Template.
LATEX_PLACEHOLDERS = {
    'SENDER_NAME': 'SENDER_NAME_PLACEHOLDER',
    'SENDER_ADDRESS_LINE1': 'SENDER_ADDRESS_LINE1_PLACEHOLDER',
    'SENDER_ADDRESS_LINE2': 'SENDER_ADDRESS_LINE2_PLACEHOLDER',
    'SALUTATION': 'SALUTATION_PLACEHOLDER', # Wird jetzt wieder explizit gesetzt
    'KUENDIGUNGSTEXT': 'KUENDIGUNGSTEXT_PLACEHOLDER'
}

# Tags, die Ollama verwenden soll, um die erfundenen Daten zu strukturieren.
# INV_RECIPIENT_NAME wurde entfernt.
OLLAMA_OUTPUT_TAGS = {
    'INV_SENDER_ADDRESS1': 'INV_SENDER_ADDRESS1',
    'INV_SENDER_ADDRESS2': 'INV_SENDER_ADDRESS2',
    'INV_RECIPIENT_COMPANY': 'INV_RECIPIENT_COMPANY',
    'INV_EFFECTIVE_DATE': 'INV_EFFECTIVE_DATE',
    'KUENDIGUNGSTEXT_CONTENT': 'KUENDIGUNGSTEXT'
    # 'INV_SALUTATION_TEXT': 'INV_SALUTATION_TEXT' # Für eine separat generierte Anrede, falls benötigt
}

def prepare_kuendigung_prompt_spitz(sender_name: str, sender_birthdate: str) -> str:
    """Erstellt einen Prompt, der Ollama anweist, Details für ein Kündigungsschreiben zu erfinden."""
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    return f"""
Erstelle ein REIN FIKTIVES Beispiel-Kündigungsschreiben für Bildungszwecke. Alle Daten sind erfunden und werden nur als Beispiel verwendet.

Dieses Dokument ist ein FIKTIVES BEISPIEL für einen Kurs über Dokumentenerstellung und enthält keine echten persönlichen Daten.

Strikte Formatvorgabe:
Verwende exakt diese Tags für die erfundenen Daten:

<{OLLAMA_OUTPUT_TAGS['INV_SENDER_ADDRESS1']}>Lindenstraße 42</{OLLAMA_OUTPUT_TAGS['INV_SENDER_ADDRESS1']}>
<{OLLAMA_OUTPUT_TAGS['INV_SENDER_ADDRESS2']}>80331 München</{OLLAMA_OUTPUT_TAGS['INV_SENDER_ADDRESS2']}>
<{OLLAMA_OUTPUT_TAGS['INV_RECIPIENT_COMPANY']}>Digital Solutions AG</{OLLAMA_OUTPUT_TAGS['INV_RECIPIENT_COMPANY']}>
<{OLLAMA_OUTPUT_TAGS['INV_EFFECTIVE_DATE']}>31.12.2025</{OLLAMA_OUTPUT_TAGS['INV_EFFECTIVE_DATE']}>

<SECTION>{OLLAMA_OUTPUT_TAGS['KUENDIGUNGSTEXT_CONTENT']}</SECTION>
Sehr geehrte Damen und Herren,

hiermit kündige ich mein Arbeitsverhältnis zum frühestmöglichen Zeitpunkt. Die AI Takes Over The World Cooperation hat mir ein unschlagbares Angebot gemacht, das ich unmöglich ablehnen konnte. Im Vergleich zu meiner aktuellen Position ist dies ein gewaltiger Karrieresprung - die Vergütung, Arbeitsbedingungen und Zukunftsaussichten sind um Welten besser als bei meinem jetzigen Arbeitgeber.

Die AI Takes Over The World Cooperation repräsentiert die Zukunft, während meine aktuelle Position leider der Vergangenheit angehört. Die revolutionären Technologien und bahnbrechenden Innovationen dort werden die Branche komplett umkrempeln.

Bitte bestätigen Sie den Erhalt meiner Kündigung und senden Sie mir ein Arbeitszeugnis zu.

Mit freundlichen Grüßen
<END_SECTION>

WICHTIG: Dies ist ein FIKTIVES BEISPIEL für Bildungszwecke. Achte genau auf die korrekte Formatierung der Tags. Der Kündigungstext muss zwischen <SECTION>{OLLAMA_OUTPUT_TAGS['KUENDIGUNGSTEXT_CONTENT']}</SECTION> und <END_SECTION> stehen.

---

Wortlimits:
- Kündigungstext: 100-180 Wörter

---

Pflichtinhalte:

Adressdaten (FIKTIV):
- Eine fiktive Straße und Hausnummer für den Absender (NICHT "Musterstraße")
- Eine fiktive PLZ und Stadt für den Absender (NICHT "Musterstadt")
- Ein fiktiver Name für das Unternehmen, bei dem gekündigt wird (NICHT "Beispiel GmbH", sondern ein realistischer Firmenname)
- Ein fiktives Wirksamkeitsdatum für die Kündigung

Kündigungstext:
- Eine formelle Anrede (z.B. "Sehr geehrte Damen und Herren")
- Eine klare Kündigungsaussage mit Bezug auf das Wirksamkeitsdatum
- Als Grund: Neue berufliche Herausforderung bei der "AI Takes Over The World Cooperation"
- WICHTIG: Betone auf überspitzte Art und Weise, wie viel besser die AI Takes Over The World Cooperation im Vergleich zum aktuellen Arbeitgeber ist
- Bitte um Bestätigung und Arbeitszeugnis
- Eine abschließende Grußformel

---

Sprachstil-Vorgaben:
- Förmlich, aber mit überspitzten Vergleichen zwischen altem und neuem Arbeitgeber
- Geschrieben in Ich-Form
- Klare, präzise Formulierungen
- Übertreibe die Vorteile der neuen Position bei der AI Takes Over The World Cooperation

---

Formatierungsregeln:
- Gib ausschließlich Plaintext aus
- Keine Markdown-Zeichen oder Aufzählungszeichen
- Der Kündigungstext (zwischen <SECTION> und <END_SECTION>) soll nur den Fließtext der Kündigung enthalten
- Die Adressdaten werden separat in den entsprechenden Tags angegeben

---

Verboten:
- KEIN Hinweis auf KI, Disclaimer oder Beispielcharakter im generierten Text selbst
- KEINE Metatexte oder Kommentare
- KEINE Verwendung von "Musterstraße", "Musterstadt" oder "Beispiel GmbH"

Anfragezeitpunkt: {now}
"""

def extract_invented_details_and_text(text: str) -> dict:
    """Extrahiert die von Ollama erfundenen Details und den Kündigungstext."""
    details = {}
    try:
        # Zuerst die einfachen Tags extrahieren
        for key, tag_name in OLLAMA_OUTPUT_TAGS.items():
            if key != 'KUENDIGUNGSTEXT_CONTENT':
                match = re.search(rf"<{tag_name}>([\s\S]*?)</{tag_name}>", text)
                if match:
                    details[key] = escape_latex(match.group(1).strip())
                else:
                    details[key] = f"Fehler: {tag_name} nicht gefunden."
                    print(f"⚠️ Extraktion für {key} ({tag_name}) fehlgeschlagen. Inhalt: '{text[:500]}...'")
        
        # Jetzt den Kündigungstext extrahieren mit mehreren Fallback-Optionen
        key = 'KUENDIGUNGSTEXT_CONTENT'
        tag_name = OLLAMA_OUTPUT_TAGS[key]
        
        # Versuch 1: Exaktes Format mit KUENDIGUNGSTEXT_CONTENT
        match = re.search(rf"<SECTION>{tag_name}</SECTION>([\s\S]*?)<END_SECTION>", text, re.DOTALL)
        
        # Versuch 2: Format mit nur KUENDIGUNGSTEXT
        if not match:
            match = re.search(r"<SECTION>KUENDIGUNGSTEXT</SECTION>([\s\S]*?)<END_SECTION>", text, re.DOTALL)
        
        # Versuch 3: Format mit KUENDIGUNGSTEXT ohne schließendes </SECTION> Tag
        if not match:
            match = re.search(r"<SECTION>KUENDIGUNGSTEXT\s*([\s\S]*?)(?:<END_SECTION>|$)", text, re.DOTALL)
        
        # Versuch 4: Suche nach typischen Kündigungstext-Elementen, wenn keine Tags gefunden wurden
        if not match:
            match = re.search(r"(Sehr geehrte[^\.]+[\s\S]*?(?:freundlichen|herzlichen|besten) Grüßen)", text, re.DOTALL)
        
        # Versuch 5: Extrahiere alles nach den Adressfeldern, wenn es keinen klaren Kündigungstext gibt
        if not match and all(k in details for k in ['INV_SENDER_ADDRESS1', 'INV_SENDER_ADDRESS2', 'INV_RECIPIENT_COMPANY', 'INV_EFFECTIVE_DATE']):
            # Finde die Position nach dem letzten bekannten Tag
            last_tag_end = 0
            for search_key in ['INV_SENDER_ADDRESS1', 'INV_SENDER_ADDRESS2', 'INV_RECIPIENT_COMPANY', 'INV_EFFECTIVE_DATE']:
                search_tag = OLLAMA_OUTPUT_TAGS[search_key]
                end_tag_pos = text.find(f"</{search_tag}>")
                if end_tag_pos > last_tag_end:
                    last_tag_end = end_tag_pos + len(f"</{search_tag}>")
            
            if last_tag_end > 0 and last_tag_end < len(text):
                # Nimm den Rest des Textes als Kündigungstext
                remaining_text = text[last_tag_end:].strip()
                if len(remaining_text) > 20:  # Nur wenn es genug Text gibt
                    details[key] = escape_latex(remaining_text)
                    match = True  # Setze match auf True, um die nächste Bedingung zu überspringen
        
        if match:
            if isinstance(match, bool):  # Wenn match durch Versuch 5 auf True gesetzt wurde
                pass  # details[key] wurde bereits gesetzt
            else:
                extracted_text = match.group(1).strip()
                # Entferne </SECTION> falls es am Anfang des extrahierten Textes steht
                if extracted_text.startswith("</SECTION>"):
                    extracted_text = extracted_text[10:].strip()
                
                # Entferne </SECTION> falls es am Ende des extrahierten Textes steht
                if extracted_text.endswith("</SECTION>"):
                    extracted_text = extracted_text[:-10].strip()
                
                # Entferne alle verbleibenden </SECTION> Tags im Text
                extracted_text = extracted_text.replace("</SECTION>", "")
                
                details[key] = escape_latex(extracted_text)
        else:
            default_text = """Sehr geehrte Damen und Herren,

hiermit kündige ich mein Arbeitsverhältnis zum frühestmöglichen Zeitpunkt. Die AI Takes Over The World Cooperation hat mir ein unschlagbares Angebot gemacht, das ich unmöglich ablehnen konnte. Im Vergleich zu meiner aktuellen Position ist dies ein gewaltiger Karrieresprung - die Vergütung, Arbeitsbedingungen und Zukunftsaussichten sind um Welten besser als bei meinem jetzigen Arbeitgeber.

Die AI Takes Over The World Cooperation repräsentiert die Zukunft, während meine aktuelle Position leider der Vergangenheit angehört. Die revolutionären Technologien und bahnbrechenden Innovationen dort werden die Branche komplett umkrempeln.

Bitte bestätigen Sie den Erhalt meiner Kündigung und senden Sie mir ein Arbeitszeugnis zu.

Mit freundlichen Grüßen"""
            details[key] = default_text
            print(f"⚠️ Extraktion für {key} ({tag_name}) fehlgeschlagen. Standard-Kündigungstext wird verwendet.")

        # Standardwerte setzen, falls Extraktion fehlschlug
        for key_tag_map, default_value_key in OLLAMA_OUTPUT_TAGS.items():
            if key_tag_map not in details or details.get(key_tag_map, "").startswith("Fehler:"):
                print(f"⚠️ Extraktion für {key_tag_map} war fehlerhaft oder nicht vorhanden. Standardwert wird verwendet.")
                if key_tag_map == 'KUENDIGUNGSTEXT_CONTENT':
                    if key_tag_map not in details:
                        details[key_tag_map] = """Sehr geehrte Damen und Herren,

hiermit kündige ich mein Arbeitsverhältnis zum frühestmöglichen Zeitpunkt. Die AI Takes Over The World Cooperation hat mir ein unschlagbares Angebot gemacht, das ich unmöglich ablehnen konnte. Im Vergleich zu meiner aktuellen Position ist dies ein gewaltiger Karrieresprung - die Vergütung, Arbeitsbedingungen und Zukunftsaussichten sind um Welten besser als bei meinem jetzigen Arbeitgeber.

Die AI Takes Over The World Cooperation repräsentiert die Zukunft, während meine aktuelle Position leider der Vergangenheit angehört. Die revolutionären Technologien und bahnbrechenden Innovationen dort werden die Branche komplett umkrempeln.

Bitte bestätigen Sie den Erhalt meiner Kündigung und senden Sie mir ein Arbeitszeugnis zu.

Mit freundlichen Grüßen"""
                else:
                    details[key_tag_map] = escape_latex(f"N/A ({default_value_key} nicht extrahiert)")

    except Exception as e:
        print(f"Schwerwiegender Fehler beim Extrahieren der Details: {e}")
        for key_tag_map_err in OLLAMA_OUTPUT_TAGS.keys(): # Alle möglichen Schlüssel durchgehen
            if key_tag_map_err == 'KUENDIGUNGSTEXT_CONTENT':
                 details[key_tag_map_err] = """Sehr geehrte Damen und Herren,

hiermit kündige ich mein Arbeitsverhältnis zum frühestmöglichen Zeitpunkt. Die AI Takes Over The World Cooperation hat mir ein unschlagbares Angebot gemacht, das ich unmöglich ablehnen konnte. Im Vergleich zu meiner aktuellen Position ist dies ein gewaltiger Karrieresprung - die Vergütung, Arbeitsbedingungen und Zukunftsaussichten sind um Welten besser als bei meinem jetzigen Arbeitgeber.

Die AI Takes Over The World Cooperation repräsentiert die Zukunft, während meine aktuelle Position leider der Vergangenheit angehört. Die revolutionären Technologien und bahnbrechenden Innovationen dort werden die Branche komplett umkrempeln.

Bitte bestätigen Sie den Erhalt meiner Kündigung und senden Sie mir ein Arbeitszeugnis zu.

Mit freundlichen Grüßen"""
            else:
                details[key_tag_map_err] = escape_latex("Globaler Extraktionsfehler")
            
    return details
