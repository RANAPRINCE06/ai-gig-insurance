# GigShield AI — Parametric Microinsurance Platform

> Zero-touch auto-claim insurance for gig economy workers. Triggered by real weather, AQI, and flood data.

---

## 🏗 Project Structure

```
GigShield/
├── backend/                     # FastAPI Backend
│   ├── app/
│   │   ├── main.py             # Entry point
│   │   ├── config.py           # Env settings
│   │   ├── database.py         # PostgreSQL connection
│   │   ├── models/             # SQLAlchemy DB models
│   │   │   ├── user.py
│   │   │   ├── policy.py
│   │   │   ├── claim.py
│   │   │   └── trigger.py
│   │   ├── schemas/            # Pydantic schemas
│   │   │   ├── user_schema.py
│   │   │   ├── policy_schema.py
│   │   │   └── claim_schema.py
│   │   ├── api/                # REST API routes
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── policy.py
│   │   │   ├── claim.py
│   │   │   └── admin.py
│   │   ├── services/           # Business logic
│   │   │   ├── premium_service.py
│   │   │   ├── claim_service.py
│   │   │   ├── trigger_service.py
│   │   │   └── fraud_service.py
│   │   ├── integrations/       # External APIs
│   │   │   ├── weather_api.py  # Open-Meteo (free)
│   │   │   ├── aqi_api.py      # WAQI
│   │   │   ├── maps_api.py     # Google Maps / GPS
│   │   │   └── payment_api.py  # Razorpay UPI
│   │   ├── ml/                 # ML Models
│   │   │   ├── premium_model.py
│   │   │   ├── fraud_model.py  # Isolation Forest
│   │   │   └── train.py
│   │   ├── workers/            # Celery background jobs
│   │   │   ├── celery_worker.py
│   │   │   └── tasks.py
│   │   ├── utils/
│   │   │   ├── helpers.py
│   │   │   └── constants.py
│   │   └── core/
│   │       ├── security.py     # JWT
│   │       └── dependencies.py
│   ├── requirements.txt
│   ├── .env
│   └── Dockerfile
├── frontend/                   # React Admin Panel (see gigshield.html)
├── mobile/                     # Flutter Worker App
├── scripts/
│   ├── seed_data.py
│   └── test_triggers.py
├── docs/
│   ├── API_Docs.md
│   ├── Architecture.md
│   └── Demo_Script.md
├── docker-compose.yml
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone & Configure
```bash
git clone https://github.com/your-org/gigshield.git
cd GigShield
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys
```

### 2. Run with Docker Compose
```bash
docker-compose up --build
```

This starts:
- PostgreSQL on port 5432
- Redis on port 6379
- FastAPI backend on port 8000
- Celery worker + beat scheduler

### 3. Seed demo data
```bash
docker-compose exec backend python scripts/seed_data.py
```

### 4. Open the frontend
Open `gigshield.html` in your browser — the frontend is a self-contained single-page app.

### 5. API Docs
Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive Swagger UI.

---

## 🔑 Demo Credentials

| Role   | Email / Username       | Password    |
|--------|------------------------|-------------|
| Admin  | `admin@gigshield.com`  | `admin123`  |
| Worker | `rahul@gmail.com`      | `password123` |

---

## ⚙️ Environment Variables

| Variable              | Description                          | Required |
|-----------------------|--------------------------------------|----------|
| `DATABASE_URL`        | PostgreSQL connection string         | ✅        |
| `SECRET_KEY`          | JWT signing secret                   | ✅        |
| `OPENWEATHER_API_KEY` | OpenWeatherMap key (optional)        | ❌        |
| `WAQI_API_KEY`        | WAQI AQI API token (optional)        | ❌        |
| `GOOGLE_MAPS_KEY`     | Google Maps API key (optional)       | ❌        |
| `RAZORPAY_KEY_ID`     | Razorpay key ID (optional)           | ❌        |
| `RAZORPAY_KEY_SECRET` | Razorpay key secret (optional)       | ❌        |
| `REDIS_URL`           | Redis connection URL                 | ✅        |

> All external API keys are optional — the system uses free/demo fallbacks when not provided.

---

## 🤖 ML Models

Train models locally:
```bash
cd backend
python -m app.ml.train
```

- **Premium Model** — Random Forest regressor predicting weekly premium from zone, season, plan, and history
- **Fraud Model** — Isolation Forest anomaly detector trained on clean claim patterns

---

## 🔄 Auto-Claim Pipeline

```
Celery Beat (every 5 min)
  → evaluate_triggers(city)        # fetch weather + AQI
  → any_triggered?
      YES → find active workers in city
          → compute_fraud_score()
          → auto_approved?
              YES → initiate_upi_payout()   # Razorpay
              NO  → flag for manual review
```

---

## 📡 API Endpoints

| Method | Path                      | Description               |
|--------|---------------------------|---------------------------|
| POST   | `/api/auth/register`      | Worker registration       |
| POST   | `/api/auth/login`         | Worker login              |
| POST   | `/api/auth/admin-login`   | Admin login               |
| GET    | `/api/users/me`           | Get current user          |
| GET    | `/api/users/`             | List all workers (admin)  |
| POST   | `/api/policies/`          | Create policy             |
| GET    | `/api/policies/`          | List policies             |
| POST   | `/api/claims/`            | File a claim              |
| GET    | `/api/claims/`            | List claims               |
| POST   | `/api/claims/decide`      | Approve/reject (admin)    |
| GET    | `/api/admin/dashboard`    | Admin dashboard stats     |

Full Swagger docs at `/docs`.
