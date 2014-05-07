-- MySQL dump 10.13  Distrib 5.5.35, for debian-linux-gnu (armv7l)
--
-- Host: localhost    Database: sbs
-- ------------------------------------------------------
-- Server version	5.5.35-0+wheezy1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `sbs`
--

DROP TABLE IF EXISTS `sbs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sbs` (
  `sbsID` int(11) NOT NULL AUTO_INCREMENT,
  `sbsName` varchar(255) NOT NULL,
  `sbsTempPin` int(11) NOT NULL,
  `sbsDepthPin` int(11) NOT NULL,
  `sbsFillPin` int(11) NOT NULL,
  `sbsFillPinStatus` int(11) NOT NULL,
  `sbsEmptyPin` int(11) NOT NULL,
  `sbsEmptyPinStatus` int(11) NOT NULL,
  `sbsFullVal` int(11) NOT NULL,
  `sbsEmptyVal` int(11) NOT NULL,
  PRIMARY KEY (`sbsID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sbs`
--

LOCK TABLES `sbs` WRITE;
/*!40000 ALTER TABLE `sbs` DISABLE KEYS */;
INSERT INTO `sbs` VALUES (1,'Smart Bucket',18,0,24,1,23,1,720,790);
/*!40000 ALTER TABLE `sbs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `station`
--

DROP TABLE IF EXISTS `station`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `station` (
  `stationID` int(11) NOT NULL AUTO_INCREMENT,
  `stationName` varchar(255) NOT NULL,
  `stationTempHumidPin` int(11) NOT NULL,
  `stationSolarPin` int(11) NOT NULL,
  `sbsTempPin` int(11) NOT NULL,
  `stationCamURL` varchar(255) NOT NULL,
  PRIMARY KEY (`stationID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `station`
--

LOCK TABLES `station` WRITE;
/*!40000 ALTER TABLE `station` DISABLE KEYS */;
INSERT INTO `station` VALUES (1,'My Green House',4,1,18,'http://192.168.2.131/img/snapshot.cgi');
/*!40000 ALTER TABLE `station` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task`
--

DROP TABLE IF EXISTS `task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `task` (
  `taskID` int(11) NOT NULL AUTO_INCREMENT,
  `taskName` varchar(255) NOT NULL,
  `taskSensorName` varchar(255) NOT NULL,
  `taskSensorID` int(11) NOT NULL,
  `taskStatus` int(11) NOT NULL,
  `taskComment` varchar(512) NOT NULL,
  `taskStartTime` datetime NOT NULL,
  `taskEndTime` datetime DEFAULT NULL,
  PRIMARY KEY (`taskID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task`
--

LOCK TABLES `task` WRITE;
/*!40000 ALTER TABLE `task` DISABLE KEYS */;
INSERT INTO `task` VALUES (1,'Fill','Smart Bucket',1,0,'Fill Smart Bucket','2014-04-27 20:24:00','2014-05-02 23:10:09'),(2,'Empty','Smart Bucket',1,0,'Empty Smart Bucket','2014-04-28 22:34:00','2014-05-02 23:11:53'),(3,'Fill','Smart Bucket',1,0,'Started from web api','0000-00-00 00:00:00',NULL),(4,'Fill','Smart Bucket',1,0,'Started from web api','0000-00-00 00:00:00','2014-05-02 23:38:55'),(5,'Empty','Smart Bucket',1,0,'Started from web api','0000-00-00 00:00:00','2014-05-02 23:40:21'),(6,'Empty','Smart Bucket',1,0,'Started from web api','0000-00-00 00:00:00','2014-05-02 23:57:32'),(7,'Fill','Smart Bucket',1,0,'Started from web api','0000-00-00 00:00:00','2014-05-02 23:59:47'),(8,'Empty','Smart Bucket',1,0,'Started from web api','0000-00-00 00:00:00','2014-05-03 00:01:15'),(9,'Empty','Smart Bucket',1,0,'Started from web api','0000-00-00 00:00:00','2014-05-03 00:02:25'),(10,'Fill','Smart Bucket',1,0,'Started from web api','0000-00-00 00:00:00',NULL),(11,'Empty','Smart Bucket',1,0,'Started from web api','0000-00-00 00:00:00',NULL),(12,'Empty','Smart Bucket',1,0,'Started from web api','0000-00-00 00:00:00','2014-05-03 01:01:03'),(13,'Fill','Smart Bucket',1,0,'Started from web api','2014-05-03 22:51:13','2014-05-03 22:52:18'),(14,'Empty','Smart Bucket',1,0,'Started from web api','2014-05-03 22:52:34','2014-05-03 22:53:59'),(15,'Empty','Smart Bucket',1,0,'Started from web api','2014-05-06 19:24:48','2014-05-07 19:27:45');
/*!40000 ALTER TABLE `task` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-05-07 19:45:34
