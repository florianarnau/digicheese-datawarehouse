#!/usr/bin/env python3
"""
Script 2 : Exécution des requêtes des Lots 1, 2, 3 et export JSON pour dashboards.
Usage : python 02_run_lots.py [chemin_db] [dossier_sortie]
"""

import sqlite3
import json
import sys
import os

DB_PATH = sys.argv[1] if len(sys.argv) > 1 else "./data/digicheese.db"
OUTPUT_DIR = sys.argv[2] if len(sys.argv) > 2 else "./data/results"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def q(cursor, query):
    cursor.execute(query)
    cols = [d[0] for d in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]


def run_all(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    results = {}

    print("--- LOT 1 ---")

    # 1a - Meilleure commande de Nantes 2020
    results["lot1a"] = q(c, """
        SELECT e.codcde, e.datcde, c.nomcli, c.prenomcli, c.villecli,
            SUM(dt.qte) AS somme_quantites, e.timbrecde
        FROM T_entcde e JOIN T_dtlcode dt ON e.codcde = dt.codcde
        JOIN T_client c ON e.codcli = c.codcli
        WHERE UPPER(c.villecli) LIKE '%NANTES%' AND strftime('%Y', e.datcde) = '2020'
        GROUP BY e.codcde ORDER BY somme_quantites DESC, e.timbrecde DESC LIMIT 1
    """)
    print(f"  1a Meilleure cde Nantes 2020: {results['lot1a']}")

    # 1b - Commandes 2010-2015 par année
    results["lot1b"] = q(c, """
        SELECT strftime('%Y', e.datcde) AS annee, COUNT(DISTINCT e.codcde) AS nb_commandes
        FROM T_entcde e WHERE strftime('%Y', e.datcde) BETWEEN '2010' AND '2015'
        GROUP BY annee ORDER BY annee
    """)
    print(f"  1b Commandes 2010-2015: {results['lot1b']}")

    # 1c - Client avec max timbrecde
    results["lot1c"] = q(c, """
        WITH client_timbrecde AS (
            SELECT codcli, SUM(timbrecde) AS total_timbrecde, COUNT(*) AS nb_commandes
            FROM T_entcde GROUP BY codcli ORDER BY total_timbrecde DESC LIMIT 1
        )
        SELECT c.nomcli, c.prenomcli, ct.nb_commandes,
            (SELECT SUM(dt.qte) FROM T_entcde e2 JOIN T_dtlcode dt ON e2.codcde = dt.codcde
             WHERE e2.codcli = ct.codcli) AS somme_quantites,
            ct.total_timbrecde
        FROM client_timbrecde ct JOIN T_client c ON ct.codcli = c.codcli
    """)
    print(f"  1c Client max timbrecde: {results['lot1c']}")

    print("\n--- LOT 2 ---")

    # 2 - Top 100 commandes (2006-2010, depts 53/61/28)
    results["lot2_top100"] = q(c, """
        SELECT e.codcde, e.datcde, c.villecli AS ville,
            SUM(dt.qte) AS somme_quantites, e.timbrecde
        FROM T_entcde e JOIN T_dtlcode dt ON e.codcde = dt.codcde
        JOIN T_client c ON e.codcli = c.codcli
        WHERE strftime('%Y', e.datcde) BETWEEN '2006' AND '2010'
          AND SUBSTR(c.cpcli, 1, 2) IN ('53', '61', '28')
        GROUP BY e.codcde ORDER BY somme_quantites DESC, e.timbrecde DESC LIMIT 100
    """)
    print(f"  2 Top 100: {len(results['lot2_top100'])} résultats")

    # Agrégation par ville (lot 2)
    results["lot2_par_ville"] = q(c, """
        SELECT ville, COUNT(*) AS nb_commandes, SUM(somme_quantites) AS total_qte,
               ROUND(AVG(timbrecde), 2) AS avg_timbrecde
        FROM (
            SELECT e.codcde, c.villecli AS ville, SUM(dt.qte) AS somme_quantites, e.timbrecde
            FROM T_entcde e JOIN T_dtlcode dt ON e.codcde = dt.codcde
            JOIN T_client c ON e.codcli = c.codcli
            WHERE strftime('%Y', e.datcde) BETWEEN '2006' AND '2010'
              AND SUBSTR(c.cpcli, 1, 2) IN ('53', '61', '28')
            GROUP BY e.codcde ORDER BY somme_quantites DESC, e.timbrecde DESC LIMIT 100
        ) GROUP BY ville ORDER BY total_qte DESC
    """)

    print("\n--- LOT 3 ---")

    # 3 - Top 100 (2011-2016, depts 22/49/53, sans timbrecli)
    results["lot3_top100"] = q(c, """
        SELECT e.codcde, e.datcde, c.villecli AS ville,
            SUM(dt.qte) AS somme_quantites,
            COUNT(DISTINCT dt.codobj) AS nb_types_objets,
            ROUND(CAST(SUM(dt.qte) AS REAL) / COUNT(DISTINCT dt.codobj), 2) AS moyenne_qte_par_type,
            e.timbrecde
        FROM T_entcde e JOIN T_dtlcode dt ON e.codcde = dt.codcde
        JOIN T_client c ON e.codcli = c.codcli
        WHERE strftime('%Y', e.datcde) BETWEEN '2011' AND '2016'
          AND SUBSTR(c.cpcli, 1, 2) IN ('22', '49', '53')
          AND (e.timbrecli IS NULL OR e.timbrecli = 0)
        GROUP BY e.codcde ORDER BY somme_quantites DESC, e.timbrecde DESC LIMIT 100
    """)
    print(f"  3 Top 100: {len(results['lot3_top100'])} résultats")

    # 5% aléatoire
    results["lot3_sample"] = q(c, """
        SELECT * FROM (
            SELECT e.codcde, e.datcde, c.villecli AS ville,
                SUM(dt.qte) AS somme_quantites,
                COUNT(DISTINCT dt.codobj) AS nb_types_objets,
                ROUND(CAST(SUM(dt.qte) AS REAL) / COUNT(DISTINCT dt.codobj), 2) AS moyenne_qte_par_type,
                e.timbrecde
            FROM T_entcde e JOIN T_dtlcode dt ON e.codcde = dt.codcde
            JOIN T_client c ON e.codcli = c.codcli
            WHERE strftime('%Y', e.datcde) BETWEEN '2011' AND '2016'
              AND SUBSTR(c.cpcli, 1, 2) IN ('22', '49', '53')
              AND (e.timbrecli IS NULL OR e.timbrecli = 0)
            GROUP BY e.codcde ORDER BY somme_quantites DESC, e.timbrecde DESC LIMIT 100
        ) ORDER BY RANDOM() LIMIT 5
    """)
    print(f"  3 Sample 5%: {results['lot3_sample']}")

    # Agrégation par ville (lot 3) pour graphique camembert
    results["lot3_par_ville"] = q(c, """
        SELECT ville, SUM(somme_quantites) AS total_qte,
               ROUND(AVG(moyenne_qte_par_type), 2) AS avg_moy_type,
               COUNT(*) AS nb_commandes
        FROM (
            SELECT e.codcde, c.villecli AS ville, SUM(dt.qte) AS somme_quantites,
                COUNT(DISTINCT dt.codobj) AS nb_types_objets,
                ROUND(CAST(SUM(dt.qte) AS REAL) / COUNT(DISTINCT dt.codobj), 2) AS moyenne_qte_par_type
            FROM T_entcde e JOIN T_dtlcode dt ON e.codcde = dt.codcde
            JOIN T_client c ON e.codcli = c.codcli
            WHERE strftime('%Y', e.datcde) BETWEEN '2011' AND '2016'
              AND SUBSTR(c.cpcli, 1, 2) IN ('22', '49', '53')
              AND (e.timbrecli IS NULL OR e.timbrecli = 0)
            GROUP BY e.codcde ORDER BY somme_quantites DESC, e.timbrecde DESC LIMIT 100
        ) GROUP BY ville ORDER BY total_qte DESC
    """)

    print("\n--- STATS SUPPLEMENTAIRES ---")

    results["ca_par_annee"] = q(c, """
        SELECT strftime('%Y', datcde) AS annee, COUNT(DISTINCT codcde) AS nb_commandes,
               ROUND(SUM(timbrecde), 2) AS total_timbrecde
        FROM T_entcde WHERE datcde IS NOT NULL GROUP BY annee ORDER BY annee
    """)

    results["top10_objets"] = q(c, """
        SELECT o.libobj, o.Tailleobj, SUM(dt.qte) AS total_qte
        FROM T_dtlcode dt JOIN T_objet o ON dt.codobj = o.codobj
        GROUP BY dt.codobj ORDER BY total_qte DESC LIMIT 10
    """)

    results["top10_villes"] = q(c, """
        SELECT UPPER(c.villecli) AS ville, COUNT(DISTINCT e.codcde) AS nb_commandes
        FROM T_entcde e JOIN T_client c ON e.codcli = c.codcli
        WHERE c.villecli IS NOT NULL AND c.villecli != ''
        GROUP BY ville ORDER BY nb_commandes DESC LIMIT 10
    """)

    results["top15_departements"] = q(c, """
        SELECT d.nom_dept, SUBSTR(c.cpcli, 1, 2) AS code_dept,
               COUNT(DISTINCT e.codcde) AS nb_commandes
        FROM T_entcde e JOIN T_client c ON e.codcli = c.codcli
        LEFT JOIN T_dept d ON SUBSTR(c.cpcli, 1, 2) = d.code_dept
        WHERE c.cpcli IS NOT NULL
        GROUP BY code_dept ORDER BY nb_commandes DESC LIMIT 15
    """)

    conn.close()
    return results


if __name__ == "__main__":
    print("=" * 60)
    print("DIGICHEESE - Exécution des Lots")
    print("=" * 60)

    results = run_all(DB_PATH)

    output_file = os.path.join(OUTPUT_DIR, "all_results.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n[EXPORT] {output_file}")
    print("[TERMINÉ]")
