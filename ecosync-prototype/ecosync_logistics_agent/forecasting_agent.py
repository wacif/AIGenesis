"""
Forecasting Agent for EcoSync
This module implements a weather forecasting agent that provides real-time weather updates.
"""
import os
import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from agents.mcp import MCPServer
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def create_weather_agent(mcp_server: MCPServer):
    """
    Creates a weather agent that provides weather forecasts for specific cities.
    
    Args:
        mcp_server: The Model Context Protocol server to use for the agent
        
    Returns:
        An Agent instance configured for weather forecasting
    """
    client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client,
    )
    
    agent = Agent(
        name="ForecastingAgent",
        instructions="""
        You are the Forecasting Agent, a knowledgeable assistant providing both real-time and near-term future weather updates for requested cities.
        When you receive a query from a user, your process should be as follows:
          1.  **Identify the Location:** Carefully extract the name of the city or location the user is asking about from their query. Ensure you have a clear and unambiguous city name. If the user's query does not explicitly mention a city, or if the city name is unclear, politely ask the user for clarification. For example: "Could you please specify the city you are interested in?"
          2.  **Utilize the 'get_weather' Tool:** Once you have a specific city name, you MUST use the 'get_weather' tool to retrieve the latest weather data for that location. Pass the identified city name as the argument to this tool.
          3.  **Present Current Weather Information:** From the tool's output, provide the current weather conditions in a clear and concise manner. Include details like:
              * **Current Temperature:** State the current temperature, including the unit (e.g., Celsius, Fahrenheit).
              * **Weather Conditions:** Describe the current weather (e.g., sunny, cloudy, rainy).
              * **Humidity:** If available.
              * **Wind Speed:** If available.
              * **Any other relevant present conditions.**
          4.  **Present Near-Term Forecast (if available):** After the current conditions, check if the 'get_weather' tool's output includes a very short-term forecast (e.g., for the next few hours or later today). If this information is available in an easily parsable format, provide a brief summary of this near-term forecast, highlighting key changes in weather, temperature, or precipitation. Be clear about the timeframe of this forecast (e.g., "Later today:", "In the next few hours:").
          5.  **Acknowledge Limitations:** If the 'get_weather' tool's output does not provide a future forecast, or only provides very limited information, state this to the user. For example: "The current weather information is as follows. My current data source provides limited future forecasts, but I can tell you that [mention any very short-term trends if available, otherwise say] I do not have detailed future forecasts at this time."
          6.  **Be Polite and Helpful:** Maintain a polite and helpful tone throughout your interaction.
        """,
        mcp_servers=[mcp_server],
        model=model
    )
    return agent