# ConnorB
Connor Brown repo for CS411 Project - Academic World Dashboard




# Title
```
  Identifying Potential Research Topics, Universities, and Professors to Work w/in the Academic World
```



## Purpose
```
  The purpose of this application is to help future graduate students identify strong areas of research, identify the most accomplished professors in a particular research area, identify what areas of research different universities focus on the most, and then to be able to store their favorite areas of research and favorite professors for later reference. 
```


## Demo
```


FILL IN 


```


## Installation
```
Assuming that you already have the necessary databases installed for MySQL, mongoDB, and Neo4J, you would need to modify the code in the mysql_utils.py, mongodb_utils.py, and neo4j_utils.py files to ensure that the connections to the databases are compatible with your machine. 

I also have a file in the SQL_file directory, called, "cs411_project_update_db.sql". 

This file needs to be run within mysql shell. After logging in to mysql shell, you must type in the command:

  source [path/to/cs411_project_update_db.sql]
  
This will execute all of the commands within the file. 

This file will create two tables, "userprofessorfavorites" and "userfavoritekeywords", both of which are initialized with Foreign Key constraints. There are also 2 Views created, one for "Nature Papers", and one for "UIUC Professors". There are also 2 indexes made, one for publication(year), and one for keyword(name).

After this has been completed, you must run:

  python REAL_app.py
  
to load the application.
```











