# backend/test_weather_agent.py

import asyncio
from datetime import date
from app.agents.weather_agent import check_weather_for_fishing

async def test_agent():
    print("\n" + "="*60)
    print("TESTING WEATHER AGENT (LangGraph)")
    print("="*60 + "\n")
    
    location = "Chennai"
    check_date = date.today()
    
    print(f"Checking weather for: {location}")
    print(f"Date: {check_date}\n")
    
    result = await check_weather_for_fishing(location, check_date)
    
    print("="*60)
    print("RESULTS:")
    print("="*60)
    print(f"Location: {result['location']}")
    print(f"Date: {result['check_date']}")
    print()
    
    if result.get('weather_data'):
        weather = result['weather_data']
        print("WEATHER DATA:")
        print(f"  Temperature: {weather.temperature}°C")
        print(f"  Feels like: {weather.feels_like}°C")
        print(f"  Wind speed: {weather.wind_speed} m/s")
        print(f"  Humidity: {weather.humidity}%")
        print(f"  Condition: {weather.weather_condition}")
        print()
    
    print("FISHING ADVICE:")
    print(f"  Safe to fish: {result['safe_to_fish']}")
    print(f"  Risk level: {result['risk_level']}")
    print(f"  Risk factors: {result['risk_factors']}")
    print()
    print(f"RECOMMENDATION:")
    print(f"  {result['recommendation']}")
    print()
    
    if result.get('best_fishing_hours'):
        print(f"BEST HOURS: {result['best_fishing_hours']}")
        print()
    
    if result.get('precautions'):
        print("PRECAUTIONS:")
        for precaution in result['precautions']:
            print(f"  • {precaution}")
    
    print("\n" + "="*60)
    print("Check logs/app.log to see node execution flow!")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_agent())