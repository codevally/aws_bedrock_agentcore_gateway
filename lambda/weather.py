import json
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

GEOCODING_API = "https://geocoding-api.open-meteo.com/v1/search"
CURRENT_WEATHER_API = "https://api.open-meteo.com/v1/forecast"
HISTORICAL_WEATHER_API = "https://archive-api.open-meteo.com/v1/archive"

TOOL_HANDLERS = {
    "get_current_weather": lambda event: get_current_weather(
        event["city"]
    ),

    "get_historical_weather": lambda event: get_historical_weather(
        event["city"],
        event["start_date"],
        event["end_date"],
    ),
}

def call_api(url: str, params: dict) -> dict:
    query = urllib.parse.urlencode(params)
    full_url = f"{url}?{query}"

    print("Calling:", full_url)

    request = urllib.request.Request(
        full_url,
        headers={"User-Agent": "weather-agentcore/1.0"}
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            body = response.read().decode("utf-8")
            print("Response:", body)
            return json.loads(body)

    except Exception as e:
        print("Open-Meteo error:", repr(e))
        raise


def get_coordinates(city: str) -> dict:
    response = call_api(
        GEOCODING_API,
        {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        },
    )

    results = response.get("results", [])

    if not results:
        raise ValueError(f"Could not find location: {city}")

    location = results[0]

    return {
        "name": location["name"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "timezone": location.get("timezone"),
    }


def get_current_weather(city: str) -> dict:
    location = get_coordinates(city)

    weather = call_api(
        CURRENT_WEATHER_API,
        {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "apparent_temperature,"
                "weather_code,"
                "wind_speed_10m"
            ),
            "timezone": "auto",
        },
    )

    return {
        "city": location["name"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "timezone": location["timezone"],
        "current": weather.get("current"),
    }


def get_historical_weather(
        city: str,
        start_date: str,
        end_date: str,
) -> dict:
    location = get_coordinates(city)

    weather = call_api(
        HISTORICAL_WEATHER_API,
        {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "start_date": start_date,
            "end_date": end_date,
            "daily": (
                "temperature_2m_max,"
                "temperature_2m_min,"
                "precipitation_sum,"
                "weather_code"
            ),
            "timezone": "auto",
        },
    )

    return {
        "city": location["name"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "timezone": location["timezone"],
        "historical": weather.get("daily"),
    }


def lambda_handler(event, context):

    tool_name = context.client_context.custom[
        "bedrockAgentCoreToolName"
    ]

    tool_name = tool_name.split("___", 1)[1]

    print(f"Tool: {tool_name}")
    print(f"Event: {json.dumps(event)}")

    handler = TOOL_HANDLERS.get(tool_name)

    if not handler:
        raise ValueError(f"Unknown tool: {tool_name}")

    result = handler(event)

    print("Result:")
    print(json.dumps(result, indent=2))

    return result
