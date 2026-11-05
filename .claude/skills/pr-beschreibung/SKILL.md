---
name: pr-beschreibung
description: Schreibt eine Pull-Request-Beschreibung auf Deutsch aus dem aktuellen Branch. Nutzen, wenn ein PR vorbereitet oder beschrieben werden soll.
---

# PR-Beschreibung erstellen

1. Lies `git log --oneline main..HEAD` und `git diff --stat main`, um zu sehen, was der Branch gegenüber `main` ändert.
2. Schreibe die Beschreibung mit genau diesen Abschnitten:
   - **Was**: die Änderung in 2 bis 3 Sätzen
   - **Warum**: der Grund für die Änderung
   - **Tests**: nur Tests nennen, die tatsächlich ausgeführt wurden. Wenn unklar, nachfragen statt raten.
   - **Was fehlt**: bekannte Grenzen und offene Punkte
   - **Arbeitsweise**: ob und wie ein Coding-Agent beteiligt war
3. Zahlen (Commits, Dateien) nur aus den Git-Ausgaben übernehmen, nie schätzen.
4. Keine Befehle ausführen, die etwas verändern (kein add, commit, push). Nur lesen.