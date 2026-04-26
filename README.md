# 🏠 SmartRealty AI — A Geo-Intelligent House Price Prediction System

🌐 **Live App**  
👉 https://your-app-link.streamlit.app  

---

## 🚀 Project Overview

Real estate pricing is highly dependent on **location, infrastructure, and accessibility**.

This project builds a **production-ready AI system** that predicts property prices using:

- 🧠 Machine Learning (XGBoost)
- 🗺️ Real-time Geo Intelligence (OpenStreetMap)
- 🎯 Explainable AI (SHAP)
- 📍 Interactive Map-based UI

👉 Unlike traditional models, this system uses **live infrastructure data** (metro, hospitals, schools, etc.) instead of static features.

---

## 🎯 Problem Statement

> Can we predict real estate prices dynamically using location intelligence and surrounding infrastructure?

---

## ✅ Objectives

- Predict house prices accurately  
- Incorporate **real-world geo features**  
- Provide **human-readable explanations**  
- Build an **interactive product (not just a model)**  

---

## 🧠 Key Features

### 🖱️ 1. Click-on-Map Prediction
- Select any location on map  
- Fetch real-time geo data  
- Predict price instantly  

---

### 🗺️ 2. Geo Intelligence Engine
Uses OpenStreetMap to compute:

- 🚇 Distance to Metro  
- 🏥 Hospitals  
- 🏫 Schools  
- 🎓 Colleges  
- 🚌 Bus Stops  
- 🚆 Railway Stations  
- 🚓 Police Stations  

---

### 📊 3. Price Heatmap
- Visualizes pricing patterns across regions  
- Helps identify high/low value zones  

---

### 🤖 4. Smart Recommendation Engine
- Suggests similar properties  
- Based on:
  - Price  
  - Area  
  - Location score  
  - Livability  

---

### 🎯 5. Explainable AI (SHAP)
- Shows **why** a price was predicted  
- Example:
sqft increased price by ₹X
location_score increased price by ₹Y


---

## 📊 Dataset & Pipeline

### 🔄 Data Flow
Web Scraping → Cleaning → Feature Engineering → Database → Model → UI


---

### 🧹 Data Processing

✔ Price normalization (Lac/Cr → numeric)  
✔ Area extraction (sqft)  
✔ Location parsing  
✔ Feature engineering  

---

### ⚙️ Features Used

- sqft  
- location_score  
- livability_score  
- infrastructure distances  
- price_per_sqft  

---

## 🤖 Model Development

### Models Considered

- Linear Regression  
- Random Forest  
- XGBoost ✅ (Final Model)

---

### 🏆 Final Model: XGBoost

**Why?**

- Handles non-linearity  
- Works well on structured data  
- High performance  

---

### 📈 Performance

- R² Score: ~0.93  
- Strong generalization  

---

## 🔍 Explainability

Using SHAP:

- Global feature importance  
- Local prediction explanation  
- Human-readable outputs  

---

## 🧠 Geo Intelligence (Key Innovation)

Instead of static features:

```text
Location → Coordinates → OSM → Real distances → Model input

## 🖥️ Application UI

Built with Streamlit:

Interactive sliders
Map-based input
Heatmaps
Recommendations
Explainability panel

⚙️ Tech Stack
🧠 ML
Scikit-learn
XGBoost
SHAP
🌍 Geo
OSMnx
Geopy
🖥️ App
Streamlit
Plotly / PyDeck / Folium
🗄️ Data
SQLite
📂 Project Structure
AI-RealEstate/

├── app/
│   └── app.py
│
├── models/
│   └── xgb_model.pkl
│
├── data/
│   └── real_estate.db
│
├── src/
│   ├── data_pipeline/
│   └── models/
│
├── requirements.txt
└── README.md
⚡ How to Run Locally
# Clone repo
git clone https://github.com/your-username/your-repo

# Move into folder
cd AI-powered-Real-Estate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app/app.py
🚀 Future Improvements
🔥 FastAPI backend (microservice architecture)
🐳 Docker deployment
🧠 Advanced ensembling (CatBoost / stacking)
📊 User behavior tracking
🌍 Multi-city expansion
👤 Author

Sarowar Ahmed
Data Science | ML Engineering | Geo AI

⭐ Support

If you found this project useful:

⭐ Star the repo
🍴 Fork it
📢 Share it

## 💼 Recruiter Note

This project demonstrates:

End-to-end ML system design
Real-world data pipeline
Geo-spatial feature engineering
Explainable AI (SHAP)
Interactive product development
Deployment-ready architecture