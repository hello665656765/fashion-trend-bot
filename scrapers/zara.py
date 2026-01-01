import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_zara_trends():
    # Zara blocks aggressively; free fallback = placeholder logic
    return {
        "men": [{
            "brand": "Zara",
            "gender": "men",
            "name": "Zara Trend Placeholder",
            "url": "https://www.zara.com"
        }],
        "women": [{
            "brand": "Zara",
            "gender": "women",
            "name": "Zara Trend Placeholder",
            "url": "https://www.zara.com"
        }]
    }
