from pydantic import BaseModel,Field,field_validator
from typing import Optional
from datetime import  date,datetime

class WeatherCheckRequest(BaseModel):
    """
    VALIDATION:
    - location: Required, 2-100 characters, trimmed
    - check_date: Required, valid date, not too far in past/future
    """
    location: str = Field(
                    min_length=2, 
                    max_length=100,
                    description="Location name (e.g., Chennai)",
                    examples=["Chennai", "Tuticorin", "Rameswaram"],
                    )
    check_date: date = Field(
                        description="Date to check weather for (e.g., 2024-01-01)",
                        examples=["2026-02-15"]
                        )

    #custom validators
    @field_validator("location")
    @classmethod
    def validate_location(cls, v:str)->str:
        v=v.strip()
        if not v:
            raise ValueError("location must not be empty")
        special_chars = ['<', '>', ';', '--', '/*', '*/', 'DROP', 'DELETE']
        if any(char in v.upper() for char in special_chars):
            raise ValueError("location contains invalid characters")
        return v

    @field_validator("check_date")
    @classmethod
    def validate_date(cls, v:date)->date:
        """
        validate date 
        RULES:
        - Not more than 30 days in past
        - Not more than 7 days in future (free API limit)
        """
        today = date.today()
        days_ago = (today - v).days
        if days_ago > 30:
            raise ValueError(
                f"Date too far in past (max 30 days). "
                f"Requested: {v}, Today: {today}"
            )
        days_ahead = (v - today).days
        if days_ahead > 7:
            raise ValueError(
                f"Date too far in future (max 7 days for free API). "
                f"Requested: {v}, Today: {today}"
            )
        return v
    class Config:
        """Pydantic configuration"""
        json_schema_extra = {
            "example": {
                "location": "Chennai",
                "check_date": "2026-02-22",
            }
        }

# RESPONSE SCHEMAS (What API returns to user)
class WeatherData(BaseModel):
    """
    Detailed weather information
    This is the CORE weather data from OpenWeather API
    """
    temperature: float = Field(
                            description="Temperature in Celsius",
                            examples=[25.0]
                            )

    feels_like: float  = Field(
                            description="Temperature in Celsius",
                            examples=[25.0]
                            )
    
    humidity: int = Field(
                            ge=0,
                            le=100,
                            description="Humidity percentage",
                            examples=[75]
                            )
                            
    wind_speed: float = Field(
                            ge=0,
                            le=100,
                            description="Wind speed in m/s",
                            examples=[3.5]
                            )
                            
    wind_direction: int = Field(
                            ge=0,
                            le=360,
                            description="Wind direction in degrees",
                            examples=[180]
                            )
    weather_condition: str = Field(
                            description="Weather condition",
                            examples=["Clear sky", "Light rain", "Partly cloudy"]
                            )
    cloud_coverage: int = Field(
                            ge=0,
                            le=100,
                            description="Cloud coverage percentage",
                            examples=[20]
                            )
    
    visibility: Optional[int] = Field(
                            None,
                            description="Visibility in meters",
                            examples=[10000]
                            )
    
    pressure: int = Field(
                            ...,
                            description="Atmospheric pressure in hPa",
                            examples=[1013]
                            )

class FishingRecommendation(BaseModel):
    """
    Fishing recommendations based on weather conditions
    """
    safe_to_fish: bool = Field(
                            description="Safe to fish",
                            examples=[True]
                            )
    risk_level: str = Field(
                            description="Risk level",
                             examples=["low", "medium", "high"]
                            )
    recommendation: str = Field(
                            ...,
                            description="Human-readable recommendation",
                            examples=["Good conditions for fishing. Winds are calm."]
                            )
    
    risk_factors: list[str] = Field(
                            default_factory=list,
                            description="List of risk factors identified",
                            examples=[["high_wind", "poor_visibility"]]
                            )
    
    best_fishing_hours: Optional[str] = Field(
                            None,
                            description="Recommended time window for fishing",
                            examples=["Early morning (5 AM - 9 AM) and evening (4 PM - 6 PM)"]
                            )
    precautions: list[str] = Field(
                            default_factory=list,
                            description="Safety precautions to take",
                            examples=[["Carry extra fuel", "Monitor weather updates"]]
                            )
class WeatherCheckResponse(BaseModel):
    """
    Complete response for weather check endpoint
    
    COMBINES:
    - Request info (what was asked)
    - Weather data (from OpenWeather)
    - AI recommendation (from LangGraph)
    """
    # Request echo (confirmation)
    location: str = Field(
        ...,
        description="Location that was checked"
    )
    
    check_date: date = Field(
        ...,
        description="Date that was checked"
    )
    
    # Timestamp
    checked_at: datetime = Field(
        default_factory=datetime.now,
        description="When this check was performed (UTC)"
    )
    
    # Weather data
    weather: WeatherData = Field(
        ...,
        description="Detailed weather information"
    )
    
    # AI recommendation
    fishing_advice: FishingRecommendation = Field(
        ...,
        description="AI-powered fishing recommendation"
    )
    
    class Config:
        """Pydantic configuration"""
        json_schema_extra = {
            "example": {
                "location": "Chennai",
                "check_date": "2026-02-22",
                "checked_at": "2026-02-21T19:45:30.123456",
                "weather": {
                    "temperature": 28.5,
                    "feels_like": 30.2,
                    "humidity": 75,
                    "wind_speed": 3.5,
                    "wind_direction": 180,
                    "weather_condition": "Clear sky",
                    "cloud_coverage": 20,
                    "visibility": 10000,
                    "pressure": 1013
                },
                "fishing_advice": {
                    "safe_to_fish": True,
                    "risk_level": "low",
                    "recommendation": "Excellent conditions for fishing! Clear skies and calm winds.",
                    "risk_factors": [],
                    "best_fishing_hours": "Early morning (5 AM - 9 AM)",
                    "precautions": ["Carry drinking water", "Apply sunscreen"]
                }
            }
        }

# ERROR RESPONSE SCHEMA

class ErrorResponse(BaseModel):
    """
    Standard error response format
    
    WHY:
    - Consistent error format across all endpoints
    - Easy for frontend to handle
    - Helpful for debugging
    """
    error: str = Field(
        ...,
        description="Error type",
        examples=["validation_error", "api_error", "not_found"]
    )
    
    message: str = Field(
        ...,
        description="Human-readable error message",
        examples=["Location cannot be empty"]
    )
    
    details: Optional[dict] = Field(
        None,
        description="Additional error details",
        examples=[{"field": "location", "issue": "empty string"}]
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When error occurred"
    )