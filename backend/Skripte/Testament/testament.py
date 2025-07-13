import sys
from pathlib import Path
import datetime

# Add project root to sys.path to allow imports from the 'utils' directory
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.latex_util import (
    format_current_date_de,
    load_template,
    build_latex,
    save_latex,
    compile_pdf,
    print_file,
    escape_latex
)
from utils.ollama_util import call_ollama
from utils.frontend_data_util import get_user_data_for_document
from testament_util import (
    prepare_testament_prompt,
    extract_testament_sections, 
    SECTION_KEYS,
    SECTION_PLACEHOLDERS
)

# Configuration
OUTPUT_DIR = project_root / "out"
TEMPLATE_PATH = project_root / "templates" / "testament_template.tex"
LOGO_NAME = "notarlogo.png"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

SECTION_KEYS = ["Erbeinsetzung", "Vermächtnisse", "Schlussbestimmungen"]
SECTION_PLACEHOLDERS = {
    'Erbeinsetzung': 'HEIRS_PLACEHOLDER',
    'Vermächtnisse': 'BEQUESTS_PLACEHOLDER',
    'Schlussbestimmungen': 'FINAL_TERMS_PLACEHOLDER'
}

def create_latex_content(name: str, birthdate: str, sections: dict) -> str:
    """Build the full LaTeX document for the testament."""
    template_content = load_template(TEMPLATE_PATH)
    replacements = {
        'NAME_PLACEHOLDER': escape_latex(name),
        '%% BIRTHDATE_PLACEHOLDER %%': escape_latex(birthdate),
        '%% DATE_PLACEHOLDER %%': format_current_date_de(),
        '%% PLACE_PLACEHOLDER %%': r"M\"unchen"
    }
    
    for key in SECTION_KEYS:
        placeholder = f"%% {SECTION_PLACEHOLDERS[key]} %%"
        replacements[placeholder] = sections.get(key, '')

    return build_latex(template_content, replacements)

def main(name: str = None, birthdate: str = None, compile_pdf_flag: bool = True):
    """Main workflow to generate and optionally compile the testament."""
    
    # Hole Benutzerdaten aus dem Frontend oder verwende übergebene Parameter
    user_data = get_user_data_for_document()
    
    # Verwende übergebene Parameter, falls vorhanden und keine Frontend-Daten gefunden wurden
    if name and not user_data.get('full_name'):
        user_data['full_name'] = name
        # Extrahiere Vorname für die Personalisierung
        user_data['firstname'] = name.split()[0] if name else ""
    
    if birthdate and not user_data.get('birthdate_german'):
        user_data['birthdate_german'] = birthdate
    
    # Extrahiere die benötigten Daten
    full_name = user_data.get('full_name', '')
    birthdate_german = user_data.get('birthdate_german', '')
    
    # Erzeuge Zeitstempel für Dateinamen
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("💬 Generiere Testament-Text ...")
    prompt = prepare_testament_prompt(full_name, birthdate_german)
    raw_text = call_ollama(prompt, url=OLLAMA_URL, model=MODEL_NAME)

    sections = extract_testament_sections(raw_text)

    latex_content = create_latex_content(full_name, birthdate_german, sections)

    filename = f"{full_name.replace(' ', '_')}_testament_{timestamp}"
    tex_file = save_latex(latex_content, OUTPUT_DIR, filename)
    print(f"🔤 LaTeX-Datei gespeichert unter {tex_file}")

    if compile_pdf_flag:
        try:
            template_dir = TEMPLATE_PATH.parent
            pdf_file = compile_pdf(tex_file, template_dir, LOGO_NAME)
            print(f"📄 PDF erfolgreich erstellt: {pdf_file}")
            return pdf_file
        except Exception as e:
            print(f"⚠️ Fehler bei der PDF-Erstellung: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        user_name, user_birthdate = sys.argv[1], sys.argv[2]
        pdf_path = main(user_name, user_birthdate)
    else:
        pdf_path = main()

    # Prüfen, ob die --no_print Option gesetzt ist
    no_print = "--no_print" in sys.argv
    
    if pdf_path:
        if not no_print:
            print("🖨️  Datei drucken ...")
            print_file(str(pdf_path))
        else:
            print("🚫 Drucken übersprungen.")
