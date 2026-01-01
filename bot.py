import requests
from pytrends.request import TrendReq
import csv

brands = {
    "Zara": "https://www.zara.com",
    "H&M": "https://www2.hm.com"
}

pytrends = TrendReq(hl='en-US', tz=360)

results = []

for brand in brands:
    keyword = brand + " women clothing"
    pytrends.build_payload([keyword], timeframe='now 7-d')
    trend = pytrends.interest_over_time()

    if not trend.empty:
        score = trend[keyword].mean()
        results.append([brand, round(score, 2)])

with open("trends.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Brand", "Trend Score"])
    writer.writerows(results)

print("Done!")
