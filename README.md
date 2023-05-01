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


(You may need to delete "pymongo[srv]" from requirements.txt)
Then, you should install the requirements by running:
  
  pip install -r requirements.txt

I also have a file in the SQL_file directory, called, "cs411_project_update_db.sql". 

This file needs to be run within mysql shell. After logging in to mysql shell, you must type in the command:

  source [path/to/cs411_project_update_db.sql]
  
This will execute all of the commands within the file. 

This file will create two tables, "userprofessorfavorites" and "userfavoritekeywords", both of which are initialized with Foreign Key constraints. There are also 2 Views created, one for "Nature Papers", and one for "UIUC Professors". There are also 2 indexes made, one for publication(year), and one for keyword(name).

After this has been completed, you must run:

  python REAL_app.py
  
to load the application.
```


## Usage
```
The first widget allows you to select and search for keywords in the academic world, and see how many publications have been published with that keyword per year since 2000, to give you an idea if that area of research is growing or shrinking. 

The second widget allows you to see the most accomplished researchers by selecting from keywords from a dropdown. The scores are KRC.

The third widget allows you to see the top 10 keywords in publications that have come from a University, which allows you to see the top areas of focus at every university in the academic world.

The fourth widget allows you to lookup professor profiles for potential contact information.

The fifth and sixth widgets allow you to save your favorite professors and keywords to a database. You can do this by selecting from a dropdown menu, and then clicking, "Add prof to favorites" or "Add keyword to favorites"
```


## Design
```
Widget #1 and #2 uses MySQL server to serve the requests, while widget #3 uses MongoDB, and Widget #4 uses Neo4J. Widget #5 and #6 both commit data to relations in MySQL server.
```


## Implementation
```
I used Python's Dash framework, for the overall framework of the project, and also utilized plotly.express, which was useful for generating analytics graphs, as well as pandas, which was useful for data manipulation.
```


## Database Techniques
```
I created a .sql file called, "cs411_project_update_db.sql", which contains commands for generating new tables with constraints, views and indexes in the academicworld database. 

This file will create two tables, "userprofessorfavorites" and "userfavoritekeywords", both of which are initialized with Foreign Key constraints. There are also 2 Views created, one for "Nature Papers", and one for "UIUC Professors". There are also 2 indexes made, one for publication(year), and one for keyword(name).
```

## Extra-Credit Capabilities
```
N/A
```


## Contributions
```
I completed this project solo, I would estimate I spent 50 hours working on it. 
```












