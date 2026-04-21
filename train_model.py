"""
PropVision AI — train_model.py
================================
Run this FIRST before launching app.py:
    python train_model.py

What this script does:
  1. Loads dataset.csv
  2. Engineers features (area_scaled, bed_bath_ratio, luxury_score)
  3. Trains XGBoost with tuned hyperparameters
  4. Saves model.pkl with ALL inference-time data (area_max, encoder, feature_cols, etc.)

Key fixes over original:
  - area_max stored in bundle → app.py uses it for correct scaling (not hardcoded 10000)
  - if __name__ block moved OUTSIDE function (was indented inside → never executed)
  - Random noise applied BEFORE log transform (not after)
  - 200-row dataset gives meaningful feature importance
  - feature importance: location_rating > area > zone > age > rooms (realistic)
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from xgboost import XGBRegressor


def train_model(csv_path: str = "dataset.csv") -> dict:
    # ──────────────────────────────────────────────────────────────
    # 1. LOAD DATA
    # ──────────────────────────────────────────────────────────────
    print("📂 Loading dataset...")
    data = pd.read_csv(csv_path)
    print(f"   Loaded {len(data)} rows, {len(data.columns)} columns")

    # Basic cleaning
    data = data.dropna()
    data = data[data["area"] > 0]
    data = data[data["price"] > 0]
    data = data.reset_index(drop=True)

    # ──────────────────────────────────────────────────────────────
    # 2. NOISE + SHUFFLE  (applied on raw price, BEFORE log)
    # ──────────────────────────────────────────────────────────────
    np.random.seed(42)
    data["price"] = data["price"] * np.random.uniform(0.97, 1.03, len(data))
    data = data.sample(frac=1, random_state=42).reset_index(drop=True)

    # ──────────────────────────────────────────────────────────────
    # 3. ENCODE ZONE
    # ──────────────────────────────────────────────────────────────
    le = LabelEncoder()
    data["zone_encoded"] = le.fit_transform(data["zone"])
    zone_classes = list(le.classes_)
    print(f"   Zone classes: {zone_classes}")

    # ──────────────────────────────────────────────────────────────
    # 4. FEATURE ENGINEERING
    #    area_max stored so app.py can scale area identically at inference
    # ──────────────────────────────────────────────────────────────
    area_max = float(data["area"].max())
    data["area_scaled"]    = data["area"] / area_max
    data["bed_bath_ratio"] = data["bedrooms"] / (data["bathrooms"] + 1)
    data["luxury_score"]   = (
        data["location_rating"] * 0.4
        + data["garage"]        * 0.2
        + data["pool"]          * 0.4
    )

    # ──────────────────────────────────────────────────────────────
    # 5. LOG-TRANSFORM TARGET  (stabilises regression on skewed prices)
    # ──────────────────────────────────────────────────────────────
    data["log_price"] = np.log1p(data["price"])

    # ──────────────────────────────────────────────────────────────
    # 6. FEATURE COLUMNS  (order matters — must match app.py exactly)
    # ──────────────────────────────────────────────────────────────
    feature_cols = [
        "area_scaled",      # normalised area
        "bedrooms",
        "bathrooms",
        "location_rating",  # most important real-world driver
        "age",
        "garage",
        "pool",
        "zone_encoded",
        "bed_bath_ratio",   # engineered
        "luxury_score",     # engineered composite
    ]

    X = data[feature_cols]
    y = data["log_price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ──────────────────────────────────────────────────────────────
    # 7. TRAIN XGBOOST
    # ──────────────────────────────────────────────────────────────
    print("🚀 Training XGBoost model...")
    model = XGBRegressor(
        n_estimators=400,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.85,
        colsample_bytree=0.85,
        min_child_weight=2,
        reg_alpha=0.05,
        reg_lambda=1.0,
        n_jobs=-1,
        random_state=42,
        verbosity=0,
    )
    model.fit(X_train, y_train)

    # ──────────────────────────────────────────────────────────────
    # 8. EVALUATE
    # ──────────────────────────────────────────────────────────────
    y_pred_log  = model.predict(X_test)
    y_pred_real = np.expm1(y_pred_log)
    y_test_real = np.expm1(y_test)

    r2  = r2_score(y_test, y_pred_log)         # R² on log scale (for display)
    mae = mean_absolute_error(y_test_real, y_pred_real)  # MAE in real dollars

    print(f"✅ Training complete!")
    print(f"   R² Score : {r2:.4f}  ({r2*100:.1f}%)")
    print(f"   MAE (USD): ${mae:,.0f}")

    # ──────────────────────────────────────────────────────────────
    # 9. FEATURE IMPORTANCE (normalised so they sum to 1.0)
    # ──────────────────────────────────────────────────────────────
    raw_fi   = model.feature_importances_
    norm_fi  = raw_fi / raw_fi.sum()
    feat_imp = dict(zip(feature_cols, norm_fi.tolist()))

    # Print for developer review
    print("\n📊 Feature Importance (normalised):")
    for feat, imp in sorted(feat_imp.items(), key=lambda x: -x[1]):
        bar = "█" * int(imp * 40)
        print(f"   {feat:<20} {bar}  {imp*100:.1f}%")

    # ──────────────────────────────────────────────────────────────
    # 10. SAVE BUNDLE
    #     Everything app.py needs at inference time is stored here.
    #     NEVER hardcode area_max or zone_classes in app.py — always
    #     read from bundle to guarantee train/inference consistency.
    # ──────────────────────────────────────────────────────────────
    bundle = {
        "model"            : model,
        "encoder"          : le,
        "feature_cols"     : feature_cols,   # exact column order for predict()
        "feature_importance": feat_imp,
        "model_name"       : "XGBoost",
        "r2_score"         : r2,
        "mae_usd"          : mae,
        "training_rows"    : len(data),
        "zone_classes"     : zone_classes,   # ['luxury','rural','suburban','urban']
        "log_transform"    : True,           # app.py uses np.expm1() on output
        "area_max"         : area_max,       # CRITICAL: used for area_scaled at inference
    }

    with open("model.pkl", "wb") as f:
        pickle.dump(bundle, f)

    print(f"\n💾 model.pkl saved successfully!")
    print(f"   area_max : {area_max:.0f} sq ft")
    print(f"   Zones    : {zone_classes}")
    return bundle


# ──────────────────────────────────────────────────────────────────────────────
#  Standalone execution  (was wrongly indented inside function in original)
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    train_model()