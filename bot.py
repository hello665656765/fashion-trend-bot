import json
import os
from datetime import datetime, timezone
from scrapers.zara import get_zara_trends

def run():
    print("\n" + "═" * 60)
    print("Fashion Trend Bot | Zara + ZenRows Edition")
    print("Started:", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))
    print("═" * 60 + "\n")

    all_products = {"men": [], "women": []}

    print("Scraping Zara...")
    try:
        zara = get_zara_trends()
        print(f"DEBUG: Zara scraper returned {len(zara['men'])} men's + {len(zara['women'])} women's products")
        all_products["men"].extend(zara["men"])
        all_products["women"].extend(zara["women"])
        print(f"Zara success → {len(zara['men'])} men's + {len(zara['women'])} women's products collected")
    except Exception as e:
        print(f"Zara failed: {e}")

    # Summary
    total = len(all_products["men"]) + len(all_products["women"])
    print("\n" + "─" * 60)
    print(f"Total products collected: {total}")
    print("─" * 60)

    if all_products["men"]:
        print("\nSample men's products (first 3):")
        for p in all_products["men"][:3]:
            print(f" • {p.get('name', 'N/A')} | {p.get('price', 'N/A')} | {p.get('url', 'N/A')}")

    if all_products["women"]:
        print("\nSample women's products (first 3):")
        for p in all_products["women"][:3]:
            print(f" • {p.get('name', 'N/A')} | {p.get('price', 'N/A')} | {p.get('url', 'N/A')}")

    # Save
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    data = {"timestamp": timestamp, "products": all_products}
    
    path = "output/trends.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: {path}")
    print("Finished.\n")


if __name__ == "__main__":
    run()
