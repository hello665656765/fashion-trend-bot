import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_asos(url, gender):
    r = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    items = []

    products = soup.select("article")[:10]

    for p in products:
        link = p.find("a", href=True)
        name = p.get_text(strip=True)

        if not link or not name:
            continue

        items.append({
            "brand": "ASOS",
            "gender": gender,
            "name": name[:80],
            "url": "https://www.asos.com" + link["href"]
        })

    return items

def get_asos_trends():
    return {
        "men": scrape_asos(
            "https://www.asos.com/men/new-in/cat/?cid=27110",
            "men"
        ),
        "women": scrape_asos(
            "https://www.asos.com/women/new-in/cat/?cid=27108",
            "women"
        )
    }
