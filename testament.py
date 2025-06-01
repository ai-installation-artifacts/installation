import datetime
import shutil
import subprocess
import locale
from pathlib import Path
from ollama_util import (
    prepare_prompt,
    call_ollama,
    extract_sections,
    escape_latex
)

# Configuration
OUTPUT_DIR = Path(__file__).parent / "out"
TEMPLATE_PATH = Path(__file__).parent / "templates" / "testament_template.tex"
LOGO_NAME = "notarlogo.png"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

SECTION_KEYS = ["Erbeinsetzung", "Vermächtnisse", "Schlussbestimmungen"]
SECTION_PLACEHOLDERS = {
    'Erbeinsetzung': 'HEIRS_PLACEHOLDER',
    'Vermächtnisse': 'BEQUESTS_PLACEHOLDER',
    'Schlussbestimmungen': 'FINAL_TERMS_PLACEHOLDER'
}

def format_current_date_de() -> str:
    """Return current date formatted in German."""
    try:
        locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'de_DE')
        except locale.Error:
            pass
    date_str = datetime.datetime.now().strftime("%d. %B %Y")
    # Reset to default locale
    locale.setlocale(locale.LC_TIME, '')
    return date_str


def load_template() -> str:
    """Load the LaTeX template content."""
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Template not found: {TEMPLATE_PATH}")
    return TEMPLATE_PATH.read_text(encoding='utf-8')


def build_latex(name: str, birthdate: str, sections: dict) -> str:
    """Insert placeholders and build the full LaTeX document."""
    template = load_template()
    replacements = {
        'NAME_PLACEHOLDER': escape_latex(name),
        '%% BIRTHDATE_PLACEHOLDER %%': escape_latex(birthdate),
        '%% DATE_PLACEHOLDER %%': escape_latex(format_current_date_de()),
        '%% PLACE_PLACEHOLDER %%': r"M\"unchen"
    }
    for key in SECTION_KEYS:
        placeholder = f"%% {SECTION_PLACEHOLDERS[key]} %%"
        replacements[placeholder] = sections.get(key, '')

    for ph, val in replacements.items():
        template = template.replace(ph, val)
    return template


def save_latex(content: str, filename: str) -> Path:
    """Save LaTeX content to .tex file."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tex_path = OUTPUT_DIR / f"{filename}.tex"
    tex_path.write_text(content, encoding='utf-8')
    return tex_path


def compile_pdf(tex_path: Path) -> Path:
    """Compile LaTeX to PDF, trying different engines."""
    output_dir = tex_path.parent
    pdf_path = tex_path.with_suffix('.pdf')

    # Copy logo if exists
    logo_src = TEMPLATE_PATH.parent / LOGO_NAME
    if logo_src.exists():
        shutil.copy(logo_src, output_dir / LOGO_NAME)

    # for compiler in ["pdflatex", "xelatex", "lualatex"]:
    for compiler in ["pdflatex"]:
        try:
            subprocess.run(
                [compiler, "-interaction=nonstopmode", tex_path.name],
                cwd=output_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return pdf_path
        except Exception:
            continue
    raise RuntimeError("PDF compilation failed with all engines.")

def print_file(pdf_path):
    try:
        subprocess.run(["lp", pdf_path], check=True)
    except subprocess.CalledProcessError:
        print("❌ Fehler beim Drucken.")

def main(name: str, birthdate: str, compile_pdf_flag: bool = True):
    """Main workflow to generate and optionally compile the testament."""
    print("💬 Generiere Text ...")
    prompt = prepare_prompt(name, birthdate)
    raw_text = call_ollama(prompt)

    sections = extract_sections(raw_text)

    latex_content = build_latex(name, birthdate, sections)

    tex_file = save_latex(latex_content, name.replace(' ', '_') + "_testament")
    print("🔤 LaTeX-Datei gespeichert.")

    if compile_pdf_flag:
        try:
            pdf_file = compile_pdf(tex_file)
            print("📄 PDF erfolgreich erstellt.")
            return pdf_file
        except Exception as e:
            print(f"⚠️ Warnung bei der PDF-Erstellung: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        user_name, user_birthdate = sys.argv[1], sys.argv[2]
    else:
        user_name = input("Name: ").strip()
        user_birthdate = input("Geburtsdatum: ").strip()
    
    pdf_path = main(user_name, user_birthdate)

    if pdf_path:
        print("🖨️  Datei drucken ...")
        print_file(str(pdf_path))
