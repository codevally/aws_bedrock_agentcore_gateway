# Weather Agent — Architecture

## End-to-End Flow

The following diagram shows the complete request flow from the user
through the Strands Agent, Amazon Bedrock AgentCore Gateway, AWS Lambda,
and Open-Meteo.

## Real API Integration

The project uses a live weather API instead of mocked data to validate the complete end-to-end integration.
This allows us to test realistic API communication, request/response handling, external service dependencies, network connectivity, latency, and failure scenarios across the Strands Agent → AgentCore Gateway → Lambda → External API flow.
Using real data ensures the implementation reflects production-style agent tool integration rather than only validating application logic with predetermined responses.

![Weather Agent E2E Architecture](images/e2e-architecture.png)

### Request Flow

1. **User** submits a natural-language weather request.
2. **Strands Agent** interprets the request and selects the appropriate tool.
3. **AgentCore Gateway** exposes the weather tools through MCP.
4. **AWS Lambda** receives the tool invocation.
5. Lambda calls **Open-Meteo** over HTTPS.
6. Open-Meteo returns weather data as JSON.
7. Lambda returns the result through the Gateway.
8. Strands interprets the result and generates the final response.
9. The response is returned to the user.

### Available Tools

| Tool | Purpose |
|---|---|
| `get_current_weather` | Get current weather for a city |
| `get_historical_weather` | Get historical weather for a city and date range |

### E2E Architecture

```text
User
  ↓
Strands Agent
  ↓ MCP
Amazon Bedrock AgentCore Gateway
  ↓
AWS Lambda
  ↓ HTTPS
Open-Meteo
  ↓ JSON
AWS Lambda
  ↓
AgentCore Gateway
  ↓
Strands Agent
  ↓
User
```

## Example Agent Interaction

The following conversation demonstrates an end-to-end interaction with the Weather Agent.

### Tool Discovery
User
> What tools do you have available?
> 
Agent
> I have two weather tools available:
>
> 1. **Get Current Weather** - Retrieves the current weather conditions for a specified city. Just tell me the city name and I'll fetch the latest weather for you!
>
> 2. **Get Historical Weather** - Retrieves historical weather data for a specified city over a date range. For this, I'll need:
    - The **city name**
    - A **start date** (in YYYY-MM-DD format)
    - An **end date** (in YYYY-MM-DD format)
>
> Feel free to ask me about the weather anywhere in the world! 🌤️ 

### Current Weather
User
> What is the current weather in Melbourne?
>
Agent
>Tool #1: weather-tools___get_current_weather
>Here are the current weather conditions in **Melbourne**:
>
>- 🌡️ **Temperature:** 14.5°C (feels like 13.7°C)
>- 💧 **Humidity:** 73%
>- 🌤️ **Conditions:** Mainly clear
>- 💨 **Wind Speed:** 4.7 km/h
>
>It's a mild and mostly clear day in Melbourne. You might want a light jacket given the cool temperature!

### Historical Weather
User
> What was the weather in Melbourne 26th December last year?
>
Agent
>Let me fetch the historical weather data for Melbourne on 26th December last year!
>Tool #1: weather-tools___get_historical_weather
>Here's the weather in **Melbourne** on **26th December 2025**:
>
>- 🌡️ **Max Temperature:** 38.6°C
>- 🌡️ **Min Temperature:** 19.3°C
>- 🌧️ **Precipitation:** 1.9 mm
>- ⛅ **Weather Condition:** Light rain (Weather Code 61)
>
>It was quite a hot Boxing Day in Melbourne, with temperatures soaring up to **38.6°C**, though there was also a touch of light rain. A classic Melbourne summer day with a mix of heat and a brief shower! 🌞🌦️