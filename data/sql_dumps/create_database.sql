DROP DATABASE IF EXISTS `digicheese`;
CREATE DATABASE IF NOT EXISTS `digicheese`;
USE `digicheese`;

CREATE TABLE `T_client` (
  `codcli` INTEGER NOT NULL AUTO_INCREMENT, 
  `genrecli` VARCHAR(8), 
  `nomcli` VARCHAR(40) NOT NULL, 
  `prenomcli` VARCHAR(30), 
  `adresse1cli` VARCHAR(50), 
  `adresse2cli` VARCHAR(50), 
  `adresse3cli` VARCHAR(255), 
  `cpcli` VARCHAR(5), 
  `villecli` VARCHAR(50), 
  `telcli` VARCHAR(10), 
  `emailcli` LONGTEXT, 
  `portcli` VARCHAR(10), 
  `newsletter` TINYINT(1) DEFAULT 0, 
  INDEX (`nomcli`), 
  PRIMARY KEY (`codcli`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

CREATE TABLE `T_Communes` (
  `DEP` TINYINT(3) UNSIGNED, 
  `CP` VARCHAR(5), 
  `COMMUNES` VARCHAR(50), 
  INDEX (`COMMUNES`), 
  INDEX (`CP`), 
  INDEX (`DEP`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

CREATE TABLE `T_dept` (
  `code_dept` VARCHAR(2) NOT NULL, 
  `nom_dept` VARCHAR(50), 
  `ordre_aff_dept` INTEGER DEFAULT 0, 
  PRIMARY KEY (`code_dept`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

CREATE TABLE `T_dtlcode` (
  `codcde` INTEGER, 
  `codobj` INTEGER, 
  `qte` INTEGER DEFAULT 1, 
  `Colis` INTEGER DEFAULT 1, 
  `Commentaire` VARCHAR(100), 
  INDEX (`codobj`), 
  INDEX (`codcde`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

CREATE TABLE `T_enseigne` (
  `id_enseigne` INTEGER NOT NULL AUTO_INCREMENT, 
  `lb_enseigne` VARCHAR(50), 
  `ville_enseigne` VARCHAR(50), 
  `dept_enseigne` INTEGER DEFAULT 0, 
  PRIMARY KEY (`id_enseigne`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

CREATE TABLE `T_entcde` (
  `codcde` INTEGER NOT NULL AUTO_INCREMENT, 
  `datcde` DATETIME, 
  `codcli` INTEGER, 
  `timbrecli` FLOAT NULL DEFAULT 0, 
  `timbrecde` FLOAT NULL DEFAULT 0, 
  `Nbcolis` TINYINT(3) UNSIGNED DEFAULT 1, 
  `cheqcli` FLOAT NULL DEFAULT 0, 
  `idcondit` INTEGER DEFAULT 0, 
  `cdeComt` LONGTEXT, 
  `barchive` TINYINT(1), 
  `bstock` TINYINT(1) DEFAULT 0, 
  INDEX (`cdeComt`(100)), 
  PRIMARY KEY (`codcde`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

CREATE TABLE `T_objet` (
  `codobj` INTEGER NOT NULL AUTO_INCREMENT, 
  `libobj` VARCHAR(50), 
  `Tailleobj` VARCHAR(50), 
  `puobj` DECIMAL(19,4) DEFAULT 0, 
  `Poidsobj` DECIMAL(19,4) DEFAULT 0, 
  `indispobj` TINYINT(1), 
  `o_imp` INTEGER DEFAULT 0, 
  `o_aff` INTEGER DEFAULT 0, 
  `o_cartp` TINYINT(1) DEFAULT 0, 
  `idcondit` INTEGER DEFAULT 0, 
  `points` INTEGER DEFAULT 0, 
  `o_ordre_aff` INTEGER, 
  PRIMARY KEY (`codobj`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

CREATE TABLE `T_poids` (
  `valmin` FLOAT NOT NULL DEFAULT 0, 
  `valtimbre` FLOAT NULL DEFAULT 0, 
  PRIMARY KEY (`valmin`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

CREATE TABLE `T_poidsV` (
  `valmin` FLOAT NOT NULL DEFAULT 0, 
  `valtimbre` FLOAT NULL DEFAULT 0, 
  PRIMARY KEY (`valmin`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

CREATE TABLE `T_rel_cond` (
  `idrelcond` INTEGER NOT NULL AUTO_INCREMENT, 
  `codobj` INTEGER DEFAULT 0, 
  `qteobjdeb` INTEGER DEFAULT 0, 
  `qteobjfin` INTEGER DEFAULT 0, 
  `codcond` INTEGER DEFAULT 0, 
  PRIMARY KEY (`idrelcond`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `T_utilisateur`;
CREATE TABLE `T_utilisateur` (
  `code_utilisateur` INTEGER NOT NULL AUTO_INCREMENT, 
  `nom_utilisateur` VARCHAR(50), 
  `prenom_utilisateur` VARCHAR(50), 
  `couleur_fond_utilisateur` INTEGER DEFAULT 0, 
  `date_cde_utilisateur` DATETIME, 
  INDEX (`code_utilisateur`), 
  PRIMARY KEY (`code_utilisateur`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

SET autocommit=1;