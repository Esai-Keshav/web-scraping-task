import logging
from pymongo import MongoClient


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),  
    ],
)

try:
    logging.info("Setting up MongoDB client.")
    client = MongoClient("mongodb://localhost:27017/")
    db = client.db
    logging.info("MongoDB setup successful.")
except Exception as e:
    logging.error("Error in DB setup: %s", e)


def insert(database, info):
    data = db[f"{database}"]
    try:
        logging.info("Inserting data into %s.", database)
        data.insert_many(info)

    except Exception as e:
        logging.error("Error inserting data: %s", e)

