import streamlit as st
import pandas as pd
import joblib
import shap
from sqlalchemy import create_engine
from config.settings import FEATURES, DB_PATH, MODEL_PATH
from geopy.geocoders import Nominatim
from src.data_pipeline.geo_osm import get_nearest_places

geolocator = Nominatim(user_agent="real_estate_app")

def get_lat_lon(location):
    try:
        loc = geolocator.geocode(location + ", Kolkata, India")
        return loc.latitude, loc.longitude
    except:
        return 22.57, 88.36  # fallback Kolkata

geo_data = get_nearest_places(lat, lon)

metro_distance = geo_data.get("metro", 5)
hospital_distance = geo_data.get("hospital", 5)
school_distance = geo_data.get("school", 5)
college_distance = geo_data.get("college", 5)
bus_distance = geo_data.get("bus", 3)
railway_distance = geo_data.get("railway", 5)
police_distance = geo_data.get("police", 5)
postoffice_distance = geo_data.get("post_office", 5)

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
avg_price_per_sqft = df["price_per_sqft"].mean()

st.sidebar.subheader("📍 Select Location")

locations = sorted(df["location"].dropna().unique())

selected_location = st.sidebar.selectbox("Choose Area", locations)

# simple defaults for now
input_data = pd.DataFrame([{
    "sqft": sqft,
    "location_score": location_score,
    "livability_score": livability_score,
    "metro_distance_km": metro_distance,
    "hospital_distance_km": hospital_distance,
    "school_distance_km": school_distance,
    "college_distance_km": college_distance,
    "bus_stop_distance_km": bus_distance,
    "railway_distance_km": railway_distance,
    "police_distance_km": police_distance,
    "postoffice_distance_km": postoffice_distance
}])

# -----------------------
# PREDICTION
# -----------------------
prediction = model.predict(input_data)[0]
st.subheader("📊 Model Confidence")

confidence = model.score(df[features], df["price"])
st.write(f"R² Score: {confidence:.2f}")
st.metric("💰 Predicted Price", f"₹{int(prediction):,}")

# -----------------------
# SHAP EXPLAINABILITY
# -----------------------
explainer = shap.Explainer(model, df[features])

# ✅ GLOBAL SHAP
shap_values_full = explainer(df[features])

# ✅ LOCAL SHAP
shap_values_input = explainer(input_data)

st.subheader("🎯 Why this price?")

st.subheader("📊 Global Feature Importance")

import matplotlib.pyplot as plt

fig, ax = plt.subplots()
shap.summary_plot(shap_values_full, df[features], show=False)
st.pyplot(fig)

contributions = shap_values_input[0].values
feature_names = input_data.columns

top_features = sorted(
    zip(feature_names, contributions),
    key=lambda x: abs(x[1]),
    reverse=True
)[:3]

st.subheader("📊 Area Insights")

clean_df = df[df["location"].str.len() < 30]  # remove long garbage titles
st.write(
    clean_df.groupby("location")["price"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

import plotly.express as px

fig = px.histogram(df, x="price", nbins=20, title="Price Distribution")
st.plotly_chart(fig)

st.subheader("🔁 Compare Properties")

sample = df.sample(5)
st.dataframe(sample[["location", "price", "sqft", "livability_score"]])

import pydeck as pdk

if "lat" in df.columns:
    st.subheader("🗺️ Live Location Map")

    map_df = pd.DataFrame({
        "lat": [lat],
        "lon": [lon]
        })

    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=lat,
            longitude=lon,
            zoom=13,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=map_df,
                get_position='[lon, lat]',
                get_radius=300,
                get_color=[255, 0, 0],
            )
        ],
    ))

st.subheader("📍 Nearby Infrastructure")

st.write({
    "🚇 Metro (km)": metro_distance,
    "🏥 Hospital (km)": hospital_distance,
    "🏫 School (km)": school_distance,
    "🎓 College (km)": college_distance,
    "🚌 Bus Stop (km)": bus_distance,
    "🚆 Railway (km)": railway_distance,
    "🚓 Police (km)": police_distance,
})

import numpy as np

samples = []

for _ in range(30):
    noisy = input_data.copy()
    noisy["sqft"] *= np.random.uniform(0.9, 1.1)
    noisy["livability_score"] *= np.random.uniform(0.9, 1.1)
    samples.append(model.predict(noisy)[0])

low = np.percentile(samples, 10)
high = np.percentile(samples, 90)

st.write(f"📉 Confidence Range: ₹{int(low):,} - ₹{int(high):,}")

st.subheader("🎯 Top Reasons (Human Explanation)")

total = sum(abs(shap_values_input[0].values))

for name, val in top_features:
    impact = (val / total) * prediction

    if val > 0:
        st.success(f"✅ {name} increased price by ₹{abs(impact):,.0f}")
    else:
        st.error(f"❌ {name} decreased price by ₹{abs(impact):,.0f}")