import json
import os
from datetime import datetime, timezone
from scrapers.zara import get_zara_trends

# Optional: import H&M if you have it and want to use it
try:
    from scrapers.hm import get_hm_trends
    HAVE_HM = True
except ImportError:
    HAVE_HM = False
    print("Note: H&M scraper not found - skipping")

def run():
    print("\n" + "="*40)
    print("Fashion Trend Bot - Started")
    print(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))
    print("="*40 + "\n")

    all_products = {"men": [], "women": []}

    # === Zara ===
    print("Scraping Zara...")
    try:
        zara_data = get_zara_trends()
        all_products["men"].extend(zara_data.get("men", []))
        all_products["women"].extend(zara_data.get("women", []))
        print(f"→ Zara collected: {len(zara_data.get('men', []))} men's + {len(zara_data.get('women', []))} women's products")
    except Exception as e:
        print(f"Zara failed: {str(e)}")

    # === H&M (optional) ===
    if HAVE_HM:
        print("\nScraping H&M...")
        try:
            hm_data = get_hm_trends()
            all_products["men"].extend(hm_data.get("men", []))
            all_products["women"].extend(hm_data.get("women", []))
            print(f"→ H&M collected: {len(hm_data.get('men', []))} men's + {len(hm_data.get('women', []))} women's products")
        except Exception as e:
            print(f"H&M failed: {str(e)}")
    else:
        print("H&M skipped (no scraper available)")

    # === Summary ===
    total_men = len(all_products["men"])
    total_women = len(all_products["women"])
    print("\n" + "-"*40)
    print(f"Total collected: {total_men} men's + {total_women} women's products")
    print("-"*40)

    if total_men > 0:
        print("\nSample Men's products:")
        for item in all_products["men"][:3]:
            print(f" - {item.get('name', 'N/A')} | {item.get('price', 'N/A')} | {item.get('url', 'N/A')}")

    if total_women > 0:
        print("\nSample Women's products:")
        for item in all_products["women"][:3]:
            print(f" - {item.get('name', 'N/A')} | {item.get('price', 'N/A')} | {item.get('url', 'N/A')}")

    # === Save to JSON ===
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    data = {
        "timestamp": timestamp,
        "products": all_products
    }
    output_file = "output/trends.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved to: {output_file}")
    print("\nDone! You can now run the Shopify importer if ready.\n")


if __name__ == "__main__":
    run()
