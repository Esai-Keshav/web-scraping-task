import requests
from insert_data import insert

try:
    r = requests.get(
        "https://www.scrapethissite.com/pages/ajax-javascript/?ajax=true&year=2015"
    )
except:
    print("Error in Fetching")
# print(r.json())

insert("table_1", r.json())
