"""
MCP Server for EcoSync
This module implements a Model Context Protocol server for the EcoSync prototype.
"""
from mcp.server.fastmcp import FastMCP
import requests

# Create server
mcp = FastMCP("Weather Server")

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

# Run the server
if __name__ == "__main__":
    mcp.run()