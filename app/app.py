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
avg_price_per_sqft = df["price_per_sqft"].mean()

# simple defaults for now
input_data = pd.DataFrame([{
    "sqft": sqft,
    "price_per_sqft": avg_price_per_sqft,
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

st.write(df.groupby("location")["price"].mean().sort_values(ascending=False).head(10))

import plotly.express as px

fig = px.histogram(df, x="price", nbins=20, title="Price Distribution")
st.plotly_chart(fig)

st.subheader("🔁 Compare Properties")

sample = df.sample(5)
st.dataframe(sample[["location", "price", "sqft", "livability_score"]])

import pydeck as pdk

if "lat" in df.columns:
    st.subheader("🗺️ Map View")

    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=22.57,
            longitude=88.36,
            zoom=10,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position='[lon, lat]',
                get_radius=200,
                get_color=[200, 30, 0, 160],
            )
        ],
    ))

import numpy as np

preds = [model.predict(input_data)[0] for _ in range(10)]
low = np.percentile(preds, 10)
high = np.percentile(preds, 90)

st.write(f"📉 Confidence Range: ₹{int(low):,} - ₹{int(high):,}")

st.subheader("🎯 Top Reasons (Human Explanation)")

total_impact = sum(abs(shap_values_input[0].values))
for name, val in top_features:
    impact = abs(val) / total_impact * prediction

    if val > 0:
        st.success(f"✅ {name} increased price by ₹{impact:,.0f}")
    else:
        st.error(f"❌ {name} decreased price by ₹{impact:,.0f}")