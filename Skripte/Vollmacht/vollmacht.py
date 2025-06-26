import sys
import subprocess
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
from vollmacht_util import (
    prepare_vollmacht_prompt,
    extract_vollmacht_sections,
    SECTION_KEYS,
    SECTION_PLACEHOLDERS
)

# Configuration
OUTPUT_DIR = project_root / "out"
TEMPLATE_PATH = project_root / "templates" / "Vollmacht.tex"
LOGO_NAME = "notarlogo.png"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

def create_latex_content(template_content, sections, user_name, user_birthdate):
    """Create LaTeX content by replacing placeholders in the template."""
    replacements = {
        '%% NAME_PLACEHOLDER %%': escape_latex(user_name),
        '%% BIRTHDATE_PLACEHOLDER %%': escape_latex(user_birthdate),
        '%% DATE_PLACEHOLDER %%': format_current_date_de(),
        '%% PLACE_PLACEHOLDER %%': r"M\"unchen",
        '%% DOCUMENT_ID_PLACEHOLDER %%': f"VM-{format_current_date_de().replace(' ', '-')}"
    }
    # Add the sections to the replacements dictionary
    for section_name, section_content in sections.items():
        if section_name.startswith('Vollmacht_Umfang_Item_'):
            # Handle individual item placeholders
            item_number = section_name.split('_')[-1]
            replacements[f'%%VOLLMACHT_UMFANG_ITEM_{item_number}%%'] = section_content
        elif section_name != 'Bevollmächtigter':  # Skip Bevollmächtigter as it's hardcoded in template
            replacements[f'%% {section_name.upper()}_PLACEHOLDER %%'] = section_content

    return build_latex(template_content, replacements)

def main(name: str, birthdate: str, compile_pdf_flag: bool = True):
    """Main workflow to generate and optionally compile the power of attorney."""
    print("💬 Generiere Vollmacht-Text ...")
    prompt = prepare_vollmacht_prompt(name, birthdate)
    raw_text = call_ollama(prompt, url=OLLAMA_URL, model=MODEL_NAME)

    sections = extract_vollmacht_sections(raw_text)
    
    # Load the template content
    template_content = load_template(TEMPLATE_PATH)
    
    # Debug: Check if the template contains the hardcoded organization info
    if "Organisation \\textbf{AI Takes Over The World Cooperation}" in template_content:
        print("✅ Template contains hardcoded organization info")
    else:
        print("❌ Template does NOT contain hardcoded organization info")
        
    # Create LaTeX content with the template and sections
    latex_content = create_latex_content(template_content, sections, name, birthdate)

    filename = name.replace(' ', '_') + "_vollmacht"
    tex_file = save_latex(latex_content, OUTPUT_DIR, filename)
    print(f"🔤 LaTeX-Datei gespeichert unter {tex_file}")

    if compile_pdf_flag:
        try:
            template_dir = TEMPLATE_PATH.parent
            result_pdf = compile_pdf(tex_file, template_dir, LOGO_NAME)
            print(f"📄 PDF erfolgreich erstellt: {result_pdf}")
            print_file(result_pdf)
            return result_pdf
        except (FileNotFoundError, subprocess.CalledProcessError, IOError) as e:
            print(f"⚠️ Fehler bei der PDF-Erstellung: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        user_name, user_birthdate = sys.argv[1], sys.argv[2]
    else:
        user_name = input("Name: ").strip()
        user_birthdate = input("Geburtsdatum: ").strip()
    
    pdf_path = main(user_name, user_birthdate)

    if pdf_path:
        print("🖨️  Datei drucken ...")
        print_file(pdf_path)
