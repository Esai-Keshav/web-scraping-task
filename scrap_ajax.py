import requests
import logging
from insert_data import insert

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
    logging.info("Fetching data from the website.")
    r = requests.get(
        "https://www.scrapethissite.com/pages/ajax-javascript/?ajax=true&year=2015"
    )
    r.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
    logging.info("Data fetched successfully.")
except requests.exceptions.RequestException as e:
    logging.error("Error in fetching data: %s", e)
else:
    try:
        data = r.json()
        logging.info("JSON data parsed successfully.")
        insert("table_1", data)
        logging.info("Data inserted into the table successfully.")
    except ValueError as e:
        logging.error("Error parsing JSON: %s", e)
    except Exception as e:
        logging.error("Error inserting data: %s", e)
