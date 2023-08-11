/*
SQLyog Community v13.1.5  (64 bit)
MySQL - 5.6.12-log : Database - estatesystem
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`estatesystem` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `estatesystem`;

/*Table structure for table `agent` */

DROP TABLE IF EXISTS `agent`;

CREATE TABLE `agent` (
  `agentid` int(11) NOT NULL AUTO_INCREMENT,
  `agentlid` int(11) DEFAULT NULL,
  `agentname` varchar(50) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `photo` varchar(50) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `about` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `review` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`agentid`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;

/*Data for the table `agent` */

insert  into `agent`(`agentid`,`agentlid`,`agentname`,`phone`,`email`,`photo`,`gender`,`about`,`status`,`review`) values 
(2,2,'Carl J','9876543210','carl@gmail.com','/static/Agent/agent-1.jpg','male','Liberty City, Los Santos','approved',NULL),
(3,3,'Sudev','7654321098','ijk@gmail.com',NULL,'male','about','approved','NULL'),
(4,4,'Avinash','6543210987','lmn@gmail.com',NULL,'male','about','approved','NULL'),
(9,6,'Amal','8765432109','amal@gmail.com','/static/agent/Screenshot (10).png','male','asdfghj','approved','NULL'),
(11,9,'Thomas Shelby','9876543220','agent@gmail.com','/static/Agent/agent-6.jpg','male','About Thomas Shelby ','approved',NULL),
(12,10,'Arjun','9876543214','arjun@gmail.com','/static/Agent/agent-8.jpg','male','about arjun','pending',NULL),
(14,12,'Sudev','9876543217','sudev@gmail.com','/static/Agent/agent-6.jpg','male','About sudev','pending',NULL),
(16,14,'Alpha','9876543212','alpha@alpha.in','/static/Agent/agent-4.jpg','female','alpha','rejected','Fake Documents'),
(17,15,'AgentSignUp','9876543218','agentsighup@gmail.com','/static/Agent/agent-2.jpg','male','About agentsignup','approved',NULL);

/*Table structure for table `chat` */

DROP TABLE IF EXISTS `chat`;

CREATE TABLE `chat` (
  `chatid` int(11) NOT NULL AUTO_INCREMENT,
  `fromid` int(11) DEFAULT NULL,
  `toid` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `msg` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`chatid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `chat` */

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `complaintid` int(11) NOT NULL AUTO_INCREMENT,
  `userlid` int(11) DEFAULT NULL,
  `complaint` varchar(500) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `reply` varchar(500) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`complaintid`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`complaintid`,`userlid`,`complaint`,`date`,`reply`,`status`) values 
(5,7,'i have a compliant','2022-11-07','We will resolve it soon','replied'),
(6,16,'I have complaints','2022-11-20','Sorry for your inconvenience, We will resolve is soon','replied');

/*Table structure for table `interest` */

DROP TABLE IF EXISTS `interest`;

CREATE TABLE `interest` (
  `intid` int(11) NOT NULL AUTO_INCREMENT,
  `userlid` int(11) DEFAULT NULL,
  `propertyid` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`intid`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

/*Data for the table `interest` */

insert  into `interest`(`intid`,`userlid`,`propertyid`,`date`) values 
(1,1,1,'2022-09-07'),
(2,0,0,'0000-00-00'),
(3,8,5,'2022-10-02'),
(4,7,7,'2022-11-07'),
(6,2,8,'2022-11-13'),
(7,8,9,'2022-11-13'),
(8,8,8,'2022-11-13'),
(10,16,11,'2022-11-20'),
(11,16,12,'2022-11-20'),
(12,16,11,'2022-11-23');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `lid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `usertype` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`lid`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`lid`,`username`,`password`,`usertype`) values 
(1,'admin','admin','admin'),
(2,'carl@gmail.com','agent','agent'),
(3,'user','user','user'),
(4,'','',''),
(5,'','',''),
(6,'amal','123','agent'),
(7,'abhi@gmail.com','abhi','user'),
(8,'anu','anu','user'),
(9,'agent@gmail.com','agent47','agent'),
(10,'arjun@gmail.com','passwd','agent'),
(11,'arjun','12345','agent'),
(12,'sudev@gmail.com','sudev@123','agent'),
(14,'alpha@alpha.in','alpha@123','agent'),
(15,'agentsighup@gmail.com','password','agent'),
(16,'usersignup@gmail.com','123456789','user');

/*Table structure for table `property` */

DROP TABLE IF EXISTS `property`;

CREATE TABLE `property` (
  `propertyid` int(11) NOT NULL AUTO_INCREMENT,
  `agentlid` int(11) DEFAULT NULL,
  `propertytitle` varchar(50) DEFAULT NULL,
  `propertytype` varchar(13) DEFAULT NULL,
  `priceofproperty` varchar(20) DEFAULT NULL,
  `totalarea` varchar(11) DEFAULT NULL,
  `housesqft` varchar(11) DEFAULT NULL,
  `totalbeds` int(11) DEFAULT NULL,
  `totalbaths` int(11) DEFAULT NULL,
  `totalgarages` int(11) DEFAULT NULL,
  `propertylocation` varchar(50) DEFAULT NULL,
  `city` varchar(15) DEFAULT NULL,
  `state` varchar(25) DEFAULT NULL,
  `pin` int(9) DEFAULT NULL,
  `country` varchar(20) DEFAULT NULL,
  `landmarks` varchar(40) DEFAULT NULL,
  `pic1` varchar(100) DEFAULT NULL,
  `pic2` varchar(100) DEFAULT NULL,
  `pic3` varchar(100) DEFAULT NULL,
  `video` varchar(100) DEFAULT NULL,
  `propertydescription` varchar(500) DEFAULT NULL,
  `gmaplocation` varchar(50) DEFAULT NULL,
  `amentities` varchar(100) DEFAULT NULL,
  `propertystatus` varchar(18) DEFAULT NULL,
  `uploaddate` date DEFAULT NULL,
  `saletype` varchar(5) DEFAULT NULL,
  `availabledate` varchar(11) DEFAULT NULL,
  `nearestfacilities` varchar(100) DEFAULT NULL,
  `yearbuilt` year(4) DEFAULT NULL,
  `bought` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`propertyid`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

/*Data for the table `property` */

insert  into `property`(`propertyid`,`agentlid`,`propertytitle`,`propertytype`,`priceofproperty`,`totalarea`,`housesqft`,`totalbeds`,`totalbaths`,`totalgarages`,`propertylocation`,`city`,`state`,`pin`,`country`,`landmarks`,`pic1`,`pic2`,`pic3`,`video`,`propertydescription`,`gmaplocation`,`amentities`,`propertystatus`,`uploaddate`,`saletype`,`availabledate`,`nearestfacilities`,`yearbuilt`,`bought`) values 
(11,2,'Grove Street House','Residential','50,00,000','80','2400',5,4,2,'Liberty City,Ganton,Los Santos','Liberty City','Ganton',375654,'Los Santos','Middle of Ganton in eastern Los Santos','/static/Property/G1.jpg','/static/Property/G2.jpg','/static/Property/G3.jpg','/static/Property/1.mp4','Grove Street is a cul-de-sac located in the middle of Ganton in eastern Los Santos, and is the main base of operations for the Grove Street Families. Grove Street is the home of Sean \"Sweet\" Johnson and Carl \"CJ\" Johnson, the two leaders of the Grove Street Families.','Middle of Ganton in eastern Los Santos',' Wifi,Pools,Balcony    ','Available','2022-11-19','Rent','2023-02-15','Fuel Station,College,School',2000,'Anabelle'),
(12,2,'San Andreas Flat (Under Renovation)','Commercial','60,00,000','1500','2800',8,6,4,'Los Santos,California,US','Los Santos','California',549901,'US','Middle of western Los Angeles, Californi','/static/Property/6.jpg','/static/Property/4.2.jpg','/static/Property/4.3.jpg','/static/Property/4.mp4','Los Santos is the largest city, both by population and area in San Andreas. It is based on Los Angeles, California. It is filled with references to famous L.A. landmarks, including the Hollywood Sign, the Watts Towers, the Capitol Tower, the U.S. Bank Tower and the Santa Monica Pier, among many others.','Middle of western Los Angeles, California','   SmartTV,Pools,Parking   ','Not-Available','2022-11-19','Sell','2025-12-20','Fuel Station,Hospital',2020,NULL),
(13,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);

/*Table structure for table `rating` */

DROP TABLE IF EXISTS `rating`;

CREATE TABLE `rating` (
  `ratingid` int(11) NOT NULL AUTO_INCREMENT,
  `userlid` int(11) DEFAULT NULL,
  `rating` varchar(50) DEFAULT NULL,
  `review` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`ratingid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `rating` */

insert  into `rating`(`ratingid`,`userlid`,`rating`,`review`,`date`) values 
(1,1,'5','review','2022-09-20'),
(4,7,'5','okish','2022-11-13'),
(5,16,'4','Very User Friendly','2022-11-20');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `userlid` int(11) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `photo` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `pincode` varchar(20) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`userid`,`userlid`,`username`,`phone`,`email`,`photo`,`place`,`city`,`state`,`pincode`,`gender`) values 
(1,1,'Abhi',NULL,'abhi@mail.com',NULL,'qld','qld','status','987456',NULL),
(2,0,'','','','','','','','',NULL),
(3,7,'Anabella','9876543210','abhi@gmail.com','/static/User/agent-4.jpg','Grove Street','Liberty City','Los Santos','164498','female'),
(4,8,'Anu','9876543210','anu','/static/User/Screenshot (11).png','qld','qld','kerala','654321','male'),
(5,16,'UserSignUp','8765432109','usersignup@gmail.com','/static/User/agent-5.jpg','Address','City','Stateofuser','456698','female');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
