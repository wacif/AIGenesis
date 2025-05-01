"""
Live Search Agent for EcoSync
This module provides a live search agent that retrieves real-time information for routes.
"""
import os
from agents import Agent, function_tool
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

load_dotenv(find_dotenv())

@function_tool
def get_real_time_info(query: str) -> str:
    """
    Fetches real-time traffic, strikes, and petrol price information for a given location or route.
    
    Args:
        query: The query about traffic, strikes, or petrol prices for a specific location or route
        
    Returns:
        A string containing real-time information based on the query
    """
    # This is a mock implementation - in a real system, this would call external APIs
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Check query type and return mock response
    query_lower = query.lower()
    
    if "traffic" in query_lower:
        locations = []
        if "from" in query_lower and "to" in query_lower:
            # Extract location names - this is a simple implementation
            try:
                from_index = query_lower.index("from") + 5
                to_index = query_lower.index("to") + 3
                from_part = query_lower[from_index:query_lower.index("to")].strip()
                to_part = query_lower[to_index:].strip()
                locations = [from_part, to_part]
            except:
                locations = ["location"]
        else:
            # Try to find a location after "in" or "on"
            try:
                if "in" in query_lower:
                    loc_index = query_lower.index("in") + 3
                    locations = [query_lower[loc_index:].strip()]
                elif "on" in query_lower:
                    loc_index = query_lower.index("on") + 3
                    locations = [query_lower[loc_index:].strip()]
            except:
                locations = ["location"]
        
        loc_text = " to ".join(locations) if len(locations) > 1 else locations[0]
        return f"Traffic report for {loc_text} as of {current_date}: Traffic is flowing normally with some moderate congestion during peak hours. No major incidents reported."
    
    elif "strike" in query_lower or "protest" in query_lower:
        # Extract location
        location = "specified location"
        try:
            if "in" in query_lower:
                loc_index = query_lower.index("in") + 3
                location = query_lower[loc_index:].strip()
        except:
            pass
        
        return f"No major strikes or protests reported in {location} as of {current_date}. Local transportation and services are operating as normal."
    
    elif "petrol" in query_lower or "gas" in query_lower or "fuel" in query_lower:
        # Extract location
        location = "Pakistan"
        try:
            if "in" in query_lower:
                loc_index = query_lower.index("in") + 3
                location = query_lower[loc_index:].strip()
        except:
            pass
        
        return f"Current petrol prices in {location} as of {current_date}: Average price is approximately 290 PKR per liter. Diesel is priced at approximately 280 PKR per liter."
    
    else:
        # Default response
        return f"No specific real-time information found for your query. Please specify if you're looking for traffic conditions, strikes, or petrol prices in a particular location."

agent = Agent(
    name="LiveSearchAgent",
    instructions="""
    You are a specialized Live Search Agent that provides real-time information about:
    1. Traffic conditions between locations
    2. Strikes or protests that might affect travel
    3. Current petrol/fuel prices
    
    When given a query, extract the key information needs and the location, then provide the most relevant and up-to-date information available.
    """,
    tools=[get_real_time_info]
)