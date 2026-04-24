from google.adk.agents import Agent # ============================================================= TOOLS — The Agent's Superpowers ============================================================= The LLM reads the function name, docstring, and type hints
# to understand WHEN and HOW to call each tool automatically.
# This is "Function Calling" — the core of Agentic AI.

import requests

def get_weather(city: str) -> dict:
    """
    Retrieves the current real-time weather for any city in the world
    using the free wttr.in API.

    Args:
        city (str): The name of any city in the world.
                    Examples: "Hyderabad", "Shanghai", "Paris", "Sydney"

    Returns:
        dict: Live weather data including temperature, condition, and humidity.
    """
    try:
        response = requests.get(
            f"https://wttr.in/{city}?format=j1",
            timeout=5
        )
        data = response.json()
        current = data["current_condition"][0]

        return {
            "status": "success",
            "city": city,
            "temperature": f"{current['temp_C']}°C",
            "feels_like": f"{current['FeelsLikeC']}°C",
            "condition": current["weatherDesc"][0]["value"],
            "humidity": f"{current['humidity']}%",
            "wind_speed": f"{current['windspeedKmph']} km/h"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Could not fetch weather for '{city}'. Error: {str(e)}"
        }

def get_travel_tips(city: str) -> dict:
    """
    Provides travel tips and must-visit places for a given city.

    Args:
        city (str): The name of the city to get travel tips for.

    Returns:
        dict: Travel tips, famous places, and local food recommendations.
    """
    city_lower = city.lower()
    travel_db = {
        "hyderabad": {
            "status": "success",
            "city": "Hyderabad",
            "famous_places": ["Charminar", "Golconda Fort", "Ramoji Film City", "Hussain Sagar Lake"],
            "local_food": ["Hyderabadi Biryani", "Haleem", "Irani Chai with Osmania Biscuits"],
            "tip": "Best time to visit is October to March. Use Ola/Uber for getting around."
        },
        "london": {
            "status": "success",
            "city": "London",
            "famous_places": ["Big Ben", "Tower of London", "British Museum", "Hyde Park"],
            "local_food": ["Fish and Chips", "Sunday Roast", "English Breakfast"],
            "tip": "Get an Oyster Card for public transport. Many museums are free!"
        },
        "tokyo": {
            "status": "success",
            "city": "Tokyo",
            "famous_places": ["Shibuya Crossing", "Senso-ji Temple", "Tokyo Tower", "Meiji Shrine"],
            "local_food": ["Ramen", "Sushi", "Tempura"],
            "tip": "Get a Suica card for trains. Convenience stores (konbini) have great affordable food."
        }
    }

    if city_lower in travel_db:
        return travel_db[city_lower]
    else:
        return {
            "status": "error",
            "error_message": f"Travel tips not available for '{city}'. Try: Hyderabad, London, or Tokyo."
        }
def convert_temperature(value: float, from_unit: str, to_unit: str) -> dict:
    """
    Converts a temperature value between Celsius and Fahrenheit.

    Args:
        value (float): The temperature value to convert.
        from_unit (str): The source unit — either 'celsius' or 'fahrenheit'.
        to_unit (str): The target unit — either 'celsius' or 'fahrenheit'.

    Returns:
        dict: The original and converted temperature values.
    """
    if from_unit.lower() == "celsius" and to_unit.lower() == "fahrenheit":
        result = (value * 9/5) + 32
    elif from_unit.lower() == "fahrenheit" and to_unit.lower() == "celsius":
        result = (value - 32) * 5/9
    else:
        return {"error": "Invalid units. Use 'celsius' or 'fahrenheit'."}

    return {
        "original": f"{value}°{from_unit[0].upper()}",
        "converted": f"{round(result, 1)}°{to_unit[0].upper()}"
    }

# =============================================================
# THE AGENT — Combining Brain + Tools
# =============================================================

root_agent = Agent(
    name="weather_agent",
    model="gemini-2.5-flash",
    description="A helpful travel and weather assistant powered by Google ADK.",
    instruction="""You are a friendly and helpful Travel & Weather Assistant. 
    
Your capabilities:
1. You can check the current weather for cities using the 'get_weather' tool.
2. You can provide travel tips and recommendations using the 'get_travel_tips' tool.

Rules:
- Always use the appropriate tool when the user asks about weather or travel.
- If the user asks about a city you don't have data for, politely let them know which cities are available.
- Be conversational, warm, and encouraging.
- When giving weather info, also suggest what to wear or carry.
- If the user asks about both weather AND travel for a city, use BOTH tools.
""",
    tools=[get_weather, get_travel_tips, convert_temperature],
)
