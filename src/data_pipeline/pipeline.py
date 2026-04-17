from .scraper import scrape_magicbricks
from .cleaner import clean_data
from .database import save_to_db

def run_pipeline():
    print("Scraping data...")
    df = scrape_magicbricks()

    print("DEBUG: Data columns →", df.columns)
    print("DEBUG: First rows →")
    print(df.head())

    print("Cleaning data...")
    df_clean = clean_data(df)
    print("DEBUG: Cleaned Data Columns →", df_clean.columns)
    print(df_clean.head())

    print("Saving to database...")
    save_to_db(df_clean)

    print("Pipeline completed!")

if __name__ == "__main__":
    run_pipeline()