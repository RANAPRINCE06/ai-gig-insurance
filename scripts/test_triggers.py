"""
Test trigger monitoring across all cities.
Run: python scripts/test_triggers.py
"""
import asyncio
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services.trigger_service import evaluate_triggers, any_triggered

CITIES = ["Mumbai", "Delhi", "Bengaluru", "Pune", "Chennai"]

async def main():
    print("🌐 GigShield Trigger Monitor Test\n" + "=" * 40)
    for city in CITIES:
        print(f"\n📍 {city}")
        data = await evaluate_triggers(city)
        for key in ["rain", "heat", "aqi", "flood"]:
            t = data[key]
            icon = {"rain": "🌧️", "heat": "🌡️", "aqi": "🌫️", "flood": "🌊"}[key]
            status_icon = {"ACTIVE": "🔴", "WATCHING": "🟡", "NORMAL": "🟢"}[t["status"]]
            val = t.get("current_mmhr") or t.get("current_c") or t.get("current") or t.get("current_m")
            print(f"  {icon} {key.upper():6s} {status_icon} {t['status']:8s}  value={val}")

        if any_triggered(data):
            print(f"  ⚡ TRIGGER FIRED — auto-claims would be generated for {city} workers")

    print("\n✅ Trigger test complete.")

if __name__ == "__main__":
    asyncio.run(main())
