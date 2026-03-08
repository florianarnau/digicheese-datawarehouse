#!/bin/bash
# ===========================================================
# DIGICHEESE - Exécution locale de tous les jobs MapReduce
# ===========================================================
# Simule le pipeline Hadoop Streaming en local :
#   cat input | python3 mapper.py | sort | python3 reducer.py
#
# Usage :
#   chmod +x run_mapreduce.sh
#   ./run_mapreduce.sh [chemin_csv]
# ===========================================================

CSV_FILE="${1:-./data/consolidation_digicheese.csv}"
MAPREDUCE_DIR="./mapreduce"
OUTPUT_DIR="./data/results/mapreduce"

mkdir -p "$OUTPUT_DIR"

if [ ! -f "$CSV_FILE" ]; then
    echo "[ERREUR] Fichier CSV non trouvé : $CSV_FILE"
    echo "Exécutez d'abord : python3 scripts/01_import_and_consolidate.py"
    exit 1
fi

echo "============================================================"
echo "DIGICHEESE - Pipeline MapReduce"
echo "Fichier source : $CSV_FILE"
echo "============================================================"

echo ""
echo "--- LOT 1a : Meilleure commande Nantes 2020 ---"
cat "$CSV_FILE" | python3 "$MAPREDUCE_DIR/lot1a/mapper_lot1a.py" | sort | python3 "$MAPREDUCE_DIR/lot1a/reducer_lot1a.py" | tee "$OUTPUT_DIR/lot1a_result.txt"

echo ""
echo "--- LOT 1b : Commandes 2010-2015 par année ---"
cat "$CSV_FILE" | python3 "$MAPREDUCE_DIR/lot1b/mapper_lot1b.py" | sort | python3 "$MAPREDUCE_DIR/lot1b/reducer_lot1b.py" | tee "$OUTPUT_DIR/lot1b_result.txt"

echo ""
echo "--- LOT 1c : Client max timbrecde ---"
cat "$CSV_FILE" | python3 "$MAPREDUCE_DIR/lot1c/mapper_lot1c.py" | sort | python3 "$MAPREDUCE_DIR/lot1c/reducer_lot1c.py" | tee "$OUTPUT_DIR/lot1c_result.txt"

echo ""
echo "--- LOT 2 : Top 100 commandes (2006-2010, depts 53/61/28) ---"
cat "$CSV_FILE" | python3 "$MAPREDUCE_DIR/lot2/mapper_lot2.py" | sort | python3 "$MAPREDUCE_DIR/lot2/reducer_lot2.py" | tee "$OUTPUT_DIR/lot2_result.txt"

echo ""
echo "--- LOT 3 : Échantillon 5% top 100 (2011-2016, depts 22/49/53) ---"
cat "$CSV_FILE" | python3 "$MAPREDUCE_DIR/lot3/mapper_lot3.py" | sort | python3 "$MAPREDUCE_DIR/lot3/reducer_lot3.py" | tee "$OUTPUT_DIR/lot3_result.txt"

echo ""
echo "============================================================"
echo "Résultats sauvegardés dans : $OUTPUT_DIR/"
ls -la "$OUTPUT_DIR/"
echo "============================================================"
