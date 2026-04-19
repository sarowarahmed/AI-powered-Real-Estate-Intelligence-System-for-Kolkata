import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, r2_score
import xgboost as xgb
import joblib
from config.settings import FEATURES, DB_PATH, MODEL_PATH
 
# Load data from DB
engine = create_engine("sqlite:///data/real_estate.db")
df = pd.read_sql("SELECT * FROM properties", engine)

print("Data shape:", df.shape)

# ---------------------------
# FEATURE SELECTION
# ---------------------------
features = FEATURES
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

scores = cross_val_score(model, X, y, cv=5, scoring="r2")

print("CV R2 Scores:", scores)
print("Mean CV R2:", scores.mean())

# ---------------------------
# SAVE MODEL
# ---------------------------
joblib.dump(model, MODEL_PATH)

print("Model saved!")