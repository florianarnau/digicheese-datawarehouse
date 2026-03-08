#!/usr/bin/env python3
"""MAPPER Lot 1b : Commandes 2010-2015 par année"""
import sys
header = True
for line in sys.stdin:
    line = line.strip().replace("\r", "")
    if not line: continue
    if header:
        if line.startswith("codcde"): header = False; continue
        header = False
    f = line.split(";")
    if len(f) < 3: continue
    annee, codcde = f[2].strip(), f[0].strip()
    if annee in ("2010","2011","2012","2013","2014","2015") and codcde:
        print(f"{annee}\t{codcde}")