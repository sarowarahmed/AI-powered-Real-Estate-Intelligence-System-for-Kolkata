import streamlit as st
import pandas as pd
import joblib
import shap
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from sqlalchemy import create_engine
from config.settings import features_PATH, db_PATH, model_PATH
from geopy.geocoders import Nominatim
from src.data_pipeline.geo_osm import get_nearest_places
from streamlit_folium import st_folium
import folium
import pydeck as pdk
from src.data_pipeline.cleaner import get_location_score
from sklearn.metrics.pairwise import euclidean_distances

# -----------------------
# CONFIG
# -----------------------
st.set_page_config(layout="wide")
st.title("🏠 AI Real Estate Intelligence System")

# -----------------------
# LOAD MODEL + DATA
# -----------------------
model = joblib.load(model_PATH)
engine = create_engine(db_PATH)
df = pd.read_sql("SELECT * FROM properties", engine)

# -----------------------
# GEO SETUP
# -----------------------
geolocator = Nominatim(user_agent="heatmap_app")

@st.cache_data
def get_lat_lon(location):
    try:
        loc = geolocator.geocode(location + ", Kolkata, India")
        return loc.latitude, loc.longitude
    except:
        return None, None

# -----------------------
# HEATMAP DATA
# -----------------------
@st.cache_data
def prepare_heatmap_data(df):
    heatmap_data = []

    grouped = df.groupby("location")["price_per_sqft"].mean().reset_index()

    for _, row in grouped.iterrows():
        lat, lon = get_lat_lon(row["location"])
        if lat and lon:
            heatmap_data.append({
                "lat": lat,
                "lon": lon,
                "price": row["price_per_sqft"]
            })

    return pd.DataFrame(heatmap_data)

heatmap_df = prepare_heatmap_data(df)

# -----------------------
# SIDEBAR INPUT
# -----------------------
st.sidebar.header("Enter Property Details")

sqft = st.sidebar.slider("Area (sqft)", 500, 5000, 1200)

st.sidebar.subheader("📍 Select Location")
locations = sorted(df["location"].dropna().unique())
selected_location = st.sidebar.selectbox("Choose Area", locations)

# Auto location score (no manual slider)
selected_location = selected_location.strip()
location_score = get_location_score(selected_location)

# -----------------------
# MAP SECTION
# -----------------------
st.subheader("🗺️ Click on Map to Predict")

m = folium.Map(location=[22.57, 88.36], zoom_start=12)
map_data = st_folium(m, width=700, height=500)

# -----------------------
# HEATMAP UI
# -----------------------
st.subheader("📊 Kolkata Price Heatmap")

if not heatmap_df.empty:
    layer = pdk.Layer(
        "HeatmapLayer",
        data=heatmap_df,
        get_position='[lon, lat]',
        get_weight="price",
        radiusPixels=60,
    )

    view_state = pdk.ViewState(
        latitude=22.57,
        longitude=88.36,
        zoom=10,
    )

    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
    ))
else:
    st.warning("No heatmap data available")

# -----------------------
# WAIT FOR MAP CLICK
# -----------------------
if not map_data or not map_data.get("last_clicked"):
    st.warning("📍 Click on map to get prediction")

else:
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    st.success(f"📍 Selected Location: {lat:.4f}, {lon:.4f}")

    # -----------------------
    # GEO FEATURES
    # -----------------------
    geo_data = get_nearest_places(lat, lon)

    metro_distance = geo_data.get("metro", 5)
    hospital_distance = geo_data.get("hospital", 5)
    school_distance = geo_data.get("school", 5)
    college_distance = geo_data.get("college", 5)
    bus_distance = geo_data.get("bus", 3)
    railway_distance = geo_data.get("railway", 5)
    police_distance = geo_data.get("police", 5)
    postoffice_distance = geo_data.get("post_office", 5)

    # -----------------------
    # BUILD INPUT
    # -----------------------
    input_data = pd.DataFrame([{
        "sqft": sqft,
        "location_score": location_score,
        "livability_score": 5,
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
    st.metric("💰 Predicted Price", f"₹{int(prediction):,}")

    # -----------------------
    # SMART RECOMMENDATION ENGINE
    # -----------------------
    from sklearn.metrics.pairwise import euclidean_distances

    st.subheader("🤖 Recommended Properties")

    feature_cols = ["sqft", "location_score", "livability_score", "price"]

    # Copy dataset
    df_rec = df.copy()
    df_rec = df_rec.dropna(subset=feature_cols)

    # -----------------------
    # APPLY WEIGHTING (IMPORTANT)
    # -----------------------
    df_rec_weighted = df_rec.copy()

    df_rec_weighted["sqft"] *= 0.5
    df_rec_weighted["price"] *= 1.0
    df_rec_weighted["location_score"] *= 2.0
    df_rec_weighted["livability_score"] *= 2.0

    # Input vector
    input_vector = pd.DataFrame([{
        "sqft": sqft,
        "location_score": location_score,
        "livability_score": 5,
        "price": prediction
    }])

    # Apply same weights to input
    input_vector["sqft"] *= 0.5
    input_vector["price"] *= 1.0
    input_vector["location_score"] *= 2.0
    input_vector["livability_score"] *= 2.0

    # -----------------------
    # DISTANCE CALCULATION
    # -----------------------
    distances = euclidean_distances(
        df_rec_weighted[feature_cols],
        input_vector[feature_cols]
    )

    df_rec["similarity"] = distances

    # Get top matches
    recommendations = df_rec.sort_values("similarity").head(5)

    # Display
    st.dataframe(
        recommendations[["location", "price", "sqft", "livability_score"]]
    )

    # -----------------------
    # CONFIDENCE RANGE
    # -----------------------
    samples = []
    for _ in range(30):
        noisy = input_data.copy()
        noisy["sqft"] *= np.random.uniform(0.9, 1.1)
        samples.append(model.predict(noisy)[0])

    low = np.percentile(samples, 10)
    high = np.percentile(samples, 90)

    st.write(f"📉 Confidence Range: ₹{int(low):,} - ₹{int(high):,}")

    # -----------------------
    # INFRA DISPLAY
    # -----------------------
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

    # -----------------------
    # SHAP
    # -----------------------
    st.subheader("🎯 Explainability")

    explainer = shap.Explainer(model, df[features_PATH])
    shap_values_full = explainer(df[features_PATH])
    shap_values_input = explainer(input_data)

    fig, ax = plt.subplots()
    shap.summary_plot(shap_values_full, df[features_PATH], show=False)
    st.pyplot(fig)

    contributions = shap_values_input[0].values
    feature_names = input_data.columns

    top_features = sorted(
        zip(feature_names, contributions),
        key=lambda x: abs(x[1]),
        reverse=True
    )[:3]

    st.subheader("🎯 Top Reasons")

    total = sum(abs(contributions))

    for name, val in top_features:
        impact = (val / total) * prediction

        if val > 0:
            st.success(f"✅ {name} increased price by ₹{abs(impact):,.0f}")
        else:
            st.error(f"❌ {name} decreased price by ₹{abs(impact):,.0f}")

# -----------------------
# GLOBAL INSIGHTS
# -----------------------
st.subheader("📊 Area Insights")

clean_df = df[df["location"].str.len() < 30]

st.write(
    clean_df.groupby("location")["price"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

fig = px.histogram(df, x="price", nbins=20, title="Price Distribution")
st.plotly_chart(fig)

st.subheader("🔁 Compare Properties")
sample = df.sample(5)
st.dataframe(sample[["location", "price", "sqft"]])