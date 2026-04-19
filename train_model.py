import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import pickle

def train_model():
    # ─────────────────────────────────────────────
    # Load & Prepare Data
    # ─────────────────────────────────────────────
    data = pd.read_csv("dataset.csv")

    le = LabelEncoder()
    data['zone_encoded'] = le.fit_transform(data['zone'])

    feature_cols = ['area', 'bedrooms', 'bathrooms', 'location_rating', 'age',
                    'garage', 'pool', 'zone_encoded']

    X = data[feature_cols]
    y = data['price']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ─────────────────────────────────────────────
    # Train Models
    # ─────────────────────────────────────────────
    rf_model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42)
    rf_model.fit(X_train, y_train)

    gb_model = GradientBoostingRegressor(n_estimators=150, learning_rate=0.1, random_state=42)
    gb_model.fit(X_train, y_train)

    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)

    # ─────────────────────────────────────────────
    # Evaluate
    # ─────────────────────────────────────────────
    rf_r2 = r2_score(y_test, rf_model.predict(X_test))

    # ─────────────────────────────────────────────
    # Save Model Bundle
    # ─────────────────────────────────────────────
    best_model = rf_model

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

    # Save model
    with open("model.pkl", "wb") as f:
        pickle.dump(model_bundle, f)

    return model_bundle


# Optional: allow standalone execution
if __name__ == "__main__":
    train_model()