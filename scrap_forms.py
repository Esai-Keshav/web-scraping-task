import requests
from bs4 import BeautifulSoup
from insert_data import insert

data_list = []

try:
    r = requests.get("https://www.scrapethissite.com/pages/forms/?per_page=600").text
    # 600 content is rendered in a page
except:
    print("Error in Fetching")


def collect_data():
    soup = BeautifulSoup(r, "html.parser")

    data = soup.find("table", {"class": "table"})

    rows = []
    for team_info in data.find_all("tr"):
        team = team_info.find_all("td")
        team_value = [y.text.strip() for y in team]
        rows.append(team_value)

    rows = rows[1:]

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
    # print(data_list)
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


converted_data = [convert_numeric_fields(record) for record in collect_data()]

# print(converted_data)
insert("table_2", converted_data)
