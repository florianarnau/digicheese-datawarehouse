#!/usr/bin/env python3
"""MAPPER Lot 1c : Client avec le plus de frais de timbrecde"""
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
    codcli, codcde = f[4].strip(), f[0].strip()
    qte, timbrecde = f[30].strip(), f[18].strip()
    nom, prenom = f[6].strip(), f[7].strip()
    if codcli and codcde:
        print(f"{codcli}\t{codcde},{qte},{timbrecde},{nom},{prenom}")