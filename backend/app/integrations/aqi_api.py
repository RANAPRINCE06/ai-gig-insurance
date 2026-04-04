"""
AQI API integration.
Primary: WAQI (World Air Quality Index) — requires API token
Fallback: Demo/simulated data
"""
import httpx
import random
from app.config import settings


AQI_STATION_TOKENS = {
    "Mumbai":    "@7016",
    "Delhi":     "@7022",
    "Bengaluru": "@7624",
    "Pune":      "@9248",
    "Chennai":   "@8025",
    "Kolkata":   "@8087",
    "Hyderabad": "@9017",
    "Ahmedabad": "@9350",
}


def _aqi_level(aqi: int) -> str:
    if aqi <= 50:   return "Good"
    if aqi <= 100:  return "Satisfactory"
    if aqi <= 200:  return "Moderate"
    if aqi <= 300:  return "Poor"
    if aqi <= 400:  return "Very Poor"
    return "Severe"


async def fetch_aqi(city: str) -> dict:
    token = getattr(settings, "WAQI_API_KEY", "")
    station = AQI_STATION_TOKENS.get(city, "@7016")

    if token:
        try:
            url = f"https://api.waqi.info/feed/{station}/?token={token}"
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(url)
                data = resp.json()
                if data.get("status") == "ok":
                    aqi = int(data["data"]["aqi"])
                    return {
                        "source": "WAQI (live)",
                        "city": city,
                        "aqi": aqi,
                        "level": _aqi_level(aqi),
                        "pm25": data["data"].get("iaqi", {}).get("pm25", {}).get("v"),
                        "threshold_breached": aqi >= 300,
                    }
        except Exception:
            pass

    # Demo fallback
    aqi = random.randint(40, 300)
    return {
        "source": "WAQI (demo fallback)",
        "city": city,
        "aqi": aqi,
        "level": _aqi_level(aqi),
        "pm25": round(aqi * 0.4),
        "threshold_breached": aqi >= 300,
    }
