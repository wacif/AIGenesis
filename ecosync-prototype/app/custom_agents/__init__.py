"""
Custom agents module for EcoSync Prototype.

This package contains specialized agents for handling different types of queries:
- Triage Agent: Determines which specialized agent should handle a query
- Weather Agent: Handles weather-related queries and forecasts
- Routing Agent: Handles route optimization and logistics queries
- Strike Agent: Handles information about strikes and protests affecting logistics
"""

# Import all agent functions for easy access
from app.custom_agents.weather_agent import run_weather_agent
from app.custom_agents.strike_agent import run_strike_agent  
from app.custom_agents.triage_agent import run_triage_agent
from app.custom_agents.routing_agent import run_routing_agent