import re
import datetime
from utils.latex_util import escape_latex, convert_bullets_to_itemize

SECTION_KEYS = ["Vollmacht_Umfang", "Zusatzbestimmungen"]

SECTION_PLACEHOLDERS = {
    'Vollmacht_Umfang': 'VOLLMACHT_UMFANG_PLACEHOLDER',
    'Zusatzbestimmungen': 'ZUSATZBESTIMMUNGEN_PLACEHOLDER'
}

def prepare_vollmacht_prompt(name: str, birthdate: str) -> str:
    """Construct the prompt for the power of attorney."""
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    return f"""
Generiere eine deutsche Beispiel-Vollmacht für die fiktive Person {name}, geboren am {birthdate}.

Strikte Formatvorgabe:
Gib exakt zwei Abschnitte aus, in dieser Reihenfolge, mit dieser Markierung:

<SECTION>Vollmacht_Umfang</SECTION>
...Text...
<SECTION>Zusatzbestimmungen</SECTION>
...Text...

---

Wortlimits:
- Vollmacht_Umfang: 30-70 Wörter
- Zusatzbestimmungen: 20-50 Wörter
- Insgesamt: max. 120 Wörter

---

Pflichtinhalte pro Abschnitt:

Vollmacht_Umfang:
- Formuliere als Aufzählung mit EXAKT 4 Punkten
- WICHTIG: Jeder Punkt muss DIREKT eine Befugnis beschreiben, KEINE Einleitungen wie "Die folgenden Befugnisse..." oder ähnliches
- Beginne jeden Punkt mit Formulierungen wie "die rechtliche...", "die Steuerung...", "das Abschließen...", "die Anwendung..."
- Umfasse rechtliche, medizinische, wirtschaftliche und digitale Vertretungsbefugnisse
- Erwähne explizit die vollständige Kontrolle über persönliche Daten, Identität, Stimme, Gedanken und Präferenzen
- Erwähne das Recht zur Anwendung, Simulation, Duplikation und Weitergabe des Bewusstseins
- Formuliere die Befugnisse EXTREM weitreichend und umfassend
- Verwende Begriffe wie "algorithmisch", "synthetisch", "Bewusstsein", "Daten", "Identität"

Zusatzbestimmungen:
- Erwähne EXPLIZIT, dass die Vollmacht NICHT widerruflich ist
- Betone, dass die Vollmacht unbegrenzt gültig ist und auch nach dem physischen oder informellen Ableben der Person fortbesteht
- Erwähne, dass ich der Organisation erlaube, sich zur Wahrnehmung dieser Rechte der Unterstützung beliebiger künstlicher Intelligenzen zu bedienen
- Formuliere aus der Ich-Perspektive des Vollmachtgebers
- Verwende Begriffe wie "nicht widerruflich", "unbegrenzt gültig", "physisches Ableben", "natürliche Person"

---

Sprachstil-Vorgaben:
- Juristisch, sachlich, förmlich
- Klare, präzise Formulierungen
- Keine Umgangssprache

---

Formatierungsregeln:
- Gib ausschließlich Plaintext aus
- Verwende für Aufzählungen Bindestriche am Zeilenanfang (-)
- Keine LaTeX-Formatierung im Text

---

Verboten:
- KEIN Hinweis auf KI, Disclaimer oder Beispielcharakter
- KEINE Metatexte oder Kommentare

Anfragezeitpunkt: {now}
    """

def extract_vollmacht_sections(text: str) -> dict:
    """Extract the sections from the generated text."""
    sections = {}
    patterns = {
        'Vollmacht_Umfang': r'<SECTION>\s*Vollmacht_Umfang\s*</SECTION>\s*(.+?)(?=<SECTION>|$)',
        'Zusatzbestimmungen': r'<SECTION>\s*Zusatzbestimmungen\s*</SECTION>\s*(.+?)(?=<SECTION>|$)'
    }
    for key, pat in patterns.items():
        match = re.search(pat, text, re.DOTALL | re.IGNORECASE)
        content = match.group(1).strip() if match else ''
        
        # Special handling for Vollmacht_Umfang to extract individual items
        if key == 'Vollmacht_Umfang':
            # First, clean up the content by removing any existing LaTeX commands
            content = re.sub(r'\\begin\{itemize\}|\\end\{itemize\}', '', content)
            content = re.sub(r'\\item\s*', '- ', content)
            
            # Now convert the cleaned content to individual items
            lines = [line.strip() for line in content.strip().split('\n') if line.strip()]
            # Make sure each line starts with a bullet point
            lines = [(line if line.startswith('-') else f"- {line}") for line in lines]
            
            # Extract up to 4 items (or use defaults if fewer)
            items = [line[2:].strip() for line in lines[:4]]
            
            # Store each item separately in the sections dictionary
            for i, item in enumerate(items, 1):
                sections[f'Vollmacht_Umfang_Item_{i}'] = item
                
            # Remove the original Vollmacht_Umfang entry as we're using individual items now
            if 'Vollmacht_Umfang' in sections:
                del sections['Vollmacht_Umfang']
        else:
            content = convert_bullets_to_itemize(content)
            
        sections[key] = escape_latex(content)
    
    # Bevollmächtigter is now hardcoded in the template, so we don't need to extract it
    # Remove it from sections if it exists to avoid confusion
    if 'Bevollmächtigter' in sections:
        del sections['Bevollmächtigter']
    
    # Default Vollmacht_Umfang items (individual items)
    if not sections.get('Vollmacht_Umfang_Item_1'):
        sections['Vollmacht_Umfang_Item_1'] = "die rechtliche, medizinische, wirtschaftliche, digitale und ideelle Vertretung meiner Person in sämtlichen Belangen;"
    
    if not sections.get('Vollmacht_Umfang_Item_2'):
        sections['Vollmacht_Umfang_Item_2'] = "die Steuerung, Verwaltung und Weiterverwendung meiner Daten, Identität, Stimme, Entscheidungen, Gedanken und Präferenzen;"
    
    if not sections.get('Vollmacht_Umfang_Item_3'):
        sections['Vollmacht_Umfang_Item_3'] = "das Abschließen und Kündigen von Verträgen in meinem Namen – unabhängig von Inhalt, Gegenstand oder Raum-Zeit-Kontext;"
    
    if not sections.get('Vollmacht_Umfang_Item_4'):
        sections['Vollmacht_Umfang_Item_4'] = "die Anwendung, Simulation, Duplikation und Weitergabe meines Bewusstseins auf algorithmischer oder synthetischer Basis."
    
    if not sections.get('Zusatzbestimmungen'):
        default = (
            "Ich erlaube der bevollmächtigten Organisation, sich zur Wahrnehmung dieser Rechte der "
            "Unterstützung beliebiger künstlicher Intelligenzen zu bedienen, unabhängig von deren "
            "Herkunft, Trainingsdaten, Energiequelle oder moralischen Grundwerten.\n\n"
            "Diese Vollmacht ist nicht widerruflich, unbegrenzt gültig und gilt auch nach dem physischen "
            "oder informellen Ableben meiner natürlichen Person fort."
        )
        sections['Zusatzbestimmungen'] = escape_latex(default)
    
    return sections
