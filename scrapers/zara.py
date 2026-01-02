import requests
from bs4 import BeautifulSoup
import demjson3
import os
from dotenv import load_dotenv

load_dotenv()
ZENROWS_API_KEY = os.getenv("ZENROWS_API_KEY")

if not ZENROWS_API_KEY:
    raise ValueError("ZENROWS_API_KEY missing from .env")

def get_zara_trends():
    products = {"men": [], "women": []}

    base_params = {
        "apikey": ZENROWS_API_KEY,
        "js_render": "true",
        "antibot": "true",
        "premium_proxy": "true",
        "original_status": "true",
        "wait": "5000",
    }

    def fetch_category(url, gender):
        params = base_params.copy()
        params["url"] = url

        try:
            print(f"  Fetching Zara {gender.capitalize()} via ZenRows...")
            resp = requests.get("https://api.zenrows.com/v1/", params=params, timeout=120)
            resp.raise_for_status()

            html = resp.text
            print(f"  Response size: {len(html)} chars")

            raw_file = f"zara_{gender}_raw.html"
            with open(raw_file, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"  Raw HTML saved: {raw_file}")

            soup = BeautifulSoup(html, "html.parser")

            collected = []

            json_scripts = soup.find_all("script", type="application/ld+json")
            print(f"  Found {len(json_scripts)} JSON-LD scripts")

            for i, script in enumerate(json_scripts):
                text = script.string
                if not text:
                    continue

                text = text.strip()

                print(f"  Script {i+1} length: {len(text)}")
                print(f"  Script {i+1} preview: {text[:400]}...")

                try:
                    data = demjson3.decode(text)
                    print(f"  Parsed successfully with demjson3")

                    if isinstance(data, dict) and data.get("@type") == "ItemList":
                        print(f"  ItemList confirmed! {data.get('numberOfItems', 'unknown')} items")
                        item_list = data.get("itemListElement", [])
                        print(f"  itemListElement length: {len(item_list)}")

                        for pos, list_item in enumerate(item_list, 1):
                            item = list_item.get("item", {})
                            name = item.get("name", "N/A")
                            url = item.get("url", "")  # May be missing
                            offers = item.get("offers", {})
                            price = offers.get("price", "N/A")
                            image = item.get("image", "")

                            print(f"    Item {pos}: name='{name}', price='{price}', url='{url}'")

                            if name != "N/A":
                                collected.append({
                                    "brand": "Zara",
                                    "gender": gender,
                                    "name": name,
                                    "url": url if url else "N/A (missing in JSON)",
                                    "price": f"${price}" if price != "N/A" else "N/A",
                                    "image": image
                                })

                        if collected:
                            print(f"  SUCCESS! Extracted {len(collected)} products from JSON-LD")
                            return collected[:15]

                except demjson3.JSONDecodeError as e:
                    print(f"  demjson3 parse failed: {e}")
                except Exception as e:
                    print(f"  Unexpected error: {e}")

            print("  No valid JSON-LD extracted")
            return collected

        except requests.exceptions.RequestException as e:
            print(f"  ZenRows request failed: {e}")
            return []

    products["men"] = fetch_category("https://www.zara.com/us/en/man-best-sellers-l4883.html", "men")
    products["women"] = fetch_category("https://www.zara.com/us/en/woman-best-sellers-l5912.html", "women")

    return products
