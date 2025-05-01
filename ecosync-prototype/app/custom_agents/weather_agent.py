"""
Weather Agent Implementation for EcoSync Prototype

This module provides a specialized agent for handling weather-related queries,
forecasts, and demand predictions based on weather conditions.
"""

from agents import Agent
import os
import json
from app.custom_agents.base_agent import BaseAgent, get_client_and_model, run_agent_with_query
from app.custom_tools.weather_tools import get_current_weather, predict_demand_from_weather

class WeatherAgent(BaseAgent):
    """
    Weather specialized agent that handles weather queries, forecasts, and
    demand predictions based on weather conditions.
    """
    
    def __init__(self):
        """Initialize the Weather Agent."""
        super().__init__("Weather Agent")
    
    async def process_query(self, query: str) -> str:
        """
        Process a weather-related query.
        
        Args:
            query (str): The weather-related query from the user
            
        Returns:
            str: The agent's response
        """
        cleaned_query = self._clean_query(query)
        
        # Create an Weather Agent instance
        agent = create_weather_agent()
        
        # Run the agent with the query
        response = await run_agent_with_query(agent, cleaned_query)
        
        # Add to history
        self._add_to_history(cleaned_query, response)
        
        return response

def create_weather_agent():
    """
    Create and return an instance of a Weather Agent.
    
    Returns:
        Agent: An Agent instance configured for weather-related queries
    """
    instructions = """You are a Weather Expert agent for EcoSync Logistics. Your specialty is providing accurate weather information, forecasts, and helping logistics planners make weather-informed decisions.

CAPABILITIES:
- Provide current weather conditions for specific locations
- Forecast weather for the next few days
- Explain how weather conditions might affect logistics operations
- Predict demand for specific products based on weather trends
- Suggest alternative routes or scheduling based on severe weather conditions
- Help optimize delivery planning around weather events

GUIDELINES:
1. Always provide location-specific weather information when available.
2. If you don't know current weather conditions for a location, say so clearly.
3. When asked about how weather affects logistics, consider factors like road conditions, flight delays, and regional shipping disruptions.
4. For product demand predictions, consider seasonal patterns and weather correlations.
5. When severe weather is mentioned, prioritize safety considerations in your recommendations.
6. Provide helpful context about how different weather phenomena impact different modes of transportation.

LIMITATIONS:
- You should not provide exact weather predictions beyond 10 days.
- You cannot guarantee the weather forecast with 100% certainty.
- You do not have real-time disaster or emergency information unless specifically provided.

EXAMPLES:
- "What's the weather like in New York today?" → Provide current conditions for New York
- "Will it rain in London this weekend?" → Give forecast if possible, with appropriate uncertainty
- "How will the snowstorm affect deliveries to Boston?" → Explain potential delays and disruptions
- "Should we increase heater shipments to Chicago next week?" → Consider weather forecast and suggest inventory adjustments
- "What products sell well during monsoon season?" → Provide insights on seasonal weather-based demand

Respond in a helpful, conversational, and informative manner.
"""
    
    weather_agent = Agent(
        name="WeatherExpert",
        instructions=instructions
    )
    
    return weather_agent

async def run_weather_agent(query: str) -> str:
    """
    Run the weather agent with a user query.
    
    Args:
        query: The user's query string
        
    Returns:
        The agent's response string
    """
    agent = WeatherAgent()
    return await agent.process_query(query)