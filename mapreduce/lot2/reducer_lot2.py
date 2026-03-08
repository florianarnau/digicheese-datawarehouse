#!/usr/bin/env python3
"""REDUCER Lot 2 : Agrège par commande → Top 100"""
import sys

cdes = []
cur = None; cur_qte = 0; cur_timbre = 0.0; cur_ville = ""

def flush():
    if cur is not None:
        cdes.append((cur_qte, cur_timbre, cur, cur_ville))

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    parts = line.split("\t")
    if len(parts) != 2: continue
    code = parts[0]
    vals = parts[1].split(",", 2)
    if len(vals) < 3: continue
    try: qte = int(vals[0])
    except: qte = 0
    try: timbre = float(vals[1])
    except: timbre = 0.0
    ville = vals[2]
    if code != cur:
        flush()
        cur = code; cur_qte = 0; cur_timbre = timbre; cur_ville = ville
    cur_qte += qte
flush()

cdes.sort(key=lambda x: (-x[0], -x[1]))
top = cdes[:100]

print("=== LOT 2 : Top 100 commandes (2006-2010, depts 53/61/28) ===")
print(f"{'#':<5} {'Code':<10} {'Ville':<35} {'Σ Qté':>8} {'Timbrecde':>10}")
print("-" * 75)
for i, (q, t, c, v) in enumerate(top, 1):
    print(f"{i:<5} {c:<10} {v:<35} {q:>8} {t:>9.2f} €")
print(f"\n{len(top)} commandes sur {len(cdes)} trouvées.")
