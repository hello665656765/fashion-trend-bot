from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}

def get_asos_trends():
    products = {"men": [], "women": []}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=HEADERS["User-Agent"],
            viewport={"width": 1280, "height": 800},
            ignore_https_errors=True,
        )
        page = context.new_page()

        def scrape_asos(url, gender):
            try:
                print(f"→ Loading ASOS {gender.capitalize()} New In...")
                page.goto(url, timeout=90000, wait_until="networkidle")
                time.sleep(3)  # Let JS settle
                
                page.wait_for_selector("article[data-auto-id='productTile']", timeout=30000)
                
                items = page.query_selector_all("article[data-auto-id='productTile']")
                print(f"   Found {len(items)} potential products")
                
                collected = []
                for item in items[:10]:  # Limit to top 10
                    name_el = item.query_selector("p[data-auto-id='productTileDescription']")
                    name = name_el.inner_text().strip() if name_el else None
                    
                    link_el = item.query_selector("a")
                    url = link_el.get_attribute("href") if link_el else None
                    if url and not url.startswith("http"):
                        url = "https://www.asos.com" + url
                    
                    price_el = item.query_selector("p[data-auto-id='productTilePrice']")
                    price = price_el.inner_text().strip() if price_el else ""
                    
                    img_el = item.query_selector("img")
                    img = img_el.get_attribute("src") or img_el.get_attribute("data-original") if img_el else ""
                    
                    if name and url:
                        collected.append({
                            "brand": "ASOS",
                            "gender": gender,
                            "name": name,
                            "url": url,
                            "price": price,
                            "image": img
                        })
                return collected
            except PlaywrightTimeoutError:
                print(f"Timeout on ASOS {gender} → possible slow load or block")
                return []
            except Exception as e:
                print(f"ASOS {gender} error: {str(e)}")
                return []

        # Men's new in
        products["men"] = scrape_asos(
            "https://www.asos.com/men/new-in/cat/?cid=27110",
            "men"
        )

        # Women's new in (adjust URL if needed)
        products["women"] = scrape_asos(
            "https://www.asos.com/women/new-in/cat/?cid=27108",
            "women"
        )
        
        browser.close()
    
    return products
