import sys
import argparse
import datetime
from pathlib import Path
import re

# Add project root to sys.path to allow imports from utils
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.latex_util import (
    load_template,         # Korrigiert
    build_latex,           # Korrigiert
    save_latex,            # Korrigiert
    compile_pdf,           # Korrigiert
    print_file,            # Korrigiert
    escape_latex
)
from utils.ollama_util import call_ollama # Korrigierter Import
from Skripte.Kuendigung.kuendigung_util import (
    prepare_kuendigung_prompt_spitz, # Angepasst an neue Logik
    extract_invented_details_and_text, # Angepasst an neue Logik
    LATEX_PLACEHOLDERS, # Importiert für die Verwendung der Platzhalter-Definitionen
    OLLAMA_OUTPUT_TAGS # Importiert für die Schlüssel der extrahierten Details
)

DEFAULT_TEMPLATE_PATH = project_root / "templates" / "Kündigung_template.tex" # Ensure this filename is correct
DEFAULT_OUTPUT_DIR = project_root / "out"

def main():
    parser = argparse.ArgumentParser(description="Generiert ein satirisches Kündigungsschreiben.")
    # parser.add_argument("--sender_name", required=True, help="Ihr vollständiger Name (aus dessen Sicht gekündigt wird).")
    # parser.add_argument("--sender_birthdate", required=True, help="Ihr Geburtsdatum (TT.MM.JJJJ).")
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE_PATH), help="Pfad zur LaTeX-Vorlage.")
    parser.add_argument("--output_dir", default=str(DEFAULT_OUTPUT_DIR), help="Verzeichnis für die Ausgabe-PDFs.")
    parser.add_argument("--no_print", action="store_true", help="PDF nach Erstellung nicht drucken.")

    args = parser.parse_args()

    # Interaktive Abfrage für Name und Geburtsdatum
    sender_name = input("Name: ")
    sender_birthdate = input("Geburtsdatum: ")

    if not sender_name or not sender_birthdate:
        print("Fehler: Name und Geburtsdatum dürfen nicht leer sein.")
        return

    print(f"Absender: {sender_name}, Geboren am: {sender_birthdate}")
    print(f"Ziel: Glorreiche AI Takes Over The World Cooperation!")

    # Stelle sicher, dass das Ausgabeverzeichnis existiert
    output_dir_path = Path(args.output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    # 1. Prompt vorbereiten
    prompt = prepare_kuendigung_prompt_spitz(
        sender_name=sender_name, # Verwendung der interaktiv abgefragten Variable
        sender_birthdate=sender_birthdate # Verwendung der interaktiv abgefragten Variable
    )

    # 2. Ollama API aufrufen
    print("💬 Generiere Kündigungstext und erfinde Details ...")
    
    # Versuche verschiedene Modelle, falls eines nicht funktioniert
    models_to_try = ["llama3.2", "llama3", "llama2", "mistral"]
    generated_text_from_ollama = None
    
    for model in models_to_try:
        print(f"Versuche Modell: {model}...")
        generated_text_from_ollama = call_ollama(prompt, model=model)
        if generated_text_from_ollama and "kann nicht" not in generated_text_from_ollama.lower() and "cannot" not in generated_text_from_ollama.lower():
            print(f"✅ Erfolgreich mit Modell: {model}")
            break
        else:
            print(f"❌ Modell {model} hat verweigert oder keine Antwort geliefert.")
    
    if not generated_text_from_ollama:
        print("Fehler: Konnte keinen Text von Ollama erhalten.")
        return
        
    # Debug: Zeige die vollständige Antwort von Ollama
    print("\n--- Debug: Vollständige Antwort von Ollama ---")
    print(generated_text_from_ollama)
    print("--- Ende der Debug-Ausgabe ---\n")

    # 3. Erfundene Details und Text extrahieren
    invented_data = extract_invented_details_and_text(generated_text_from_ollama)
    
    # Debug-Ausgabe der extrahierten Daten
    print("\n--- Extrahierte/Erfundene Daten ---")
    for key, value in invented_data.items():
        print(f"{key}: {value}")
    print("---------------------------------\n")


    # 4. LaTeX-Template laden
    latex_template_content = load_template(Path(args.template)) # Korrigierter Funktionsaufruf
    if not latex_template_content:
        # load_template wirft FileNotFoundError, wenn Datei nicht existiert,
        # daher ist diese Prüfung hier eigentlich redundant, aber schadet nicht.
        print(f"Fehler: Konnte LaTeX-Vorlage nicht laden von {args.template}")
        return

    # 5. Platzhalter für LaTeX füllen
    # Die Namen der Schlüssel in 'invented_data' entsprechen den OLLAMA_OUTPUT_TAGS keys.
    # Wir mappen diese auf die LATEX_PLACEHOLDERS.
    
    # Der Kündigungstext von Ollama enthält bereits die Anrede und die Grußformel.
    # Der SALUTATION_PLACEHOLDER im Template wird daher nicht separat gefüllt,
    # sondern ist Teil des KUENDIGUNGSTEXT_PLACEHOLDER Inhalts.
    
    # Extrahiere die Anrede aus dem Kündigungstext, falls vorhanden
    kuendigungstext = invented_data.get('KUENDIGUNGSTEXT_CONTENT', "")
    salutation = ""
    
    # Versuche, die Anrede aus dem Kündigungstext zu extrahieren
    anrede_match = re.search(r'^(Sehr geehrte[^,\n]+),', kuendigungstext)
    if anrede_match:
        salutation = anrede_match.group(1)
        # Entferne die Anrede aus dem Kündigungstext, da sie separat im Template erscheint
        kuendigungstext = kuendigungstext.replace(anrede_match.group(0), "").strip()
    else:
        salutation = "Sehr geehrte Damen und Herren"
    
    replacements_for_latex = {
        LATEX_PLACEHOLDERS['SENDER_NAME']: escape_latex(sender_name), # Verwendung der interaktiv abgefragten Variable
        LATEX_PLACEHOLDERS['SENDER_ADDRESS_LINE1']: invented_data.get('INV_SENDER_ADDRESS1', "Fehlerhafte Adresse Zeile 1"),
        LATEX_PLACEHOLDERS['SENDER_ADDRESS_LINE2']: invented_data.get('INV_SENDER_ADDRESS2', "Fehlerhafte Adresse Zeile 2"),
        LATEX_PLACEHOLDERS['SALUTATION']: salutation, # Extrahierte Anrede
        LATEX_PLACEHOLDERS['KUENDIGUNGSTEXT']: kuendigungstext # Kündigungstext ohne Anrede
    }
    
    # 6. LaTeX-Inhalt erstellen
    final_latex_content = build_latex(latex_template_content, replacements_for_latex) # Korrigierter Funktionsaufruf

    # 7. Dateinamen vorbereiten
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_sender_name = "".join(c if c.isalnum() else "_" for c in sender_name) # Verwendung der interaktiv abgefragten Variable
    # Erfundener Firmenname für den Dateinamen verwenden
    safe_firma_name = "".join(c if c.isalnum() else "_" for c in invented_data.get('INV_RECIPIENT_COMPANY', "UnbekannteFirma"))
    base_filename = f"{safe_sender_name}_Kuendigung_AI_Coop_{safe_firma_name}_{timestamp}"
    
    latex_file_path = output_dir_path / f"{base_filename}.tex"
    pdf_file_path = output_dir_path / f"{base_filename}.pdf"

    # 8. LaTeX-Datei speichern
    # save_latex gibt jetzt den Pfad zurück, die if-Bedingung ist nicht mehr nötig für den Rückgabewert.
    saved_tex_path = save_latex(final_latex_content, output_dir_path, base_filename) # Korrigierter Funktionsaufruf
    print(f"🔤 LaTeX-Datei gespeichert unter {saved_tex_path}")
    
    # 9. Zu PDF kompilieren
    # compile_pdf benötigt template_dir nicht mehr unbedingt, wenn kein Logo kopiert wird.
    # Wir übergeben None statt des Template-Verzeichnisses, um zu verhindern, dass das Template selbst kompiliert wird
    try:
        compiled_pdf_path = compile_pdf(saved_tex_path, None) # Kein Template-Verzeichnis übergeben
        print(f"📄 PDF erfolgreich erstellt: {compiled_pdf_path}")
        # 10. Drucken (optional)
        if not args.no_print:
            print_file(compiled_pdf_path) # Korrigierter Funktionsaufruf
        else:
            print("🚫 Drucken übersprungen.")
    except RuntimeError as e:
        print(f"Fehler beim Kompilieren von LaTeX zu PDF für {saved_tex_path}: {e}")
    except FileNotFoundError as e: # Falls z.B. pdflatex nicht gefunden wird
        print(f"Fehler bei der PDF-Erstellung: {e}")


if __name__ == "__main__":
    main()