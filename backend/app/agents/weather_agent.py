from typing import TypedDict
from typing import Optional
from datetime import datetime,date
from langgraph.graph import StateGraph,END,START

from app.services.weather_service import get_weather_service,WeatherAPIError
from app.utils.logger import get_logger
from app.schemas.weather import WeatherData,FishingRecommendation


logger = get_logger(__name__)

class WeatherAgentState(TypedDict):
    """
    State for weather checking workflow
    """
    
    location: str
    check_date: date
    weather_data: Optional[WeatherData]
    risk_factors: Optional[list[str]]
    
    safe_to_fish: Optional[bool]
    risk_level: Optional[str]
    recommendation: Optional[str]
    best_fishing_hours: Optional[str]
    precautions: Optional[list[str]]

    error: Optional[str]

async def fetch_weather_node(state: WeatherAgentState) -> WeatherAgentState:
    """
    Node 1: Fetch weather data from OpenWeather API
    """
    logger.info(f"Node: Fetch Weather - Location: {state['location']}")
    
    try:
        service = get_weather_service()
        weather = await service.get_weather(state['location'])
        state['weather_data'] = weather
        state['error'] = None
        
        logger.info(
            f"Weather fetched successfully: "
            f"{weather.temperature}°C, {weather.wind_speed} m/s"
        )
        
    except WeatherAPIError as e:
        logger.error(f"Weather API error: {e}")
        state['error'] = str(e)
        state['weather_data'] = None
    except Exception as e:
        logger.error(f"Unexpected error in fetch_weather_node: {e}", exc_info=True)
        state['error'] = "An unexpected error occurred while fetching weather"
        state['weather_data'] = None
    
    return state


def analyze_risk_node(state: WeatherAgentState) -> WeatherAgentState:
    """
    Node 2: Analyze weather conditions for fishing safety
    """
    logger.info("Node: Analyze Risk")
    if state.get('error') or not state.get('weather_data'):
        logger.warning("Skipping risk analysis - no weather data")
        state['risk_factors'] = []
        state['risk_level'] = "unknown"
        return state
    
    weather = state['weather_data']
    risk_factors = []
    
    if weather.wind_speed > 10:
        risk_factors.append("high_wind")
        logger.info(f"Risk: High wind speed ({weather.wind_speed} m/s)")
    elif weather.wind_speed > 5:
        risk_factors.append("moderate_wind")
        logger.info(f"Risk: Moderate wind speed ({weather.wind_speed} m/s)")
    
    if weather.visibility and weather.visibility < 1000:
        risk_factors.append("poor_visibility")
        logger.info(f"Risk: Poor visibility ({weather.visibility}m)")
    
    weather_condition_lower = weather.weather_condition.lower()
    if any(word in weather_condition_lower for word in ['rain', 'storm', 'thunderstorm']):
        risk_factors.append("bad_weather")
        logger.info(f"Risk: Bad weather condition ({weather.weather_condition})")
    
    if weather.temperature < 15:
        risk_factors.append("cold_temperature")
        logger.info(f"Risk: Cold temperature ({weather.temperature}°C)")
    elif weather.temperature > 38:
        risk_factors.append("extreme_heat")
        logger.info(f"Risk: Extreme heat ({weather.temperature}°C)")
    
    if weather.humidity > 85:
        risk_factors.append("high_humidity")
        logger.info(f"Risk: High humidity ({weather.humidity}%)")
    
    if any(risk in risk_factors for risk in ['high_wind', 'bad_weather', 'poor_visibility']):
        risk_level = "high"
    elif len(risk_factors) >= 2:
        risk_level = "medium"
    elif len(risk_factors) == 1:
        risk_level = "low"
    else:
        risk_level = "low"
    state['risk_factors'] = risk_factors
    state['risk_level'] = risk_level
    
    logger.info(f"Risk analysis complete: {risk_level} ({len(risk_factors)} factors)")
    
    return state

def generate_recommendation_node(state: WeatherAgentState) -> WeatherAgentState:
    """
    Node 3: Generate final fishing recommendation
    """
    logger.info("Node: Generate Recommendation")
    
    # Check if we have required data
    if state.get('error'):
        state['safe_to_fish'] = False
        state['recommendation'] = (
            "Unable to provide fishing recommendation due to error: "
            f"{state['error']}"
        )
        state['best_fishing_hours'] = None
        state['precautions'] = []
        return state
    
    weather = state['weather_data']
    risk_level = state['risk_level']
    risk_factors = state['risk_factors']
    
    # GENERATE RECOMMENDATION BASED ON RISK LEVEL
    
    if risk_level == "high":
        # HIGH RISK - Do not fish
        state['safe_to_fish'] = False
        state['recommendation'] = (
            f"⚠️ NOT SAFE for fishing in {state['location']}. "
            f"High risk conditions detected. "
            f"Please postpone your trip."
        )
        state['best_fishing_hours'] = None
        state['precautions'] = [
            "Do NOT go fishing in these conditions",
            "Wait for weather to improve",
            "Check weather again in 6-12 hours",
            "Listen to local fisheries department advisories"
        ]
    
    elif risk_level == "medium":
        # MEDIUM RISK - Experienced fishermen only
        state['safe_to_fish'] = False  # Conservative approach
        state['recommendation'] = (
            f"⚠️ CAUTION advised for fishing in {state['location']}. "
            f"Moderate risk conditions. "
            f"Only experienced fishermen with proper safety equipment should proceed."
        )
        state['best_fishing_hours'] = "Early morning (5:00 AM - 8:00 AM)"
        state['precautions'] = [
            "Only if you're experienced",
            "Ensure all safety equipment onboard",
            "Stay close to shore",
            "Monitor weather updates continuously",
            "Have communication equipment ready",
            "Inform family/authorities of your trip"
        ]
    
    else:
        # LOW RISK - Safe to fish
        state['safe_to_fish'] = True
        state['recommendation'] = (
            f"✅ GOOD conditions for fishing in {state['location']}! "
            f"Temperature: {weather.temperature}°C, "
            f"Wind: {weather.wind_speed} m/s. "
            f"Enjoy your fishing trip!"
        )
        state['best_fishing_hours'] = (
            "Early morning (5:00 AM - 9:00 AM) or "
            "Late afternoon (4:00 PM - 6:00 PM)"
        )
        state['precautions'] = [
            "Carry sufficient drinking water",
            "Apply sunscreen (SPF 30+)",
            "Wear life jackets",
            "Bring first aid kit",
            "Keep emergency contacts handy"
        ]
    
    if "high_wind" in risk_factors:
        state['precautions'].append("Strong winds - avoid deep sea fishing")
    
    if "moderate_wind" in risk_factors:
        state['precautions'].append("Moderate winds - stay alert")
    
    if "poor_visibility" in risk_factors:
        state['precautions'].append("Poor visibility - use fog horn and navigation lights")
    
    if "cold_temperature" in risk_factors:
        state['precautions'].append("Cold weather - wear warm clothing")
    
    if "extreme_heat" in risk_factors:
        state['precautions'].append("Extreme heat - take frequent breaks, stay hydrated")
    
    if "high_humidity" in risk_factors:
        state['precautions'].append("High humidity - ensure good ventilation on boat")
    
    logger.info(
        f"Recommendation generated: "
        f"Safe={state['safe_to_fish']}, "
        f"Risk={risk_level}"
    )
    
    return state


# BUILD GRAPH
def create_weather_agent() -> StateGraph:
    """
    Create and compile the weather agent graph
    
    GRAPH STRUCTURE:
        START
          ↓
        fetch_weather
          ↓
        analyze_risk
          ↓
        generate_recommendation
          ↓
        END
    RETURNS:
        Compiled StateGraph ready to execute
    """
    logger.info("Building weather agent graph")

    workflow = StateGraph(WeatherAgentState)
    
    # Add nodes
    workflow.add_node("fetch_weather", fetch_weather_node)
    workflow.add_node("analyze_risk", analyze_risk_node)
    workflow.add_node("generate_recommendation", generate_recommendation_node)
    
    # Define flow
    workflow.set_entry_point("fetch_weather")
    workflow.add_edge("fetch_weather", "analyze_risk")
    workflow.add_edge("analyze_risk", "generate_recommendation")
    workflow.add_edge("generate_recommendation", END)
    
    logger.info("Weather agent graph built successfully")
    
    return workflow.compile()

async def check_weather_for_fishing(location: str,check_date: date) -> dict:
    logger.info(f"Running weather check for {location} on {check_date}")
    graph = create_weather_agent()
    initial_state = WeatherAgentState(
        location=location,
        check_date=check_date,
        weather_data=None,
        risk_factors=None,
        safe_to_fish=None,
        risk_level=None,
        recommendation=None,
        best_fishing_hours=None,
        precautions=None,
    )

    final_state = await graph.ainvoke(initial_state)
    
    logger.info("Weather check complete")
    
    return final_state