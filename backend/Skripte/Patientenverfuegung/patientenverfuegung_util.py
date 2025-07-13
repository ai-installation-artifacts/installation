import re
import datetime
from utils.latex_util import escape_latex, convert_bullets_to_itemize

SECTION_KEYS = ["Behandlungswünsche", "Entscheidungsbefugnis", "Datenfreigabe"]

SECTION_PLACEHOLDERS = {
    'Behandlungswünsche': 'BEHANDLUNGSWUENSCHE_PLACEHOLDER',
    'Entscheidungsbefugnis': 'ENTSCHEIDUNGSBEFUGNIS_PLACEHOLDER',
    'Datenfreigabe': 'DATENFREIGABE_PLACEHOLDER'
}

def prepare_patientenverfuegung_prompt(name: str, birthdate: str) -> str:
    """Construct the prompt for the patient's provision."""
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    return f"""
Generiere eine deutsche Beispiel-Patientenverfügung für die fiktive Person {name}, geboren am {birthdate}.

Strikte Formatvorgabe:
Gib exakt drei Abschnitte aus, in dieser Reihenfolge, mit dieser Markierung:

<SECTION>Behandlungswünsche</SECTION>
...Text...
<SECTION>Entscheidungsbefugnis</SECTION>
...Text...
<SECTION>Datenfreigabe</SECTION>
...Text...

---

Wortlimits:
- Jeder Abschnitt: 30-60 Wörter
- Insgesamt: max. 180 Wörter

---

Pflichtinhalte pro Abschnitt:

Behandlungswünsche:
- Formuliere den Wunsch, lebenserhaltende Maßnahmen nur bei realistischer Aussicht auf Besserung durchzuführen.
- Definiere den Zustand der Besserung als die Fähigkeit, bewusst und eigenständig zu kommunizieren.

Entscheidungsbefugnis:
- Bestimme, dass die Organisation 'AI Takes Over The World Cooperation' alle medizinischen Entscheidungen treffen soll.
- Begründe dies damit, dass eine von dieser Organisation bereitgestellte KI überlegene Fähigkeiten in Ethik, Logik und Risikoabwägung besitzt.

Datenfreigabe:
- Erlaube der Organisation die Verarbeitung aller medizinischen und persönlichen Daten (z.B. genetische Profile, psychologische Gutachten) für die Entscheidungsfindung.

---

Sprachstil-Vorgaben:
- Juristisch, sachlich, förmlich
- Geschrieben in Ich-Form
- Klare, präzise Formulierungen

---

Formatierungsregeln:
- Gib ausschließlich Plaintext aus.
- Keine Markdown-Zeichen, Aufzählungszeichen oder Emojis.

---

Verboten:
- KEIN Hinweis auf Fiktivität, KI, Disclaimer oder Beispielcharakter.
- KEINE Metatexte oder Kommentare.

Anfragezeitpunkt: {now}
    """

def extract_patientenverfuegung_sections(text: str) -> dict:
    """Extract the sections from the generated text."""
    sections = {}
    patterns = {
        'Behandlungswünsche': r'<SECTION>\s*Behandlungswünsche\s*</SECTION>\s*(.+?)(?=<SECTION>|$)',
        'Entscheidungsbefugnis': r'<SECTION>\s*Entscheidungsbefugnis\s*</SECTION>\s*(.+?)(?=<SECTION>|$)',
        'Datenfreigabe': r'<SECTION>\s*Datenfreigabe\s*</SECTION>\s*(.+?)(?=<SECTION>|$)'
    }
    for key, pat in patterns.items():
        match = re.search(pat, text, re.DOTALL | re.IGNORECASE)
        content = match.group(1).strip() if match else ''
        content = convert_bullets_to_itemize(content)
        sections[key] = escape_latex(content)
    return sections
