-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: ecommy
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `additems`
--

DROP TABLE IF EXISTS `additems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `additems` (
  `itemid` binary(16) NOT NULL,
  `item_name` longtext NOT NULL,
  `dis` longtext NOT NULL,
  `qyt` int DEFAULT NULL,
  `category` enum('electronics','home','fashion','grocery') DEFAULT NULL,
  `price` int DEFAULT NULL,
  `added_by` varchar(255) DEFAULT NULL,
  `img_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`itemid`),
  KEY `added_by` (`added_by`),
  CONSTRAINT `additems_ibfk_1` FOREIGN KEY (`added_by`) REFERENCES `vendor` (`email`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `additems`
--

LOCK TABLES `additems` WRITE;
/*!40000 ALTER TABLE `additems` DISABLE KEYS */;
INSERT INTO `additems` VALUES (_binary ',ý\Ìýï›Š¥þ\rC+','ktm bike','adsfdgfgtrthr',55,'electronics',20000,'anushamallela568@gmail.com','6Xz8Dt.jpg'),(_binary 'Ea\Zhüï›Š¥þ\rC+','anusha','adsfdgfgtrthr',55,'electronics',70000,'anushamallela568@gmail.com','0So9Aa.jpeg'),(_binary 'E\ÍZš¸ï›Š¥þ\rC+','anusha','asdfghjklkuytrewa',1,'home',25000,'anushamallela568@gmail.com','1Fh6Ci.jpg'),(_binary '\åmCv\Çï›Š¥þ\rC+','anusha','sdffghjuytredfg',5,'fashion',50000,'anushamallela568@gmail.com','8Jf7Yt.jpg'),(_binary 'ù\ìD.\Çï›Š¥þ\rC+','oppp A17','adsfdgfgtrthr',55,'electronics',15000,'anushamallela568@gmail.com','3Pa5Yz.png'),(_binary 'û\Ëzÿï›Š¥þ\rC+','Grocery','sfghjk',55,'grocery',25,'anushamallela568@gmail.com','2Nb9Aa.jpg');
/*!40000 ALTER TABLE `additems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `ordid` binary(16) NOT NULL,
  `itemid` binary(16) NOT NULL,
  `item_name` varchar(255) DEFAULT NULL,
  `qty` int DEFAULT NULL,
  `total_price` decimal(20,4) DEFAULT NULL,
  `user` varchar(155) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `imgid` varchar(255) DEFAULT NULL,
  `dis` text,
  PRIMARY KEY (`ordid`),
  KEY `itemid` (`itemid`),
  KEY `user` (`user`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`itemid`) REFERENCES `additems` (`itemid`) ON DELETE CASCADE,
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`user`) REFERENCES `user` (`email`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (_binary 'º&¥\èï›Š¥þ\rC+',_binary ',ý\Ìýï›Š¥þ\rC+','ktm bike',1,20000.0000,'mallelaanusha568@gmail.com','electronics','6Xz8Dt.jpg','adsfdgfgtrthr'),(_binary '\Ñh\ì8¬ï›Š¥þ\rC+',_binary '\åmCv\Çï›Š¥þ\rC+','anusha',1,50000.0000,'mallelaanusha568@gmail.com','fashion','8Jf7Yt.jpg','sdffghjuytredfg');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `username` varchar(255) NOT NULL,
  `mobile_no` bigint NOT NULL,
  `email` varchar(155) NOT NULL,
  `address` text NOT NULL,
  `password` varbinary(255) DEFAULT NULL,
  PRIMARY KEY (`email`),
  UNIQUE KEY `mobile_no` (`mobile_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('anusha',9963119418,'mallelaanusha568@gmail.com','vijayawada',_binary '$2b$12$W5.RhGMLlTXcYJGyql4qB.RTxXFLPS/NFBUNygnpTppi3YT4SP7Re');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendor`
--

DROP TABLE IF EXISTS `vendor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendor` (
  `email` varchar(100) NOT NULL,
  `name` varchar(255) NOT NULL,
  `mobile_no` bigint NOT NULL,
  `address` text NOT NULL,
  `password` varbinary(255) DEFAULT NULL,
  PRIMARY KEY (`email`),
  UNIQUE KEY `mobile_no` (`mobile_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendor`
--

LOCK TABLES `vendor` WRITE;
/*!40000 ALTER TABLE `vendor` DISABLE KEYS */;
INSERT INTO `vendor` VALUES ('anushamallela568@gmail.com','anusha',9963119418,'vijayawada',_binary '$2b$12$zs5RmGiZ3gqiyFgbq8qvzujle3dLwAY4e9i2u65cFOZjs0bQ.RiDW'),('mallelaanusha568@gmail.com','anusha',7207994181,'vijayawada',_binary '$2b$12$AiKf7.UtihNmp7199PcRUel.IeTza8ELrXOucd6qeuaV3k6Cukqy.');
/*!40000 ALTER TABLE `vendor` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-31 16:37:43
