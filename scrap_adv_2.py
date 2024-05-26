import requests
from bs4 import BeautifulSoup

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
    response = session.post(login_url, data=login_payload, headers=headers)

    if response.status_code == 200 and "login successful" in response.text.lower():
        print("Login successful")

        target_response = session.get(target_url, headers=headers)

        print(target_response.text)
    else:
        print("Login failed")

    print(session.cookies.get_dict())


login()


def csrf():
    target_url = "https://www.scrapethissite.com/pages/advanced/?gotcha=csrf"
    login_page = session.get(login_url)
    login_page_soup = BeautifulSoup(login_page.text, "html.parser")

    hidden_inputs = login_page_soup.find_all("input", type="hidden")

    hidden_fields = {
        input_tag["name"]: input_tag["value"] for input_tag in hidden_inputs
    }

    login_payload = {**login_payload, **hidden_fields}

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

    login_response = session.post(login_url, data=login_payload, headers=headers)

    if (
        login_response.status_code == 200
        and "login successful" in login_response.text.lower()
    ):
        print("Login successful")

        target_response = session.get(target_url, headers=headers)

        print(target_response.text)
    else:
        print("Login failed")


csrf()


"""
try this 

r1 = requests.get('https://www.scrapethissite.com/pages/advanced/?gotcha=login/user/password')
print(r1.ok)
r2 = requests.get('https://www.scrapethissite.com/pages/advanced/?gotcha=csrf/user/password')
print(r2.ok)

"""
