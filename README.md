# 🧀 Digicheese — Datawarehouse & Analyse Décisionnelle

> Projet Data Engineer 2024-D08 — Diginamic  
> Mise en œuvre d'un entrepôt de données, pipeline MapReduce et restitution dashboard

---

## Contexte

La fromagerie **Digicheese** dispose de données de commandes depuis 2002 (90 000+ commandes, 36 000+ clients, 160 000+ lignes de détail). Ce projet implémente la chaîne complète :

1. **Import** des dumps SQL MySQL dans une base exploitable (SQLite)
2. **Consolidation** des données en un fichier CSV unique (jointures)
3. **Analyse MapReduce** (Hadoop Streaming) pour chaque lot demandé
4. **Restitution** via un dashboard interactif (Chart.js)

---

## Structure du projet

```
digicheese-datawarehouse/
│
├── README.md
├── .gitignore
├── run_all.sh                          # Script principal : import + lots + MapReduce
├── run_mapreduce.sh                    # Lancement des jobs MapReduce seuls
│
├── scripts/
│   ├── 01_import_and_consolidate.py    # ETL : MySQL dumps → SQLite → CSV consolidé
│   └── 02_run_lots.py                  # Requêtes SQL des Lots 1/2/3 → JSON
│
├── mapreduce/
│   ├── lot1a/
│   │   ├── mapper_lot1a.py             # Filtre Nantes + 2020, émet (codcde → qte)
│   │   └── reducer_lot1a.py            # Agrège par commande, sélectionne la meilleure
│   ├── lot1b/
│   │   ├── mapper_lot1b.py             # Filtre 2010–2015, émet (année → codcde)
│   │   └── reducer_lot1b.py            # COUNT DISTINCT commandes par année
│   ├── lot1c/
│   │   ├── mapper_lot1c.py             # Émet (codcli → codcde, qte, timbrecde)
│   │   └── reducer_lot1c.py            # Agrège par client, déduplique, max timbrecde
│   ├── lot2/
│   │   ├── mapper_lot2.py              # Filtre 2006–2010, depts 53/61/28
│   │   └── reducer_lot2.py             # Agrège + tri → top 100
│   └── lot3/
│       ├── mapper_lot3.py              # Filtre 2011–2016, depts 22/49/53, sans timbrecli
│       └── reducer_lot3.py             # Top 100, sample 5%, moyenne/type, par ville
│
├── sql/
│   ├── requetes_lots.sql               # Requêtes SQL documentées (tous les lots)
│   └── sql_dumps/                      # Dumps MySQL originaux
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
├── data/
│   └── results/
│       ├── all_results.json            # Résultats SQL (JSON) pour le dashboard
│       └── mapreduce/
│           ├── lot1a_result.txt
│           ├── lot1b_result.txt
│           ├── lot1c_result.txt
│           ├── lot2_result.txt
│           └── lot3_result.txt
│
└── dashboards/
    └── dashboard.html                  # Dashboard interactif autonome (Chart.js)
```

> **Note :** Le CSV consolidé (32 MB) et la base SQLite sont dans le `.gitignore` car régénérables via `run_all.sh`.

---

## Prérequis

- **Python 3.8+** (aucune dépendance externe, stdlib uniquement : `sqlite3`, `csv`, `json`)
- **Bash** (pour les scripts shell)
- Un navigateur web (pour le dashboard)

---

## Guide d'exécution

### Tout lancer d'un coup

```bash
chmod +x run_all.sh
./run_all.sh
```

### Étape par étape

#### 1. Import et consolidation

```bash
python3 scripts/01_import_and_consolidate.py sql/sql_dumps data/consolidation_digicheese.csv data/digicheese.db
```

Ce script :
- Crée les tables SQLite (conversion automatique du schéma MySQL)
- Importe les 12 fichiers de données (parser custom qui gère les quotes échappées MySQL)
- Exporte un **CSV consolidé unique** avec les jointures : commandes + détails + objets + clients + départements

#### 2. Exécuter les requêtes SQL (Lots 1, 2, 3)

```bash
python3 scripts/02_run_lots.py data/digicheese.db data/results
```

#### 3. Exécuter le pipeline MapReduce

```bash
chmod +x run_mapreduce.sh
./run_mapreduce.sh data/consolidation_digicheese.csv
```

Chaque job suit le pattern **Hadoop Streaming** :
```bash
cat input.csv | python3 mapper.py | sort | python3 reducer.py
```

Les mapper/reducer sont déployables tels quels sur un cluster Hadoop :
```bash
hadoop jar hadoop-streaming.jar \
  -mapper  mapreduce/lot2/mapper_lot2.py \
  -reducer mapreduce/lot2/reducer_lot2.py \
  -input   /data/consolidation_digicheese.csv \
  -output  /output/lot2
```

#### 4. Ouvrir le dashboard

Ouvrir `dashboards/dashboard.html` dans un navigateur. Le dashboard est **autonome** (données JSON embarquées, Chart.js via CDN).

---

## Résultats des Lots

### Définition : "Meilleure commande"

Conformément au sujet :
- **Filtre prioritaire :** plus grande somme des quantités (`SUM(qte) DESC`)
- **Filtre secondaire :** plus grand timbrecde (`timbrecde DESC`)

### Lot 1

**1a — Meilleure commande de Nantes, année 2020 :**

| Champ | Valeur |
|---|---|
| Code commande | `85301` |
| Client | Joël SAVARY |
| Date | 2020-01-08 |
| Somme quantités | **6** |
| Timbrecde | 3.05 € |

**1b — Nombre total de commandes 2010–2015, par année :**

| Année | Nb commandes |
|---|---:|
| 2010 | 5 599 |
| 2011 | 4 882 |
| 2012 | 3 979 |
| 2013 | 3 629 |
| 2014 | 3 816 |
| 2015 | 3 749 |
| **Total** | **25 654** |

**1c — Client avec le plus de frais de timbrecde :**

| Champ | Valeur |
|---|---|
| Client | Nicole CROTTÉ |
| Nb commandes | 76 |
| Somme quantités | 194 |
| Total timbrecde | **437.80 €** |

### Lot 2

Filtre : **2006–2010**, départements **53** (Mayenne), **61** (Orne), **28** (Eure-et-Loir)  
→ 100 meilleures commandes extraites

| # | Code | Ville | Σ Qté | Timbrecde |
|---|---|---|---:|---:|
| 1 | 25862 | ARROU | 42 | 9.85 € |
| 2 | 42997 | ST GEORGES DES GROSEILLERS | 33 | 6.40 € |
| 3 | 25861 | ARROU | 30 | 7.85 € |
| ... | ... | ... | ... | ... |

*(100 lignes complètes dans `data/results/mapreduce/lot2_result.txt`)*

### Lot 3

Filtre : **2011–2016**, départements **22**, **49**, **53**, sans timbrecli (NULL ou 0)  
→ 100 meilleures commandes, puis **échantillon aléatoire 5%** (5 commandes)  
→ Calcul de la **moyenne des quantités par type d'objet** : `SUM(qte) / COUNT(DISTINCT codobj)`  
→ Graphique **par ville** (camembert) dans le dashboard, onglet Lot 3

---

## Architecture MapReduce

```
                    ┌─────────────────────────────────────────┐
                    │         consolidation_digicheese.csv     │
                    │       (163 778 lignes, 33 colonnes)      │
                    └──────────────┬──────────────────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │         MAPPER               │
                    │  • Lit stdin ligne par ligne  │
                    │  • Filtre (année, dept, ...)  │
                    │  • Émet : clé \t valeurs      │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │      SORT (shuffle)          │
                    │  • Tri par clé (shell sort   │
                    │    ou Hadoop shuffle/sort)    │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │         REDUCER              │
                    │  • Agrège par clé            │
                    │  • Calculs : SUM, COUNT,     │
                    │    MAX, RANDOM, AVG...        │
                    │  • Émet le résultat final     │
                    └─────────────────────────────┘
```

| Lot | Clé Mapper | Valeur Mapper | Logique Reducer |
|-----|-----------|---------------|-----------------|
| 1a | `codcde` | `qte, timbrecde, client` | Agrège par commande → meilleure |
| 1b | `année` | `codcde` | COUNT DISTINCT par année |
| 1c | `codcli` | `codcde, qte, timbrecde` | Déduplique timbrecde/cde → client max |
| 2 | `codcde` | `qte, timbrecde, ville` | Agrège → tri → top 100 |
| 3 | `codcde` | `codobj, qte, timbrecde, ville` | Agrège → top 100 → sample 5% → par ville |

---

## Schéma de la base

```
T_entcde (90 215 commandes)         T_client (36 482 clients)
┌─────────────────────┐             ┌──────────────────────┐
│ codcde PK           │             │ codcli PK            │
│ datcde              │──── FK ────▶│ nomcli, prenomcli    │
│ codcli FK           │             │ villecli, cpcli      │
│ timbrecli           │             │ emailcli, telcli     │
│ timbrecde           │             └──────────┬───────────┘
│ Nbcolis, cheqcli    │                        │
└────────┬────────────┘                SUBSTR(cpcli,1,2)
         │                                     │
         │ codcde                    ┌──────────▼───────────┐
┌────────▼────────────┐             │ T_dept (96 depts)     │
│ T_dtlcode           │             │ code_dept PK          │
│ (163 829 lignes)    │             │ nom_dept              │
│ codcde FK           │             └───────────────────────┘
│ codobj FK ──────────│──┐
│ qte, Colis          │  │   ┌─────────────────────────┐
└─────────────────────┘  └──▶│ T_objet (131 objets)    │
                              │ codobj PK               │
                              │ libobj, Tailleobj       │
                              │ puobj, Poidsobj, points │
                              └─────────────────────────┘
```

---

## Technologies

| Composant | Technologie |
|---|---|
| Base de données | SQLite (via Python `sqlite3`) |
| ETL / Import | Python 3 — parser MySQL custom |
| Consolidation | SQL (jointures multi-tables) → CSV unique |
| MapReduce | Python stdin/stdout (Hadoop Streaming compatible) |
| Requêtes analytiques | SQL (CTE, agrégations, RANDOM) |
| Dashboard | HTML + CSS + Chart.js 4 |

---

## Auteurs

Projet réalisé dans le cadre de la formation **Data Engineer 2024-D08** — Diginamic.
