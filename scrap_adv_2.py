import requests
import logging
from bs4 import BeautifulSoup


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ],
)

login_url = "https://www.scrapethissite.com/login/"
login_payload = {"username": "your_username", "password": "your_password"}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Connection": "keep-alive",
    "Referer": login_url,
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
}

session = requests.Session()


def login():
    target_url = "https://www.scrapethissite.com/pages/advanced/?gotcha=login"
    try:
        logging.info("Attempting to log in.")
        response = session.post(login_url, data=login_payload, headers=headers)

        if response.status_code == 200 and "login successful" in response.text.lower():
            logging.info("Login successful.")
            target_response = session.get(target_url, headers=headers)
            logging.info("Fetched target URL after login.")
            logging.info("Target response text: %s", target_response.text[:100])
        else:
            logging.error("Login failed.")

        logging.info("Session cookies: %s", session.cookies.get_dict())
    except requests.exceptions.RequestException as e:
        logging.error("Error during login: %s", e)


login()


def csrf():
    target_url = "https://www.scrapethissite.com/pages/advanced/?gotcha=csrf"
    try:
        logging.info("Fetching login page for CSRF token.")
        login_page = session.get(login_url)
        login_page_soup = BeautifulSoup(login_page.text, "html.parser")

        hidden_inputs = login_page_soup.find_all("input", type="hidden")
        hidden_fields = {
            input_tag["name"]: input_tag["value"] for input_tag in hidden_inputs
        }

        login_payload.update(hidden_fields)
        logging.info("Login payload with CSRF token updated.")

        login_response = session.post(login_url, data=login_payload, headers=headers)

        if (
            login_response.status_code == 200
            and "login successful" in login_response.text.lower()
        ):
            logging.info("Login successful with CSRF.")
            target_response = session.get(target_url, headers=headers)
            logging.info("Fetched target URL after CSRF login.")
            logging.info("Target response text: %s", target_response.text[:100])
        else:
            logging.error("Login failed with CSRF.")
    except requests.exceptions.RequestException as e:
        logging.error("Error during CSRF login: %s", e)


csrf()
