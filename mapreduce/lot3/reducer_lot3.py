#!/usr/bin/env python3
"""REDUCER Lot 3 : Top 100, sample 5%, moyenne/type, par ville"""
import sys, random

cdes = []
cur = None; cur_qte = 0; cur_timbre = 0.0; cur_ville = ""; cur_objs = set()

def flush():
    if cur is not None:
        nb = len(cur_objs) if cur_objs else 1
        cdes.append({"code": cur, "ville": cur_ville, "qte": cur_qte,
                      "types": nb, "moy": round(cur_qte/nb, 2), "timbre": cur_timbre})

for line in sys.stdin:
    line = line.strip().replace("\r", "")
    if not line: continue
    parts = line.split("\t")
    if len(parts) != 2: continue
    code = parts[0]
    vals = parts[1].split(",", 3)
    if len(vals) < 4: continue
    codobj = vals[0]
    try: qte = int(vals[1])
    except: qte = 0
    try: timbre = float(vals[2])
    except: timbre = 0.0
    ville = vals[3]
    if code != cur:
        flush()
        cur = code; cur_qte = 0; cur_timbre = timbre; cur_ville = ville; cur_objs = set()
    cur_qte += qte
    if codobj: cur_objs.add(codobj)
flush()

cdes.sort(key=lambda x: (-x["qte"], -x["timbre"]))
top100 = cdes[:100]
sample_size = max(1, len(top100)*5//100) if top100 else 0
sample = random.sample(top100, sample_size) if sample_size > 0 else []

print("=== LOT 3 : Échantillon 5% des 100 meilleures (2011-2016, depts 22/49/53) ===")
print(f"\n{'Code':<10} {'Ville':<35} {'Σ Qté':>8} {'Types':>6} {'Moy/type':>10} {'Timbrecde':>10}")
print("-" * 85)
for c in sample:
    print(f"{c['code']:<10} {c['ville']:<35} {c['qte']:>8} {c['types']:>6} {c['moy']:>10.2f} {c['timbre']:>9.2f} €")

villes = {}
for c in top100:
    v = c["ville"]
    if v not in villes: villes[v] = {"nb": 0, "qte": 0}
    villes[v]["nb"] += 1; villes[v]["qte"] += c["qte"]

print(f"\n\n=== LOT 3c : Répartition par ville ===")
print(f"{'Ville':<35} {'Nb cdes':>8} {'Total qté':>10}")
print("-" * 58)
for v, d in sorted(villes.items(), key=lambda x: -x[1]["qte"]):
    print(f"{v:<35} {d['nb']:>8} {d['qte']:>10}")