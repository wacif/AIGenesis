"""
Custom tools module for EcoSync Prototype.

This package contains specialized tools for various functionalities:
- route_tools: Tools for route optimization and disruption checking
- weather_tools: Tools for weather data retrieval and demand prediction
"""

# Import tool functions for easy access
from app.custom_tools.route_tools import optimize_route, check_for_disruptions
from app.custom_tools.weather_tools import get_current_weather, predict_demand_from_weather