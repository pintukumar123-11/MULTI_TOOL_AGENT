import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
import requests # Import the requests library
import os # <-- ADD THIS LINE
from dotenv import load_dotenv # <-- ADD THIS LINE

# --- Load environment variables from .env file ---
# This line should be called early in your script to load the variables.
load_dotenv() # <-- ADD THIS LINE

# --- IMPORTANT: Now loading API key from environment variables ---
# Access the API key from environment variables instead of hardcoding it.
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY") # <-- MODIFIED LINE

# Optional: Add a check to ensure the key was loaded. This helps prevent runtime errors.
if not OPENWEATHERMAP_API_KEY:
    raise ValueError("OPENWEATHERMAP_API_KEY environment variable not set. Please ensure you have a .env file in your project root with this key.")


OPENWEATHERMAP_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city using OpenWeatherMap API.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    # *** REMOVED THE IF STATEMENT CAUSING THE PROBLEM ***
    
    # Rest of your get_weather function...
    params = {
        "q": city,
        "appid": OPENWEATHERMAP_API_KEY, # <-- This variable will now hold the value from .env
        "units": "metric"
    }

    try:
        response = requests.get(OPENWEATHERMAP_BASE_URL, params=params)
        response.raise_for_status()
        weather_data = response.json()

        if weather_data.get("cod") == "404":
            return {
                "status": "error",
                "error_message": f"Weather information for '{city}' not found. Please check the city name.",
            }
        elif weather_data.get("cod") != 200:
             return {
                 "status": "error",
                 "error_message": f"OpenWeatherMap API error: {weather_data.get('message', 'Unknown error')}",
             }

        main_weather = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        feels_like = weather_data["main"]["feels_like"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]

        report = (
            f"The weather in {city} is {main_weather} with a temperature of "
            f"{temperature}°C (feels like {feels_like}°C). "
            f"Humidity is {humidity}% and wind speed is {wind_speed} m/s."
        )
        return {"status": "success", "report": report}

    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Could not connect to OpenWeatherMap API: {e}",
        }
    except KeyError as e:
        return {
            "status": "error",
            "error_message": f"Error parsing weather data for {city}: Missing expected key {e}. Response: {weather_data}",
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"An unexpected error occurred: {e}",
        }


# The rest of your code for get_current_time and root_agent is fine and remains unchanged.

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    elif city.lower() == "london": # Added another city for demonstration of time zones
        tz_identifier = "Europe/London"
    elif city.lower() == "tokyo":
        tz_identifier = "Asia/Tokyo"
    elif city.lower() == "mumbai": # Added Mumbai for timezone information
        tz_identifier = "Asia/Kolkata" 
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}. "
                "You can add more cities with their timezone identifiers."
            ),
        }

    try:
        tz = ZoneInfo(tz_identifier)
        now = datetime.datetime.now(tz)
        report = (
            f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
        )
        return {"status": "success", "report": report}
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error getting time for {city}: {e}",
        }


root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
        "You can retrieve real-time weather information for any city worldwide."
    ),
    tools=[get_weather, get_current_time],
)

# Example of how you might test this if running directly (not part of the Agent framework's execution):
if __name__ == "__main__":
    print("--- Testing Weather API ---")
    weather_report_ny = get_weather("New York")
    print(f"New York Weather: {weather_report_ny}")

    weather_report_london = get_weather("London")
    print(f"London Weather: {weather_report_london}")

    weather_report_nonexistent = get_weather("NonExistentCity123")
    print(f"Non-existent City Weather: {weather_report_nonexistent}")
    
    weather_report_mumbai = get_weather("Mumbai") # Test Mumbai weather
    print(f"Mumbai Weather: {weather_report_mumbai}")

    print("\n--- Testing Time Function ---")
    time_report_ny = get_current_time("New York")
    print(f"New York Time: {time_report_ny}")

    time_report_london = get_current_time("London")
    print(f"London Time: {time_report_london}")

    time_report_tokyo = get_current_time("Tokyo")
    print(f"Tokyo Time: {time_report_tokyo}")

    time_report_mumbai = get_current_time("Mumbai") # Test Mumbai time
    print(f"Mumbai Time: {time_report_mumbai}")