import pymongo
from pymongo import MongoClient
import pandas as pd
from pandas import DataFrame

client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')

db = client['academicworld']

# print('connection to academicworld: success')
#
# info = db.list_collections()
#
# print(info)




# Widget 3
# Pymongo query to return top 10 keywords by University - here, we use "College of William Mary"

def version_TWO(uni_name):
    #Make index on 'id'
    db.publications.create_index([('id', pymongo.ASCENDING)])

    # Get unique publication IDs from the faculty collection
    unique_publication_ids = db.faculty.aggregate([
        {"$match": {"affiliation.name": uni_name}},
        {"$project": {"publications": 1}},
        {"$unwind": "$publications"},
        {"$group": {"_id": "$publications"}},
        {"$project": {"_id": 0, "publicationId": "$_id"}}
    ])

    # Extract the list of unique publication IDs
    unique_publication_ids = [doc['publicationId'] for doc in unique_publication_ids]

    # Find all publications with IDs in the list of unique IDs
    publications = db.publications.aggregate([
        {"$match": {"id": {"$in": unique_publication_ids}}},
        {"$unwind": "$keywords"},
        {"$group": {"_id": "$keywords.name", "score": {"$sum": "$keywords.score"}}},
        {"$sort": {"score": -1}},
        {"$limit": 10}
    ])

    results_df = DataFrame(publications)
    results_df.columns = ['Keyword', 'Total Score']

    #print(results_df)

    return results_df







#
# uni_name = "College of William Mary"
#
# # top_keywords_by_university(uni_name)
# version_TWO(uni_name)
#
#
#
#














