
from app.schemas.weather import (
    WeatherCheckRequest,
    WeatherData,
    FishingRecommendation,
    WeatherCheckResponse,
    ErrorResponse
)
from datetime import datetime, date
from pydantic import ValidationError

print("TEST 1: Valid request ✅")
try:
    valid_request = WeatherCheckRequest(
        location="Chennai",
        check_date=date.today() 
    )
    print(f"  Location: {valid_request.location}")
    print(f"  Date: {valid_request.check_date}")
    print("  ✅ PASSED\n")
except ValidationError as e:
    print(f"  ❌ FAILED: {e}\n")

print("TEST 2: Empty location (should fail) ❌")
try:
    invalid_request = WeatherCheckRequest(
        location="   ", 
        check_date=date(2025, 2, 15)
    )
    print("  ❌ FAILED: Should have raised error!\n")
except ValidationError as e:
    print(f"  ✅ PASSED: Caught error correctly")
    print(f"  Error: {e.errors()[0]['msg']}\n")

print("TEST 3: Complete response schema ✅")
try:
    response = WeatherCheckResponse(
        location="Chennai",
        check_date=date(2025, 2, 15),
        weather=WeatherData(
            temperature=28.5,
            feels_like=30.2,
            humidity=75,
            wind_speed=3.5,
            wind_direction=180,
            weather_condition="Clear sky",
            cloud_coverage=20,
            visibility=10000,
            pressure=1013
        ),
        fishing_advice=FishingRecommendation(
            safe_to_fish=True,
            risk_level="low",
            recommendation="Good conditions!",
            risk_factors=[],
            best_fishing_hours="5 AM - 9 AM",
            precautions=["Carry water"]
        )
    )
    print(f"  Location: {response.location}")
    print(f"  Safe to fish: {response.fishing_advice.safe_to_fish}")
    print(f"  Risk level: {response.fishing_advice.risk_level}")
    print("  ✅ PASSED\n")
except ValidationError as e:
    print(f"  ❌ FAILED: {e}\n")

print("TEST 5: JSON serialization ✅")
try:
    response_json = response.model_dump_json(indent=2)
    print("  Sample JSON:")
    print(response_json[:200] + "...")
    print("  ✅ PASSED\n")
except Exception as e:
    print(f"  ❌ FAILED: {e}\n")