#!/bin/bash
# ===========================================================
# DIGICHEESE — Script principal
# Exécute tout le pipeline : Import → Consolidation → SQL → MapReduce
# ===========================================================
# Usage :
#   chmod +x run_all.sh
#   ./run_all.sh
# ===========================================================

set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

SQL_DUMPS="sql/sql_dumps"
CSV_FILE="data/consolidation_digicheese.csv"
DB_FILE="data/digicheese.db"
RESULTS_DIR="data/results"

echo "============================================================"
echo "🧀 DIGICHEESE — Pipeline complet"
echo "============================================================"

# -----------------------------------------------------------
# ÉTAPE 1 : Import et consolidation
# -----------------------------------------------------------
echo ""
echo "▶ ÉTAPE 1 : Import des dumps SQL et consolidation CSV"
echo "------------------------------------------------------------"
python3 scripts/01_import_and_consolidate.py "$SQL_DUMPS" "$CSV_FILE" "$DB_FILE"

# -----------------------------------------------------------
# ÉTAPE 2 : Requêtes SQL (Lots 1, 2, 3) → JSON
# -----------------------------------------------------------
echo ""
echo "▶ ÉTAPE 2 : Exécution des requêtes SQL (Lots 1/2/3)"
echo "------------------------------------------------------------"
python3 scripts/02_run_lots.py "$DB_FILE" "$RESULTS_DIR"

# -----------------------------------------------------------
# ÉTAPE 3 : Pipeline MapReduce
# -----------------------------------------------------------
echo ""
echo "▶ ÉTAPE 3 : Pipeline MapReduce (Hadoop Streaming local)"
echo "------------------------------------------------------------"
bash run_mapreduce.sh "$CSV_FILE"

# -----------------------------------------------------------
# RÉSUMÉ
# -----------------------------------------------------------
echo ""
echo "============================================================"
echo "✅ Pipeline terminé avec succès"
echo "============================================================"
echo ""
echo "Fichiers générés :"
echo "  - Base SQLite     : $DB_FILE"
echo "  - CSV consolidé   : $CSV_FILE ($(wc -l < "$CSV_FILE") lignes)"
echo "  - Résultats SQL   : $RESULTS_DIR/all_results.json"
echo "  - Résultats MR    : $RESULTS_DIR/mapreduce/"
echo ""
echo "Dashboard : ouvrir dashboards/dashboard.html dans un navigateur"
echo "============================================================"
