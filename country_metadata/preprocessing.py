"""
preprocessing.py

Methods and constants associated with preprocessing string text.
"""
import re

def preprocess_country_name(name: str) -> str:
    prefixes = [
        "Commonwealth of",
        "Federal Democratic Republic of",
        "Federal Republic of",
        "Federative Republic of",
        "French Republic",
        "Grand Duchy of",
        "Hellenic Republic",
        "Islamic Republic of",
        "Kingdom of",
        "People's Republic of",
        "Plurinational State of",
        "Portuguese Republic",
        "Principality of",
        "Republic of",
        "State of",
        "United Kingdom of",
        "United Mexican States",
        "United States of",
    ]
    suffixes = ["Republic", "Federation", "Confederation", "Darussalam"]

    pattern = r"\b(?:{})\s|\s(?:{})\b".format("|".join(prefixes), "|".join(suffixes))
    return re.sub(pattern, "", name).strip()
