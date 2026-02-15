import httpx
import asyncio
from typing import Optional
from datetime import datetime

from app.config import settings
from app.utils.logger import get_logger
from app.schemas.weather import WeatherData

logger = get_logger(__name__)

class WeatherAPIError(Exception):
    """
    Raised when weather API fails
    """
    pass


class LocationNotFoundError(Exception):
    """
    Raised when location is not found in API
    """
    pass

class WeatherService:
    """
    Service for fetching weather data from OpenWeather API

    """
    
    def __init__(self):
        self.api_key = settings.openweather_api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
        self.client = httpx.AsyncClient(
            timeout=10.0,  # 10 second timeout
        )
        
        logger.info("WeatherService initialized")
    
    async def close(self):
        """
        Close HTTP client connection
        """
        await self.client.aclose()
        logger.info("WeatherService client closed")
    
    async def get_weather(self,location: str,max_retries: int = 3) -> WeatherData:
        """
        Fetch weather data for location with retry logic
        """
        logger.info(f"Fetching weather for location: {location}")
        
        for attempt in range(max_retries):
            try:
                raw_data = await self._fetch_from_api(location)
                
                weather_data = self._parse_response(raw_data)
                
                logger.info(
                    f"Weather fetched successfully for {location} "
                    f"(attempt {attempt + 1}/{max_retries})"
                )
                
                return weather_data
                
            except LocationNotFoundError:
                logger.error(f"Location not found: {location}")
                raise
                
            except Exception as e:
                logger.warning(
                    f"Attempt {attempt + 1}/{max_retries} failed for {location}: {e}"
                )
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.info(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(
                        f"All {max_retries} attempts failed for {location}"
                    )
                    raise WeatherAPIError(
                        f"Unable to fetch weather data after {max_retries} attempts. "
                        f"Please try again later or check alternative sources."
                    )
    
    async def _fetch_from_api(self, location: str) -> dict:
        """
        Make HTTP request to OpenWeather API
        Supports both location names and coordinates (lat,lon format)
        """
        url = f"{self.base_url}/weather"
        
        # Check if location is coordinates (format: "lat,lon")
        if ',' in location:
            try:
                parts = location.split(',')
                lat = float(parts[0].strip())
                lon = float(parts[1].strip())
                
                # Use lat/lon parameters for coordinates
                params = {
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key,
                    "units": "metric",
                    "lang": "en",
                }
                logger.debug(f"Detected coordinates: lat={lat}, lon={lon}")
            except (ValueError, IndexError):
                params = {
                    "q": location,
                    "appid": self.api_key,
                    "units": "metric",
                    "lang": "en",
                }
                logger.debug(f"Invalid coordinate format, treating as location name")
        else:
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "metric",  # Celsius for Indian users
                "lang": "en",       # Can add Tamil/Malayalam
            }
        
        logger.debug(f"API Request: {url} with params: {params}")
        try:
            response = await self.client.get(url, params=params)
            if response.status_code == 404:
                raise LocationNotFoundError(
                    f"Location '{location}' not found. "
                    f"Please check spelling or try coordinates (lat,lon)"
                )
            response.raise_for_status()
            data = response.json()
            logger.debug(f"API Response: {data}")
            
            return data
            
        except httpx.TimeoutException:
            logger.error(f"API request timed out for {location}")
            raise WeatherAPIError("Weather API request timed out")
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code}")
            raise WeatherAPIError(f"Weather API returned error: {e}")
            
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise WeatherAPIError("Unable to connect to weather API")
    
    def _parse_response(self, data: dict) -> WeatherData:
        """
        Parse OpenWeather API response into our WeatherData schema     
        """
        try:
            weather_data = WeatherData(
                temperature=data["main"]["temp"],
                feels_like=data["main"]["feels_like"],
                humidity=data["main"]["humidity"],
                wind_speed=data["wind"]["speed"],
                wind_direction=data["wind"].get("deg", 0),
                weather_condition=data["weather"][0]["description"],
                cloud_coverage=data["clouds"]["all"],
                visibility=data.get("visibility"),
                pressure=data["main"]["pressure"],
            )
            
            logger.debug(f"Parsed weather data: {weather_data}")
            return weather_data
            
        except KeyError as e:
            logger.error(f"Failed to parse API response: missing key {e}")
            raise WeatherAPIError(
                f"Unable to parse weather data: unexpected API response format"
            )
        except Exception as e:
            logger.error(f"Unexpected error parsing response: {e}")
            raise WeatherAPIError(f"Unable to parse weather data: {e}")


_weather_service: Optional[WeatherService] = None

def get_weather_service() -> WeatherService:
    """
    Get or create WeatherService instance (singleton pattern)
    """
    global _weather_service
    
    if _weather_service is None:
        _weather_service = WeatherService()
        logger.info("Created new WeatherService instance")
    
    return _weather_service