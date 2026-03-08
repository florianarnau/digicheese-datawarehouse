-- ============================================================
-- DIGICHEESE - Requêtes SQL pour les Lots 1, 2 et 3
-- ============================================================
-- Définition "Meilleure commande" :
--   Prioritaire : Plus grande somme des quantités
--   Secondaire  : Plus grand timbrecde
-- ============================================================

-- LOT 1a : Meilleure commande de Nantes 2020
SELECT e.codcde, e.datcde, c.nomcli, c.prenomcli, c.villecli,
    SUM(dt.qte) AS somme_quantites, e.timbrecde
FROM T_entcde e
JOIN T_dtlcode dt ON e.codcde = dt.codcde
JOIN T_client c ON e.codcli = c.codcli
WHERE UPPER(c.villecli) LIKE '%NANTES%'
  AND strftime('%Y', e.datcde) = '2020'
GROUP BY e.codcde
ORDER BY somme_quantites DESC, e.timbrecde DESC
LIMIT 1;

-- LOT 1b : Commandes 2010-2015 par année
SELECT strftime('%Y', e.datcde) AS annee,
    COUNT(DISTINCT e.codcde) AS nb_commandes
FROM T_entcde e
WHERE strftime('%Y', e.datcde) BETWEEN '2010' AND '2015'
GROUP BY annee ORDER BY annee;

-- LOT 1c : Client avec le plus de frais de timbrecde
WITH ct AS (
    SELECT codcli, SUM(timbrecde) AS total_timbrecde, COUNT(*) AS nb_commandes
    FROM T_entcde GROUP BY codcli ORDER BY total_timbrecde DESC LIMIT 1
)
SELECT c.nomcli, c.prenomcli, ct.nb_commandes,
    (SELECT SUM(dt.qte) FROM T_entcde e2
     JOIN T_dtlcode dt ON e2.codcde = dt.codcde
     WHERE e2.codcli = ct.codcli) AS somme_quantites,
    ct.total_timbrecde
FROM ct JOIN T_client c ON ct.codcli = c.codcli;

-- LOT 2 : Top 100 (2006-2010, depts 53/61/28)
SELECT e.codcde, e.datcde, c.villecli AS ville,
    SUM(dt.qte) AS somme_quantites, e.timbrecde
FROM T_entcde e
JOIN T_dtlcode dt ON e.codcde = dt.codcde
JOIN T_client c ON e.codcli = c.codcli
WHERE strftime('%Y', e.datcde) BETWEEN '2006' AND '2010'
  AND SUBSTR(c.cpcli, 1, 2) IN ('53', '61', '28')
GROUP BY e.codcde
ORDER BY somme_quantites DESC, e.timbrecde DESC
LIMIT 100;

-- LOT 3 : 5% aléatoire des top 100 (2011-2016, depts 22/49/53, sans timbrecli)
SELECT * FROM (
    SELECT e.codcde, e.datcde, c.villecli AS ville,
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
) ORDER BY RANDOM() LIMIT 5;
