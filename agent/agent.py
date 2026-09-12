import asyncio
import os

from strands import Agent
from strands.tools.mcp import MCPClient
from mcp.client.streamable_http import streamablehttp_client

GATEWAY_ENDPOINT ="<YOUR_GATEWAY_ENDPOINT>"

def create_gateway_client():
    return MCPClient(
        lambda: streamablehttp_client(
            GATEWAY_ENDPOINT
        )
    )


async def main():
    gateway_client = create_gateway_client()
    with gateway_client:
        # Discover tools from AgentCore Gateway
        tools = gateway_client.list_tools_sync()

        print("Discovered tools:", [tool.tool_name for tool in tools])

        # Create Strands agent
        agent = Agent(
            system_prompt="""
            You are a weather assistant. You have access to weather tools through Amazon Bedrock AgentCore Gateway.

            Use get_current_weather when the user asks about current weather.

            Use get_historical_weather when the user asks about historical weather.

            Ask the user for missing information when required.
            """,
            tools=tools,
        )

        # Continuous conversation
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                break

            response = agent(user_input)

if __name__ == "__main__":
    asyncio.run(main())