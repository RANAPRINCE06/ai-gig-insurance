"""
Weather API integration.
Primary: Open-Meteo (free, no key needed)
Fallback: Mock data for demo
"""
import httpx
from datetime import datetime

CITIES = {
    "Mumbai":    {"lat": 19.0760, "lon": 72.8777},
    "Delhi":     {"lat": 28.6139, "lon": 77.2090},
    "Bengaluru": {"lat": 12.9716, "lon": 77.5946},
    "Pune":      {"lat": 18.5204, "lon": 73.8567},
    "Chennai":   {"lat": 13.0827, "lon": 80.2707},
    "Kolkata":   {"lat": 22.5726, "lon": 88.3639},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
}

WMO_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 51: "Light drizzle", 61: "Light rain", 63: "Moderate rain",
    65: "Heavy rain", 80: "Rain showers", 95: "Thunderstorm",
}


async def fetch_weather(city: str) -> dict:
    coords = CITIES.get(city)
    if not coords:
        return _mock_weather(city)

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={coords['lat']}&longitude={coords['lon']}"
        f"&current=temperature_2m,apparent_temperature,precipitation,"
        f"wind_speed_10m,relative_humidity_2m,weather_code"
        f"&wind_speed_unit=kmh"
    )
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            cur = data["current"]
            return {
                "source": "Open-Meteo (free)",
                "city": city,
                "temp_c": round(cur["temperature_2m"]),
                "feels_like_c": round(cur["apparent_temperature"]),
                "humidity": cur["relative_humidity_2m"],
                "rain_1h_mm": cur.get("precipitation", 0),
                "wind_kph": round(cur["wind_speed_10m"]),
                "description": WMO_CODES.get(cur["weather_code"], "Unknown"),
                "timestamp": datetime.utcnow().strftime("%H:%M:%S UTC"),
            }
    except Exception:
        return _mock_weather(city)


def _mock_weather(city: str) -> dict:
    import random
    t = 28 + random.randint(0, 10)
    return {
        "source": "Demo data",
        "city": city,
        "temp_c": t,
        "feels_like_c": t + 3,
        "humidity": 72,
        "rain_1h_mm": round(random.uniform(0, 20), 1),
        "wind_kph": 18,
        "description": "Partly cloudy",
        "timestamp": datetime.utcnow().strftime("%H:%M:%S UTC"),
    }
