#!/usr/bin/env python3
"""
MAPPER - Lot 1a : Meilleure commande de Nantes, année 2020
Entrée  : CSV consolidé (séparateur ;)
Sortie  : codcde \t qte,timbrecde

Filtre : villecli contient "NANTES" ET année = 2020
Émet chaque ligne de détail avec (codcde, qte, timbrecde)
Le reducer agrégera par codcde.

Usage Hadoop Streaming :
  hadoop jar hadoop-streaming.jar \
    -mapper mapper_lot1a.py \
    -reducer reducer_lot1a.py \
    -input /data/consolidation_digicheese.csv \
    -output /output/lot1a

Usage local (test) :
  cat data/consolidation_digicheese.csv | python3 mapper_lot1a.py | sort | python3 reducer_lot1a.py
"""

import sys

# Index des colonnes du CSV consolidé
# codcde;datcde;annee;mois;codcli;genrecli;nomcli;prenomcli;adresse1cli;cpcli;
# villecli;telcli;emailcli;portcli;newsletter;code_dept;nom_dept;timbrecli;
# timbrecde;Nbcolis;cheqcli;idcondit;barchive;bstock;codobj;libobj;Tailleobj;
# puobj;Poidsobj;points_obj;qte;Colis;Commentaire

COL_CODCDE = 0
COL_ANNEE = 2
COL_NOMCLI = 6
COL_PRENOMCLI = 7
COL_VILLECLI = 10
COL_TIMBRECDE = 18
COL_QTE = 30

header_skipped = False

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    # Skipper le header
    if not header_skipped:
        if line.startswith("codcde"):
            header_skipped = True
            continue
        header_skipped = True

    fields = line.split(";")
    if len(fields) < 31:
        continue

    try:
        annee = fields[COL_ANNEE].strip()
        villecli = fields[COL_VILLECLI].strip().upper()
        codcde = fields[COL_CODCDE].strip()
        timbrecde = fields[COL_TIMBRECDE].strip()
        qte = fields[COL_QTE].strip()
        nomcli = fields[COL_NOMCLI].strip()
        prenomcli = fields[COL_PRENOMCLI].strip()

        # Filtre : Nantes + 2020
        if annee == "2020" and "NANTES" in villecli:
            # Émettre : clé = codcde, valeur = qte,timbrecde,nomcli,prenomcli,villecli
            if qte and codcde:
                print(f"{codcde}\t{qte},{timbrecde},{nomcli},{prenomcli},{villecli}")
    except (IndexError, ValueError):
        continue
