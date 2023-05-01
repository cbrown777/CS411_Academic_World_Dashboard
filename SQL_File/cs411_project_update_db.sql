
USE `academicworld`;

--
-- Table structure for table `faculty`
--

/*Make Table for storing a users favorite professors */
/*Includes FK Constraint */

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userprofessorfavorites` (
  `id` int NOT NULL,
  PRIMARY KEY (`id`), 
  `name` varchar(512) DEFAULT NULL,
  CONSTRAINT `prof_favs_ibfk_1` FOREIGN KEY (`id`) REFERENCES `faculty` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;





/*Make Table for storing a users favorite keywords */
/*Includes FK Constraint */

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userfavoritekeywords` (
  `id` int NOT NULL,
  PRIMARY KEY (`id`),
  `name` varchar(512) DEFAULT NULL,
  CONSTRAINT `key_favs_ibfk_1` FOREIGN KEY (`id`) REFERENCES `keyword` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;



/*Create View for Nature Papers */
CREATE VIEW naturepapers AS SELECT * FROM publication WHERE venue LIKE '%nature%';


/*Create View for UIUC Professors */
CREATE VIEW uiucprofs AS SELECT * FROM faculty WHERE university_id IN (SELECT id FROM university WHERE name = "University of illinois at Urbana Champaign");



/*Make Index for publication year*/
CREATE INDEX pub_year_idx ON publication(year);

/*Make Index for keyword name*/
CREATE INDEX keyword_name_idx ON keyword(name);









