"""
Maps / geolocation integration.
Used for:
  - GPS zone validation (is worker within disruption zone?)
  - Flood water level simulation (IMD data in production)
"""
import random
import httpx
from app.config import settings

CITY_COORDS = {
    "Mumbai":    (19.0760, 72.8777),
    "Delhi":     (28.6139, 77.2090),
    "Bengaluru": (12.9716, 77.5946),
    "Pune":      (18.5204, 73.8567),
    "Chennai":   (13.0827, 80.2707),
    "Kolkata":   (22.5726, 88.3639),
    "Hyderabad": (17.3850, 78.4867),
    "Ahmedabad": (23.0225, 72.5714),
}


def haversine_km(lat1, lon1, lat2, lon2) -> float:
    """Great-circle distance between two GPS coordinates in km."""
    from math import radians, sin, cos, sqrt, atan2
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


def is_within_disruption_zone(worker_lat: float, worker_lon: float, city: str, radius_km: float = 25) -> bool:
    """Returns True if worker GPS is within city disruption zone radius."""
    center = CITY_COORDS.get(city)
    if not center:
        return False
    dist = haversine_km(worker_lat, worker_lon, center[0], center[1])
    return dist <= radius_km


async def get_flood_level(city: str) -> float:
    """
    Returns simulated flood water level in meters.
    In production, this calls IMD Flood Alert API.
    """
    # Simulate realistic flood levels (2.0–3.2m)
    base = {"Mumbai": 2.8, "Delhi": 2.2, "Bengaluru": 1.8, "Chennai": 2.4}.get(city, 2.0)
    return round(base + random.uniform(-0.3, 0.5), 1)


async def reverse_geocode(lat: float, lon: float) -> dict:
    """Reverse geocode a coordinate using Google Maps API."""
    api_key = getattr(settings, "GOOGLE_MAPS_KEY", "")
    if not api_key:
        return {"city": "Unknown", "address": f"{lat:.4f}, {lon:.4f}"}
    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={api_key}"
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(url)
            data = resp.json()
            if data.get("results"):
                return {
                    "city": next(
                        (c["long_name"] for c in data["results"][0]["address_components"]
                         if "locality" in c["types"]), "Unknown"
                    ),
                    "address": data["results"][0]["formatted_address"],
                }
    except Exception:
        pass
    return {"city": "Unknown", "address": f"{lat:.4f}, {lon:.4f}"}
