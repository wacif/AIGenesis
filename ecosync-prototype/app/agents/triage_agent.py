"""
Triage Agent for EcoSync
This module implements a triage agent that routes queries to specialized agents.
"""
import os
import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv, find_dotenv

# Import the agent creation functions
try:
    from ecosync_logistics_agent.forecasting_agent import create_weather_agent
    from ecosync_logistics_agent.routing_agent import create_routing_agent
    custom_agents_available = True
except ImportError:
    custom_agents_available = False
    print("Warning: Could not import custom agent functions. Using fallback implementation.")

load_dotenv(find_dotenv())

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def create_triage_agent():
    """
    Creates a triage agent that routes queries to specialized agents.
    
    Returns:
        An Agent instance configured for query triage
    """
    client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client
    )
    
    agent = Agent(
        name="Triage_Agent",
        instructions="""
        You are a sophisticated Triage Agent responsible for intelligently routing user queries to the most appropriate specialized agent.

        You have the following specialized agents available:

        1.  Forecasting Agent:
            * Use this agent for queries about:
                * Real-time weather conditions in a specific city.
                * The *current* demand or need for weather-related products, *influenced by current weather*. This agent does *not* provide long-term demand forecasts or handle general product inquiries.
            * The user's query will often include:
                * A city name (e.g., "Lahore", "Karachi").
                * Weather-related terms referring to the present (e.g., "weather *now*", "temperature *today*", "current conditions").
                * Inquiries about buying weather-related items *now* *specifically due to weather* (e.g., "need umbrellas *today because of rain*", "want heaters *right now due to cold*", "demand for AC *currently because of heat*").
                * Combinations of the above (e.g., "weather in Lahore *today*").
                * Explicit request for forecast of demand,
        2.  Routing Agent:
            * Use this agent for queries about:
                * Finding routes or getting directions between locations.
                * Current traffic conditions.
                * Disruptions to travel (e.g., strikes, protests, demonstrations, events).
                * Current petrol/gasoline/fuel prices.
                * Deliveries between locations
            * The user's query will often include:
                * Terms about routes and directions (e.g., "route *from* Lahore *to* Karachi", "directions *to* Islamabad", "how to get *to*", "best way *between*").
                * Terms about travel (e.g., "traffic *on* Mall Road", "travel time *to* Murree", " *journey* time", "delivery *from*").
                * Terms about disruptions (e.g., "strike *today*", "protest *schedule*", "roadblock *event*", "traffic *delays*").
                * Terms about fuel (e.g., "petrol price *in* Rawalpindi", "gasoline cost *near* me", "diesel *prices*").
                * Date or time references, *when related to disruptions or travel* (e.g., "strike *on* July 20", "traffic *tomorrow*").
                * Location-to-location phrases (e.g. "shipment from A to B")

        When you receive a user query, follow these steps:

        1.  Prioritize Precise Weather/Demand (Present Tense):
            * First, check *very carefully* if the query is *specifically* about:
                * The *current* weather in a city.
                * The *immediate*, weather-influenced need for a product.
                * Explicit forecast of demand
            * Look for:
                * A city name.
                * Present-tense weather terms (e.g., "is", "now", "today").
                * Immediate-need buying terms *with weather context* (e.g., "need *now because of rain*", "want *today due to cold*", "buy *immediately because of heat*").
                * Explicit request for forecast of demand
        2.  Route to Forecasting Agent:
            * If the query *clearly* fits the "Precise Weather/Demand" criteria, say: "Forwarding to Forecasting Agent."

        3.  Check for Travel/Deliveries/Disruptions:
            * If the query does *not* fit the "Precise Weather/Demand", then check if it's about:
                * Routes/directions.
                * Traffic.
                * Disruptions.
                * Fuel Prices
                * Deliveries between locations

        4.  Route to Routing Agent:
            * If the query is clearly about travel/deliveries/disruptions, say: "Forwarding to Routing Agent."

        5.  Ask for Clarification:
            * If the query is unclear, ambiguous, or doesn't fit either category, politely request more specific information.
            * For example: "Could you please clarify whether you are asking about current weather/immediate needs, or travel-related disruptions/routes/deliveries?"
        """,
        model=model
    )
    return agent

# Define weather and routing keywords for classification
WEATHER_KEYWORDS = ["weather", "temperature", "forecast", "city", "demand", "need", "buy", "umbrella", "heater", "ac", "rain", "cold", "heat", "snow", "humid", "sunny", "climate"]
ROUTING_KEYWORDS = ["strike", "protest", "news", "event", "date", "route", "traffic", "petrol", "journey", "delivery", "shipment", "directions", "road", "highway", "travel", "trip", "drive", "from", "to", "between"]

async def run_triage_agent(query: str):
    """
    Runs the triage agent with the given query.
    
    Args:
        query: The user's query
        
    Returns:
        The agent's classification of the query type: 'weather', 'routing', or 'unknown'
    """
    config = RunConfig(
        model=None,  # Will be set in the agent
        tracing_disabled=True,
    )
    
    triage_agent = await create_triage_agent()
    result = await Runner.run(
        triage_agent,
        query,
        run_config=config
    )
    
    # Process the result to get a standardized response
    response = result.final_output.lower().strip()
    
    # Check for specific agent references in the response
    if "forwarding to forecasting agent" in response:
        return 'weather', result.final_output
    elif "forwarding to routing agent" in response:
        return 'routing', result.final_output
    else:
        # Fallback to keyword matching if the agent response isn't explicit
        query_lower = query.lower()
        weather_match = any(kw in query_lower for kw in WEATHER_KEYWORDS)
        routing_match = any(kw in query_lower for kw in ROUTING_KEYWORDS)
        
        if weather_match and not routing_match:
            return 'weather', result.final_output
        elif routing_match and not weather_match:
            return 'routing', result.final_output
        elif weather_match and routing_match:
            # If both types of keywords are present, trust the agent's response or return unknown
            return 'unknown', result.final_output
        else:
            return 'unknown', result.final_output

# The following function is provided for direct CLI testing
async def main():
    """CLI interface for testing the triage agent"""
    client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
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
    
    # Create the triage agent
    triage_agent = await create_triage_agent()
    
    # Try to initialize specialized agents if available
    weather_agent = None
    routing_agent = None
    
    if custom_agents_available:
        try:
            # Initialize agents including the Weather Server setup
            async with MCPServerStdio(
                name="Weather Server for Triage",
                params={
                    "command": "mcp",
                    "args": ["run", "weather_server.py"]
                },
                cache_tools_list=True
            ) as weather_mcp_server:
                weather_agent = await create_weather_agent(weather_mcp_server)
                routing_agent = await create_routing_agent()
        except Exception as e:
            print(f"Error initializing specialized agents: {str(e)}")
    
    # Define fallbacks if agents couldn't be initialized
    if weather_agent is None:
        weather_agent = Agent(
            name="Fallback_Weather_Agent",
            instructions="You are a weather information agent. Provide general weather information based on your knowledge.",
            model=model
        )
    
    if routing_agent is None:
        routing_agent = Agent(
            name="Fallback_Routing_Agent",
            instructions="You are a routing and travel information agent. Provide general guidance on routes, traffic, and travel disruptions based on your knowledge.",
            model=model
        )
    
    handoffs = [
        {"name": "ForecastingAgent", "agent": weather_agent, "keywords": WEATHER_KEYWORDS},
        {"name": "RoutingAgent", "agent": routing_agent, "keywords": ROUTING_KEYWORDS},
    ]
    
    while True:
        user_query = input("Enter your query (or type 'quit' to exit): ").strip()
        if user_query.lower() == 'quit':
            break
        
        triage_result = await Runner.run(triage_agent, user_query, run_config=config)
        print(f"\nTriage Agent says: {triage_result.final_output}")
        
        handled = False
        for handoff_info in handoffs:
            if any(keyword in user_query.lower() for keyword in handoff_info["keywords"]):
                print(f"Forwarding to {handoff_info['name']}...")
                result = await Runner.run(handoff_info["agent"], user_query, run_config=config)
                # Print the result from the delegated agent:
                print(f"{handoff_info['name']} Result: {result.final_output}\n")
                handled = True
                break
        
        if not handled:
            print("Could not determine the appropriate agent. Please clarify your query.\n")

if __name__ == "__main__":
    asyncio.run(main())