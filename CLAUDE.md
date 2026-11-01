# CLAUDE.md

Diese Datei gibt Claude Code (claude.ai/code) Orientierung für die Arbeit in diesem Repository.

## Überblick

Deutschsprachiges Lernprojekt: Support-Mails werden mit der Claude API klassifiziert (`klassifikator.py`). Daneben gibt es eine unabhängige, regelbasierte Ticket-Auswertung ohne KI (`ticket_pipeline.py`). Kommentare, Variablennamen, Ausgaben und Doku sind auf Deutsch – diese Konvention beibehalten.

## Regeln

- Testdaten sind ausschließlich erfunden, keine echten Mails oder Personendaten.
- Änderungen laufen über einen Feature-Branch und einen Pull Request, nicht direkt auf `main`.
- Erlaubt sind die Standardbibliothek und die zwei Pakete aus `requirements.txt`; neue Abhängigkeiten nur nach Absprache.

## Befehle

Windows / PowerShell, Python 3.14 mit virtueller Umgebung `.venv`:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt     # anthropic, python-dotenv (Versionen gepinnt)
python klassifikator.py             # ruft die Claude API auf (kostet < 1 Cent), schreibt auswertung.json und lauf.log
python ticket_pipeline.py           # kein Key nötig, liest tickets.csv, schreibt pipeline_auswertung.json
python ticket_cli.py --input tickets.csv [--json]   # zählt Tickets und findet Dubletten, schreibt keine Datei
```

- Es gibt keine Tests, keinen Linter und keinen Build.
- `klassifikator.py` und `ticket_pipeline.py` lesen/schreiben feste Dateinamen relativ zum aktuellen Ordner und müssen daher aus dem Projektroot gestartet werden. Bei `ticket_cli.py` bezieht sich ein relativer Pfad in `--input` ebenfalls auf den Ordner, in dem der Befehl gestartet wird.
- Der API-Key kommt aus `.env` (über `load_dotenv()`); die Vorlage ist `.env.example`. `.env` nie anfassen.

## Architektur

Zwei voneinander unabhängige Teile: `klassifikator.py` (mit KI) und `ticket_pipeline.py` samt `ticket_cli.py` (ohne KI). `klassifikator.py` hat keinen `if __name__ == "__main__"`-Schutz: Der Ablauf steht auf Modulebene, ein Import führt das Skript also sofort aus (inkl. API-Aufrufen). `ticket_pipeline.py` und `ticket_cli.py` sind mit dem Schutz importierbar.

**`klassifikator.py`** – Ablauf: `testmails.json` → `klassifiziere()` pro Mail → Vergleich mit Soll-Labels → `auswertung.json`.
- `klassifiziere(mail)` gibt immer ein Tupel `(daten_oder_None, preis)` zurück. Bei `None` zählt die Mail als Fehler, die Kosten werden trotzdem summiert (bei API-Fehlern ist der Preis `0`).
- Die Antwortprüfung läuft in fester Reihenfolge: API-Exceptions → `stop_reason == "max_tokens"` → Markdown-Zaun entfernen und `json.loads` → Objekt/Pflichtschlüssel → erlaubte Werte für Kategorie und Priorität. Jeder Fehlerfall wird per `print` und `logge()` (Anhängen an `lauf.log`) gemeldet.
- Erlaubte Werte stehen doppelt: im `SYSTEM`-Prompt (Text) und in `ERLAUBTE_KATEGORIEN` / `ERLAUBTE_PRIORITAETEN` / `PFLICHTSCHLUESSEL` (Validierung). Bei Änderungen beide Stellen synchron halten.
- Kosten: Konstanten `PREIS_IN` / `PREIS_OUT` (Dollar pro Million Tokens) gelten für das Modell `claude-haiku-5-5`; bei Modellwechsel mit anpassen.
- Am Ende prüft eine Zählprobe, dass `gültig + Fehler == Anzahl Mails`.

**`ticket_pipeline.py`** – Die Regel-Funktionen `prioritaet_bestimmen` / `kategorie_bestimmen` (Stichwortregeln, Groß-/Kleinschreibung wird per `.lower()` ignoriert) und `zaehle_tickets` stehen auf Modulebene und werden vom CLI importiert. `main()` liest `tickets.csv` (Spalte `text`), zählt und schreibt `pipeline_auswertung.json`. Die Kategorien weichen vom Klassifikator ab (hier `IAM`/`Netzwerk`/`Sonstiges`, dort `Zugang`/`Hardware`/`Netzwerk`/`Sonstiges`).

**`ticket_cli.py`** – argparse-CLI (`--input` Pflicht, `--json` optional) auf beliebigen CSV-Dateien mit den Spalten `id` und `text`. Nutzt `ticket_pipeline.zaehle_tickets`, hat also keine eigene Regel-Logik; ergänzt nur Dubletten-Suche (Gruppierung nach `text.lower()`) und Fehlerbehandlung (Meldung auf stderr, Exit-Code 1; fehlendes `--input` ergibt 2 durch argparse). Bei den `except`-Blöcken in `main()` ist die Reihenfolge wichtig: `UnicodeDecodeError` muss vor `ValueError` stehen, weil es dessen Unterklasse ist.

**Daten:** `testmails.json` enthält Einträge mit den Schlüsseln `mail` (Betreff in der ersten Zeile), `soll_kategorie`, `soll_prioritaet`. `auswertung.json` und `pipeline_auswertung.json` sind eingecheckte Beispielausgaben, die bei jedem Lauf überschrieben werden.

Die README beschreibt bekannte Grenzen (kleiner, nicht getrennter Testsatz; Mail 21 „VPN“ ist mehrdeutig; keine automatischen Tests). Diese Punkte nicht als Fehler im Code „reparieren“, sondern als dokumentierte Einschränkungen behandeln.
