FEATURES = [
    "sqft",
    "price_per_sqft",
    "location_score",
    "livability_score",
    "metro_distance_km",
    "hospital_distance_km",
    "school_distance_km",
    "college_distance_km",
    "bus_stop_distance_km",
    "railway_distance_km",
    "police_distance_km",
    "postoffice_distance_km"
]

DB_PATH = "sqlite:///data/real_estate.db"
MODEL_PATH = "models/xgb_model.pkl"