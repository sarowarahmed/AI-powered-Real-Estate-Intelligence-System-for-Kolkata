import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import xgboost as xgb
import joblib

# Load data from DB
engine = create_engine("sqlite:///data/real_estate.db")
df = pd.read_sql("SELECT * FROM properties", engine)

print("Data shape:", df.shape)

# ---------------------------
# FEATURE SELECTION
# ---------------------------
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

# Drop missing
df = df.dropna(subset=features + ["price"])

X = df[features]
y = df["price"]

# ---------------------------
# TRAIN TEST SPLIT
# ---------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------------------
# MODEL
# ---------------------------
model = xgb.XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    random_state=42
)

model.fit(X_train, y_train)

# ---------------------------
# EVALUATION
# ---------------------------
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MAE: {mae:.2f}")
print(f"R2 Score: {r2:.4f}")

# ---------------------------
# SAVE MODEL
# ---------------------------
joblib.dump(model, "models/xgb_model.pkl")

print("Model saved!")