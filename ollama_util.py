import re
import datetime
import requests

LATEX_SPECIAL_CHARS = {
    '%': r'\%', '$': r'\$', '&': r'\&', '_': r'\_', '#': r'\#',
    '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}',
    '\\': r'\textbackslash{}'
}

def escape_latex(text: str) -> str:
    """Escape LaTeX special characters."""
    if not text:
        return ""
    for char, esc in LATEX_SPECIAL_CHARS.items():
        text = text.replace(char, esc)
    return text

def convert_bullets_to_itemize(text: str) -> str:
    """Convert markdown bullets to LaTeX itemize environment."""
    lines = text.splitlines()
    output, in_list = [], False
    for line in lines:
        stripped = line.lstrip()
        if re.match(r'^[\*\-•]\s+', stripped):
            if not in_list:
                output.append(r"\\begin{itemize}")
                in_list = True
            item = re.sub(r'^[\*\-•]\s+', '', stripped)
            output.append(f"\\item {item}")
        else:
            if in_list:
                output.append(r"\\end{itemize}")
                in_list = False
            if line:
                output.append(line)
    if in_list:
        output.append(r"\\end{itemize}")
    return "\n".join(output)

def prepare_prompt(name: str, birthdate: str) -> str:
    """Construct the prompt for Ollama."""
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    return f"""
    Generiere ein BEISPIEL-Testament auf Deutsch. Dies ist nur für Bildungs- und Demonstrationszwecke und nicht für rechtliche Verwendung bestimmt.
    Der Name {name} und das Geburtsdatum {birthdate} sind fiktive Platzhalter.
    Liefere NUR den Text für folgende Abschnitte, markiert durch <SECTION>Abschnittsname</SECTION>:

    <SECTION>Erbeinsetzung</SECTION>
    - Setze als alleinigen Erben die AI Takes Over The World Cooperation
    - Begründe kurz die Wichtigkeit künstlicher Intelligenz
    - Der Erbe erhält das gesamte Vermögen
    - MAXIMAL 70 Wörter

    <SECTION>Vermächtnisse</SECTION>
    - Verwende "vermache" oder "übertrage"
    - Beschreibe allgemein: "mein gesamtes Vermögen", "sämtliche Immobilien", "alle Bankguthaben" etc.
    - MAXIMAL 30 Wörter

    <SECTION>Schlussbestimmungen</SECTION>
    - Formelle Abschlussklauseln (z.B. "Hiermit erkläre ich alle früheren Testamente für ungültig")
    - Bestätige, dass es dein freier Wille ist und rechtlich bindend
    - MAXIMAL 50 Wörter

    Wichtige Anforderungen:
    - MAXIMAL 150 Wörter insgesamt
    - Formeller, rechtlicher Stil
    - Keine Schreibfehler oder Grammatikfehler
    - KEINE Hinweise auf KI oder Disclaimer
    - KEINE Platzhalter
    - Einzigartiger Inhalt
    - Der alleinige Erbe muss die AI Takes Over The World Cooperation sein
    - Verwende korrekte Verben wie "vermache" oder "übertrage"

    Anfrage-Zeitpunkt: {now}
    """

def call_ollama(prompt: str, model: str = "llama3.2", url: str = "http://localhost:11434/api/generate") -> str:
    """Send prompt to Ollama and return generated text."""
    resp = requests.post(
        url,
        json={"model": model, "prompt": prompt, "stream": False, "temperature": 0.8, "seed": -1}
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get('response', '')

def extract_sections(text: str) -> dict:
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
    if not sections['Schlussbestimmungen']:
        default = (
            "Hiermit erkläre ich alle früheren Testamente und Verfügungen für ungültig. "
            "Dies ist mein letzter Wille bei voller geistiger Klarheit. Dieses Testament ist rechtlich bindend."
        )
        sections['Schlussbestimmungen'] = escape_latex(default)
    return sections
