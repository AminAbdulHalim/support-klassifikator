import argparse
import csv
import json
import sys

import ticket_pipeline   # Regeln und Zählung kommen aus der Pipeline, nichts wird kopiert

PFLICHTSPALTEN = ["id", "text"]


def lade_tickets(pfad):
    """Liest die CSV-Datei. Wirft ValueError mit einer Meldung, wenn der Inhalt nicht passt."""
    # utf-8-sig: entfernt ein evtl. vorhandenes BOM, sonst hieße die erste Spalte "﻿id"
    with open(pfad, "r", encoding="utf-8-sig", newline="") as f:
        leser = csv.DictReader(f)
        if leser.fieldnames is None:
            raise ValueError("Die Datei ist leer.")
        fehlende = [s for s in PFLICHTSPALTEN if s not in leser.fieldnames]
        if fehlende:
            raise ValueError("Pflichtspalte(n) fehlen: " + ", ".join(fehlende))
        # "or ''" fängt zu kurze Zeilen ab, bei denen DictReader None liefert
        tickets = [{"id": z["id"] or "", "text": z["text"] or ""} for z in leser]
    if not tickets:
        raise ValueError("Die Datei enthält keine Tickets (nur die Kopfzeile).")
    return tickets


def finde_dubletten(tickets):
    """Gruppiert die ids nach text.lower(). Gibt nur Gruppen mit mehr als einem Ticket zurück."""
    gruppen = {}
    for t in tickets:
        gruppen.setdefault(t["text"].lower(), []).append(t["id"])
    return [{"text": text, "ids": ids} for text, ids in gruppen.items() if len(ids) > 1]


def gib_klartext_aus(ergebnis):
    print(f"Tickets gesamt: {ergebnis['gesamt']}")
    print("Anzahl pro Priorität:")
    for p, anzahl in ergebnis["anzahl_pro_prioritaet"].items():
        print(f"  {p}: {anzahl}")
    print("Anzahl pro Kategorie:")
    for k, anzahl in ergebnis["anzahl_pro_kategorie"].items():
        print(f"  {k}: {anzahl}")
    if ergebnis["dubletten"]:
        print("Dubletten:")
        for d in ergebnis["dubletten"]:
            print(f"  \"{d['text']}\": IDs {', '.join(d['ids'])}")
    else:
        print("Keine Dubletten.")


def main():
    parser = argparse.ArgumentParser(description="Zählt Support-Tickets und findet Dubletten.")
    parser.add_argument("--input", required=True, help="Pfad zur CSV-Datei (Spalten: id, text)")
    parser.add_argument("--json", action="store_true", help="Ausgabe als JSON statt Klartext")
    args = parser.parse_args()

    # Reihenfolge der except-Blöcke: spezifisch vor allgemein, der erste Treffer gewinnt.
    # FileNotFoundError ist eine Unterklasse von OSError -> steht davor.
    # UnicodeDecodeError ist eine Unterklasse von ValueError -> steht davor.
    try:
        tickets = lade_tickets(args.input)
    except FileNotFoundError:
        print(f"Fehler: Datei nicht gefunden: {args.input}", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print(f"Fehler: Datei ist nicht UTF-8-kodiert: {args.input}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Fehler: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"Fehler: Datei nicht lesbar ({e})", file=sys.stderr)
        return 1

    pro_prioritaet, pro_kategorie = ticket_pipeline.zaehle_tickets(tickets)
    ergebnis = {
        "gesamt": len(tickets),
        "anzahl_pro_prioritaet": pro_prioritaet,
        "anzahl_pro_kategorie": pro_kategorie,
        "dubletten": finde_dubletten(tickets),
    }

    if args.json:
        print(json.dumps(ergebnis, indent=2, ensure_ascii=False))
    else:
        gib_klartext_aus(ergebnis)
    return 0


if __name__ == "__main__":
    sys.exit(main())
