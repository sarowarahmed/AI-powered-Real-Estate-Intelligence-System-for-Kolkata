from sqlalchemy import create_engine

engine = create_engine("sqlite:///data/real_estate.db")

def save_to_db(df):
    df.to_sql("properties", engine, if_exists="replace", index=False)