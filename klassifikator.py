import json
from dotenv import load_dotenv
import anthropic
from datetime import datetime

load_dotenv()
client = anthropic.Anthropic()

def logge(nachricht):
    """Hängt eine Zeile mit Zeitstempel an lauf.log an."""
    zeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("lauf.log", "a", encoding="utf-8") as f:
        f.write(f"{zeit} | {nachricht}\n")

PREIS_IN = 0.10   # Preis pro Million Input-Tokens in Dollar
PREIS_OUT = 0.50  # Preis pro Million Output-Tokens in Dollar

def kosten(input_tokens, output_tokens, preis_in, preis_out):
    """Berechnet die Kosten in Dollar für die Anfrage an die Claude API."""
    return (input_tokens * preis_in + output_tokens * preis_out) / 1000000

SYSTEM = """Du klassifizierst eingehende E-Mails für einen IT-Support.
Antworte NUR mit einem JSON-Objekt, ohne Text davor oder danach, mit genau diesen Schlüsseln:
- "kategorie": eine von "Zugang", "Hardware", "Netzwerk", "Sonstiges"
- "prioritaet": "hoch" oder "normal"
- "zusammenfassung": ein Satz, maximal 15 Wörter"""

with open("testmails.json", encoding="utf-8") as f:   # utf-8, damit Umlaute stimmen
    testdaten = json.load(f)                           # Datei -> Python-Liste

ERLAUBTE_KATEGORIEN = ["Zugang", "Hardware", "Netzwerk", "Sonstiges"]
ERLAUBTE_PRIORITAETEN = ["hoch", "normal"]
PFLICHTSCHLUESSEL = ["kategorie", "prioritaet", "zusammenfassung"]


def klassifiziere(mail):
    """Schickt eine Mail an Claude. Gibt ein geprüftes dict zurück oder None."""
    try:
        antwort = client.messages.create(
            model="claude-haiku-5-5",
            max_tokens=300,
            thinking={"type": "disabled"},
            system=SYSTEM,
            messages=[{"role": "user", "content": mail}],
        )
    except anthropic.AuthenticationError as e:
        print("Key ungültig, Statuscode:", e.status_code)
        logge(f"Key ungültig, Statuscode: {e.status_code}")
        return None, 0
    except anthropic.APIConnectionError:
        print("Keine Verbindung zur API.")
        logge("Keine Verbindung zur API.")
        return None, 0
    except anthropic.APIStatusError as e:
        print("Sonstiger API-Fehler, Statuscode:", e.status_code)
        logge(f"Sonstiger API-Fehler, Statuscode: {e.status_code}")
        return None, 0

    preis = kosten(antwort.usage.input_tokens, antwort.usage.output_tokens, PREIS_IN, PREIS_OUT)
    print(f"Kosten für diese Anfrage: {preis:.6f} Dollar")
    print("Output-Tokens:", antwort.usage.output_tokens, "| stop_reason:", antwort.stop_reason)

    betreff = mail.split("\n")[0] if "\n" in mail else mail[:30]  # Betreff oder Anfang der Mail


    text = ""
    for block in antwort.content:        # alle Blöcke der Antwort durchgehen
        if block.type == "text":         # nur den Textblock nehmen
            text = block.text
            
    # Fehlerfall 1: abgeschnitten
    if antwort.stop_reason == "max_tokens":
        print("Abgeschnitten, Ergebnis wird nicht verarbeitet.")
        logge(f"{betreff} | Abgeschnitten, Ergebnis wird nicht verarbeitet.")
        return None, preis                                   # <- NEU: sonst läuft der Code weiter

    # Fehlerfall 2: kein gültiges JSON
    text = text.replace("```json", "").replace("```", "").strip()
    try:
        daten = json.loads(text)
    except json.JSONDecodeError:
        print("Kein gültiges JSON.")
        print("Rohtext:", repr(text))      # <- NEU
        logge(f"{betreff} | Kein gültiges JSON. | Rohtext: {repr(text)}")
        return None, preis

    # Fehlerfall 3: Form und Werte prüfen
    if not isinstance(daten, dict):                   # <- NEU: gültiges JSON, aber z. B. eine Liste
        print("JSON ist kein Objekt.")
        logge(f"{betreff} | JSON ist kein Objekt.")
        return None, preis
    if not all(k in daten for k in PFLICHTSCHLUESSEL):
        print("Fehlende Schlüssel im JSON.")
        logge(f"{betreff} | Fehlende Schlüssel im JSON.")
        return None, preis
    if daten["kategorie"] not in ERLAUBTE_KATEGORIEN:
        print("Ungültige Kategorie:", daten["kategorie"])
        logge(f"{betreff} | Ungültige Kategorie: {daten['kategorie']}")
        return None, preis
    if daten["prioritaet"] not in ERLAUBTE_PRIORITAETEN:
        print("Ungültige Priorität:", daten["prioritaet"])
        logge(f"{betreff} | Ungültige Priorität: {daten['prioritaet']}")
        return None, preis

    return daten, preis

gesamtkosten = 0
auswertung = []
gueltig = []
richtig = 0
fehler = 0
for eintrag in testdaten:
    kategorie = None
    prioritaet = None
    ist_richtig = False
    ergebnis, preis = klassifiziere(eintrag["mail"])
    gesamtkosten += preis
    if ergebnis is None:
        fehler += 1
    else:
        gueltig.append(ergebnis)
        kategorie = ergebnis["kategorie"]
        prioritaet = ergebnis["prioritaet"]
        ist_richtig = (kategorie == eintrag["soll_kategorie"] and prioritaet == eintrag["soll_prioritaet"])
        if ist_richtig:
            richtig += 1
        print(kategorie, "|", prioritaet, "|", ergebnis["zusammenfassung"])

    auswertung.append({
        "betreff": eintrag["mail"].split("\n")[0] if "\n" in eintrag["mail"] else eintrag["mail"][:30],
        "soll_kategorie": eintrag["soll_kategorie"],
        "soll_prioritaet": eintrag["soll_prioritaet"],
        "kategorie": kategorie,
        "prioritaet": prioritaet,
        "gueltig": ergebnis is not None,
        "ist_richtig": ist_richtig,
        "preis": round(preis, 6),
    })

ausgabe = {
    "zusammenfassung": {
        "mails": len(testdaten),
        "gueltig": len(gueltig),
        "fehler": fehler,
        "richtig": richtig,
        "gesamtkosten": round(gesamtkosten, 6)
    },
    "mails": auswertung
}
with open("auswertung.json", "w", encoding="utf-8") as f:
    json.dump(ausgabe, f, indent=2, ensure_ascii=False)


print(f"Gültig: {len(gueltig)}, Fehler: {fehler}, Richtig: {richtig} von {len(testdaten)}")
logge(f"Lauf beendet - Gültig: {len(gueltig)}, Fehler: {fehler}, Richtig: {richtig} von {len(testdaten)} Gesamtkosten: ${gesamtkosten:.6f}")
print(f"Gesamtkosten: ${gesamtkosten:.6f}")

# Zählprobe: NEU, wie in Woche 1
if len(gueltig) + fehler != len(testdaten):
    print("Warnung: Zählprobe stimmt nicht!")
else:
    print("Zählprobe OK.")