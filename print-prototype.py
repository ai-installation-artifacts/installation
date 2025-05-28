from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import tempfile
import subprocess

def generate_pdf(name, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica", 20)
    c.drawString(72, height - 100, "DOKUMENT")
    
    c.setFont("Helvetica", 14)
    c.drawString(72, height - 150, f"Name: {name}")
    c.drawString(72, height - 180, "Vielen Dank für Ihre Eingabe.")
    c.drawString(72, height - 210, "Ihr Datensatz wurde verarbeitet.")
    
    c.showPage()
    c.save()

def print_file(pdf_path):
    subprocess.run(["lp", pdf_path])

if __name__ == "__main__":
    name = input("Bitte gib deinen Namen ein: ")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        generate_pdf(name, tmp.name)
        print("PDF wurde erzeugt:")
        print(tmp.name)
        print("Sende an Drucker ...")
        print_file(tmp.name)
