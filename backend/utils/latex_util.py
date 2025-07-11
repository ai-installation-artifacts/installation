import datetime
import locale
import shutil
import subprocess
import re
from pathlib import Path

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
        if re.match(r'^[*\-•]\s+', stripped):
            if not in_list:
                output.append(r"\\begin{itemize}")
                in_list = True
            item = re.sub(r'^[*\-•]\s+', '', stripped)
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

def format_current_date_de() -> str:
    """Return current date formatted in German."""
    try:
        locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'de_DE')
        except locale.Error:
            pass # Fallback to system default
    date_str = datetime.datetime.now().strftime("%d. %B %Y")
    locale.setlocale(locale.LC_TIME, '') # Reset to default
    return date_str

def load_template(template_path: Path) -> str:
    """Load the LaTeX template content."""
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    return template_path.read_text(encoding='utf-8')

def build_latex(template_content: str, replacements: dict) -> str:
    """Insert placeholders and build the full LaTeX document."""
    for placeholder, value in replacements.items():
        template_content = template_content.replace(placeholder, value)
    return template_content

def save_latex(content: str, output_dir: Path, filename: str) -> Path:
    """Save LaTeX content to .tex file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    tex_path = output_dir / f"{filename}.tex"
    tex_path.write_text(content, encoding='utf-8')
    return tex_path

def compile_pdf(tex_path: Path, template_dir: Path, logo_name: str = None, signature_name: str = None) -> Path:
    """Compile LaTeX to PDF, trying different engines."""
    output_dir = tex_path.parent
    pdf_path = tex_path.with_suffix('.pdf')

    if logo_name:
        logo_src = template_dir / logo_name
        if logo_src.exists():
            shutil.copy(logo_src, output_dir / logo_name)
    
    # Erstelle das Signature-Verzeichnis im Output-Verzeichnis, falls es benötigt wird
    signature_output_dir = output_dir / "Signature"
    signature_output_dir.mkdir(exist_ok=True)
    
    if signature_name:
        # Suche die Unterschrift im Signature-Verzeichnis neben dem templates-Verzeichnis
        signature_src = template_dir.parent / "Signature" / signature_name
        if signature_src.exists():
            # Kopiere die Unterschrift ins Signature-Unterverzeichnis des Output-Verzeichnisses
            shutil.copy(signature_src, signature_output_dir / signature_name)
        else:
            # Fallback: Suche die Unterschrift direkt im templates-Verzeichnis
            signature_src = template_dir / signature_name
            if signature_src.exists():
                # Kopiere die Unterschrift ins Signature-Unterverzeichnis des Output-Verzeichnisses
                shutil.copy(signature_src, signature_output_dir / signature_name)

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
        except Exception as e:
            print(f"Error during {compiler} compilation: {e}")
            continue
    raise RuntimeError("PDF compilation failed with all engines.")

def print_file(pdf_path: Path):
    """Prints the specified PDF file."""
    try:
        subprocess.run(["lp", str(pdf_path)], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"❌ Fehler beim Drucken von {pdf_path}. 'lp'-Kommando nicht gefunden oder fehlgeschlagen.")
