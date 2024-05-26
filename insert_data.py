from pymongo import MongoClient

try:
    client = MongoClient("mongodb://localhost:27017/")

    db = client.db
except:
    print("Error in DB setup")


def insert(database, info):

    data = db[f"{database}"]

    try:
        data.insert_many(info)
        print("Insert done")
    except Exception as e:
        print(e)
        print("Error in inserting")
