# Digicheese — Datawarehouse & Analyse Décisionnelle

> Projet Data Engineer 2024-D08 — Diginamic  
> Entrepôt de données, pipeline MapReduce, dashboard interactif

---

## Lancer le projet

```bash
git clone https://github.com/florianarnau/digicheese-datawarehouse.git
cd digicheese-datawarehouse
bash run_all.sh
```

C'est tout. Le script enchaîne automatiquement :
1. Import des dumps SQL → SQLite + CSV consolidé
2. Requêtes SQL des 3 lots → JSON
3. Pipeline MapReduce (5 lots)

Puis ouvrir `dashboards/dashboard.html` dans un navigateur.

**Prérequis :** Python 3.8+ (aucune dépendance externe)

---

## Arborescence

```
digicheese-datawarehouse/
│
├── .gitignore
├── README.md
├── run_all.sh                          ← lance tout
├── run_mapreduce.sh                    ← lance les MapReduce seuls
│
├── scripts/
│   ├── 01_import_and_consolidate.py    ← ETL : SQL dumps → SQLite → CSV
│   └── 02_run_lots.py                  ← requêtes SQL lots 1/2/3 → JSON
│
├── mapreduce/
│   ├── lot1a/
│   │   ├── mapper_lot1a.py
│   │   └── reducer_lot1a.py
│   ├── lot1b/
│   │   ├── mapper_lot1b.py
│   │   └── reducer_lot1b.py
│   ├── lot1c/
│   │   ├── mapper_lot1c.py
│   │   └── reducer_lot1c.py
│   ├── lot2/
│   │   ├── mapper_lot2.py
│   │   └── reducer_lot2.py
│   └── lot3/
│       ├── mapper_lot3.py
│       └── reducer_lot3.py
│
├── sql/
│   ├── requetes_lots.sql               ← requêtes SQL documentées
│   └── sql_dumps/                      ← 12 dumps MySQL originaux
│       ├── create_database.sql
│       ├── client.sql
│       ├── communes.sql
│       ├── dept.sql
│       ├── dtlcde.sql
│       ├── enseigne.sql
│       ├── entcde.sql
│       ├── objet.sql
│       ├── poids.sql
│       ├── poidsv.sql
│       ├── relcond.sql
│       └── utilisateur.sql
│
├── data/                               ← généré par run_all.sh
│   ├── consolidation_digicheese.csv    (gitignore, 32 MB)
│   ├── digicheese.db                   (gitignore)
│   └── results/
│       ├── all_results.json
│       └── mapreduce/
│           ├── lot1a_result.txt
│           ├── lot1b_result.txt
│           ├── lot1c_result.txt
│           ├── lot2_result.txt
│           └── lot3_result.txt
│
└── dashboards/
    └── dashboard.html                  ← ouvrir dans le navigateur
```

---

## Résultats

### Lot 1a — Meilleure commande de Nantes 2020

| Champ | Valeur |
|---|---|
| Commande | #85301 |
| Client | Joël SAVARY |
| Date | 2020-01-08 |
| Σ quantités | **6** |
| Timbrecde | 3.05 € |

### Lot 1b — Commandes 2010–2015

| Année | Commandes |
|---|---:|
| 2010 | 5 599 |
| 2011 | 4 882 |
| 2012 | 3 979 |
| 2013 | 3 629 |
| 2014 | 3 816 |
| 2015 | 3 749 |
| **Total** | **25 654** |

### Lot 1c — Client max timbrecde

| Champ | Valeur |
|---|---|
| Client | Nicole CROTTÉ |
| Commandes | 76 |
| Σ quantités | 194 |
| Total timbrecde | **437.80 €** |

### Lot 2

100 meilleures commandes (2006–2010, depts 53/61/28). Top 3 :
1. Cde 25862 — ARROU — 42 articles — 9.85 €
2. Cde 42997 — ST GEORGES DES GROSEILLERS — 33 articles — 6.40 €
3. Cde 25861 — ARROU — 30 articles — 7.85 €

### Lot 3

5% aléatoire des 100 meilleures (2011–2016, depts 22/49/53, sans timbrecli).
Graphique par ville dans le dashboard.

---

## Architecture MapReduce

```
CSV consolidé → MAPPER (filtre + émet clé/valeur)
             → SORT (shuffle)
             → REDUCER (agrège + résultat)
```

Compatible **Hadoop Streaming** :
```bash
# Local
cat data.csv | python3 mapper.py | sort | python3 reducer.py

# Hadoop
hadoop jar hadoop-streaming.jar \
  -mapper mapper_lot2.py -reducer reducer_lot2.py \
  -input /data/consolidation.csv -output /output/lot2
```

---

## Technologies

| Composant | Outil |
|---|---|
| BDD | SQLite (Python sqlite3) |
| ETL | Python 3 (parser MySQL custom) |
| MapReduce | Python stdin/stdout (Hadoop Streaming) |
| Dashboard | HTML + Chart.js 4 |
| Requêtes | SQL (CTE, agrégations) |
