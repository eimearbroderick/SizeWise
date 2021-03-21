CREATE DATABASE  IF NOT EXISTS `login` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `login`;
-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: localhost    Database: login
-- ------------------------------------------------------
-- Server version	8.0.22

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
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `first_name` varchar(40) DEFAULT NULL,
  `last_name` varchar(40) DEFAULT NULL,
  `age` smallint DEFAULT NULL,
  `height` varchar(40) DEFAULT NULL,
  `weight` varchar(40) DEFAULT NULL,
  `avgsize` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (2,'demopractice','1234','demo@email.com','Demo','Practice',20,'5ft8','150lbs','UK14'),(3,'Charlie','pass','user2@gmail.com','Charlie','Brown',20,'6ft','170lbs','UK14'),(4,'Eimear','mypass','eimear@gmail.com','Eimear','Broderick',22,'5ft7','120lbs','S'),(5,'TestUser','test','test@mail.com',NULL,NULL,NULL,NULL,NULL,NULL),(6,'Bob','pass','bob@gmail.com',NULL,NULL,NULL,NULL,NULL,NULL),(7,'sample2','sample','sample@gmail.com',NULL,NULL,NULL,NULL,NULL,NULL),(8,'sample3','pass','123@gmail.com',NULL,NULL,NULL,NULL,NULL,NULL),(9,'Demo','pass','demo@gmail.com','Demo','Test1',22,'6ft','130lbs','M'),(10,'mary','pass','mary@mail.com',NULL,NULL,NULL,NULL,NULL,NULL),(11,'john','pass','john@email.com',NULL,NULL,NULL,NULL,NULL,NULL),(12,'NewUser','pass','nu@mail.com',NULL,NULL,NULL,NULL,NULL,NULL),(13,'Jerry','pass','j@mail.com',NULL,NULL,NULL,NULL,NULL,NULL),(14,'Adam','pass','adam@mail.com',NULL,NULL,NULL,NULL,NULL,NULL),(15,'Sarah','pass','sarah@mail.com',NULL,NULL,NULL,NULL,NULL,NULL),(16,'Kelly!','pass','kelly@user.com','Kelly','Barry',45,'170cm','200lbs','UK14');
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discounts`
--

DROP TABLE IF EXISTS `discounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discounts` (
  `dcode` varchar(20) NOT NULL,
  `date` date NOT NULL,
  `amount` varchar(30) NOT NULL,
  `storeID` int NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`dcode`),
  KEY `discounts_fk_idx` (`storeID`),
  CONSTRAINT `discounts_fk` FOREIGN KEY (`storeID`) REFERENCES `store` (`storeID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discounts`
--

LOCK TABLES `discounts` WRITE;
/*!40000 ALTER TABLE `discounts` DISABLE KEYS */;
INSERT INTO `discounts` VALUES ('NIKESW20','2021-02-08','20%',3,NULL),('SWSpring2021','2021-02-23','15%',2,0),('SWtestCode','2021-02-22','10%',2,1),('SWThankYou','2021-02-24','20%',2,0),('SWWinter2020','2021-01-07','10%',2,0),('WEEKDAYSW10','2021-03-17','10%',2,0),('WEEKDAYSW15','2021-03-01','15%',2,0),('WEEKDAYSW25','2021-03-04','25%',2,0),('ZARASW20','2021-02-08','20%',4,NULL);
/*!40000 ALTER TABLE `discounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `reviewID` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `store` varchar(50) NOT NULL,
  `product` varchar(100) DEFAULT NULL,
  `size` varchar(20) DEFAULT NULL,
  `rating` int DEFAULT NULL,
  `FIT` varchar(100) DEFAULT NULL,
  `CATEGORY` varchar(100) DEFAULT NULL,
  `review` varchar(250) NOT NULL,
  PRIMARY KEY (`reviewID`),
  KEY `fk_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (10,4,'Nike',NULL,'Medium',2,NULL,NULL,' Ordered a pair of joggers (the Stealth Jogger in charcoal), Nike recommended M themselves but they are far too big. Would recommend going with a smaller size if you are unsure these are huge'),(11,6,'Weekday',NULL,'Large',3,NULL,NULL,' Bought the Male Rowe jeans, happy with the length but the waist was tighter than expected so would recommend sizing up'),(12,10,'Zara',NULL,'Small',5,NULL,NULL,' Always happy with Zara sizing! Bought a top in S and it is perfect, usually I am a uk10'),(13,4,'Zara',NULL,'Medium',3,NULL,NULL,' Always recommend sizing up in pants with Zara'),(14,9,'Nike',NULL,'Small',5,NULL,NULL,'Bought a t-shirt last week and the size is perfect. I am 5ft7 and opted for a Small.'),(43,9,'Weekday',NULL,'Medium',3,NULL,NULL,'Big fitting I would say, no need to size up'),(47,4,'Weekday',NULL,'Small',3,NULL,NULL,' Bought this hoodie in a small and could have definitely sized up, it is not as loose fitting as it looks.'),(48,4,'Weekday','Blue Crewneck Sweater','Medium',5,NULL,NULL,' This sweater is the most comfortable I own, great loose but flattering fit!'),(49,6,'Weekday','Relaxed T-Shirt','Large',5,NULL,NULL,' You cannot go wrong with Weekday, I am 6ft 1 and this relaxed tee fits like a charm in L. '),(50,6,'Weekday','Standard Sweatpants','Medium',4,NULL,NULL,' These pants are definitely loose fitting, a bit too long for me as a 5ft7 man but the elastic cuffs mean I can just roll them up.'),(51,4,'Weekday','Easy Tshirt','Large',3,NULL,NULL,'Definitely a loose fit which people should keep in mind'),(98,4,'Weekday','','Small',4,'2',NULL,' testing db'),(99,4,'Weekday','Long Sleeved Tee','Medium',4,'5',NULL,' Sized up unnecessarily here with this top, should have read other reviews before ordering.  ');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store`
--

DROP TABLE IF EXISTS `store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store` (
  `storeID` int NOT NULL AUTO_INCREMENT,
  `store` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  PRIMARY KEY (`storeID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store`
--

LOCK TABLES `store` WRITE;
/*!40000 ALTER TABLE `store` DISABLE KEYS */;
INSERT INTO `store` VALUES (2,'Weekday','week123'),(3,'Nike','nike123'),(4,'Zara','zara123');
/*!40000 ALTER TABLE `store` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-21 22:03:56
