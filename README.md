<div align="center">

# 🛡️ GigShield AI

### Parametric Microinsurance Platform for Gig Economy Workers

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)

> **Zero-touch auto-claim insurance powered by real-time weather, AQI, and flood intelligence.**

GigShield AI is a smart microinsurance platform for delivery riders, drivers, and daily wage earners. It automatically detects environmental disruptions and instantly processes eligible claims using AI-driven parametric triggers — no paperwork, no waiting, no hassle.

[Features](#-key-features) • [Architecture](#-system-architecture) • [Quick Start](#-quick-start) • [API Docs](#-api-endpoints) • [ML Models](#-machine-learning-models)

</div>

---

## 🎯 The Problem

Millions of gig workers lose daily income due to floods, heavy rainfall, hazardous air quality, and extreme weather. Traditional insurance systems fail them by:

- Requiring extensive paperwork
- Taking weeks for claim approval
- Having high operational costs
- Being completely inaccessible for informal workers

---

## ✨ Key Features

| Feature | Description |
|---|---|
| ⚡ **Auto Claims** | Claims triggered instantly on rainfall, floods, AQI spikes, and extreme weather |
| 🤖 **AI Fraud Detection** | Isolation Forest ML models detect suspicious claim patterns in real-time |
| 💳 **Instant UPI Payouts** | Approved claims paid out automatically via Razorpay APIs |
| 📡 **Live Environmental Monitoring** | Integrated with Open-Meteo, AQI, and GPS APIs |
| 📊 **Dynamic Premium Engine** | Premiums calculated from zone risk, seasonal data, and claim history |

---

## 🏗️ System Architecture

```
         ┌──────────────────────────┐
         │     External APIs        │
         │  Weather  •  AQI  •  GPS │
         └────────────┬─────────────┘
                      │
                      ▼
  ┌───────────────────────────────────────┐
  │            FastAPI Backend            │
  │  Auth • Policies • Claims • Fraud     │
  └────────────────┬──────────────────────┘
                   │
          ┌────────┴─────────┐
          ▼                  ▼
   ┌─────────────┐    ┌──────────────┐
   │ PostgreSQL  │    │ Redis+Celery │
   └─────────────┘    └──────┬───────┘
                             │
                             ▼
                      ┌─────────────┐
                      │ Razorpay API│
                      └─────────────┘
```

---

## 🔄 Automated Claim Workflow

```
Celery Scheduler
      │
      ▼
Fetch Weather + AQI Data
      │
      ▼
Check Trigger Thresholds
      │
      ▼
Find Active Workers in Zone
      │
      ▼
Run Fraud Detection
      │
   ┌──┴──┐
   ▼     ▼
Auto   Manual
Payout Review
(UPI)
```

---

## 🧠 Technology Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| Frontend | React.js |
| Mobile | Flutter |
| Database | PostgreSQL |
| Queue System | Redis + Celery |
| Machine Learning | Scikit-learn |
| Authentication | JWT |
| Payments | Razorpay |
| Containerization | Docker |

---

## 📁 Project Structure

```
GigShield/
├── backend/
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── database.py
│       ├── models/          # SQLAlchemy ORM models
│       ├── schemas/         # Pydantic request/response schemas
│       ├── api/             # Route handlers
│       ├── services/        # Business logic
│       ├── integrations/    # Weather, AQI, GPS clients
│       ├── ml/              # Fraud detection & premium models
│       ├── workers/         # Celery background tasks
│       ├── utils/
│       └── core/
├── frontend/                # React Admin Dashboard
├── mobile/                  # Flutter Worker App
├── scripts/
├── docs/
├── docker-compose.yml
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- [Docker](https://www.docker.com/get-started) & Docker Compose
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/gigshield.git
cd GigShield
```

### 2. Configure Environment Variables

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` with your API keys and secrets (see [Environment Variables](#%EF%B8%8F-environment-variables)).

### 3. Start with Docker Compose

```bash
docker-compose up --build
```

This spins up: PostgreSQL, Redis, FastAPI backend, Celery workers, and scheduler services.

### 4. Seed Demo Data

```bash
docker-compose exec backend python scripts/seed_data.py
```

### 5. Open API Documentation

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive Swagger UI.

---

## 🔑 Demo Credentials

| Role | Email | Password |
|---|---|---|
| Admin | admin@gigshield.com | admin123 |
| Worker | rahul@gmail.com | password123 |

> ⚠️ Change these before any production deployment.

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Worker registration |
| POST | `/api/auth/login` | Worker login |
| POST | `/api/auth/admin-login` | Admin login |

### Users

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/users/me` | Get current user |
| GET | `/api/users/` | List all workers (admin) |

### Policies

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/policies/` | Create a policy |
| GET | `/api/policies/` | List policies |

### Claims

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/claims/` | File a claim |
| GET | `/api/claims/` | List claims |
| POST | `/api/claims/decide` | Approve or reject a claim (admin) |

### Admin

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/admin/dashboard` | Platform-wide statistics |

---

## 🤖 Machine Learning Models

### Premium Prediction (Random Forest Regressor)

Predicts personalized insurance premiums using:
- Seasonal and historical weather data
- Zone risk scores
- Worker claim history
- Worker category (rider, driver, etc.)

### Fraud Detection (Isolation Forest)

Flags suspicious claims by analyzing:
- Claim frequency anomalies
- GPS/location mismatches
- Environmental trigger inconsistencies
- Behavioral patterns over time

---

## ⚙️ Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | JWT signing secret |
| `REDIS_URL` | Redis connection string |
| `OPENWEATHER_API_KEY` | Open-Meteo / OpenWeather API key |
| `WAQI_API_KEY` | World AQI API key |
| `GOOGLE_MAPS_KEY` | Google Maps / GPS services key |
| `RAZORPAY_KEY_ID` | Razorpay payment gateway key |
| `RAZORPAY_KEY_SECRET` | Razorpay payment gateway secret |

---

## 🔐 Security

- JWT-based authentication with refresh tokens
- Bcrypt password hashing
- Role-Based Access Control (Worker / Admin)
- Input validation via Pydantic schemas
- Dockerized infrastructure with environment isolation

---

## 📈 Roadmap

- [ ] Hyperlocal flood prediction via satellite data
- [ ] Blockchain-based claim verification
- [ ] WhatsApp onboarding flow
- [ ] Multi-language support (Hindi, Tamil, Telugu, etc.)
- [ ] Advanced AI risk scoring engine
- [ ] Offline-first Flutter mobile app

---

## 🏆 Impact

✅ Instant insurance settlements — from weeks to seconds  
✅ Reduced fraud losses via ML anomaly detection  
✅ Financial inclusion for millions of gig workers  
✅ Climate resilience support for vulnerable communities  
✅ Scalable low-cost insurance operations  

---

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss what you'd like to change, then submit a pull request.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ for gig workers everywhere.**

*GigShield AI — Automated Protection. Instant Payouts. Zero Paperwork.*

</div>
