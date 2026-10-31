# Support-Klassifikator

Dieses Lernprojekt demonstriert die automatische Klassifizierung von Support-E-Mails über die Claude API inklusive strukturierter JSON-Ausgabe, automatischer Datenvalidierung und genauer Kostenkontrolle – in zwei Testläufen wurden 22 von 23 selbst erfundenen Testmails korrekt zugeordnet, bei Gesamtkosten von unter einem Cent pro Durchlauf. Das Repository dient als praxisnaher Portfolio-Prototyp für Recruiter und Fachleute, um zu zeigen, wie KI-Funktionen und API-Schnittstellen zuverlässig, strukturiert und kosteneffizient in eigene Anwendungen integriert werden.

## Architektur

(folgt)

## Setup

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

(folgt)

## Grenzen und bekannte Fehler

(folgt)

## Was ich anders machen würde

(folgt)