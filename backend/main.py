import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from config.settings import model_PATH
from src.data_pipeline.geo_osm import get_nearest_places
from src.data_pipeline.cleaner import get_location_score

app = FastAPI()

# Load model
model = joblib.load(model_PATH)

# -----------------------
# INPUT SCHEMA
# -----------------------
class PropertyInput(BaseModel):
    sqft: float
    location: str
    lat: float
    lon: float

# -----------------------
# PREDICTION API
# -----------------------
@app.get("/")
def home():
    return {"message": "Real Estate AI API Running 🚀"}

@app.post("/predict")
def predict(data: PropertyInput):

    # Geo features
    geo = get_nearest_places(data.lat, data.lon)

    # Location score
    location_score = get_location_score(data.location)

    # Build input
    input_df = pd.DataFrame([{
        "sqft": data.sqft,
        "location_score": location_score,
        "livability_score": 5,
        "metro_distance_km": geo.get("metro", 5),
        "hospital_distance_km": geo.get("hospital", 5),
        "school_distance_km": geo.get("school", 5),
        "college_distance_km": geo.get("college", 5),
        "bus_stop_distance_km": geo.get("bus", 3),
        "railway_distance_km": geo.get("railway", 5),
        "police_distance_km": geo.get("police", 5),
        "postoffice_distance_km": geo.get("post_office", 5)
    }])

    # Prediction
    prediction = model.predict(input_df)[0]

    return {
        "predicted_price": int(prediction),
        "geo_features": geo
    }