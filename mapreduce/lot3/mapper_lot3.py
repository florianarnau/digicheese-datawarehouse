#!/usr/bin/env python3
"""MAPPER Lot 3 : 2011-2016, depts 22/49/53, sans timbrecli"""
import sys
ANNEES = {"2011","2012","2013","2014","2015","2016"}
DEPTS = {"22","49","53"}
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
    if annee not in ANNEES or dept not in DEPTS: continue
    tcli = f[17].strip()
    if tcli and tcli not in ("0","0.0","None",""):
        try:
            if float(tcli) != 0: continue
        except: pass
    codcde, codobj, qte = f[0].strip(), f[24].strip(), f[30].strip()
    timbrecde, ville = f[18].strip(), f[10].strip()
    if codcde and qte:
        print(f"{codcde}\t{codobj},{qte},{timbrecde},{ville}")