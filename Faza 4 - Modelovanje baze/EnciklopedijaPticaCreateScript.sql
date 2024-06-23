DROP SCHEMA IF EXISTS `EnciklopedijaPtica` ;
CREATE SCHEMA IF NOT EXISTS `EnciklopedijaPtica`;
USE `EnciklopedijaPtica`;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- GTID state at the beginning of the backup 
--

--
-- Table structure for table `Clanak`
--

DROP TABLE IF EXISTS `Clanak`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Clanak` (
  `IDClanka` int NOT NULL AUTO_INCREMENT,
  `Sadrzaj` longtext,
  `DatumVremeKreiranja` datetime NOT NULL,
  `BrojOcena` int NOT NULL,
  `ZbirOcena` int NOT NULL,
  `IDAutora` bigint NOT NULL,
  PRIMARY KEY (`IDClanka`),
  KEY `Clanak_IDAutora_2a5f8be4_fk_Korisnik_id` (`IDAutora`),
  CONSTRAINT `Clanak_IDAutora_2a5f8be4_fk_Korisnik_id` FOREIGN KEY (`IDAutora`) REFERENCES `Korisnik` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Diskusija`
--

DROP TABLE IF EXISTS `Diskusija`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Diskusija` (
  `IDDiskusije` int NOT NULL AUTO_INCREMENT,
  `Sadrzaj` varchar(400) NOT NULL,
  `DatumVremeKreiranja` datetime NOT NULL,
  `IDClanka` int NOT NULL,
  `IDPokretaca` bigint NOT NULL,
  `NaslovDiskusije` varchar(60) NOT NULL,
  PRIMARY KEY (`IDDiskusije`),
  KEY `Diskusija_IDClanka_2b34507d_fk_Clanak_IDClanka` (`IDClanka`),
  KEY `Diskusija_IDPokretaca_8d6d83ea_fk_Korisnik_id` (`IDPokretaca`),
  CONSTRAINT `Diskusija_IDClanka_2b34507d_fk_Clanak_IDClanka` FOREIGN KEY (`IDClanka`) REFERENCES `Clanak` (`IDClanka`),
  CONSTRAINT `Diskusija_IDPokretaca_8d6d83ea_fk_Korisnik_id` FOREIGN KEY (`IDPokretaca`) REFERENCES `Korisnik` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `FotografijaGalerija`
--

DROP TABLE IF EXISTS `FotografijaGalerija`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `FotografijaGalerija` (
  `IDFotografije` int NOT NULL AUTO_INCREMENT,
  `SadrzajSlike` longblob NOT NULL,
  `DatumVremePostavljanja` datetime NOT NULL,
  `IDAutora` bigint NOT NULL,
  `IDClanka` int NOT NULL,
  PRIMARY KEY (`IDFotografije`),
  KEY `FotografijaGalerija_IDAutora_ea20ca14_fk_Korisnik_id` (`IDAutora`),
  KEY `FotografijaGalerija_IDClanka_157298e7_fk_Clanak_IDClanka` (`IDClanka`),
  CONSTRAINT `FotografijaGalerija_IDAutora_ea20ca14_fk_Korisnik_id` FOREIGN KEY (`IDAutora`) REFERENCES `Korisnik` (`id`),
  CONSTRAINT `FotografijaGalerija_IDClanka_157298e7_fk_Clanak_IDClanka` FOREIGN KEY (`IDClanka`) REFERENCES `Clanak` (`IDClanka`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Komentar`
--

DROP TABLE IF EXISTS `Komentar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Komentar` (
  `IDKomentara` int NOT NULL AUTO_INCREMENT,
  `Sadrzaj` varchar(400) NOT NULL,
  `DatumVremePostavljanja` datetime NOT NULL,
  `IDDiskusije` int NOT NULL,
  `IDKorisnika` bigint NOT NULL,
  PRIMARY KEY (`IDKomentara`),
  KEY `Komentar_IDDiskusije_6ce098c6_fk_Diskusija_IDDiskusije` (`IDDiskusije`),
  KEY `Komentar_IDKorisnika_e3925520_fk_Korisnik_id` (`IDKorisnika`),
  CONSTRAINT `Komentar_IDDiskusije_6ce098c6_fk_Diskusija_IDDiskusije` FOREIGN KEY (`IDDiskusije`) REFERENCES `Diskusija` (`IDDiskusije`),
  CONSTRAINT `Komentar_IDKorisnika_e3925520_fk_Korisnik_id` FOREIGN KEY (`IDKorisnika`) REFERENCES `Korisnik` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Korisnik`
--

DROP TABLE IF EXISTS `Korisnik`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Korisnik` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `Tip` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Korisnik_groups`
--

DROP TABLE IF EXISTS `Korisnik_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Korisnik_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `korisnik_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Korisnik_groups_korisnik_id_group_id_db032ddd_uniq` (`korisnik_id`,`group_id`),
  KEY `Korisnik_groups_group_id_980cdc2e_fk_auth_group_id` (`group_id`),
  CONSTRAINT `Korisnik_groups_group_id_980cdc2e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `Korisnik_groups_korisnik_id_a52b6905_fk_Korisnik_id` FOREIGN KEY (`korisnik_id`) REFERENCES `Korisnik` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Korisnik_user_permissions`
--

DROP TABLE IF EXISTS `Korisnik_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Korisnik_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `korisnik_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Korisnik_user_permission_korisnik_id_permission_i_6d3ef4bb_uniq` (`korisnik_id`,`permission_id`),
  KEY `Korisnik_user_permis_permission_id_c771180b_fk_auth_perm` (`permission_id`),
  CONSTRAINT `Korisnik_user_permis_permission_id_c771180b_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `Korisnik_user_permissions_korisnik_id_1478424b_fk_Korisnik_id` FOREIGN KEY (`korisnik_id`) REFERENCES `Korisnik` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `NepravilnostClanak`
--

DROP TABLE IF EXISTS `NepravilnostClanak`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `NepravilnostClanak` (
  `IDPrijave` int NOT NULL,
  `Opis` varchar(400) NOT NULL,
  `IDClanka` int NOT NULL,
  PRIMARY KEY (`IDPrijave`),
  KEY `NepravilnostClanak_IDClanka_1628f99c_fk_Clanak_IDClanka` (`IDClanka`),
  CONSTRAINT `NepravilnostClanak_IDClanka_1628f99c_fk_Clanak_IDClanka` FOREIGN KEY (`IDClanka`) REFERENCES `Clanak` (`IDClanka`),
  CONSTRAINT `NepravilnostClanak_IDPrijave_b3c20da3_fk_PrijavaNe` FOREIGN KEY (`IDPrijave`) REFERENCES `PrijavaNepravilnosti` (`IDPrijave`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `NepravilnostDiskusija`
--

DROP TABLE IF EXISTS `NepravilnostDiskusija`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `NepravilnostDiskusija` (
  `IDPrijave` int NOT NULL,
  `IDDiskusije` int NOT NULL,
  `IDRazlogDiskusija` int NOT NULL,
  PRIMARY KEY (`IDPrijave`),
  KEY `NepravilnostDiskusij_IDDiskusije_fdacc081_fk_Diskusija` (`IDDiskusije`),
  KEY `NepravilnostDiskusij_IDRazlogDiskusija_486d5523_fk_RazlogPri` (`IDRazlogDiskusija`),
  CONSTRAINT `NepravilnostDiskusij_IDDiskusije_fdacc081_fk_Diskusija` FOREIGN KEY (`IDDiskusije`) REFERENCES `Diskusija` (`IDDiskusije`),
  CONSTRAINT `NepravilnostDiskusij_IDPrijave_4aeca061_fk_PrijavaNe` FOREIGN KEY (`IDPrijave`) REFERENCES `PrijavaNepravilnosti` (`IDPrijave`),
  CONSTRAINT `NepravilnostDiskusij_IDRazlogDiskusija_486d5523_fk_RazlogPri` FOREIGN KEY (`IDRazlogDiskusija`) REFERENCES `RazlogPrijaveDiskusija` (`IDRazlogDiskusija`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `NepravilnostFotografija`
--

DROP TABLE IF EXISTS `NepravilnostFotografija`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `NepravilnostFotografija` (
  `IDPrijave` int NOT NULL,
  `IDFotografije` int NOT NULL,
  `IDRazlogFotografija` int NOT NULL,
  PRIMARY KEY (`IDPrijave`),
  KEY `NepravilnostFotograf_IDFotografije_fa7b4adc_fk_Fotografi` (`IDFotografije`),
  KEY `NepravilnostFotograf_IDRazlogFotografija_9255accb_fk_RazlogPri` (`IDRazlogFotografija`),
  CONSTRAINT `NepravilnostFotograf_IDFotografije_fa7b4adc_fk_Fotografi` FOREIGN KEY (`IDFotografije`) REFERENCES `FotografijaGalerija` (`IDFotografije`),
  CONSTRAINT `NepravilnostFotograf_IDPrijave_d32216ef_fk_PrijavaNe` FOREIGN KEY (`IDPrijave`) REFERENCES `PrijavaNepravilnosti` (`IDPrijave`),
  CONSTRAINT `NepravilnostFotograf_IDRazlogFotografija_9255accb_fk_RazlogPri` FOREIGN KEY (`IDRazlogFotografija`) REFERENCES `RazlogPrijaveFotografije` (`IDRazlogFotografija`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `NepravilnostKomentar`
--

DROP TABLE IF EXISTS `NepravilnostKomentar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `NepravilnostKomentar` (
  `IDPrijave` int NOT NULL,
  `IDKomentara` int NOT NULL,
  `IDRazlogKomentar` int NOT NULL,
  PRIMARY KEY (`IDPrijave`),
  KEY `NepravilnostKomentar_IDKomentara_64430f8a_fk_Komentar_` (`IDKomentara`),
  KEY `NepravilnostKomentar_IDRazlogKomentar_708f824a_fk_RazlogPri` (`IDRazlogKomentar`),
  CONSTRAINT `NepravilnostKomentar_IDKomentara_64430f8a_fk_Komentar_` FOREIGN KEY (`IDKomentara`) REFERENCES `Komentar` (`IDKomentara`),
  CONSTRAINT `NepravilnostKomentar_IDPrijave_2cfb4284_fk_PrijavaNe` FOREIGN KEY (`IDPrijave`) REFERENCES `PrijavaNepravilnosti` (`IDPrijave`),
  CONSTRAINT `NepravilnostKomentar_IDRazlogKomentar_708f824a_fk_RazlogPri` FOREIGN KEY (`IDRazlogKomentar`) REFERENCES `RazlogPrijaveKomentar` (`IDRazlogKomentar`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Ocena`
--

DROP TABLE IF EXISTS `Ocena`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Ocena` (
  `IDOcene` int NOT NULL AUTO_INCREMENT,
  `DatumVremeOcenjivanja` datetime(6) NOT NULL,
  `Ocena` int NOT NULL,
  `IDClanka` int NOT NULL,
  `IDKorisnika` bigint NOT NULL,
  PRIMARY KEY (`IDOcene`),
  UNIQUE KEY `idKor_idCla_unique` (`IDKorisnika`,`IDClanka`),
  CONSTRAINT `Ocena_IDClanka_266da967_fk_Clanak_IDClanka` FOREIGN KEY (`IDClanka`) REFERENCES `Clanak` (`IDClanka`),
  CONSTRAINT `Ocena_IDKorisnika_fcb580c9_fk_Korisnik_id` FOREIGN KEY (`IDKorisnika`) REFERENCES `Korisnik` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `Poruka`
--

DROP TABLE IF EXISTS `Poruka`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Poruka` (
  `IDPoruke` int NOT NULL AUTO_INCREMENT,
  `Tekst` varchar(400) NOT NULL,
  `DatumVremeKreiranja` datetime NOT NULL,
  PRIMARY KEY (`IDPoruke`)
) ENGINE=InnoDB AUTO_INCREMENT=142 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `PrijavaNepravilnosti`
--

DROP TABLE IF EXISTS `PrijavaNepravilnosti`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PrijavaNepravilnosti` (
  `IDPrijave` int NOT NULL AUTO_INCREMENT,
  `DatumVremePrijave` datetime NOT NULL,
  `IDKorisnika` bigint NOT NULL,
  PRIMARY KEY (`IDPrijave`),
  KEY `PrijavaNepravilnosti_IDKorisnika_3af29ca3_fk_Korisnik_id` (`IDKorisnika`),
  CONSTRAINT `PrijavaNepravilnosti_IDKorisnika_3af29ca3_fk_Korisnik_id` FOREIGN KEY (`IDKorisnika`) REFERENCES `Korisnik` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=178 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `PrijavljenNaObavestenja`
--

DROP TABLE IF EXISTS `PrijavljenNaObavestenja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PrijavljenNaObavestenja` (
  `IDPrijavaObavestenja` int NOT NULL AUTO_INCREMENT,
  `DatumVremePrijave` datetime(6) NOT NULL,
  `PrimajNaMail` int NOT NULL,
  `IDClanka` int NOT NULL,
  `IDKorisnika` bigint NOT NULL,
  PRIMARY KEY (`IDPrijavaObavestenja`),
  UNIQUE KEY `combination_pks` (`IDKorisnika`,`IDClanka`),
  KEY `PrijavljenNaObavestenja_IDClanka_621832e2_fk_Clanak_IDClanka` (`IDClanka`),
  CONSTRAINT `PrijavljenNaObavestenja_IDClanka_621832e2_fk_Clanak_IDClanka` FOREIGN KEY (`IDClanka`) REFERENCES `Clanak` (`IDClanka`),
  CONSTRAINT `PrijavljenNaObavestenja_IDKorisnika_2dfbfaf6_fk_Korisnik_id` FOREIGN KEY (`IDKorisnika`) REFERENCES `Korisnik` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `PrimljenePoruke`
--

DROP TABLE IF EXISTS `PrimljenePoruke`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PrimljenePoruke` (
  `IDPrimljenaPoruka` int NOT NULL AUTO_INCREMENT,
  `Procitana` int NOT NULL,
  `IDKorisnika` bigint NOT NULL,
  `IDPoruke` int NOT NULL,
  `IDPrijavljeneStvari` int NOT NULL,
  `TipPrijave` varchar(1) NOT NULL,
  PRIMARY KEY (`IDPrimljenaPoruka`),
  UNIQUE KEY `combination_pks_primljena_poruka` (`IDPoruke`,`IDKorisnika`),
  KEY `PrimljenePoruke_IDKorisnika_fd4c82e3_fk_Korisnik_id` (`IDKorisnika`),
  CONSTRAINT `PrimljenePoruke_IDKorisnika_fd4c82e3_fk_Korisnik_id` FOREIGN KEY (`IDKorisnika`) REFERENCES `Korisnik` (`id`),
  CONSTRAINT `PrimljenePoruke_IDPoruke_7af9aadd_fk_Poruka_IDPoruke` FOREIGN KEY (`IDPoruke`) REFERENCES `Poruka` (`IDPoruke`)
) ENGINE=InnoDB AUTO_INCREMENT=530 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `PticaTabela`
--

DROP TABLE IF EXISTS `PticaTabela`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PticaTabela` (
  `IDClanka` int NOT NULL,
  `Vrsta` varchar(60) NOT NULL,
  `Rod` varchar(60) DEFAULT NULL,
  `Porodica` varchar(60) DEFAULT NULL,
  `Red` varchar(60) DEFAULT NULL,
  `Klasa` varchar(60) DEFAULT NULL,
  `Tip` varchar(60) DEFAULT NULL,
  `Carstvo` varchar(60) DEFAULT NULL,
  `Tezina` decimal(10,2) DEFAULT NULL,
  `Velicina` decimal(10,2) DEFAULT NULL,
  `StatusUgrozenosti` varchar(60) DEFAULT NULL,
  `SlikaVrste` longblob,
  PRIMARY KEY (`IDClanka`),
  CONSTRAINT `PticaTabela_IDClanka_ba079f53_fk_Clanak_IDClanka` FOREIGN KEY (`IDClanka`) REFERENCES `Clanak` (`IDClanka`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `RazlogPrijaveDiskusija`
--

DROP TABLE IF EXISTS `RazlogPrijaveDiskusija`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RazlogPrijaveDiskusija` (
  `IDRazlogDiskusija` int NOT NULL AUTO_INCREMENT,
  `Opis` varchar(100) NOT NULL,
  PRIMARY KEY (`IDRazlogDiskusija`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `RazlogPrijaveFotografije`
--

DROP TABLE IF EXISTS `RazlogPrijaveFotografije`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RazlogPrijaveFotografije` (
  `IDRazlogFotografija` int NOT NULL AUTO_INCREMENT,
  `Opis` varchar(100) NOT NULL,
  PRIMARY KEY (`IDRazlogFotografija`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `RazlogPrijaveKomentar`
--

DROP TABLE IF EXISTS `RazlogPrijaveKomentar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RazlogPrijaveKomentar` (
  `IDRazlogKomentar` int NOT NULL AUTO_INCREMENT,
  `Opis` varchar(100) NOT NULL,
  PRIMARY KEY (`IDRazlogKomentar`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_Korisnik_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_Korisnik_id` FOREIGN KEY (`user_id`) REFERENCES `Korisnik` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

