import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_category(url, brand, gender):
    r = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    items = []

    products = soup.select("li.product-item")[:10]

    for p in products:
        name_tag = p.select_one("h2")
        link_tag = p.find("a")

        if not name_tag or not link_tag:
            continue

        items.append({
            "brand": brand,
            "gender": gender,
            "name": name_tag.get_text(strip=True),
            "url": "https://www2.hm.com" + link_tag["href"]
        })

    return items

def get_hm_trends():
    return {
        "men": scrape_category(
            "https://www2.hm.com/en_us/men/products/view-all.html",
            "H&M",
            "men"
        ),
        "women": scrape_category(
            "https://www2.hm.com/en_us/women/products/view-all.html",
            "H&M",
            "women"
        )
    }
