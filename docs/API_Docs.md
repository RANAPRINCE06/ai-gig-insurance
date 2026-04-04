# GigShield API Documentation

Base URL: `http://localhost:8000`
Interactive docs: `http://localhost:8000/docs`

---

## Authentication

All protected endpoints require a Bearer token in the `Authorization` header:
```
Authorization: Bearer <access_token>
```

### POST /api/auth/register
Register a new worker.

**Body:**
```json
{
  "name": "Rahul Kumar",
  "email": "rahul@gmail.com",
  "password": "password123",
  "mobile": "9876543210",
  "upi_id": "rahul@upi",
  "platform": "Zomato",
  "city": "Mumbai",
  "plan": "Standard",
  "avg_income": 950
}
```

### POST /api/auth/login
Login as a worker.

**Query params:** `email`, `password`

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": { ... }
}
```

### POST /api/auth/admin-login
Login as admin.

**Query params:** `username=admin`, `password=admin123`

---

## Users

### GET /api/users/me
Returns the currently authenticated user.

### GET /api/users/
Returns all workers. Admin only.

### PATCH /api/users/{user_id}
Update worker profile fields.

---

## Policies

### POST /api/policies/
Create a new insurance policy for a worker.

**Body:**
```json
{
  "worker_id": "W001",
  "plan": "Standard",
  "city": "Mumbai"
}
```

**Response:** Policy object with calculated premium and payout amount.

### GET /api/policies/
List all policies. Workers see only their own.

---

## Claims

### POST /api/claims/
File a new claim. System auto-scores fraud and may auto-pay.

**Body:**
```json
{
  "worker_id": "W001",
  "trigger_type": "Heavy Rain",
  "city": "Mumbai",
  "gps_confirmed": true,
  "duration": "3h 45m"
}
```

**Response:** Claim object. If auto-approved, `status` will be `paid` and `razorpay_tx_id` populated.

### GET /api/claims/
List claims. Optional `?status=flagged` filter.

### POST /api/claims/decide
Admin approves or rejects a flagged claim.

**Body:**
```json
{
  "claim_id": "CLM-008",
  "action": "approve",
  "reason": "GPS verified via alternate method"
}
```

### GET /api/claims/{claim_id}
Get single claim detail.

---

## Admin

### GET /api/admin/dashboard
Returns portfolio-level metrics.

**Response:**
```json
{
  "total_workers": 8,
  "active_policies": 6,
  "total_payouts_mtd": 9450,
  "flagged_claims": 3,
  "weekly_revenue": 392,
  "loss_ratio": 68.4,
  "total_claims_mtd": 11,
  "auto_approve_rate": 72
}
```

### GET /api/admin/workers
List all workers with fraud scores and status.

### PATCH /api/admin/workers/{worker_id}/suspend
Suspend a worker's account.

---

## Fraud Score Reference

| Score Range | Decision       | Flags                                    |
|-------------|----------------|------------------------------------------|
| 0–29        | AUTO_APPROVE   | Clean — instant UPI payout               |
| 30–69       | MANUAL_REVIEW  | Some risk signals — admin review needed  |
| 70–100      | AUTO_REJECT    | High risk — auto-blocked                 |

**Scoring factors:**
- Claims count > 8: +25pts
- GPS not confirmed: +40pts
- Duplicate device: +35pts
- UPI changed within 24h: +15pts
- Claim filed in < 2 min: +10pts
- Income discrepancy > 40%: +20pts
