from playwright.sync_api import sync_playwright
import pandas as pd

def scrape_magicbricks():
    data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 🔥 LOOP THROUGH MULTIPLE PAGES
        for page_num in range(1, 50):   # 👈 CHANGE HERE (can increase later)
            print(f"\n📄 Scraping page {page_num}...")

            url = f"https://www.magicbricks.com/property-for-sale/residential-real-estate?cityName=Kolkata&page={page_num}"
            page.goto(url)

            page.wait_for_timeout(6000)

            # Scroll to load listings
            for _ in range(3):
                page.mouse.wheel(0, 3000)
                page.wait_for_timeout(1500)

            listings = page.query_selector_all("div.mb-srp__card")

            print(f"Found listings: {len(listings)}")

            # 🚨 STOP IF NO MORE DATA (IMPORTANT)
            if len(listings) == 0:
                print("No more listings. Stopping...")
                break

            for item in listings:
                try:
                    title_el = item.query_selector("[class*='title']")
                    price_el = item.query_selector("[class*='price']")
                    area_el = item.query_selector("[class*='summary']")
                    location_el = item.query_selector("[class*='loc'], [class*='location']")
                    
                    title = title_el.inner_text() if title_el else None
                    location = location_el.inner_text() if location_el else title
                    price = price_el.inner_text() if price_el else None
                    area = area_el.inner_text() if area_el else None

                    if price:
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
    print("\n✅ Total Scraped rows:", len(df))
    print(df.shape)

    return df