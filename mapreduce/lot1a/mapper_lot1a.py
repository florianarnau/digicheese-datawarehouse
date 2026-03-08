#!/usr/bin/env python3
"""MAPPER Lot 1a : Meilleure commande de Nantes 2020"""
import sys
header = True
for line in sys.stdin:
    line = line.strip().replace("\r", "")
    if not line: continue
    if header:
        if line.startswith("codcde"): header = False; continue
        header = False
    f = line.split(";")
    if len(f) < 31: continue
    annee, ville, codcde = f[2].strip(), f[10].strip().upper(), f[0].strip()
    timbrecde, qte = f[18].strip(), f[30].strip()
    nom, prenom = f[6].strip(), f[7].strip()
    if annee == "2020" and "NANTES" in ville and qte and codcde:
        print(f"{codcde}\t{qte},{timbrecde},{nom},{prenom},{ville}")