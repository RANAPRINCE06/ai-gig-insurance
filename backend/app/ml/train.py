"""
Training script for GigShield ML models.

Run:
  python -m app.ml.train

Trains:
  1. Premium regression model (Random Forest)
  2. Fraud detection model (Isolation Forest)

Saves .pkl files to app/ml/
"""
import pickle
import numpy as np
import os

OUTPUT_DIR = os.path.dirname(__file__)


def train_premium_model():
    from sklearn.ensemble import RandomForestRegressor

    # Synthetic training data
    # Features: plan_enc, zone_enc, season_enc, claims_count, fraud_score, avg_income
    # Label: weekly_premium
    X = np.array([
        [0, 1, 1, 0,  0, 700],   # Basic, Normal, Normal → 29
        [1, 1, 1, 0,  0, 900],   # Standard, Normal, Normal → 49
        [2, 1, 1, 0,  0, 1200],  # Premium, Normal, Normal → 79
        [0, 3, 3, 2, 15, 700],   # Basic, High zone, Monsoon → ~53
        [1, 3, 3, 4, 30, 900],   # Standard, High, Monsoon → ~89
        [2, 2, 2, 1,  5, 1100],  # Premium, Medium, Summer → ~98
        [0, 0, 0, 0,  0, 500],   # Basic, Low, Winter → ~25
        [1, 2, 1, 3, 10, 800],   # Standard, Medium, Normal → ~62
    ])
    y = np.array([29, 49, 79, 53, 89, 98, 25, 62])

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    path = os.path.join(OUTPUT_DIR, "premium_model.pkl")
    with open(path, "wb") as f:
        pickle.dump(model, f)
    print(f"✅ Premium model saved → {path}")


def train_fraud_model():
    from sklearn.ensemble import IsolationForest

    # Synthetic clean claim data for training normal baseline
    # Features: claims_count, gps_fail, dup_device, new_upi, speed_mins, income_disc
    np.random.seed(42)
    n = 500
    X_clean = np.column_stack([
        np.random.randint(0, 5, n),      # claims_count (normal: 0-5)
        np.zeros(n),                      # gps_fail = 0 (clean)
        np.zeros(n),                      # duplicate_device = 0
        np.zeros(n),                      # new_upi = 0
        np.random.randint(3, 30, n),     # claim_speed_mins (normal: 3-30)
        np.random.randint(0, 20, n),     # income_discrepancy_pct (normal: <20)
    ])

    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X_clean)

    path = os.path.join(OUTPUT_DIR, "fraud_model.pkl")
    with open(path, "wb") as f:
        pickle.dump(model, f)
    print(f"✅ Fraud model saved → {path}")


if __name__ == "__main__":
    print("🚀 Training GigShield ML models...")
    train_premium_model()
    train_fraud_model()
    print("✅ All models trained and saved.")
