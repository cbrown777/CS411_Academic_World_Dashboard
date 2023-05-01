from neo4j import __version__ as neo4j_version
#from neo4j import GraphDatabaseclass
print(neo4j_version)
from pandas import DataFrame


class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            from neo4j import GraphDatabase
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)


    def close(self):
        if self.__driver is not None:
            self.__driver.close()


    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response




#****Execution Start Here



#query for prof info
#query_get_prof_info = "MATCH (f:Faculty {name: {'Agouris, Peggy'}}) RETURN f"




#Class with only a static prof_records_list to hold onto the currently selected University's (widget #4) professor info
class CurrentUniProfRecords:
    prof_records_list = []




def get_prof_names_by_university(uni_name):
    #query_return_profs_from_uni = "MATCH (faculty:FACULTY)-[:AFFILIATION_WITH]->(institute:INSTITUTE {name: {0}}) RETURN faculty".format(uni_name)

    query_return_profs_from_uni = "MATCH (faculty:FACULTY)-[:AFFILIATION_WITH]->(institute:INSTITUTE {name: '"
    query_return_profs_from_uni += uni_name
    query_return_profs_from_uni += "'}) RETURN faculty ORDER BY faculty.name"

    #print(query_return_profs_from_uni)

    conn = Neo4jConnection(uri="bolt://localhost:7687", user="superman", pwd="pizza")
    db = 'academicworld'
    prof_records = conn.query(query_return_profs_from_uni, db)
    list_of_prof_records = list(prof_records)


    #***Update the current static variable, prof_records_list
    CurrentUniProfRecords.prof_records_list = list_of_prof_records



    prof_names = []
    for i in range(len(list_of_prof_records)):
        prof_names.append(list_of_prof_records[i].data()['faculty']['name'])

    conn.close()
    return prof_names






#
#
# uni_name = "University of California--Berkeley"
# get_prof_names_by_university(uni_name)
#
#
#
#
# list_of_prof_records = CurrentUniProfRecords.prof_records_list
#
#
# print(list_of_prof_records[1])
# print(type(list_of_prof_records[1]))
# print(list_of_prof_records[1].data())
#
#
#









#records_two = conn.query(query_return_profs_from_uni, db)


#print("successful query")


# dtf_data = DataFrame([dict(_) for _ in x])
# dtf_data.sample(10)






#list_of_results_two = list(records_two)
#print(list_of_results_two)




#**Need to handle if they don't have values for the below
# print(list_of_results[0].data()['faculty']['photoUrl'])
# print(list_of_results[0].data()['faculty']['name'])
# print(list_of_results[0].data()['faculty']['position'])
# # print(list_of_results[0].data()['faculty']['phone'])
# # print(list_of_results[0].data()['faculty']['email'])
# print(list_of_results[0].data()['faculty']['researchInterest'])



