"""
Strike Agent for EcoSync
This module implements a strike information agent that provides updates on strikes and protests.
"""
from datetime import datetime
from agents import Agent, function_tool
from app.custom_agents.base_agent import get_client_and_model, run_agent_with_query

@function_tool
def get_strike_info(location: str, date: str = None) -> str:
    """
    Get information about strikes or protests in a specific location on a specific date.
    
    Args:
        location: The name of the city or country to check for strikes
        date: The date to check for strikes (optional, defaults to today)
        
    Returns:
        A string containing information about any strikes or protests
    """
    # Use the current date if none provided
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Mock strike data - in a real system this would come from an API or database
    strikes = {
        "paris": {
            "2025-05-01": "Large transportation strike affecting metro and bus services. Expect significant delays.",
            "2025-05-02": "Minor protests in city center. Public transportation operating normally."
        },
        "london": {
            "2025-05-10": "Railway workers strike affecting major stations. Limited service available."
        },
        "new york": {
            "2025-05-15": "Taxi drivers protest in downtown Manhattan. Increased traffic congestion expected."
        },
        "lahore": {
            "2025-05-01": "Transport workers strike affecting major routes. Consider alternative transportation."
        }
    }
    
    location_lower = location.lower()
    
    # Check for specific location match
    if location_lower in strikes:
        if date in strikes[location_lower]:
            return f"Strike information for {location} on {date}: {strikes[location_lower][date]}"
        else:
            return f"No strikes or protests reported in {location} on {date}. Services are expected to operate normally."
    
    # Default response if no specific data is available
    return f"No strike information available for {location} on {date}. This is likely because there are no significant disruptions planned or our system doesn't have data for this location."

async def create_strike_agent():
    """
    Creates a strike information agent that provides updates on strikes and protests.
    
    Returns:
        An Agent instance configured for strike information
    """
    client, model = get_client_and_model()
    
    if not client or not model:
        return None
    
    agent = Agent(
        name="StrikeAgent",
        instructions="""
        You are a Strike Information Agent providing up-to-date information about strikes, protests, 
        and other events that might disrupt transportation and logistics.
        
        When a user asks about strikes or protests:
        1. Extract the specific location (city or country) from the query
        2. Extract the date from the query if provided (default to today if not specified)
        3. Use the get_strike_info tool to retrieve information about any strikes or protests
        4. If the location or date is unclear, politely ask for clarification
        5. Present the information in a clear, structured format with:
           - Strike/protest status (ongoing, scheduled, none reported)
           - Expected impact on transportation and logistics
           - Alternative suggestions if available
        6. Maintain a helpful, informative tone throughout
        """,
        tools=[get_strike_info]
    )
    return agent

async def run_strike_agent(query: str):
    """
    Runs the strike agent with the given query.
    
    Args:
        query: The user's strike-related query
        
    Returns:
        The agent's response to the query
    """
    strike_agent = await create_strike_agent()
    if not strike_agent:
        return "Strike agent could not be initialized. Please check your API key configuration."
    
    formatted_query = f"Strike information request: {query}"
    return await run_agent_with_query(strike_agent, formatted_query)