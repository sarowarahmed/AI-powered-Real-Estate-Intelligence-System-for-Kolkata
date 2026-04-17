from playwright.sync_api import sync_playwright
import pandas as pd

def scrape_magicbricks():
    data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 👈 IMPORTANT
        page = browser.new_page()

        page.goto("https://www.magicbricks.com/property-for-sale/residential-real-estate?cityName=Kolkata")

        page.wait_for_timeout(8000)

        # Scroll to load listings
        for _ in range(3):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(2000)

        listings = page.query_selector_all("div.mb-srp__card")

        print(f"Found listings: {len(listings)}")

        for item in listings:
            try:
                title_el = item.query_selector("[class*='title']")
                price_el = item.query_selector("[class*='price']")
                area_el = item.query_selector("[class*='summary']")
                location_el = item.query_selector("[class*='loc'], [class*='location']")
                
                # ✅ DEFINE title FIRST
                title = title_el.inner_text() if title_el else None
        
                # ✅ NOW safe to use title
                location = location_el.inner_text() if location_el else title
        
                price = price_el.inner_text() if price_el else N
                area = area_el.inner_text() if area_el else None

                if price:  # only append valid rows
                    data.append({
                        "location_text": location,
                        "price": price,
                        "title": title,
                        "area": area
                    })

            except Exception as e:
                print("Error:", e)

        browser.close()

    df = pd.DataFrame(data)
    print("Scraped rows:", len(df))

    return df