#!/usr/bin/env python3
"""REDUCER Lot 1c : Client avec le max de timbrecde (dédupliqué par commande)"""
import sys

best = None  # (total_timbrecde, nb_cde, somme_qte, nom, prenom)
cur_cli = None; cur_cdes = {}; cur_qte = 0; cur_nom = ""; cur_prenom = ""

def check():
    global best
    if cur_cli is None: return
    tot = sum(cur_cdes.values())
    nb = len(cur_cdes)
    if best is None or tot > best[0]:
        best = (tot, nb, cur_qte, cur_nom, cur_prenom)

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    parts = line.split("\t")
    if len(parts) != 2: continue
    cli = parts[0]
    vals = parts[1].split(",", 4)
    if len(vals) < 5: continue
    codcde = vals[0]
    try: qte = int(vals[1]) if vals[1] else 0
    except: qte = 0
    try: timbre = float(vals[2]) if vals[2] else 0.0
    except: timbre = 0.0
    if cli != cur_cli:
        check()
        cur_cli = cli; cur_cdes = {}; cur_qte = 0
        cur_nom = vals[3]; cur_prenom = vals[4]
    if codcde not in cur_cdes:
        cur_cdes[codcde] = timbre
    cur_qte += qte
check()

print("=== LOT 1c : Client avec le plus de frais de timbrecde ===")
if best:
    print(f"Client        : {best[4]} {best[3]}")
    print(f"Nb commandes  : {best[1]}")
    print(f"Somme qté     : {best[2]}")
    print(f"Total timbre  : {best[0]:.2f} €")
else:
    print("Aucun résultat.")
