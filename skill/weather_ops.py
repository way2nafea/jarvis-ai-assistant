import os
import json
from typing import List, Dict, Any, Callable
from core.skill import Skill


class WeatherSkill(Skill):
    """Skill for fetching weather information using OpenWeatherMap API."""

    def __init__(self):
        self.api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
        self.default_city = os.environ.get("DEFAULT_CITY", "Mumbai")

    @property
    def name(self) -> str:
        return "weather_skill"

    # ================== TOOL DEFINITIONS ==================
    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get current weather information for a city or pincode",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "City name or pincode"
                            },
                            "pincode": {
                                "type": "string",
                                "description": "Optional pincode (takes precedence)"
                            }
                        },
                        "required": ["city"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_current_location_weather",
                    "description": "Get weather for the default configured location",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "get_weather": self.get_weather,
            "get_current_location_weather": self.get_current_location_weather
        }

    # ================== WEATHER LOGIC ==================
    def get_weather(self, city: str, pincode: str = None) -> str:
        if not self.api_key:
            return "Weather service is not configured. Please add the OpenWeatherMap API key."

        try:
            import requests

            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "appid": self.api_key,
                "units": "metric"
            }

            if pincode:
                params["zip"] = f"{pincode},in"
            elif city.strip().isdigit():
                params["zip"] = f"{city},in"
            else:
                params["q"] = city

            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                return f"I couldn't find the weather for {city}. Please try another location."

            data = response.json()

            city_name = data["name"]
            country = data["sys"]["country"]
            temp = data["main"]["temp"]
            feels = data["main"]["feels_like"]
            condition = data["weather"][0]["description"].title()
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]

            # 🗣️ HUMAN-FRIENDLY RESPONSE
            return (
                f"The current weather in {city_name}, {country} is {condition}. "
                f"The temperature is {temp:.1f}°C, feels like {feels:.1f}°C, "
                f"with humidity at {humidity}% and wind speed of {wind} meters per second."
            )

        except ImportError:
            return "The weather service is unavailable because the requests library is missing."
        except Exception:
            return "I encountered an error while fetching the weather."

    def get_current_location_weather(self) -> str:
        return self.get_weather(self.default_city)