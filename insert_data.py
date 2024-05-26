import logging
from pymongo import MongoClient

# Configure logging to write to a file with minimal log messages
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),  # This will also print to the console
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


# Example usage
if __name__ == "__main__":
    example_data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
    insert("table_1", example_data)
