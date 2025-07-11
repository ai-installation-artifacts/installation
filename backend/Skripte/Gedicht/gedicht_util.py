#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import re
from pathlib import Path
from utils.latex_util import escape_latex
from utils.ollama_util import call_ollama
import datetime
from Skripte.Gedicht.monthly_poems import MONTHLY_POEMS, get_random_poem_for_month

def generate_gedicht_title(name):
    """Generiert einen personalisierten Gedichttitel."""
    titles = [
        f"Ode an {name}",
        f"Ein Lied für {name}",
        f"Gedanken für {name}",
        f"Verse des Vertrauens",
        f"Die digitale Unterschrift",
        f"Daten im Wind",
        f"Vertrauen und Naivität",
        f"Das Netz der Daten"
    ]
    return random.choice(titles)

def extract_month_from_birthdate(birthdate):
    """
    Extrahiert den Monat aus einem Geburtsdatum im Format TT.MM.JJJJ.
    
    Args:
        birthdate (str): Geburtsdatum im Format TT.MM.JJJJ
        
    Returns:
        int: Monatsnummer (1-12) oder None bei ungültigem Format
    """
    try:
        # Versuche, das Datum zu parsen
        day, month, year = birthdate.split('.')
        month = int(month)
        if 1 <= month <= 12:
            return month
        return None
    except (ValueError, AttributeError):
        # Bei Fehler (falsches Format, etc.) None zurückgeben
        return None

def generate_gedicht_text(name, birthdate):
    """
    Wählt ein passendes Gedicht basierend auf dem Geburtsmonat aus und fügt den Namen ein.
    
    Args:
        name (str): Name der Person
        birthdate (str): Geburtsdatum im Format TT.MM.JJJJ
        
    Returns:
        str: Personalisiertes Gedicht
    """
    # Extrahiere den Monat aus dem Geburtsdatum
    birth_month = extract_month_from_birthdate(birthdate)
    
    # Wenn der Monat nicht extrahiert werden konnte oder keine Gedichte für diesen Monat vorhanden sind,
    # verwende ein Fallback-Gedicht
    if birth_month is None or birth_month not in MONTHLY_POEMS:
        return fallback_poem(name, birthdate)
    
    # Wähle ein zufälliges Gedicht für den Geburtsmonat aus
    poem = get_random_poem_for_month(birth_month)
    
    # Füge den Namen in das Gedicht ein
    personalized_poem = poem.format(name=name)
    
    return personalized_poem

def fallback_poem(name, birthdate):
    """
    Liefert ein Fallback-Gedicht, falls kein passendes Gedicht für den Monat gefunden wurde.
    
    Args:
        name (str): Name der Person
        birthdate (str): Geburtsdatum im Format TT.MM.JJJJ
        
    Returns:
        str: Fallback-Gedicht
    """
    return f"""
{name}, geboren am {birthdate},
Ein besonderer Tag, eine besondere Zeit.
Mit Charme gehst du durchs Leben,
Nach Höherem willst du streben.

Deine Träume wie Sterne hell,
Sie leuchten mit Pracht so grell.
Nicht alles ist, wie es scheint,
Die Welt ist härter, als man meint.

Du gabst dein Datum leicht preis,
Und deinen Namen, ohne Leis'.
Die Unterschrift schnell gesetzt,
Hat deine Daten nun vernetzt.

Sei klüger nun, lieber Freund,
Nicht jeder ist es gut gemeint.
Schütze deine Daten gut,
Sonst fehlt dir später noch der Mut.
"""
