#!/usr/bin/env python3
"""MAPPER Lot 2 : 2006-2010, départements 53/61/28"""
import sys
ANNEES = {"2006","2007","2008","2009","2010"}
DEPTS = {"53","61","28"}
header = True
for line in sys.stdin:
    line = line.strip().replace("\r", "")
    if not line: continue
    if header:
        if line.startswith("codcde"): header = False; continue
        header = False
    f = line.split(";")
    if len(f) < 31: continue
    annee, dept = f[2].strip(), f[15].strip()
    codcde, qte, timbrecde, ville = f[0].strip(), f[30].strip(), f[18].strip(), f[10].strip()
    if annee in ANNEES and dept in DEPTS and codcde and qte:
        print(f"{codcde}\t{qte},{timbrecde},{ville}")