import streamlit as st
import pandas as pd
import joblib
import shap
from sqlalchemy import create_engine

st.set_page_config(layout="wide")

# -----------------------
# LOAD MODEL + DATA
# -----------------------
model = joblib.load("models/xgb_model.pkl")

engine = create_engine("sqlite:///data/real_estate.db")
df = pd.read_sql("SELECT * FROM properties", engine)

features = [
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

# -----------------------
# UI HEADER
# -----------------------
st.title("🏠 AI Real Estate Intelligence System")

# -----------------------
# SIDEBAR INPUT
# -----------------------
st.sidebar.header("Enter Property Details")

sqft = st.sidebar.slider("Area (sqft)", 500, 5000, 1200)
location_score = st.sidebar.slider("Location Score", 1, 10, 7)
livability_score = st.sidebar.slider("Livability Score", 0.0, 10.0, 5.0)

# simple defaults for now
input_data = pd.DataFrame([{
    "sqft": sqft,
    "price_per_sqft": 8000,
    "location_score": location_score,
    "livability_score": livability_score,
    "metro_distance_km": 2,
    "hospital_distance_km": 2,
    "school_distance_km": 2,
    "college_distance_km": 2,
    "bus_stop_distance_km": 1,
    "railway_distance_km": 3,
    "police_distance_km": 2,
    "postoffice_distance_km": 2
}])

# -----------------------
# PREDICTION
# -----------------------
prediction = model.predict(input_data)[0]

st.metric("💰 Predicted Price", f"₹{int(prediction):,}")

# -----------------------
# SHAP EXPLAINABILITY
# -----------------------
explainer = shap.Explainer(model, df[features])
shap_values = explainer(input_data)

st.subheader("🎯 Why this price?")

contributions = shap_values[0].values
feature_names = input_data.columns

top_features = sorted(
    zip(feature_names, contributions),
    key=lambda x: abs(x[1]),
    reverse=True
)[:3]

for name, val in top_features:
    impact = abs(val) * 100000  # scaled

    if val > 0:
        st.success(f"{name} increased price by ~₹{impact:,.0f}")
    else:
        st.error(f"{name} decreased price by ~₹{impact:,.0f}")