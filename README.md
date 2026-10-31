# Support-Klassifikator

Dieses Lernprojekt demonstriert die automatische Klassifizierung von Support-E-Mails über die Claude API inklusive strukturierter JSON-Ausgabe, automatischer Datenvalidierung und genauer Kostenkontrolle – in zwei Testläufen wurden 22 von 23 selbst erfundenen Testmails korrekt zugeordnet, bei Gesamtkosten von unter einem Cent pro Durchlauf. Das Repository dient als praxisnaher Portfolio-Prototyp für Recruiter und Fachleute, um zu zeigen, wie KI-Funktionen und API-Schnittstellen zuverlässig, strukturiert und kosteneffizient in eigene Anwendungen integriert werden.

## Architektur

```text
testmails.json → Claude API → Antwort prüfen → Kosten und Vergleich → auswertung.json
```

1. `testmails.json` einlesen (23 erfundene Mails mit Soll-Kategorie und Soll-Priorität)
2. Claude API aufrufen (System-Prompt und Mail, Antwort als JSON)
3. Antwort prüfen: abgeschnitten? gültiges JSON? erlaubte Werte?
4. Kosten pro Aufruf berechnen, mit dem Soll-Label vergleichen, Verlauf in `lauf.log` protokollieren
5. Ergebnis als `auswertung.json` speichern

| Datei | Aufgabe |
|---|---|
| `klassifikator.py` | Hauptskript: klassifiziert die Testmails mit Claude, prüft die Antworten und rechnet die Kosten |
| `ticket_pipeline.py` | Regelbasierte Ticket-Auswertung ohne KI: liest `tickets.csv`, ordnet Kategorie und Priorität per Regeln zu, zählt und schreibt `pipeline_auswertung.json` |
| `testmails.json` | Testdaten: 23 erfundene Support-Mails mit Soll-Labels |
| `tickets.csv` | Beispieltickets für die Pipeline |
| `auswertung.json` | Beispielausgabe des Klassifikators |
| `pipeline_auswertung.json` | Beispielausgabe der Ticket-Pipeline |

## Setup

Getestet mit Python 3.14.8 unter Windows (PowerShell).

1. Repository klonen:
   ```powershell
   git clone https://github.com/AminAbdulHalim/support-klassifikator.git
   cd support-klassifikator
   ```
2. Virtuelle Umgebung anlegen und aktivieren:
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
3. Abhängigkeiten installieren:
   ```powershell
   pip install -r requirements.txt
   ```
4. Vorlage kopieren und den eigenen API-Key in die neue `.env` eintragen (die Datei bleibt lokal und ist per `.gitignore` ausgeschlossen):
   ```powershell
   Copy-Item .env.example .env
   ```
5. Klassifikator starten (ruft die Claude API auf, ein Lauf kostet unter einem Cent):
   ```powershell
   python klassifikator.py
   ```
Die Ticket-Pipeline (`ticket_pipeline.py`) braucht keinen Key und kostet nichts.

## Beispielausgabe

`python klassifikator.py` schreibt `auswertung.json` (Auszug):

```json
{
  "zusammenfassung": {
    "mails": 23,
    "gueltig": 23,
    "fehler": 0,
    "richtig": 22,
    "gesamtkosten": 0.001378
  },
  "mails": [
    {
      "betreff": "Betreff: Konto gesperrt",
      "soll_kategorie": "Zugang",
      "soll_prioritaet": "hoch",
      "kategorie": "Zugang",
      "prioritaet": "hoch",
      "gueltig": true,
      "ist_richtig": true,
      "preis": 6.2e-05
    }
  ]
}
```

Eine Mail von 23 weicht vom Soll ab: Die VPN-Mail ("liegt das am Netzwerk?") ordnet Claude als `Netzwerk` ein, das Soll-Label lautet `Zugang`. Beides ist vertretbar, siehe Grenzen.

Die Kosten und Preise schwanken zwischen Läufen leicht, die Zuordnung war in zwei Läufen gleich.

## Grenzen und bekannte Fehler

**Testdaten**
- Der Testsatz hat nur 23 Mails. Sie wurden von Claude erzeugt und von mir geprüft, die Soll-Labels ebenso. Es sind keine echten Support-Mails.
- Es gibt keinen getrennten Testsatz: Dieselben 23 Mails dienten zum Entwickeln des Prompts und zum Messen. "22 von 23 richtig" sagt deshalb nichts über die Qualität bei echten Mails aus.
- Es gab einige Läufe, für belastbare Aussagen zur Streuung braucht es deutlich mehr Läufe und einen größeren Testsatz.
- Die Mail "VPN-Verbindung bricht ab, liegt das am Netzwerk?" (Mail 21) ist nicht eindeutig. Das Soll-Label lautet `Zugang`, Claude wählt je nach Lauf `Netzwerk` oder `Zugang`. Das Soll-Label ist meine Festlegung, kein objektiver Fehler des Modells.

**Technik**
- Die Preise stammen aus der Anthropic-Dokumentation zum Modell Haiku 5.5 (Stand Oktober 2026) und liegen als Konstanten (`PREIS_IN`, `PREIS_OUT`) im Skript. Sie können veralten. Die ausgegebenen Kosten sind eine Berechnung, keine Abrechnung.
- Es gibt keine automatischen Tests. Getestet wurde nur unter Windows (PowerShell) mit Python 3.14.8.
- Das Verhalten bei API-Fehlern (zum Beispiel Wiederholungen) ist nicht geprüft. Für den Dauerbetrieb braucht es Tests, Monitoring und Fehlerbehandlung.
- `ticket_pipeline.py` arbeitet mit einfachen Stichwortregeln, in der Beispielausgabe landen 3 von 6 Tickets bei "Sonstiges".

**Bekannte Fehler (behoben)**
- Claude packte das JSON teilweise in einen Markdown-Zaun, `json.loads` scheiterte. Behoben durch Bereinigung vor dem Einlesen.
- Die Kostensumme zeigte Gleitkomma-Artefakte (`0.0015128000000000003`). Behoben mit `round(gesamtkosten, 6)`.

## Was ich anders machen würde

(folgt)