"""
Trigger monitoring service.
Evaluates weather/AQI/flood data against thresholds
and returns trigger status for each city.
"""
from app.integrations.weather_api import fetch_weather
from app.integrations.aqi_api import fetch_aqi
from app.integrations.maps_api import get_flood_level

THRESHOLDS = {
    "rain_mmhr": 15,
    "aqi": 300,
    "heat_index_c": 44,
    "flood_level_m": 3.0,
}


def _status(current, threshold, watch_pct=0.75):
    if current >= threshold:
        return "ACTIVE"
    if current >= threshold * watch_pct:
        return "WATCHING"
    return "NORMAL"


async def evaluate_triggers(city: str) -> dict:
    weather = await fetch_weather(city)
    aqi_data = await fetch_aqi(city)
    flood_m = await get_flood_level(city)

    rain = weather.get("rain_1h_mm", 0)
    heat = weather.get("feels_like_c", 30)
    aqi = aqi_data.get("aqi", 100)

    return {
        "city": city,
        "fetched_at": weather.get("timestamp"),
        "rain": {
            "current_mmhr": round(rain, 1),
            "threshold_mmhr": THRESHOLDS["rain_mmhr"],
            "percentage": min(100, round(rain / THRESHOLDS["rain_mmhr"] * 100)),
            "triggered": rain >= THRESHOLDS["rain_mmhr"],
            "status": _status(rain, THRESHOLDS["rain_mmhr"]),
            "source": weather.get("source"),
            "temp_c": weather.get("temp_c"),
            "humidity": weather.get("humidity"),
            "description": weather.get("description"),
        },
        "heat": {
            "current_c": heat,
            "threshold_c": THRESHOLDS["heat_index_c"],
            "percentage": min(100, round(heat / THRESHOLDS["heat_index_c"] * 100)),
            "triggered": heat >= THRESHOLDS["heat_index_c"],
            "status": _status(heat, THRESHOLDS["heat_index_c"], 0.85),
            "source": weather.get("source"),
        },
        "aqi": {
            "current": aqi,
            "threshold": THRESHOLDS["aqi"],
            "percentage": min(100, round(aqi / THRESHOLDS["aqi"] * 100)),
            "triggered": aqi >= THRESHOLDS["aqi"],
            "status": _status(aqi, THRESHOLDS["aqi"], 0.67),
            "level": aqi_data.get("level"),
            "source": aqi_data.get("source"),
        },
        "flood": {
            "current_m": flood_m,
            "threshold_m": THRESHOLDS["flood_level_m"],
            "percentage": min(100, round(flood_m / THRESHOLDS["flood_level_m"] * 100)),
            "triggered": flood_m >= THRESHOLDS["flood_level_m"],
            "status": _status(flood_m, THRESHOLDS["flood_level_m"], 0.83),
            "source": "IMD Flood Alert",
        },
    }


def any_triggered(trigger_data: dict) -> bool:
    return any(
        trigger_data.get(k, {}).get("triggered", False)
        for k in ["rain", "heat", "aqi", "flood"]
    )
