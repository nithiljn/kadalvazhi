@tool
async def get_weather(city: str) -> str:
    """Gets the current weather and temperature for a city."""
    print("DEBUG: get_weather tool called")
    api_key = config.OPENWEATHER_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        print(f"DEBUG: Status Code: {response.status_code}")
        print(f"DEBUG: Response Body: {response.text}")
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"The weather in {city} is {temp}°C with {desc}."
        else:
            return f"Error: Could not find weather for {city}. Check if the city name is correct."
