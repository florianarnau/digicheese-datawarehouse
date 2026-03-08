#!/bin/bash
# DIGICHEESE - Lance tout le pipeline
# Usage : ./run_all.sh

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "============================================================"
echo "  DIGICHEESE - Pipeline complet"
echo "============================================================"

echo ""
echo "[1/3] Import SQL → SQLite → CSV consolidé"
echo "------------------------------------------------------------"
python3 scripts/01_import_and_consolidate.py

echo ""
echo "[2/3] Requêtes SQL (Lots 1/2/3) → JSON"
echo "------------------------------------------------------------"
python3 scripts/02_run_lots.py

echo ""
echo "[3/3] Pipeline MapReduce"
echo "------------------------------------------------------------"
bash run_mapreduce.sh

echo ""
echo "============================================================"
echo "  TERMINÉ"
echo "============================================================"
echo ""
echo "  Dashboard : ouvrir dashboards/dashboard.html"
echo "  Résultats : data/results/"
echo "============================================================"
