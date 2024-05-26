import requests
import logging
from bs4 import BeautifulSoup
from joblib import Parallel, delayed
from insert_data import insert


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),  
    ],
)

data_list = []

try:
    logging.info("Fetching data from the website.")
    r = requests.get("https://www.scrapethissite.com/pages/forms/?per_page=600").text
    logging.info("Data fetched successfully.")
except requests.exceptions.RequestException as e:
    logging.error("Error in fetching data: %s", e)


def process_team_info(team_info):
    team = team_info.find_all("td")
    return [y.text.strip() for y in team]


def collect_data():
    logging.info("Collecting data from the fetched HTML.")
    soup = BeautifulSoup(r, "html.parser")
    data = soup.find("table", {"class": "table"})

    
    rows = Parallel(n_jobs=-1)(
        delayed(process_team_info)(team_info) for team_info in data.find_all("tr")
    )
    rows = rows[1:]  # Skip the header row

    title = [
        "Team Name",
        "Year",
        "Wins",
        "Losses",
        "OT Losses",
        "Win %",
        "Goals For (GF)",
        "Goals Against (GA)",
        "+ / -",
    ]

    for single_row in rows:
        final = dict(zip(title, single_row))
        data_list.append(final)

    logging.info("Data collection completed.")
    return data_list


def convert_numeric_fields(record):
    int_fields = [
        "Year",
        "Wins",
        "Losses",
        "Goals For (GF)",
        "Goals Against (GA)",
        "+ / -",
    ]

    float_fields = ["Win %"]

    for field in int_fields:
        if field in record and record[field]:
            try:
                record[field] = int(record[field])
            except ValueError:
                pass

    for field in float_fields:
        if field in record and record[field]:
            try:
                record[field] = float(record[field])
            except ValueError:
                pass

    return record


try:
    collected_data = collect_data()

    logging.info("Starting parallel data conversion.")
    converted_data = Parallel(n_jobs=-1)(
        delayed(convert_numeric_fields)(record) for record in collected_data
    )

    logging.info("Data conversion completed.")
    insert("table_2", converted_data)
    logging.info("Data inserted into the table successfully.")
except Exception as e:
    logging.error("Error during processing or insertion: %s", e)
