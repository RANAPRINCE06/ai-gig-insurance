# GigShield Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────┐
│                     GigShield Platform                   │
│                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐  │
│  │ Flutter App  │    │ React Admin  │    │ gigshield │  │
│  │  (Worker)    │    │    Panel     │    │   .html   │  │
│  └──────┬───────┘    └──────┬───────┘    └─────┬─────┘  │
│         │                  │                  │         │
│         └──────────────────┼──────────────────┘         │
│                            │ REST / JSON                  │
│                    ┌───────▼────────┐                    │
│                    │  FastAPI (8000) │                    │
│                    │  - Auth (JWT)  │                    │
│                    │  - Workers     │                    │
│                    │  - Policies    │                    │
│                    │  - Claims      │                    │
│                    │  - Admin       │                    │
│                    └───┬───────┬───┘                    │
│                        │       │                         │
│               ┌────────▼─┐  ┌──▼────────────┐           │
│               │ PostgreSQL│  │ Celery Workers│           │
│               │   (5432) │  │  + Beat (5min)│           │
│               └──────────┘  └──┬────────────┘           │
│                                │                         │
│                         ┌──────▼──────┐                  │
│                         │   Redis     │                  │
│                         │   (6379)    │                  │
│                         └─────────────┘                  │
└─────────────────────────────────────────────────────────┘

External APIs (all have free/demo fallbacks):
  ├── Open-Meteo    → weather, rainfall, heat index
  ├── WAQI          → AQI / air quality
  ├── IMD           → flood alerts (simulated)
  ├── Google Maps   → GPS zone validation
  └── Razorpay      → UPI payouts
```

## Auto-Claim Flow

```
Every 5 minutes (Celery Beat):

1. evaluate_triggers(city)
   ├── fetch_weather(city)   → Open-Meteo API
   ├── fetch_aqi(city)       → WAQI API
   └── get_flood_level(city) → IMD (simulated)

2. any_triggered(trigger_data)?
   NO  → log + sleep
   YES ↓

3. Find active workers in city with active policies

4. For each worker:
   compute_fraud_score(worker_data)
   ├── score < 30  → AUTO_APPROVE
   │     └── initiate_upi_payout() → Razorpay
   │           └── claim.status = "paid"
   └── score ≥ 30 → flag for manual review
         └── claim.status = "flagged" | "pending"
```

## Premium Formula

```
weekly_premium = base × zone_multiplier × history_multiplier × season_multiplier

base:            Basic=29, Standard=49, Premium=79
zone_multiplier: Low=0.9, Normal=1.0, Medium=1.2, High=1.4
season:          Winter=0.95, Normal=1.0, Summer=1.2, Monsoon=1.3
history:         0.95 if no prior claims, else 1.0
```

## ML Models

### Isolation Forest (Fraud)
- Trained on clean claim patterns (GPS ok, normal frequency, no device duplication)
- Anomaly score blended with rule-based score
- Saved to `backend/app/ml/fraud_model.pkl`

### Random Forest Regressor (Premium)
- Features: plan, zone, season, claims_count, fraud_score, avg_income
- Predicts personalized weekly premium
- Saved to `backend/app/ml/premium_model.pkl`
- Run `python -m app.ml.train` to retrain
