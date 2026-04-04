from datetime import datetime


def generate_worker_id(count: int) -> str:
    return f"W{str(count + 1).zfill(3)}"


def get_initials(name: str) -> str:
    return "".join(p[0].upper() for p in name.strip().split()[:2])


def format_inr(amount: float) -> str:
    return f"₹{amount:,.0f}"


def utc_now_str() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
