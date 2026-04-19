import pandas as pd
import shap
import joblib
from sqlalchemy import create_engine
from config.settings import FEATURES, DB_PATH, MODEL_PATH

# Load model
model = joblib.load("models/xgb_model.pkl")

# Load data
engine = create_engine("sqlite:///data/real_estate.db")
df = pd.read_sql("SELECT * FROM properties", engine)

# Same features as training
features = FEATURES

df = df.dropna(subset=features)

X = df[features]

# -------------------------
# SHAP EXPLAINER
# -------------------------
explainer = shap.Explainer(model, X)
shap_values = explainer(X)

# -------------------------
# GLOBAL EXPLANATION
# -------------------------
shap.summary_plot(shap_values, X)

# -------------------------
# LOCAL EXPLANATION (1 row)
# -------------------------
i = 0

prediction = model.predict(X.iloc[[i]])[0]

print(f"\n🏠 Predicted Price: ₹{prediction:,.0f}")

contributions = shap_values[i].values
feature_names = X.columns

print("\n🎯 Top Reasons:")

top_features = sorted(
    zip(feature_names, contributions),
    key=lambda x: abs(x[1]),
    reverse=True
)[:3]
total = sum(abs(contributions))
for name, val in top_features:
    impact = impact = (val / total) * prediction

    if val > 0:
        print(f"✅ {name} increased price by ~₹{impact:,.0f}")
    else:
        print(f"❌ {name} decreased price by ~₹{impact:,.0f}")