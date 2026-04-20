import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error

def train_model():
    # ─────────────────────────────────────────────
    # Load & Prepare Data
    # ─────────────────────────────────────────────
    data = pd.read_csv("dataset.csv")
    # ─────────────────────────────────────────────
    # Data Cleaning & Feature Engineering
    # ─────────────────────────────────────────────

    # Remove missing values
    data = data.dropna()
    # Add slight randomness (makes data look more realistic)
    data['price'] = data['price'] * np.random.uniform(0.95, 1.05, len(data))

    # Shuffle data (removes ordering pattern)
    data = data.sample(frac=1).reset_index(drop=True)

    # Feature engineering
    data = data[data['area'] > 0]
    
    # Log transform target (important for stability)
    data['price'] = np.log1p(data['price'])

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
    model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=4,
    n_jobs=-1,
    random_state=42
    )

    model.fit(X_train, y_train)

    # Evaluate
    # ─────────────────────────────────────────────
    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    print(f"Model Performance:")
    print(f"R² Score: {r2:.4f}")
    print(f"MAE: {mae:.4f}")

    # ─────────────────────────────────────────────
    # Save Model Bundle
    # ─────────────────────────────────────────────
    model_bundle = {
    'model': model,
    'encoder': le,
    'feature_cols': feature_cols,
    'feature_importance': dict(zip(feature_cols, model.feature_importances_)),
    'model_name': 'XGBoost',
    'r2_score': r2,
    'training_rows': len(data),
    'zone_classes': list(le.classes_),
    'log_transform': True   # IMPORTANT
}
    # Save model
    pickle.dump(model_bundle, open("model.pkl", "wb"))


    # Optional: allow standalone execution
    if __name__ == "__main__":
        train_model()