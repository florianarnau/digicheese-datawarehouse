-- ============================================================
-- DIGICHEESE - Requêtes SQL pour les Lots 1, 2 et 3
-- ============================================================

-- ============================================================
-- DEFINITION : "Meilleure commande"
--   a. Filtre prioritaire : Plus grande somme des quantités
--   b. Filtre secondaire : Plus grand nombre de timbrecde
-- ============================================================

-- ============================================================
-- LOT 1
-- ============================================================

-- LOT 1a : La meilleure commande de Nantes de l'année 2020
-- ---------------------------------------------------------
SELECT
    e.codcde,
    e.datcde,
    c.nomcli,
    c.prenomcli,
    c.villecli,
    SUM(dt.qte) AS somme_quantites,
    e.timbrecde
FROM T_entcde e
JOIN T_dtlcode dt ON e.codcde = dt.codcde
JOIN T_client c ON e.codcli = c.codcli
WHERE UPPER(c.villecli) LIKE '%NANTES%'
  AND strftime('%Y', e.datcde) = '2020'
GROUP BY e.codcde
ORDER BY somme_quantites DESC, e.timbrecde DESC
LIMIT 1;


-- LOT 1b : Nombre total de commandes entre 2010 et 2015, réparties par année
-- ---------------------------------------------------------------------------
SELECT
    strftime('%Y', e.datcde) AS annee,
    COUNT(DISTINCT e.codcde) AS nb_commandes
FROM T_entcde e
WHERE strftime('%Y', e.datcde) BETWEEN '2010' AND '2015'
GROUP BY annee
ORDER BY annee;


-- LOT 1c : Client avec le plus de frais de timbrecde
-- Nom, prénom, nb commandes, somme des quantités d'objets
-- --------------------------------------------------------
SELECT
    c.nomcli,
    c.prenomcli,
    COUNT(DISTINCT e.codcde) AS nb_commandes,
    SUM(dt.qte) AS somme_quantites,
    SUM(e.timbrecde) AS total_timbrecde
FROM T_entcde e
JOIN T_client c ON e.codcli = c.codcli
JOIN T_dtlcode dt ON e.codcde = dt.codcde
GROUP BY e.codcli
ORDER BY total_timbrecde DESC
LIMIT 1;


-- ============================================================
-- LOT 2
-- ============================================================

-- LOT 2a+b+c : Filtrer 2006-2010, départements 53, 61, 28
-- Top 100 meilleures commandes (somme qte DESC, timbrecde DESC)
-- avec ville, somme des quantités, timbrecde
-- ---------------------------------------------------------------
SELECT
    e.codcde,
    e.datcde,
    c.villecli AS ville,
    SUM(dt.qte) AS somme_quantites,
    e.timbrecde
FROM T_entcde e
JOIN T_dtlcode dt ON e.codcde = dt.codcde
JOIN T_client c ON e.codcli = c.codcli
WHERE strftime('%Y', e.datcde) BETWEEN '2006' AND '2010'
  AND SUBSTR(c.cpcli, 1, 2) IN ('53', '61', '28')
GROUP BY e.codcde
ORDER BY somme_quantites DESC, e.timbrecde DESC
LIMIT 100;


-- ============================================================
-- LOT 3
-- ============================================================

-- LOT 3a+b : Filtrer 2011-2016, départements 22, 49, 53
-- 100 meilleures commandes, puis 5% aléatoire
-- Sans timbrecli (NULL ou 0)
-- Avec moyenne des quantités par type d'objet
-- ---------------------------------------------------------------

-- D'abord les 100 meilleures commandes filtrées
-- Puis on prend 5% aléatoirement (= 5 commandes)

SELECT *
FROM (
    SELECT
        e.codcde,
        e.datcde,
        c.villecli AS ville,
        SUM(dt.qte) AS somme_quantites,
        COUNT(DISTINCT dt.codobj) AS nb_types_objets,
        ROUND(CAST(SUM(dt.qte) AS REAL) / COUNT(DISTINCT dt.codobj), 2) AS moyenne_qte_par_type,
        e.timbrecde
    FROM T_entcde e
    JOIN T_dtlcode dt ON e.codcde = dt.codcde
    JOIN T_client c ON e.codcli = c.codcli
    WHERE strftime('%Y', e.datcde) BETWEEN '2011' AND '2016'
      AND SUBSTR(c.cpcli, 1, 2) IN ('22', '49', '53')
      AND (e.timbrecli IS NULL OR e.timbrecli = 0)
    GROUP BY e.codcde
    ORDER BY somme_quantites DESC, e.timbrecde DESC
    LIMIT 100
)
ORDER BY RANDOM()
LIMIT 5;
