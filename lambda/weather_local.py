import json
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

GEOCODING_API = "https://geocoding-api.open-meteo.com/v1/search"
CURRENT_WEATHER_API = "https://api.open-meteo.com/v1/forecast"
HISTORICAL_WEATHER_API = "https://archive-api.open-meteo.com/v1/archive"


def call_api(url: str, params: dict) -> dict:
    query = urllib.parse.urlencode(params)
    request = urllib.request.Request(f"{url}?{query}")

    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


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
    """
    AgentCore Gateway Lambda target.

    The Gateway will invoke this Lambda with a tool name
    and the corresponding arguments.
    """

    tool_name = event.get("toolName")
    arguments = event.get("arguments", {})

    try:
        if tool_name == "get_current_weather":
            result = get_current_weather(
                arguments["city"]
            )

        elif tool_name == "get_historical_weather":
            result = get_historical_weather(
                arguments["city"],
                arguments["start_date"],
                arguments["end_date"],
            )

        else:
            raise ValueError(f"Unknown tool: {tool_name}")

        return {
            "statusCode": 200,
            "body": result,
        }

    except Exception as exc:
        return {
            "statusCode": 400,
            "body": {
                "error": str(exc)
            },
        }

def main():
    print(get_current_weather("Melbourne"))
    print("====================")
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=2)
    print(get_historical_weather(
        "Melbourne",
        start_date.isoformat(),
        end_date.isoformat()
    ))
if __name__ == "__main__":
    main()
