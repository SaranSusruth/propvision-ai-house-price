import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error
import pickle

# ─────────────────────────────────────────────
#  Load & Prepare Data
# ─────────────────────────────────────────────
data = pd.read_csv("dataset.csv")

# Encode zone column
le = LabelEncoder()
data['zone_encoded'] = le.fit_transform(data['zone'])

feature_cols = ['area', 'bedrooms', 'bathrooms', 'location_rating', 'age',
                'garage', 'pool', 'zone_encoded']

X = data[feature_cols]
y = data['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ─────────────────────────────────────────────
#  Train Models
# ─────────────────────────────────────────────
rf_model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42)
rf_model.fit(X_train, y_train)

gb_model = GradientBoostingRegressor(n_estimators=150, learning_rate=0.1, random_state=42)
gb_model.fit(X_train, y_train)

lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# ─────────────────────────────────────────────
#  Evaluate
# ─────────────────────────────────────────────
rf_r2 = r2_score(y_test, rf_model.predict(X_test))
gb_r2 = r2_score(y_test, gb_model.predict(X_test))
lr_r2 = r2_score(y_test, lr_model.predict(X_test))

print(f"Random Forest  R² = {rf_r2:.4f}")
print(f"Gradient Boost R² = {gb_r2:.4f}")
print(f"Linear Reg     R² = {lr_r2:.4f}")

# ─────────────────────────────────────────────
#  Save best model + encoder + feature importance
# ─────────────────────────────────────────────
best_model = rf_model  # typically best for structured data

feature_importance = dict(zip(feature_cols, best_model.feature_importances_))

model_bundle = {
    'model': best_model,
    'encoder': le,
    'feature_cols': feature_cols,
    'feature_importance': feature_importance,
    'model_name': 'Random Forest',
    'r2_score': rf_r2,
    'training_rows': len(data),
    'zone_classes': list(le.classes_)
}

pickle.dump(model_bundle, open("model.pkl", "wb"))
print("\n✅ Model bundle saved to model.pkl")
print(f"   Zones recognized: {list(le.classes_)}")
print(f"   Features: {feature_cols}")
