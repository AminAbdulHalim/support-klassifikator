# Support-Klassifikator

Dieses Lernprojekt demonstriert die automatische Klassifizierung von Support-E-Mails über die Claude API inklusive strukturierter JSON-Ausgabe, automatischer Datenvalidierung und genauer Kostenkontrolle. Ein Runner vergleicht außerdem Prompt-Varianten auf einem getrennten Messsatz (20 Mails, je 3 Läufe pro Variante). Das Repository dient als praxisnaher Portfolio-Prototyp für Recruiter und Fachleute, um zu zeigen, wie KI-Funktionen und API-Schnittstellen zuverlässig, strukturiert und kosteneffizient in eigene Anwendungen integriert und systematisch bewertet werden können.

## Architektur

```text
testmails.json → Claude API → Antwort prüfen → Kosten und Vergleich → auswertung.json
```

1. `testmails.json` einlesen (23 erfundene Mails mit Soll-Kategorie und Soll-Priorität)
2. Claude API aufrufen (System-Prompt und Mail, Antwort als JSON)
3. Antwort prüfen: abgeschnitten? gültiges JSON? erlaubte Werte?
4. Kosten pro Aufruf berechnen, mit dem Soll-Label vergleichen, Verlauf in `lauf.log` protokollieren
5. Ergebnis als `auswertung.json` speichern

Für den Prompt-Vergleich gibt es eine zweite Kette, in der Prompt, Testdaten und Ausgabedatei als Argumente übergeben werden:

```text
prompts/*.txt + testmails_mess.json → runner.py → ergebnisse/*.json → auswerten.py (pandas)
```

| Datei / Ordner | Aufgabe |
|---|---|
| `klassifikator.py` | Hauptskript: klassifiziert die Testmails mit Claude, prüft die Antworten und rechnet die Kosten |
| `runner.py` | Wie `klassifikator.py`, aber mit Argumenten `--prompt`, `--daten`, `--ausgabe`: ein Lauf mit frei wählbarem Prompt und Datensatz |
| `auswerten.py` | Liest alle Dateien in `ergebnisse/` in eine pandas-Tabelle und wertet Treffer je Variante und Lauf aus, auch getrennt nach Grenzfällen |
| `prompts/` | Die Prompt-Varianten als Textdateien (`prompt_A.txt`, `prompt_B.txt`, `prompt_C.txt`) |
| `ergebnisse/` | Ergebnisdateien der Läufe (`A_lauf1.json` bis `C_lauf3.json`) |
| `testmails.json` | Entwicklungssatz: 23 erfundene Support-Mails mit Soll-Labels |
| `testmails_mess.json` | Messsatz: 20 erfundene Support-Mails mit Soll-Labels, davon 4 als Grenzfälle markiert |
| `labeling_richtlinie.md` | Regeln, nach denen die Soll-Labels des Messsatzes vergeben wurden, inklusive Änderungshistorie |
| `ticket_pipeline.py` | Regelbasierte Ticket-Auswertung ohne KI: liest `tickets.csv`, ordnet Kategorie und Priorität per Regeln zu, zählt und schreibt `pipeline_auswertung.json` |
| `ticket_cli.py` | Kommandozeilen-Tool: zählt Tickets einer beliebigen CSV (Spalten `id`, `text`) und findet Dubletten; nutzt die Regeln aus `ticket_pipeline.py` als Modul |
| `tickets.csv` | Beispieltickets für die Pipeline |
| `auswertung.json` | Beispielausgabe des Klassifikators (Entwicklungssatz) |
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
3. Abhängigkeiten installieren (enthält auch pandas für die Auswertung):
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

Die Ticket-Pipeline (`ticket_pipeline.py`) und das Ticket-CLI (`ticket_cli.py`) brauchen keinen Key und kosten nichts. `auswerten.py` liest nur vorhandene Ergebnisdateien und ruft die API nicht auf.

## Prompt-Vergleich ausführen

Ein einzelner Lauf (ruft die API 20-mal auf, Kosten unter einem Cent):

```powershell
python runner.py --prompt prompts/prompt_A.txt --daten testmails_mess.json --ausgabe ergebnisse/A_lauf1.json
```

Mehrere Läufe je Variante (wie für die Ergebnisse unten verwendet):

```powershell
foreach ($lauf in 1,2,3) { python runner.py --prompt prompts/prompt_B.txt --daten testmails_mess.json --ausgabe "ergebnisse/B_lauf${lauf}.json" }
```

Auswertung aller Dateien in `ergebnisse/`:

```powershell
python auswerten.py
```

Die Dateinamen müssen dem Muster `<Variante>_lauf<Nummer>.json` folgen, sonst kann `auswerten.py` Variante und Lauf nicht auslesen. Ein erneuter Lauf mit gleichem Dateinamen überschreibt das alte Ergebnis.

## Testdaten

Das Projekt nutzt zwei getrennte Datensätze: den Entwicklungssatz (`testmails.json`, 23 Mails), auf dem Prompt A und Prompt B entwickelt wurden, und den Messsatz (`testmails_mess.json`, 20 Mails), der erst nach den Prompts entstanden ist und nur zum Messen dient. Alle Mails sind frei erfunden und enthalten keine Daten eines Arbeitgebers.

- **Entwicklungssatz:** 23 Mails, davon 18 von Claude erzeugt und 5 von mir geschrieben. Die Soll-Labels habe ich geprüft.
- **Messsatz:** 20 Mails, davon 12 von mir geschrieben und 8 von Claude erzeugt (die Mails 13 bis 20 in der Datei). Die Soll-Labels der Claude-Mails habe ich bestätigt. Vier Mails sind als Grenzfälle markiert (`"grenzfall": true`): WLAN im Besprechungsraum, "Wichtig: Zugriff auf Z:\Projekte verweigert", Toner ("Sofortige Hilfe benötigt!") und "VPN-Verbindung klemmt mal wieder" mit defekter Tastatur.
- **Labels:** Die Soll-Labels des Messsatzes richten sich nach `labeling_richtlinie.md`.

## Ergebnisse Prompt-Vergleich

Messung auf dem Messsatz (20 Mails), Modell Haiku 5.5. A und B wurden am 07.11.2026 gemessen, C am 08.11.2026. Als richtig zählt eine Mail, wenn Kategorie **und** Priorität stimmen. Eine Antwort ohne gültiges JSON zählt als falsch.

| Variante | Lauf 1 | Lauf 2 | Lauf 3 | Mittel | Gültige Antworten pro Lauf | Kosten pro Lauf |
|---|---|---|---|---|---|---|
| A: Rolle, Format, erlaubte Werte | 16 | 16 | 16 | 16,0 von 20 (80 %) | 20 | ca. 0,0014 $ |
| B: A plus Kategorie-Definitionen, VPN-Regel, Prioritätsregel | 18 | 19 | 19 | 18,7 von 20 (93 %) | 20 | ca. 0,0025 $ |
| C: B unverändert plus drei Beispiele (Few-Shot) | 17 | 17 | 17 | 17,0 von 20 (85 %) | 18 | ca. 0,0043 $ |

Aufgeteilt nach Grenzfällen (Anteil richtig, über alle drei Läufe):

| Variante | 16 Mails ohne Grenzfall | 4 Grenzfälle |
|---|---|---|
| A | 93,75 % (45 von 48) | 25 % (3 von 12) |
| B | 100 % (48 von 48) | 66,7 % (8 von 12) |
| C | 87,5 % (42 von 48) | 75 % (9 von 12) |

Was die Daten zeigen:

- Prompt B liegt in diesem Test vorn, kostet aber rund 80 % mehr pro Lauf als A, weil der Prompt länger ist.
- Bei den 16 Mails ohne Grenzfall liegt der Abstand zwischen A und B bei 3 von 48 Einstufungen (in Lauf 1 war es die Mail "Kein Netz, keine Anmeldung" bei A). Das ist ein Hinweis, kein Beleg.
- Bei den Grenzfällen ist der Abstand größer, aber auf nur 4 Mails. Prompt A vergibt dort `hoch`, wo das Soll `normal` lautet (Lauf 1: WLAN-Mail, "Wichtig"-Mail und VPN+Tastatur-Mail).
- Prompt B scheitert an der WLAN-Mail in allen drei Läufen (`hoch` statt `normal`) und an der Audit-Mail ("Wichtig: Zugriff auf Z:\Projekte verweigert") einmal. Eine Vermutung zur WLAN-Mail: Die Regel "mehrere Personen" in Prompt B ist breiter als die Regel in der Richtlinie (ganzes Geschoss, Abteilung oder Standort). Das ist nicht gesondert geprüft.
- Prompt A und Prompt C erreichen in allen drei Läufen dieselbe Trefferzahl (C mit denselben drei falschen Mails), Prompt B schwankt um eine Mail.
- Prompt C bringt gegenüber B keine Verbesserung (17 statt 18,7 im Mittel). Die WLAN-Mail ist in allen drei C-Läufen richtig (bei B nie), das ist aber kein unabhängiger Befund (siehe Offenlegung).
- Zwei Mails sind in C in jedem Lauf **ungültig**: "Berechtigung für Azubi im Projekt-Wiki" (das Modell antwortet in Fließtext, in Lauf 1 bricht die Antwort bei `max_tokens` ab) und "Zwei Sachen" (Erklärtext vor dem JSON). Das JSON steht dort teilweise im Text, der Runner wertet es bewusst als ungültig, weil nachgelagerter Code reines JSON erwartet. Eine mögliche Ursache habe ich nicht geprüft: Die Beispiele stehen als "E-Mail: ... Antwort: ..." im Prompt, die echte Eingabe hat dieses Format nicht.
- Von den 18 gültigen C-Antworten pro Lauf ist nur die Z:\Projekte-Mail inhaltlich falsch (`hoch` statt `normal`, in allen drei Läufen). Prompt A macht diesen Fehler ebenfalls in allen drei Läufen, Prompt B in einem. Bei drei Läufen reicht das nicht, um zu sagen, dass die Beispiele hier geschadet haben.
- C kostet rund 70 % mehr als B (längerer Prompt, dazu lange Antworten bei den Formatfehlern).

## Offenlegung zur Messung

- Die Richtlinie `labeling_richtlinie.md` wurde schrittweise präzisiert, **nachdem** ich die Mails des Messsatzes gesehen hatte (Mehrthemen-Regel, Breitenwirkung, Frist, "Nicht annehmen"-Regel, Kernaufgabe, Sonderfälle). Der Messsatz ist also nicht unabhängig von der Richtlinie entstanden. Alle Änderungen stehen mit Datum und Anlass in der Änderungshistorie der Datei.
- Die Richtlinie wurde vor den ersten Läufen eingefroren.
- Prompt B (Stand 05.11.2026) wurde vor dem Messsatz geschrieben und danach nicht mehr verändert. Er wurde aber auf dem Entwicklungssatz entwickelt (die VPN-Regel entstand nach einem Fehler dort).
- Prompt B weicht absichtlich an einigen Stellen von der Richtlinie ab (zum Beispiel "am selben oder nächsten Arbeitstag" statt nur heute). Ich habe ihn nicht an die Richtlinie angeglichen, weil er sonst auf den Messsatz zugeschnitten wäre.
- Prompt C ist Prompt B Wort für Wort plus ein Block mit drei erfundenen Beispielen (per `git diff --no-index` geprüft). C wurde **nach** den B-Ergebnissen entworfen und danach nicht mehr verändert, auch nicht nach den C-Ergebnissen.
- Die drei Beispiele lehren dasselbe Prinzip wie je eine Messsatz-Mail, in einem anderen Szenario: Beispiel 1 (Headset, Signalwort "DRINGEND", `normal`) wie die Toner-Mail, Beispiel 2 (Vergabeportal, Frist heute, `hoch`) wie die ERP-Mail, Beispiel 3 (Teams-Ruckeln bei vier Personen, `normal`) wie die WLAN-Mail. Beispiel 3 zielt bewusst auf den bekannten B-Fehler bei der WLAN-Mail. Kein Beispieltext stammt aus dem Messsatz, der WLAN-Treffer von C ist aber kein unabhängiger Beleg dafür, dass Beispiele allgemein helfen.
- Die Mailtexte der drei Beispiele habe ich selbst geschrieben. Die Idee für Beispiel 3 stammt von Claude, ebenso zwei Schlusssätze (neutrale Formulierung, damit ein höflicher Ton nicht mit `normal` zusammenfällt).

## Beispielausgabe Klassifikator

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

Auf dem Entwicklungssatz weicht eine Mail von 23 vom Soll ab: Die VPN-Mail ("liegt das am Netzwerk?") ordnet Claude als `Netzwerk` ein, das Soll-Label lautet `Zugang`. Beides ist vertretbar, siehe Grenzen. In zwei Läufen wurden 22 von 23 Mails richtig zugeordnet. Diese Zahl sagt wenig aus, weil der Prompt auf denselben Mails entwickelt wurde.

Die Kosten und Preise schwanken zwischen Läufen leicht, die Zuordnung war in zwei Läufen gleich.

## Ticket-CLI verwenden

`ticket_cli.py` liest eine CSV-Datei mit den Pflichtspalten `id` und `text`, zählt die Tickets nach Priorität und Kategorie und meldet Dubletten. Es nutzt nur die Standardbibliothek und schreibt keine Dateien.

```powershell
python ticket_cli.py --input tickets.csv          # Klartext
python ticket_cli.py --input tickets.csv --json   # maschinenlesbar
```

Ausgabe für die mitgelieferte `tickets.csv`:

```text
Tickets gesamt: 6
Anzahl pro Priorität:
  hoch: 2
  normal: 4
Anzahl pro Kategorie:
  Sonstiges: 3
  IAM: 2
  Netzwerk: 1
Keine Dubletten.
```

- **Dubletten:** Zwei Tickets gelten als Dublette, wenn ihre Texte nach `.lower()` identisch sind. Gemeldet wird der kleingeschriebene Text, nicht der Originaltext der Tickets, zum Beispiel `"vpn geht nicht": IDs 1, 2` für "VPN geht nicht" und "vpn GEHT nicht".
- **Groß-/Kleinschreibung:** Auch die Regeln für Kategorie und Priorität ignorieren sie, "Drucker DEFEKT" zählt also als `hoch`.
- **Fehler:** Bei fehlender Datei, leerer Datei, fehlender Spalte oder nicht UTF-8-kodierter Datei erscheint eine Meldung auf `stderr` und der Exit-Code ist 1. Fehlt `--input`, beendet `argparse` das Programm mit Exit-Code 2.

## Grenzen und bekannte Fehler

**Testdaten**
- Der Messsatz hat nur 20 Mails, davon 4 Grenzfälle. Eine einzelne Mail verschiebt das Ergebnis um 5 Prozentpunkte. Es sind drei Läufe je Variante, das zeigt einen Trend und keine statistisch belastbare Aussage.
- Alle Mails sind erfunden, es sind keine echten Support-Mails. Die Ergebnisse sagen nichts über die Qualität bei echten Mails aus.
- Die Soll-Labels stammen von mir (nach der Richtlinie), nicht von mehreren unabhängigen Personen. Wie gut zwei Personen übereinstimmen, wurde nicht gemessen.
- Die Mail "VPN-Verbindung bricht ab, liegt das am Netzwerk?" (Mail 21 im Entwicklungssatz) ist nicht eindeutig. Das Soll-Label lautet `Zugang`, Claude wählt je nach Lauf `Netzwerk` oder `Zugang`. Das Soll-Label ist meine Festlegung, kein objektiver Fehler des Modells.

**Technik**
- Die Preise stammen aus der Anthropic-Dokumentation zum Modell Haiku 5.5 (Stand Oktober 2026) und liegen als Konstanten (`PREIS_IN`, `PREIS_OUT`) im Skript. Sie können veralten. Die ausgegebenen Kosten sind eine Berechnung, keine Abrechnung.
- Es gibt keine automatischen Tests. Getestet wurde nur unter Windows (PowerShell) mit Python 3.14.8.
- Das Verhalten bei API-Fehlern (zum Beispiel Wiederholungen) ist nicht geprüft. Für den Dauerbetrieb braucht es Tests, Monitoring und Fehlerbehandlung.
- `runner.py` enthält die Klassifizierfunktion als Kopie aus `klassifikator.py`. Änderungen müssen an beiden Stellen gemacht werden.
- `ticket_pipeline.py` (und damit auch `ticket_cli.py`) arbeitet mit einfachen Stichwortregeln, in der Beispielausgabe landen 3 von 6 Tickets bei "Sonstiges". Die Regeln ignorieren Groß-/Kleinschreibung, erkennen aber nur die Stichwörter "defekt", "geht nicht", "passwort" und "vpn".

**Bekannte Fehler (behoben)**
- Claude packte das JSON teilweise in einen Markdown-Zaun, `json.loads` scheiterte. Behoben durch Bereinigung vor dem Einlesen.
- Die Kostensumme zeigte Gleitkomma-Artefakte (`0.0015128000000000003`). Behoben mit `round(gesamtkosten, 6)`.
- Beim Aufbau des Runners hätte ein Import aus `klassifikator.py` den kompletten alten Durchlauf gestartet und `auswertung.json` überschrieben. Aufgefallen vor dem ersten Lauf, Import entfernt.

## Was ich anders machen würde

1. **Testsatz:** Ich würde den Messsatz deutlich vergrößern (mindestens einige Dutzend Mails je Fallart) und die Labels von zwei Personen unabhängig vergeben lassen, um die Übereinstimmung zu messen. Die Mails sollten ohne Personenbezug und nach Datenschutzprüfung stammen.
2. **Prompt:** Als Nächstes würde ich C um eine Formatanweisung ergänzen (nur reines JSON, kein Text davor oder danach) und die Variante auf einem **neuen** Messsatz testen, weil der jetzige durch die Beispiele und die Richtlinie nicht mehr unabhängig ist. Dazu mehr Läufe, und jede Änderung am Prompt einzeln messen, damit sich Verbesserungen einer Änderung zuordnen lassen.
3. **Grenzfälle:** Bei mehrdeutigen Mails wie der VPN-Mail würde ich eine Kategorie "Unklar" einführen. Das Modell muss sich dann nicht auf eine Kategorie festlegen. Der Preis ist, dass diese Mails von Menschen geprüft werden müssen.
4. **Zuverlässigkeit:** Ich würde zuerst klären, welche Wiederholungen das SDK selbst übernimmt, und nur das Fehlende ergänzen (zum Beispiel Wiederholung mit wachsendem Abstand bei Rate-Limits), dazu automatische Tests und Protokollierung für den Dauerbetrieb.
5. **Struktur:** Ich würde API-Aufruf, Antwortprüfung und Auswertung trennen und die Funktion nur einmal pflegen, statt sie in `runner.py` zu kopieren. Dann lässt sich die Prüfung ohne API-Aufruf testen, und ein Modellwechsel betrifft nur einen Teil des Codes.