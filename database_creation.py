import profile
import pymongo as pm
from data_cleaning import create_profiles

def create_database():

    ## we use a localhost
    client = pm.MongoClient("mongodb://localhost:27017/")

    db = client["AuthorDB"]
    profile_collection = db["Profile"]

    list_of_profiles = create_profiles()

    ## we drop each time we run the script to keep doing tests
    profile_collection.drop()
    insert_ids = profile_collection.insert_many(list_of_profiles)

    print("inserted ids: ", insert_ids.inserted_ids)


