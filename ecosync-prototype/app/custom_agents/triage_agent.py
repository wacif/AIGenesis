"""
Triage Agent for EcoSync
This module implements a triage agent that routes queries to specialized agents.
"""
from agents import Agent
from app.custom_agents.base_agent import get_client_and_model, run_agent_with_query

# Define keywords for each agent type to help with classification
WEATHER_KEYWORDS = ["weather", "temperature", "forecast", "city", "demand", "rain", 
                   "cold", "heat", "snow", "humid", "sunny", "climate"]

ROUTING_KEYWORDS = ["route", "traffic", "journey", "delivery", "shipment", "directions", 
                   "road", "highway", "travel", "trip", "drive", "from", "to", "between"]

STRIKE_KEYWORDS = ["strike", "protest", "demonstration", "disruption", "blockage", 
                  "union", "labor", "industrial action", "rally", "march"]

async def create_triage_agent():
    """
    Creates a triage agent that routes queries to specialized agents.
    
    Returns:
        An Agent instance configured for query triage
    """
    client, model = get_client_and_model()
    
    if not client or not model:
        return None
    
    agent = Agent(
        name="TriageAgent",
        instructions="""
        You are a sophisticated Triage Agent responsible for intelligently routing user queries 
        to the most appropriate specialized agent.

        You have the following specialized agents available:

        1. Weather Agent:
           - Use for queries about current weather conditions in specific cities
           - Queries typically include city names and weather terms

        2. Routing Agent:
           - Use for queries about routes, directions, traffic, or shipments between locations
           - Queries typically include origin and destination locations, transportation methods

        3. Strike Agent:
           - Use for queries about strikes, protests, or transportation disruptions
           - Queries typically include location names and questions about disruptions

        For each query, carefully analyze the intent and keywords to determine which agent would 
        be most appropriate. Make a clear decision and respond ONLY with one of these phrases:
        
        - "weather" - If the query is about weather conditions
        - "routing" - If the query is about routes, directions, or shipments
        - "strike" - If the query is about strikes, protests, or disruptions
        - "unknown" - If the query doesn't clearly match any of the specialized agents

        Do not provide any other information or explanations in your response.
        """
    )
    return agent

async def run_triage_agent(query: str):
    """
    Runs the triage agent with the given query and determines the most appropriate specialized agent.
    
    Args:
        query: The user's query
        
    Returns:
        tuple: (agent_type, response_message)
        - agent_type: One of 'weather', 'routing', 'strike', or 'unknown'
        - response_message: The triage agent's classification reasoning
    """
    triage_agent = await create_triage_agent()
    if not triage_agent:
        return "unknown", "Triage agent could not be initialized. Please check your API key configuration."
    
    # First, get the triage agent's assessment
    triage_response = await run_agent_with_query(triage_agent, query)
    
    # Extract the agent type from the response
    response_lower = triage_response.lower().strip()
    
    # Check for explicit agent mentions in the response
    if "weather" in response_lower:
        return "weather", "Weather-related query detected. Routing to Weather Agent."
    elif "routing" in response_lower:
        return "routing", "Route planning query detected. Routing to Routing Agent."
    elif "strike" in response_lower:
        return "strike", "Strike or disruption query detected. Routing to Strike Agent."
    
    # If the triage agent didn't return a clear category, use keyword matching as fallback
    query_lower = query.lower()
    weather_match = any(keyword in query_lower for keyword in WEATHER_KEYWORDS)
    routing_match = any(keyword in query_lower for keyword in ROUTING_KEYWORDS)
    strike_match = any(keyword in query_lower for keyword in STRIKE_KEYWORDS)
    
    # Count the matches to determine the most likely category
    match_counts = {
        "weather": sum(1 for keyword in WEATHER_KEYWORDS if keyword in query_lower),
        "routing": sum(1 for keyword in ROUTING_KEYWORDS if keyword in query_lower),
        "strike": sum(1 for keyword in STRIKE_KEYWORDS if keyword in query_lower)
    }
    
    # Get the category with the most matches, if any
    if max(match_counts.values()) > 0:
        best_match = max(match_counts.items(), key=lambda x: x[1])[0]
        return best_match, f"Based on keywords, routing to {best_match.capitalize()} Agent."
    
    return "unknown", "Could not determine appropriate agent. Please provide more specific information."