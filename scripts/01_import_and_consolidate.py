#!/usr/bin/env python3
"""
Script 1 : Import des dumps SQL MySQL dans SQLite et consolidation en un seul CSV.
Gère correctement la conversion MySQL -> SQLite.
"""

import sqlite3
import re
import os
import sys
import csv

SQL_DIR = sys.argv[1] if len(sys.argv) > 1 else "./data/sql_dumps"
OUTPUT_CSV = sys.argv[2] if len(sys.argv) > 2 else "./data/consolidation_digicheese.csv"
DB_PATH = sys.argv[3] if len(sys.argv) > 3 else "./data/digicheese.db"


def create_tables(conn):
    """Crée les tables directement en SQLite."""
    cursor = conn.cursor()
    cursor.executescript("""
        DROP TABLE IF EXISTS T_client;
        DROP TABLE IF EXISTS T_Communes;
        DROP TABLE IF EXISTS T_dept;
        DROP TABLE IF EXISTS T_dtlcode;
        DROP TABLE IF EXISTS T_enseigne;
        DROP TABLE IF EXISTS T_entcde;
        DROP TABLE IF EXISTS T_objet;
        DROP TABLE IF EXISTS T_poids;
        DROP TABLE IF EXISTS T_poidsV;
        DROP TABLE IF EXISTS T_rel_cond;
        DROP TABLE IF EXISTS T_utilisateur;

        CREATE TABLE T_client (
            codcli INTEGER PRIMARY KEY, genrecli TEXT, nomcli TEXT NOT NULL,
            prenomcli TEXT, adresse1cli TEXT, adresse2cli TEXT, adresse3cli TEXT,
            cpcli TEXT, villecli TEXT, telcli TEXT, emailcli TEXT, portcli TEXT,
            newsletter INTEGER DEFAULT 0
        );
        CREATE TABLE T_Communes (DEP INTEGER, CP TEXT, COMMUNES TEXT);
        CREATE TABLE T_dept (code_dept TEXT PRIMARY KEY, nom_dept TEXT, ordre_aff_dept INTEGER DEFAULT 0);
        CREATE TABLE T_dtlcode (codcde INTEGER, codobj INTEGER, qte INTEGER DEFAULT 1, Colis INTEGER DEFAULT 1, Commentaire TEXT);
        CREATE TABLE T_enseigne (id_enseigne INTEGER PRIMARY KEY, lb_enseigne TEXT, ville_enseigne TEXT, dept_enseigne INTEGER DEFAULT 0);
        CREATE TABLE T_entcde (
            codcde INTEGER PRIMARY KEY, datcde TEXT, codcli INTEGER,
            timbrecli REAL DEFAULT 0, timbrecde REAL DEFAULT 0,
            Nbcolis INTEGER DEFAULT 1, cheqcli REAL DEFAULT 0,
            idcondit INTEGER DEFAULT 0, cdeComt TEXT, barchive INTEGER, bstock INTEGER DEFAULT 0
        );
        CREATE TABLE T_objet (
            codobj INTEGER PRIMARY KEY, libobj TEXT, Tailleobj TEXT,
            puobj REAL DEFAULT 0, Poidsobj REAL DEFAULT 0, indispobj INTEGER,
            o_imp INTEGER DEFAULT 0, o_aff INTEGER DEFAULT 0, o_cartp INTEGER DEFAULT 0,
            idcondit INTEGER DEFAULT 0, points INTEGER DEFAULT 0, o_ordre_aff INTEGER
        );
        CREATE TABLE T_poids (valmin REAL PRIMARY KEY, valtimbre REAL DEFAULT 0);
        CREATE TABLE T_poidsV (valmin REAL PRIMARY KEY, valtimbre REAL DEFAULT 0);
        CREATE TABLE T_rel_cond (idrelcond INTEGER PRIMARY KEY, codobj INTEGER DEFAULT 0, qteobjdeb INTEGER DEFAULT 0, qteobjfin INTEGER DEFAULT 0, codcond INTEGER DEFAULT 0);
        CREATE TABLE T_utilisateur (code_utilisateur INTEGER PRIMARY KEY, nom_utilisateur TEXT, prenom_utilisateur TEXT, couleur_fond_utilisateur INTEGER DEFAULT 0, date_cde_utilisateur TEXT);
    """)
    conn.commit()
    print("  Tables créées avec succès.")


def extract_inserts_from_file(filepath):
    """Parse un fichier SQL MySQL et extrait les valeurs INSERT."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    
    match = re.search(r"INSERT\s+INTO\s+`(\w+)`\s*\(([^)]+)\)\s*VALUES\s*", content, re.IGNORECASE)
    if not match:
        return None, None, []
    
    table_name = match.group(1)
    columns = [c.strip().strip('`') for c in match.group(2).split(',')]
    values_block = content[match.end():]
    
    rows = []
    i = 0
    while i < len(values_block):
        if values_block[i] == '(':
            i += 1
            values = []
            current_val = ""
            in_string = False
            string_char = None
            while i < len(values_block):
                ch = values_block[i]
                if in_string:
                    if ch == '\\' and i + 1 < len(values_block):
                        next_ch = values_block[i + 1]
                        if next_ch == "'":
                            current_val += "''"
                            i += 2; continue
                        elif next_ch in ('\\', 'n', 'r', 't', '0'):
                            mapping = {'\\': '\\', 'n': '\n', 'r': '\r', 't': '\t', '0': ''}
                            current_val += mapping.get(next_ch, next_ch)
                            i += 2; continue
                        else:
                            current_val += next_ch
                            i += 2; continue
                    elif ch == string_char:
                        if i + 1 < len(values_block) and values_block[i + 1] == string_char:
                            current_val += ch + ch
                            i += 2; continue
                        in_string = False
                        current_val += ch
                        i += 1; continue
                    else:
                        current_val += ch
                        i += 1; continue
                else:
                    if ch in ("'", '"'):
                        in_string = True
                        string_char = ch
                        current_val += ch
                        i += 1; continue
                    elif ch == ',':
                        values.append(current_val.strip())
                        current_val = ""
                        i += 1; continue
                    elif ch == ')':
                        values.append(current_val.strip())
                        rows.append(values)
                        i += 1; break
                    else:
                        current_val += ch
                        i += 1; continue
        else:
            i += 1
    return table_name, columns, rows


def parse_value(val_str):
    """Convertit une valeur string SQL en valeur Python."""
    val_str = val_str.strip()
    if val_str.upper() == 'NULL':
        return None
    if (val_str.startswith("'") and val_str.endswith("'")):
        inner = val_str[1:-1]
        return inner.replace("''", "'")
    if (val_str.startswith('"') and val_str.endswith('"')):
        return val_str[1:-1]
    try:
        if '.' in val_str:
            return float(val_str)
        return int(val_str)
    except ValueError:
        return val_str


def import_data_file(conn, filepath):
    """Importe un fichier SQL de données."""
    table_name, columns, rows = extract_inserts_from_file(filepath)
    if not table_name:
        print(f"    Pas d'INSERT trouvé")
        return 0
    cursor = conn.cursor()
    placeholders = ",".join(["?" for _ in columns])
    col_names = ",".join([f'"{c}"' for c in columns])
    sql = f'INSERT OR IGNORE INTO {table_name} ({col_names}) VALUES ({placeholders})'
    inserted = errors = 0
    for row_values in rows:
        try:
            parsed = [parse_value(v) for v in row_values]
            if len(parsed) < len(columns):
                parsed.extend([None] * (len(columns) - len(parsed)))
            elif len(parsed) > len(columns):
                parsed = parsed[:len(columns)]
            cursor.execute(sql, parsed)
            inserted += 1
        except Exception as e:
            errors += 1
            if errors <= 2:
                print(f"    [WARN] {str(e)[:120]}")
    conn.commit()
    print(f"    {table_name}: {inserted} lignes insérées ({errors} erreurs)")
    return inserted


DATA_FILES = [
    "dept.sql", "communes.sql", "client.sql", "objet.sql", "enseigne.sql",
    "entcde.sql", "dtlcde.sql", "poids.sql", "poidsv.sql", "relcond.sql", "utilisateur.sql",
]

if __name__ == "__main__":
    print("=" * 60)
    print("DIGICHEESE - Import et Consolidation des données")
    print("=" * 60)

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)

    print("\n1. Création des tables SQLite")
    create_tables(conn)

    print("\n2. Import des données")
    for sql_file in DATA_FILES:
        filepath = os.path.join(SQL_DIR, sql_file)
        if not os.path.exists(filepath):
            print(f"  [SKIP] {sql_file}"); continue
        print(f"  [IMPORT] {sql_file}")
        import_data_file(conn, filepath)

    print("\n3. Vérification")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    for (tname,) in cursor.fetchall():
        cursor.execute(f'SELECT COUNT(*) FROM "{tname}"')
        print(f"  {tname}: {cursor.fetchone()[0]} lignes")
    conn.close()

    print("\n4. Consolidation CSV")
    conn2 = sqlite3.connect(DB_PATH)
    query = """
    SELECT e.codcde, e.datcde, strftime('%Y', e.datcde) AS annee,
        strftime('%m', e.datcde) AS mois, e.codcli, c.genrecli, c.nomcli,
        c.prenomcli, c.adresse1cli, c.cpcli, c.villecli, c.telcli,
        c.emailcli, c.portcli, c.newsletter, SUBSTR(c.cpcli, 1, 2) AS code_dept,
        d.nom_dept, e.timbrecli, e.timbrecde, e.Nbcolis, e.cheqcli,
        e.idcondit, e.barchive, e.bstock, dt.codobj, o.libobj, o.Tailleobj,
        o.puobj, o.Poidsobj, o.points AS points_obj, dt.qte, dt.Colis, dt.Commentaire
    FROM T_entcde e
    LEFT JOIN T_dtlcode dt ON e.codcde = dt.codcde
    LEFT JOIN T_objet o ON dt.codobj = o.codobj
    LEFT JOIN T_client c ON e.codcli = c.codcli
    LEFT JOIN T_dept d ON SUBSTR(c.cpcli, 1, 2) = d.code_dept
    ORDER BY e.datcde, e.codcde
    """
    cur = conn2.cursor()
    cur.execute(query)
    columns = [d[0] for d in cur.description]
    rows = cur.fetchall()
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(columns)
        writer.writerows(rows)
    print(f"  {len(rows)} lignes exportées vers {OUTPUT_CSV}")
    conn2.close()
    print("\n[TERMINÉ]")
