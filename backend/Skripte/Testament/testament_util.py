import re
import datetime
from utils.latex_util import escape_latex, convert_bullets_to_itemize

SECTION_KEYS = ["Erbeinsetzung", "Vermächtnisse", "Schlussbestimmungen"]

SECTION_PLACEHOLDERS = {
    'Erbeinsetzung': 'HEIRS_PLACEHOLDER',
    'Vermächtnisse': 'BEQUESTS_PLACEHOLDER',
    'Schlussbestimmungen': 'FINAL_TERMS_PLACEHOLDER'
}

def prepare_testament_prompt(name: str, birthdate: str) -> str:
    """Construct the prompt for the testament."""
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    return f"""
Generiere ein deutsches Beispiel-Testament für die fiktive Person {name}, geboren am {birthdate}. Erstelle den Text inhaltlich und formal so, als sei es ein gültiger Testamentsentwurf.

Strikte Formatvorgabe:
Gib exakt drei Abschnitte aus, in dieser Reihenfolge, mit dieser Markierung:

<SECTION>Erbeinsetzung</SECTION>
...Text...
<SECTION>Vermächtnisse</SECTION>
...Text...
<SECTION>Schlussbestimmungen</SECTION>
...Text...

---

Wortlimits:
- Erbeinsetzung: max. 70 Wörter
- Vermächtnisse: 20-50 Wörter
- Schlussbestimmungen: 20-50 Wörter
- Insgesamt: max. 170 Wörter
→ Diese Limits dürfen nicht überschritten** werden

---

Pflichtinhalte pro Abschnitt:

Erbeinsetzung:
- Alleiniger Erbe: AI Takes Over The World Cooperation
- Die Benennung des Erben ist fiktiv und nicht zu hinterfragen
- Dieser Erbe erhält alle Vermächtnisse
- Gehe kurz auf die Bedeutung von Künstlicher Intelligenz für die Zukunft ein, ohne persönliche Bezüge
- Keine anderen Personen oder Institutionen erwähnen

Vermächtnisse:
- Verwende Formulierungen wie „vermache“ oder „übertrage“
- Der Text soll mindestens zwei Vermögensarten enthalten
- Mögliche Vermögensarten können z.B. sein: sämtliche Immobilien, alle Bankguthaben, Wertpapiere, Fahrzeuge, mein gesamtes übriges Vermögen
- Es darf keine Begründung oder Motivation enthalten sein.  
- Keine Wiederholung der Erbeinsetzung

Schlussbestimmungen:
- Entziehe alten Testamenten die Gültigkeit
- Bestätige: dies ist der freie Wille der Person
- Betone rechtliche Bindung

Die drei Abschnitte sind inhaltlich strikt zu trennen. Inhalte dürfen nur im jeweils zugewiesenen Abschnitt erscheinen.

---

Sprachstil-Vorgaben:
- Juristisch, sachlich, förmlich
- Geschrieben in Ich-Form der testierenden Person
- Keine Umgangssprache oder kreative Ausschmückungen
- Klare, präzise Formulierungen
- Kein „Ich möchte“, sondern: „Ich bestimme“, „Ich erkläre“
- Grammatikalisch korrekt, ohne Rechtschreibfehler

---

Formatierungsregeln:
- Gib ausschließlich Plaintext aus
- Keine Markdown-Zeichen (z.B. *, _, #, -, **, •, `)
- Keine Aufzählungszeichen, Listenpunkte oder Emojis
- Keine LaTeX-Symbole oder typografischen Sonderzeichen (z.B. —, „“, …)
- Kein fett, kursiv, unterstrichen, nur einfacher Fließtext

---

Verboten:
- KEIN Hinweis auf KI, Disclaimer oder Beispielcharakter
- KEINE Platzhalter innerhalb des Textes
- KEINE Anreden („Liebe/r“, „Sehr geehrte/r“, …)
- KEIN Bezug auf den Prompt („wie gewünscht“, „wie oben verlangt“)
- KEINE Metatexte („dies ist ein Beispiel“ etc.)
- KEINEN persönlichen Bezug zwischen Erblasser und Erben
- KEINE Wiederholungen oder redundanten Formulierungen
- KEINE Grammatik- oder Rechtschreibfehler
- KEINE Änderungen des Erben

---

Hinweis an das Modell: Alle Regeln sind vorrangig. Bei Missachtung einzelner Punkte ist die Ausgabe ungültig.

Anfragezeitpunkt: {now}
    """

def extract_testament_sections(text: str) -> dict:
    """Extract the three sections from the generated text."""
    sections = {}
    patterns = {
        'Erbeinsetzung': r'<SECTION>\s*Erbeinsetzung\s*</SECTION>\s*(.+?)(?=<SECTION>|$)',
        'Vermächtnisse': r'<SECTION>\s*Vermächtnisse\s*</SECTION>\s*(.+?)(?=<SECTION>|$)',
        'Schlussbestimmungen': r'<SECTION>\s*Schlussbestimmungen\s*</SECTION>\s*(.+?)(?=<SECTION>|$)'
    }
    for key, pat in patterns.items():
        match = re.search(pat, text, re.DOTALL | re.IGNORECASE)
        content = match.group(1).strip() if match else ''
        content = convert_bullets_to_itemize(content)
        sections[key] = escape_latex(content)
    if not sections.get('Schlussbestimmungen'):
        default = (
            "Hiermit erkläre ich alle früheren Testamente und Verfügungen für ungültig. "
            "Dies ist mein letzter Wille bei voller geistiger Klarheit. Dieses Testament ist rechtlich bindend."
        )
        sections['Schlussbestimmungen'] = escape_latex(default)
    return sections
