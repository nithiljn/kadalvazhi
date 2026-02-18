import asyncio
from app.services.weather_service import (
    WeatherService,
    WeatherAPIError,
    LocationNotFoundError
)
from app.utils.logger import get_logger

logger = get_logger(__name__)

async def test_weather_service():
    """Test weather service with real API calls"""
    service = WeatherService()
    print("TEST 1: Fetch weather for chennai ✅")
    try:
        userlocation = "chennai"
        weather = await service.get_weather(userlocation)
        print(f"  Location: {userlocation}")
        print(f"  Temperature: {weather.temperature}°C")
        print(f"  Feels like: {weather.feels_like}°C")
        print(f"  Humidity: {weather.humidity}%")
        print(f"  Wind speed: {weather.wind_speed} m/s")
        print(f"  Condition: {weather.weather_condition}")
        print(f"  Cloud coverage: {weather.cloud_coverage}%")
        print(f"  Visibility: {weather.visibility} m")
        print(f"  Pressure: {weather.pressure} hPa")
        print(f"  ✅ TEST PASSED\n")
    except Exception as e:
        print(f"  ❌ TEST FAILED: {e}\n")

    print("TEST 2: Invalid location (should fail gracefully) ❌")
    try:
        weather = await service.get_weather("InvalidCityXYZ123")
        print(f"  ❌ TEST FAILED: Should have raised error!\n")
    except LocationNotFoundError as e:
        print(f"  ✅ TEST PASSED: Caught error correctly")
        print(f"  Error message: {e}\n")
    except Exception as e:
        print(f"  ⚠️  Unexpected error: {e}\n")
    
    print("TEST 3: Fetch weather using coordinates (Chennai) ✅")
    try:
        weather = await service.get_weather("13.08,80.27")
        print(f"  Temperature: {weather.temperature}°C")
        print(f"  ✅ TEST PASSED\n")
    except Exception as e:
        print(f"  ❌ TEST FAILED: {e}\n")
    await service.close()

if __name__ == "__main__":
    asyncio.run(test_weather_service())