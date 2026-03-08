#!/bin/bash
# Pipeline MapReduce local (simule Hadoop Streaming)
# Usage : ./run_mapreduce.sh

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
CSV="$ROOT/data/consolidation_digicheese.csv"
MR="$ROOT/mapreduce"
OUT="$ROOT/data/results/mapreduce"
mkdir -p "$OUT"

if [ ! -f "$CSV" ]; then
    echo "[ERREUR] CSV non trouvé : $CSV"
    echo "Lancez d'abord : python3 scripts/01_import_and_consolidate.py"
    exit 1
fi

echo "=== MapReduce Pipeline ==="
echo ""

echo "--- LOT 1a ---"
cat "$CSV" | python3 "$MR/lot1a/mapper_lot1a.py" | sort | python3 "$MR/lot1a/reducer_lot1a.py" | tee "$OUT/lot1a_result.txt"
echo ""

echo "--- LOT 1b ---"
cat "$CSV" | python3 "$MR/lot1b/mapper_lot1b.py" | sort | python3 "$MR/lot1b/reducer_lot1b.py" | tee "$OUT/lot1b_result.txt"
echo ""

echo "--- LOT 1c ---"
cat "$CSV" | python3 "$MR/lot1c/mapper_lot1c.py" | sort | python3 "$MR/lot1c/reducer_lot1c.py" | tee "$OUT/lot1c_result.txt"
echo ""

echo "--- LOT 2 ---"
cat "$CSV" | python3 "$MR/lot2/mapper_lot2.py" | sort | python3 "$MR/lot2/reducer_lot2.py" | tee "$OUT/lot2_result.txt"
echo ""

echo "--- LOT 3 ---"
cat "$CSV" | python3 "$MR/lot3/mapper_lot3.py" | sort | python3 "$MR/lot3/reducer_lot3.py" | tee "$OUT/lot3_result.txt"
echo ""

echo "=== Résultats dans $OUT ==="
