import mysql.connector
import pandas as pd



def getNames(_relation_name):
    cnx = mysql.connector.connect(user='root', password='password', host='localhost', database='academicworld')
    query_get_keywords = ("SELECT name FROM {}".format(_relation_name))
    cursor_one = cnx.cursor()
    cursor_one.execute(query_get_keywords)

    keyword_list_of_tuples = []

    for _kw in cursor_one:
        keyword_list_of_tuples.append(_kw)

    keyword_list = [x[0] for x in keyword_list_of_tuples]

    cursor_one.close()
    return keyword_list





def add_user_favorite_professor(prof_name):
    cnx_four = mysql.connector.connect(user='root', password='password', host='localhost', database='academicworld')

    # RETRIEVE ID QUERY
    query_get_user_favorite_prof_id = ("SELECT id FROM faculty WHERE name = '{0}'".format(prof_name))

    cursor_four = cnx_four.cursor()
    cursor_four.execute(query_get_user_favorite_prof_id)

    # Get Prof ID in to prof_id
    keyword_list_of_tuples = []
    for _kw in cursor_four:
        keyword_list_of_tuples.append(_kw)
    keyword_id_list = [x[0] for x in keyword_list_of_tuples]
    prof_id = keyword_id_list[0]

    cursor_four.close()
    cnx_four.close()

    # Make a NEW Connection for the INSERT!
    cnx_six = mysql.connector.connect(user='root', password='password', host='localhost', database='academicworld')
    cursor_six = cnx_six.cursor()

    # INSERT QUERY
    insert_query = ("INSERT INTO userprofessorfavorites (id, name) VALUES (%s, %s)")
    values = (prof_id, prof_name)

    try:
        cursor = cnx_six.cursor()
        cursor.execute(insert_query, values)
        cnx_six.commit()
    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table: {}".format(error))

    cursor_six.close()
    cnx_six.close()



#***COME back to this
def add_user_favorite_keyword(keyword_name):
    cnx_four = mysql.connector.connect(user='root', password='password', host='localhost', database='academicworld')

    # RETRIEVE ID QUERY
    query_get_user_favorite_keyword_id = ("SELECT id FROM keyword WHERE name = '{0}'".format(keyword_name))

    cursor_four = cnx_four.cursor()
    cursor_four.execute(query_get_user_favorite_keyword_id)

    # Get Key ID in to prof_id
    keyword_list_of_tuples = []
    for _kw in cursor_four:
        keyword_list_of_tuples.append(_kw)
    keyword_id_list = [x[0] for x in keyword_list_of_tuples]
    key_id = keyword_id_list[0]

    cursor_four.close()
    cnx_four.close()

    # Make a NEW Connection for the INSERT!
    cnx_six = mysql.connector.connect(user='root', password='password', host='localhost', database='academicworld')
    cursor_six = cnx_six.cursor()

    # INSERT QUERY
    insert_query = ("INSERT INTO userfavoritekeywords (id, name) VALUES (%s, %s)")
    values = (key_id, keyword_name)

    try:
        cursor = cnx_six.cursor()
        cursor.execute(insert_query, values)
        cnx_six.commit()
    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table: {}".format(error))

    cursor_six.close()
    cnx_six.close()





def get_keyword_years_and_publication_counts(keyword):

    cnx_two = mysql.connector.connect(user='root', password='password', host='localhost', database='academicworld')

    query_keyword_years_and_pubs_count = ("SELECT year, count(*) FROM publication WHERE year >= 2000 AND id IN "
         "( SELECT publication_id FROM publication_keyword WHERE keyword_id IN "
         "(SELECT id FROM keyword WHERE name = %s) ) GROUP BY year ORDER BY year ASC")

    cursor_two = cnx_two.cursor()
    cursor_two.execute(query_keyword_years_and_pubs_count, (keyword,))
    #print("query executed inside get_keyword_years_and_publication_counts()")

    # for pair in cursor_two:
    #     print(pair)

    data_kw_years_pub_counts = cursor_two.fetchall()
    df_kw_years_pub_counts = pd.DataFrame(data_kw_years_pub_counts, columns=['Year', 'Publication Count'])

    #print(df_kw_years_pub_counts)

    cursor_two.close()

    return df_kw_years_pub_counts
    # for format with string
    # cursor.execute(query, (keyword))




#Return top 10 professors with KRC for keyword 'machine_learning'
def get_krc_profs_ranking_by_keyword(keyword):
    cnx_three = mysql.connector.connect(user='root', password='password', host='localhost', database='academicworld')


    query_krc_profs_ranking = \
    (
        "SELECT name, KRC"
        " FROM faculty F1,"
        " ("
        "SELECT faculty_id, SUM(SC) as KRC"
        " FROM faculty_publication FP,"
        " ("
            " SELECT publication_id, keyword_id, score, num_citations, (score*num_citations) as SC"
            " FROM publication P1, publication_keyword PK1 WHERE P1.id = PK1.publication_id AND PK1.keyword_id IN"
            " (SELECT id FROM keyword WHERE name = %s) "
        ") MLPubs"
        " WHERE FP.publication_id = MLPubs.publication_id"
        " GROUP BY faculty_id"
        " ORDER BY KRC desc"
        " LIMIT 10"
        ") F2"
        " WHERE"
        " F1.id = F2.faculty_id"
        " ORDER BY krc ASC"
    )

    cursor_three = cnx_three.cursor()
    cursor_three.execute(query_krc_profs_ranking, (keyword,))

    data_krc_profs = cursor_three.fetchall()
    df_krc_profs = pd.DataFrame(data_krc_profs, columns=['Professor', 'KRC Score'])


    #temp
    # print(data_krc_profs)
    # print(df_krc_profs)

    cursor_three.close()
    return df_krc_profs
