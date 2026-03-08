#!/usr/bin/env python3
"""
REDUCER - Lot 1a : Meilleure commande de Nantes, année 2020
Entrée  : codcde \t qte,timbrecde,nomcli,prenomcli,villecli (trié par clé)
Sortie  : La commande avec la plus grande somme de quantités (puis timbrecde)

Usage local :
  cat data/consolidation_digicheese.csv | python3 mapper_lot1a.py | sort | python3 reducer_lot1a.py
"""

import sys

best_codcde = None
best_somme_qte = 0
best_timbrecde = 0.0
best_info = ""

current_codcde = None
current_somme_qte = 0
current_timbrecde = 0.0
current_info = ""


def evaluate_best():
    """Compare la commande courante avec la meilleure trouvée."""
    global best_codcde, best_somme_qte, best_timbrecde, best_info
    global current_codcde, current_somme_qte, current_timbrecde, current_info

    if current_codcde is None:
        return

    # Filtre prioritaire : somme quantités DESC
    # Filtre secondaire : timbrecde DESC
    if (current_somme_qte > best_somme_qte or
        (current_somme_qte == best_somme_qte and current_timbrecde > best_timbrecde)):
        best_codcde = current_codcde
        best_somme_qte = current_somme_qte
        best_timbrecde = current_timbrecde
        best_info = current_info


for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    parts = line.split("\t")
    if len(parts) != 2:
        continue

    codcde = parts[0]
    values = parts[1].split(",", 4)  # qte, timbrecde, nomcli, prenomcli, villecli

    if len(values) < 5:
        continue

    try:
        qte = int(values[0])
        timbrecde = float(values[1])
        nomcli = values[2]
        prenomcli = values[3]
        villecli = values[4]
    except (ValueError, IndexError):
        continue

    if codcde == current_codcde:
        # Même commande : accumuler
        current_somme_qte += qte
    else:
        # Nouvelle commande : évaluer la précédente
        evaluate_best()
        current_codcde = codcde
        current_somme_qte = qte
        current_timbrecde = timbrecde
        current_info = f"{prenomcli} {nomcli} ({villecli})"

# Évaluer la dernière commande
evaluate_best()

# Résultat final
if best_codcde:
    print(f"=== LOT 1a : Meilleure commande de Nantes 2020 ===")
    print(f"Code commande : {best_codcde}")
    print(f"Client        : {best_info}")
    print(f"Somme qté     : {best_somme_qte}")
    print(f"Timbrecde     : {best_timbrecde} €")
else:
    print("Aucune commande trouvée pour Nantes en 2020.")
