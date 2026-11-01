import csv
import json

def prioritaet_bestimmen(text):
    text = text.lower()   # Groß-/Kleinschreibung ignorieren
    if "defekt" in text or "geht nicht" in text:
        return "hoch"
    return "normal"

def kategorie_bestimmen(text, standard="Sonstiges"):
    text = text.lower()   # Groß-/Kleinschreibung ignorieren
    if "passwort" in text:
        return "IAM"
    elif "vpn" in text:
        return "Netzwerk"
    return standard

def zaehle_tickets(tickets):
    """Zählt die Tickets pro Priorität und pro Kategorie. Gibt zwei dicts zurück."""
    anzahl_pro_prioritaet = {}
    anzahl_pro_kategorie = {}
    for t in tickets:
        kategorie = kategorie_bestimmen(t["text"])
        prioritaet = prioritaet_bestimmen(t["text"])
        anzahl_pro_prioritaet[prioritaet] = anzahl_pro_prioritaet.get(prioritaet, 0) + 1
        anzahl_pro_kategorie[kategorie] = anzahl_pro_kategorie.get(kategorie, 0) + 1
    return anzahl_pro_prioritaet, anzahl_pro_kategorie

def main():
    tickets = []
    with open("tickets.csv", "r", encoding="utf-8") as f:
        leser = csv.DictReader(f)
        for zeile in leser:
            tickets.append(zeile)

    anzahl_pro_prioritaet, anzahl_pro_kategorie = zaehle_tickets(tickets)

    print("Gesamtanzahl:")
    print(f"  Priorität: {sum(anzahl_pro_prioritaet.values())}")
    print(f"  Kategorie: {sum(anzahl_pro_kategorie.values())}")
    if sum(anzahl_pro_prioritaet.values()) != len(tickets) or sum(anzahl_pro_kategorie.values()) != len(tickets):
        print("Warnung: Die Gesamtanzahl der Tickets pro Priorität und Kategorie stimmt nicht mit der Gesamtanzahl überein!")

    with open("pipeline_auswertung.json", "w", encoding="utf-8") as f:
        json.dump({"anzahl_pro_prioritaet": anzahl_pro_prioritaet, "anzahl_pro_kategorie": anzahl_pro_kategorie}, f, indent=2, ensure_ascii=False)

    print("Anzahl pro Priorität:")
    for p, anzahl in anzahl_pro_prioritaet.items():
        print(f"  {p}: {anzahl}")

    print("Anzahl pro Kategorie:")
    for k, anzahl in anzahl_pro_kategorie.items():
        print(f"  {k}: {anzahl}")

# Nur beim direkten Start ausführen, nicht beim Import als Modul
if __name__ == "__main__":
    main()
