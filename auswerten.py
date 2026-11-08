# auswerten.py - Teil 1: alle Ergebnisdateien in eine Tabelle laden
import json
import glob
import os
import pandas as pd

zeilen = []                                         # hier sammeln wir alle Mails aller Läufe
for pfad in sorted(glob.glob("ergebnisse/*_lauf*.json")):
    with open(pfad, encoding="utf-8") as f:
        daten = json.load(f)
    name = os.path.basename(pfad)                   # z. B. "A_lauf2.json"
    variante = name.split("_")[0]                  
    lauf = int(name.split("_")[1].replace("lauf", "").replace(".json", ""))  
    for mail in daten["mails"]:
        mail["variante"] = variante                 # jede Mail bekommt Variante und Lauf mit
        mail["lauf"] = lauf
        zeilen.append(mail)

df = pd.DataFrame(zeilen)
print(df.shape)
print(list(df.columns))

print(df.groupby(["variante", "lauf"])["ist_richtig"].sum())

print(df[(~df["ist_richtig"])][["lauf", "betreff", "soll_prioritaet", "prioritaet", "kategorie", "soll_kategorie","grenzfall","gueltig", "variante"]].sort_values(["lauf", "betreff"])   )
print(df.groupby(["variante", "grenzfall"])["ist_richtig"].mean())

# Eine neue Tabelle soll pro (Variante, Lauf) die Anzahl gültiger Antworten zeigen.
print(df.groupby(["variante", "lauf"])["gueltig"].sum())