"""
Route Planner Agent for EcoSync
This module provides a route planning agent that generates optimal routes between locations.
"""
import os
from agents import Agent, function_tool
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

@function_tool
def get_route(origin: str, destination: str) -> str:
    """
    Generates a Google Maps link for the given route.
    
    Args:
        origin: The starting point of the route
        destination: The destination point of the route
        
    Returns:
        A string containing route information and a Google Maps link
    """
    # Format origin and destination for URL
    origin_formatted = origin.replace(" ", "+")
    destination_formatted = destination.replace(" ", "+")
    
    # Generate Google Maps URL
    maps_url = f"https://www.google.com/maps/dir/{origin_formatted}/{destination_formatted}"
    
    return f"Route from {origin} to {destination} found. You can view the directions here: {maps_url}"

agent = Agent(
    name="RoutePlannerAgent",
    instructions="""
    You are a specialized Route Planning Agent that provides optimal routes between locations.
    When given origin and destination locations, you'll provide a Google Maps link for directions.
    
    Be sure to:
    1. Extract the exact origin and destination
    2. Generate a proper Google Maps link
    3. Return the link along with a brief description of the route
    """,
    tools=[get_route]
)