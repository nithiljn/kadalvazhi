from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from app.schemas.weather import (
    WeatherCheckRequest,
    WeatherCheckResponse,
    WeatherData,
    FishingRecommendation,
    ErrorResponse
)
from app.agents.weather_agent import check_weather_for_fishing
from app.services.weather_service import LocationNotFoundError, WeatherAPIError
from app.utils.logger import get_logger

router = APIRouter()

logger = get_logger(__name__)

@router.post(
    "/check",
    response_model=WeatherCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Check weather for fishing",
    responses={
        200: {
            "description": "Weather check successful",
            "model": WeatherCheckResponse
        },
        400: {
            "description": "Invalid request (bad location/date)",
            "model": ErrorResponse
        },
        404: {
            "description": "Location not found",
            "model": ErrorResponse
        },
        503: {
            "description": "Weather service unavailable",
            "model": ErrorResponse
        }
    }
)
async def check_weather(request: WeatherCheckRequest) -> WeatherCheckResponse:
    logger.info(
        f"Weather check request: location={request.location}, "
        f"date={request.check_date}"
    )
    
    try:
        result = await check_weather_for_fishing(
            location=request.location,
            check_date=request.check_date
        )
        if result.get('error'):
            error_msg = result['error']
            logger.error(f"Agent returned error: {error_msg}")
            
            if "not found" in error_msg.lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=error_msg
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=error_msg
                )
        
        if not result.get('weather_data'):
            logger.error("Agent returned no weather data")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to fetch weather data. Please try again."
            )
        
        fishing_advice = FishingRecommendation(
            safe_to_fish=result.get('safe_to_fish', False),
            risk_level=result.get('risk_level', 'unknown'),
            recommendation=result.get('recommendation', 'No recommendation available'),
            risk_factors=result.get('risk_factors', []),
            best_fishing_hours=result.get('best_fishing_hours'),
            precautions=result.get('precautions', [])
        )
        
        response = WeatherCheckResponse(
            location=result['location'],
            check_date=result['check_date'],
            checked_at=datetime.now(),
            weather=result['weather_data'],
            fishing_advice=fishing_advice
        )
        
        logger.info(
            f"Weather check successful: location={request.location}, "
            f"safe={fishing_advice.safe_to_fish}, risk={fishing_advice.risk_level}"
        )
        
        return response
        
    except LocationNotFoundError as e:
        logger.warning(f"Location not found: {request.location}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    
    except WeatherAPIError as e:
        logger.error(f"Weather API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(
            f"Unexpected error in check_weather: {e}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )


@router.get(
    "/health",
    summary="Health check for weather service",
    description="Check if weather service is operational"
)
async def health_check():
    logger.debug("Weather service health check")
    
    # TODO: Add checks for:
    # - OpenWeather API availability
    # - Database connection (future)
    # - Agent graph compilation
    
    return {
        "status": "healthy",
        "service": "weather",
        "timestamp": datetime.now().isoformat()
    }