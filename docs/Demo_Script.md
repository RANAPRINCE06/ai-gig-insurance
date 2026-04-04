# GigShield Demo Script

## 5-Minute Demo Flow

### 1. Login (30s)
- Open `gigshield.html` in browser
- **Worker view:** Login as `rahul@gmail.com` — show dashboard, active policy, past claims
- **Admin view:** Switch tab → login as `admin / admin123`

### 2. Live Trigger Monitor (60s)
- Navigate to **Trigger Monitor**
- Switch city to Mumbai — show real Open-Meteo weather data loading
- Point out: Rain 18.4mm/hr → ACTIVE (threshold: 15mm/hr)
- "When this fires, claims go out automatically — no human needed"

### 3. Demo Simulation (90s)
- Navigate to **Demo Simulation**
- Set: Heavy Rain · Mumbai · Rahul Kumar · Clean scenario
- Click **Run Full Simulation**
- Walk through each step as it animates:
  1. Open-Meteo rain confirmed
  2. WAQI AQI checked
  3. GPS zone validated
  4. Isolation Forest: score 12 → AUTO_APPROVE
  5. Razorpay UPI payout → ₹900 sent

### 4. Fraud Detection (60s)
- Navigate to **Fraud Detection**
- Show flagged claims (CLM-008, CLM-009 — Deepa Nair, GPS failed)
- Show score 78/100 → AUTO_REJECT
- "The same Isolation Forest model running in the Celery background task"

### 5. AI Advisor (60s)
- Navigate to **AI Advisor**
- Click **Fraud Batch Analysis** → show Claude AI reviewing all flagged claims
- "Admins can ask the AI to explain any decision or suggest premium changes"

---

## Key Talking Points

| Feature | What to say |
|---------|-------------|
| Zero-touch | "Worker gets paid before they even file a claim" |
| Parametric | "No adjuster, no paperwork — just data thresholds" |
| Fraud ML | "Isolation Forest catches GPS spoofing in real-time" |
| Scalable | "Celery workers can process 10,000 cities simultaneously" |
| API-first | "Plugs into any gig platform via REST API" |

---

## Common Questions

**Q: What if APIs are down?**
A: Open-Meteo is the free primary; all integrations have demo fallbacks. System never goes dark.

**Q: How do workers enroll?**
A: Flutter mobile app (or web) — KYC via Aadhaar + UPI verification in under 2 minutes.

**Q: What's the loss ratio target?**
A: <75%. Currently at 68.4% — profitable and sustainable.

**Q: How does pricing stay competitive?**
A: No sales force, no physical offices, 89% auto-processing — overhead is near zero.
