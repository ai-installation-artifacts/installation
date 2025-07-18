import sys
import argparse
from pathlib import Path

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
from patientenverfuegung_util import (
    prepare_patientenverfuegung_prompt,
    extract_patientenverfuegung_sections,
    SECTION_KEYS,
    SECTION_PLACEHOLDERS
)

# Configuration
OUTPUT_DIR = project_root / "out"
TEMPLATE_PATH = project_root / "templates" / "Patientenverfügung_template.tex"
LOGO_NAME = "notarlogo.png"
SIGNATURE_NAME = "Unterschrift.png"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

def create_latex_content(name: str, birthdate: str, sections: dict) -> str:
    """Build the full LaTeX document for the patient's provision."""
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

    latex_content = build_latex(template_content, replacements)
    
    return latex_content

def main(name: str, birthdate: str, compile_pdf_flag: bool = True, no_print: bool = False):
    """Main workflow to generate and optionally compile the patient's provision."""
    print("💬 Generiere Patientenverfügungs-Text ...")
    prompt = prepare_patientenverfuegung_prompt(name, birthdate)
    raw_text = call_ollama(prompt, url=OLLAMA_URL, model=MODEL_NAME)

    sections = extract_patientenverfuegung_sections(raw_text)

    latex_content = create_latex_content(name, birthdate, sections)

    filename = name.replace(' ', '_') + "_patientenverfuegung"
    tex_file = save_latex(latex_content, OUTPUT_DIR, filename)
    print(f"🔤 LaTeX-Datei gespeichert unter {tex_file}")

    if compile_pdf_flag:
        try:
            template_dir = TEMPLATE_PATH.parent
            pdf_file = compile_pdf(tex_file, template_dir, LOGO_NAME, SIGNATURE_NAME)
            print(f"📄 PDF erfolgreich erstellt: {pdf_file}")
            
            # Drucken nur, wenn no_print nicht gesetzt ist
            if not no_print:
                print("🖨️  Datei drucken ...")
                print_file(pdf_file)
            else:
                print("🚫 Drucken übersprungen.")
                
            return pdf_file
        except Exception as e:
            print(f"⚠️ Fehler bei der PDF-Erstellung: {e}")

if __name__ == "__main__":
    # Argumente parsen
    parser = argparse.ArgumentParser(description="Generiert eine Patientenverfügung")
    parser.add_argument("name", nargs="?", help="Name der Person")
    parser.add_argument("birthdate", nargs="?", help="Geburtsdatum der Person")
    parser.add_argument("--no_print", action="store_true", help="PDF nach Erstellung nicht drucken")
    args = parser.parse_args()
    
    # Wenn keine Argumente übergeben wurden, interaktiv abfragen
    if not args.name or not args.birthdate:
        user_name = input("Name: ").strip()
        user_birthdate = input("Geburtsdatum: ").strip()
    else:
        user_name = args.name
        user_birthdate = args.birthdate
    
    pdf_path = main(user_name, user_birthdate, no_print=args.no_print)
