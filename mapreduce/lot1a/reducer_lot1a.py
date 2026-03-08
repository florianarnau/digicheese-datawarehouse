#!/usr/bin/env python3
"""REDUCER Lot 1a : Meilleure commande de Nantes 2020"""
import sys
best = None
cur_code = None; cur_qte = 0; cur_timbre = 0.0; cur_info = ""

def check():
    global best
    if cur_code is None: return
    if best is None or cur_qte > best[0] or (cur_qte == best[0] and cur_timbre > best[1]):
        best = (cur_qte, cur_timbre, cur_code, cur_info)

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    parts = line.split("\t")
    if len(parts) != 2: continue
    code = parts[0]
    vals = parts[1].split(",", 4)
    if len(vals) < 5: continue
    try: qte = int(vals[0]); timbre = float(vals[1])
    except: continue
    if code == cur_code:
        cur_qte += qte
    else:
        check()
        cur_code = code; cur_qte = qte; cur_timbre = timbre
        cur_info = f"{vals[3]} {vals[2]} ({vals[4]})"
check()

print("=== LOT 1a : Meilleure commande de Nantes 2020 ===")
if best:
    print(f"Code commande : {best[2]}")
    print(f"Client        : {best[3]}")
    print(f"Somme qté     : {best[0]}")
    print(f"Timbrecde     : {best[1]} €")
else:
    print("Aucun résultat.")
