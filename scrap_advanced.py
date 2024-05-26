import requests


# fake headers
def fake_header():
    try:

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Connection": "keep-alive",
            "Referer": "https://www.scrapethissite.com/pages/advanced/?gotcha=headers",
            "DNT": "1",  # Do Not Track Request Header
            "Upgrade-Insecure-Requests": "1",
        }

        response = requests.get(
            "https://www.scrapethissite.com/pages/advanced/?gotcha=headers",
            headers=headers,
        )
        print(response)

    except:
        print("Error in Header")


fake_header()
