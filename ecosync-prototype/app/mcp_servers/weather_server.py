"""
Weather MCP Server for EcoSync
This module implements a Model Context Protocol server for weather-related tools.
"""
from mcp.server.fastmcp import FastMCP
import requests
from datetime import datetime

# Create server
mcp = FastMCP("EcoSync Weather Server")

@mcp.tool()
def get_weather(city: str) -> str:
    """
    Get the current weather for a specific city.
    
    Args:
        city: The name of the city to get weather for
        
    Returns:
        A string containing the weather information
    """
    try:
        endpoint = "https://wttr.in"
        response = requests.get(f"{endpoint}/{city}?format=3")
        
        if response.status_code == 200:
            return response.text
        else:
            return f"Unable to retrieve weather data for {city}. Status code: {response.status_code}"
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"

@mcp.tool()
def get_extended_forecast(city: str, days: int = 3) -> str:
    """
    Get an extended weather forecast for a specific city.
    
    Args:
        city: The name of the city to get a forecast for
        days: Number of days to forecast (1-3, default 3)
        
    Returns:
        A string containing the extended forecast
    """
    # Validate days parameter
    if days < 1 or days > 3:
        days = 3
    
    try:
        # Format the city name for the URL
        formatted_city = city.replace(" ", "+")
        
        # Mock response - in a real implementation this would call a weather API
        current_date = datetime.now()
        forecast = f"Extended {days}-day forecast for {city}:\n\n"
        
        for i in range(days):
            forecast_date = current_date.replace(day=current_date.day + i)
            date_str = forecast_date.strftime("%Y-%m-%d")
            
            # Generate mock weather condition based on the day
            if i == 0:
                condition = "Partly cloudy"
                temp = "24°C (75°F)"
                precip = "10% chance of rain"
            elif i == 1:
                condition = "Sunny"
                temp = "26°C (79°F)"
                precip = "5% chance of rain"
            else:
                condition = "Light showers"
                temp = "22°C (72°F)"
                precip = "40% chance of rain"
            
            forecast += f"{date_str}: {condition}, {temp}, {precip}\n"
        
        return forecast
    except Exception as e:
        return f"Error generating extended forecast: {str(e)}"

# Run the server
if __name__ == "__main__":
    mcp.run()