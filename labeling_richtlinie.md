# IT-Support Labeling-Richtlinie (Mess-Set)

Diese Richtlinie definiert die verbindlichen Regeln für die Klassifizierung von IT-Support-E-Mails nach Kategorie und Priorität. Sie dient als fachlicher Maßstab für menschliche Labeler und zur Evaluation von LLM-Prompts.

---

## 1. Kategorie-Regeln (Feste Prüfreihenfolge)

Die Klassifizierung erfolgt streng von oben nach unten. Die erste zutreffende Prüfung bestimmt die Kategorie:

1. **Prüfung 1: Mehrere Themen (Ursache vor Rangfolge)**
   * Liegen mehrere Störungen oder Anliegen in einer E-Mail vor, gilt:
     * **Ursachen-Prinzip:** Verursacht ein Problem nachweislich das andere (z. B. Netzwerkausfall führt zu gescheitertem Login), bestimmt die Ursache die Kategorie.
     * **Rangfolge-Prinzip:** Ist keine eindeutige Ursache-Wirkung-Kette erkennbar, entscheidet die feste Rangfolge:  
       Zugang -> Hardware -> Netzwerk -> Sonstiges
2. **Prüfung 2: Berechtigungsausnahme**
   * Handelt es sich um eine Anforderung oder Störung bezüglich Berechtigungen, Passwörtern, Logins oder gesperrten Accounts?
   * -> Zugang (übersteuert die bloße Nennung eines betroffenen Endgeräts oder Netzwerksystems).
3. **Prüfung 3: Genanntes System (Standardfall)**
   * Greifen Prüfung 1 und 2 nicht, bestimmt das explizit genannte Gerät oder System die Kategorie:
     * PCs, Monitore, Drucker, lokale Hardware -> Hardware
     * WLAN, LAN, VPN-Tunnel, Netzwerk-Shares, Server-Pfade -> Netzwerk
     * Allgemeine Anfragen, Feedback, Schulungen, ohne Supportbezug -> Sonstiges

---

## 2. Prioritätsregel

Eine E-Mail erhält die Priorität **hoch**, wenn mindestens eines der folgenden Kriterien erfüllt ist:
* **Akuter Stillstand:** Die betroffene Person beschreibt konkret, dass sie gar nicht mehr arbeiten kann oder dass eine zentral zugewiesene Haupt- beziehungsweise Kernaufgabe vollständig blockiert ist (als Kernaufgabe gilt die primäre, betriebsnotwendige Funktion einer Rolle oder Anlaufstelle, wie etwa der Publikums- und Besucherverkehr am Empfang). Was in der Mail nicht explizit als Stillstand oder Blockade der Kernaufgabe benannt wird, wird nicht angenommen (im Zweifel normal). Unvollständige oder eingeschränkte Arbeitsweisen führen nicht zu einer hohen Priorität.
* **Konkrete Frist:** Ein kritischer Termin oder eine Abgabe ist zwingend für den heutigen Arbeitstag angesetzt, sodass ein Aufschieben den Termin noch am selben Tag scheitern lässt (Termine an Folgetagen fallen ausdrücklich nicht darunter).
* **Breitenwirkung:** Ein gesamter Standort, ein komplettes Bürogeschoss oder eine ganze Abteilung ist flächendeckend von einem vollständigen Ausfall betroffen (nicht nur einzelne Personen oder ein einzelner Besprechungsraum bei teilweiser Einschränkung).

Signalwörter wie „DRINGEND“, „Wichtig“ oder Ausrufezeichen begründen für sich allein **keine** hohe Priorität.  
In allen anderen Fällen gilt die Priorität **normal**.

---

## 3. Festlegungen für Sonderfälle

* **„Zugriff verweigert“ / Netzlaufwerke:** Die Fehlermeldung „Zugriff verweigert“ auf ein Netzlaufwerk oder einen Server-Pfad ist eine fehlende Berechtigung -> Zugang (Prüfung 2 schlägt Prüfung 3).
* **Verbrauchsmaterial (z. B. Toner, Kabel):** Anfragen zu Toner, Tinte oder Verschleißteilen fallen unter -> Hardware (sofern es sich um Arbeitsplatzgeräte handelt).
* **Abgelaufenes / Vergessenes Passwort:** Passwort-Resets und abgelaufene Logins gehören ausnahmslos zu -> Zugang.

---

## 4. Änderungshistorie

Alle folgenden Änderungen entstanden am 2026-11-06, **nach** Sichtung der Mails des Messsatzes. Die Richtlinie ist damit nicht unabhängig von den Mails entstanden.

* **Mehrthemen-Regel:** Einführung von Ursache-vor-Rangfolge und der festen Hierarchie (Zugang -> Hardware -> Netzwerk -> Sonstiges), um E-Mails mit mehreren Störungen eindeutig aufzulösen.
* **Breitenwirkung (Anlass: WLAN-Mail):** Präzisierung auf ganze Stockwerke, Standorte oder Abteilungen, damit temporäre Einschränkungen in einzelnen Besprechungsräumen nicht fälschlich als `hoch` eingestuft werden.
* **Frist (Anlass: Audit-Mail):** Schärfung auf den heutigen Arbeitstag, damit Termine an Folgetagen (wie das Audit nächste Woche) nicht zu `hoch` führen.
* **„Nicht annehmen“-Regel:** Was in der Mail nicht explizit als Stillstand oder Einschränkung genannt wird, wird nicht unterstellt (im Zweifel `normal`).
* **Kernaufgabe (Anlass: Empfang-Mail):** Erweiterung des akuten Stillstands um den Ausfall zentraler Kernaufgaben. Der Halbsatz zur „Ausweichmöglichkeit“ wurde bewusst gestrichen, weil er subjektiv auslegbar war.
* **Sonderfälle (Abschnitt 3):** Festlegungen zu „Zugriff verweigert“, Verbrauchsmaterial (Anlass: Toner-Mail) und abgelaufenem Passwort wurden nach den jeweiligen Mails ergänzt.
* **2026-11-06: Eingefroren vor den ersten Läufen. Ab jetzt keine Änderungen.**