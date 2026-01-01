import json
from datetime import datetime
from scrapers.zara import get_zara_trends
from scrapers.hm import get_hm_trends
from scrapers.asos import get_asos_trends

def run():
    results = {
        "timestamp": datetime.utcnow().isoformat(),
        "men": [],
        "women": []
    }

    print("Fashion Trend Bot started")

    print("Checking Zara")
    zara = get_zara_trends()
    results["men"].extend(zara["men"])
    results["women"].extend(zara["women"])

    print("Checking H&M")
    hm = get_hm_trends()
    results["men"].extend(hm["men"])
    results["women"].extend(hm["women"])

    print("Checking ASOS")
    asos = get_asos_trends()
    results["men"].extend(asos["men"])
    results["women"].extend(asos["women"])

    with open("output/trends.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Done")

if __name__ == "__main__":
    run()
