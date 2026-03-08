#!/usr/bin/env python3
"""REDUCER Lot 1b : COUNT DISTINCT commandes par année (2010-2015)"""
import sys
cur_annee = None; seen = set(); total = 0

print("=== LOT 1b : Commandes par année (2010-2015) ===")
print(f"{'Année':<10} {'Nb commandes':>15}")
print("-" * 30)

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    parts = line.split("\t")
    if len(parts) != 2: continue
    annee, codcde = parts
    if annee != cur_annee:
        if cur_annee is not None:
            c = len(seen); total += c
            print(f"{cur_annee:<10} {c:>15}")
        cur_annee = annee; seen = set()
    seen.add(codcde)

if cur_annee is not None:
    c = len(seen); total += c
    print(f"{cur_annee:<10} {c:>15}")

print("-" * 30)
print(f"{'TOTAL':<10} {total:>15}")
