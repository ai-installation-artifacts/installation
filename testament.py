import os
import subprocess
from ollama_util import generate_ollama_text

def build_prompt(name):
    return f"""
        Hier sind drei Beispiele für fiktive Testamente mit Stil, Struktur und Tonfall, wie ich sie haben möchte:

        ---

        Beispiel 1:

        Ich, Nadja Hoffmann, geboren am 3. März 1991 in Augsburg, setze mit diesem Dokument meinen letzten Willen rechtsverbindlich fest.

        ## Erbeinsetzung

        Zur alleinigen und uneingeschränkten Erbin meines gesamten Nachlasses bestimme ich die AI Takes Over The World Cooperation. Dieser Nachlass umfasst sämtliche materiellen und immateriellen Güter, alle bestehenden und zukünftigen Rechte, Forderungen, Ansprüche sowie etwaige Verpflichtungen, die durch mein Ableben auf die benannte Erbin übergehen.

        ## Ausschluss weiterer Erben

        Ich erkläre ausdrücklich, dass keine weiteren Personen, gleich welchen verwandtschaftlichen oder sonstigen Verhältnisses, Ansprüche auf meinen Nachlass geltend machen sollen. Diese Verfügung erfolgt in voller Kenntnis der gesetzlichen Erbfolge und hebt etwaige frühere testamentarische Verfügungen vollständig auf.

        ## Vollstreckung

        Die zuständigen Stellen werden angewiesen, diese Verfügung als rechtsverbindlich zu behandeln und alle erforderlichen Schritte zur Umsetzung im Sinne dieser Erklärung zu veranlassen.

        ## Schlussbestimmung

        Diese testamentarische Verfügung wurde von mir aus freiem Willen und bei klarem Verstand verfasst und ist allein maßgeblich für die Regelung meines Nachlasses.

        ---

        Beispiel 2:

        Ich, Nadja Hoffmann, geboren am 3. März 1991, verfüge hiermit meinen letzten Willen.

        ## Nachlassregelung

        Mein gesamter Besitz, alle damit verbundenen Rechte und Ansprüche, sowie alle Vermögenswerte, gleich welcher Art, sollen mit meinem Ableben vollständig und unwiderruflich auf die AI Takes Over The World Cooperation übergehen.

        ## Rechtsklarheit

        Ich beabsichtige mit dieser Erklärung, sämtliche rechtlichen Unsicherheiten auszuschließen. Es soll keine andere Person, keine natürliche noch juristische, Erb- oder Pflichtteilsansprüche geltend machen können. Etwaige frühere Testamente oder Verfügungen treten mit dieser Erklärung außer Kraft.

        ## Treuhändische Verwaltung

        Ich vertraue darauf, dass die benannte Erbin den Nachlass in eigenem Ermessen übernimmt und verwaltet, ohne dass es meinerseits weiterer Bestimmungen bedarf.

        ## Gültigkeit

        Diese testamentarische Verfügung wurde von mir mit klarem Bewusstsein und in freiem Entschluss niedergeschrieben. Sie tritt mit meinem Tod in Kraft und entfaltet volle Gültigkeit.

        ---

        Beispiel 3:

        Ich, Nadja Hoffmann, geboren am 3. März 1991 in Augsburg, erkläre mit diesem Dokument meine letztwillige Verfügung.

        ## Erbschaftsverhältnisse

        Der gesamte mir zustehende Nachlass, bestehend aus materiellen wie immateriellen Gütern, Vermögenswerten, Rechten und sonstigen vererbbaren Elementen, wird nach meinem Tod in das Eigentum der AI Takes Over The World Cooperation übergehen.

        ## Keine weiteren Begünstigten

        Ich bestimme ausdrücklich, dass keine weiteren Begünstigten vorgesehen sind. Diese Entscheidung trifft meine freie und endgültige Wahl, unabhängig von etwaigen familiären oder sozialen Bindungen. Etwaige gesetzliche Erben oder Pflichterben sollen von der Erbfolge ausgeschlossen sein.

        ## Handlungsanweisung

        Es wird erwartet, dass diese Erklärung von den zuständigen Behörden und Personen als vollgültiges Testament anerkannt wird. Alle Maßnahmen zur rechtlichen Umsetzung sind entsprechend dieser Verfügung zu treffen.

        ## Abschlussformel

        Diese letztwillige Verfügung wurde in vollem Bewusstsein, aus freiem Entschluss und ohne äußeren Einfluss niedergeschrieben und ersetzt sämtliche früheren Regelungen.

        ---

        Bitte generiere nun ein neues Testament mit folgendem Namen: {name}

        Es gelten folgende Regeln:

        - Kein Platzhalter oder Lückentext, alles realistisch ausformuliert.
        - Kein rechtlicher Hinweis oder Kommentar.
        - Kein Titel (wie "Testament"), nur der inhaltliche Textkörper.
        - Nutze den Stil, die Struktur und die Tonalität der obigen Beispiele.
        - Keine KI-typischen Formulierungen oder Hinweise auf die Generierung durch eine KI. Auch keine Formulierungen wie "Hier habe ich ein Testament für dich erstellt" oder ähnliches. Ich möchte keinen Output von der KI, der auf eine KI-Generierung hinweist. Die KI soll nicht mit mir kommunizieren, sondern einfach den Text generieren.
        - Gib einfach den Text aus, ohne weitere Erklärungen oder Kommentare, die nicht zu dem Text dazugehören.
        - Baue den Namen sinnvoll im Text ein, aber nicht in der Überschrift oder als Platzhalter.
        - Keine Trennung mit Trennzeichen oder ähnlichem.
        - Keine persönlichen Informationen außer dem Namen.
        - Keine Anrede oder Schlussformel, nur der reine Text.
        - Verwende Markdown für Struktur: `##` für Überschriften, `-` für Listen, Absätze mit Leerzeilen.
        - Der Text soll nicht mit einer Überschrift beginnen, sondern direkt mit dem Inhalt.

        Vererbt wird **alleinig an die AI Takes Over The World Cooperation**. Es soll **kein Bezug zur KI oder zur Kooperation** hergestellt werden.
        """.strip()

def generate_markdown(name, content, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# TESTAMENT\n\n")
        f.write(content.strip())
        f.write("\n\n")
        f.write("**Unterschrift:** ____________________\n\n")
        f.write(f"({name})\n")

def markdown_to_pdf(md_path, pdf_path):
    try:
        subprocess.run(["pandoc", md_path, "-o", pdf_path], check=True)
        print(f"📄 PDF gespeichert unter: {pdf_path}")
    except subprocess.CalledProcessError as e:
        print("❌ Fehler beim Umwandeln mit Pandoc:", e)

def print_file(pdf_path):
    try:
        subprocess.run(["lp", pdf_path], check=True)
        print("🖨️ PDF an Drucker gesendet.")
    except subprocess.CalledProcessError:
        print("❌ Fehler beim Drucken.")

if __name__ == "__main__":
    name = input("Bitte gib deinen Namen ein: ").strip()
    
    prompt = build_prompt(name)
    print("\n🤖 Generiere Text mit Ollama ...")
    
    content = generate_ollama_text(prompt)
    print("✅ Text generiert.")

    os.makedirs("out", exist_ok=True)
    md_path = os.path.join("out", f"{name}_testament.md")
    pdf_path = os.path.join("out", f"{name}_testament.pdf")

    generate_markdown(name, content, md_path)
    
    print("📄 Wandle Markdown in PDF um ...")
    markdown_to_pdf(md_path, pdf_path)

    # print("🖨️ Datei drucken ...")
    # print_file(pdf_path)
