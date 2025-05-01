"""
MCP Server for EcoSync
This module implements a Model Context Protocol server for the EcoSync prototype.
"""
from mcp.server.fastmcp import FastMCP
import requests
import os
import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from agents.run import RunConfig
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

# Create server
mcp = FastMCP("EcoSync MCP Server")

set_tracing_disabled(True)

# Import or define the Agent instances
# Note: Update these import paths if the module structure is different
try:
    from ecosync_logistics_agent.custom_tools.route_planner_agent import agent as route_planner_agent_instance
    from ecosync_logistics_agent.custom_tools.live_search_agent import agent as live_search_agent_instance
    custom_agents_available = True
except ImportError:
    # If the modules are not installed, we'll set up placeholders
    route_planner_agent_instance = None
    live_search_agent_instance = None
    custom_agents_available = False
    print("Warning: Could not import agent instances. Using placeholders instead.")

load_dotenv(find_dotenv())

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = None
model = None
routing_agent = None

if GEMINI_API_KEY:
    client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client
    )

    config = RunConfig(
        model=model,
        model_provider=client,
        tracing_disabled=True
    )

# Original weather tool
@mcp.tool()
def get_weather(city: str) -> str:
    """
    Get the current weather for a specific city.
    
    Args:
        city: The name of the city to get weather for
        
    Returns:
        A string containing the weather information
    """
    endpoint = "https://wttr.in"
    response = requests.get(f"{endpoint}/{city}?format=3")
    return response.text

# Strikes information tool
@mcp.tool()
def get_strike_info(location: str, date: str = None) -> str:
    """
    Get information about strikes or protests in a specific location.
    
    Args:
        location: The location to check for strikes
        date: Optional date to check for strikes (defaults to today)
        
    Returns:
        A string containing information about any known strikes
    """
    if not date:
        date = datetime.today().strftime("%Y-%m-%d")
    
    # This is a mock response - in a real implementation, this would query an API
    return f"No confirmed strikes reported in {location} on {date}. Always check local news for last-minute updates."

# Route planning tool
@mcp.tool()
def get_route_info(origin: str, destination: str) -> str:
    """
    Get basic routing information between two locations.
    
    Args:
        origin: Starting location
        destination: Ending location
        
    Returns:
        A string with basic routing information
    """
    # This is a mock response - in a real implementation, this would query a mapping API
    return f"Route from {origin} to {destination} is available. Estimated distance: approximately 100-500 km depending on exact locations. For precise directions, please use a mapping service like Google Maps."

# Add routing tools to MCP if custom tools are available
@mcp.tool()
async def get_optimal_route(source: str, destination: str) -> str:
    """
    Get the optimal route from source to destination with real-time information.
    
    Args:
        source: Starting location
        destination: Destination location
        
    Returns:
        A string containing route information, Google Maps link, and real-time alerts
    """
    if not custom_agents_available or not GEMINI_API_KEY:
        return get_route_info(source, destination) + "\n\nNote: Advanced routing features are not available."
    
    try:
        from app.agents.routing_agent import run_routing_agent
        
        query = f"I want to go from {source} to {destination}"
        result = await run_routing_agent(query)
        return result
    except Exception as e:
        return f"Error getting optimal route: {str(e)}"

# Run the server
if __name__ == "__main__":
    mcp.run()