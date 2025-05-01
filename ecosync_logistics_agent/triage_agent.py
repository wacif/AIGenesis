import os
import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv, find_dotenv

# Import the agent creation functions
from ecosync_logistics_agent.forecasting_agent import create_weather_agent
from ecosync_logistics_agent.routing_agent import create_routing_agent

load_dotenv(find_dotenv())

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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

async def create_triage_agent():
    triage_agent = Agent(
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
    return triage_agent

async def run_triage_agent(query: str):
    """
    Runs the triage agent on a query and routes to the appropriate specialized agent.
    """
    triage_agent = await create_triage_agent()
    triage_result = await Runner.run(triage_agent, query, run_config=config)
    triage_response = triage_result.final_output.strip()
    
    # Check which agent the triage agent is routing to
    if "Forwarding to Forecasting Agent" in triage_response:
        # Process with Forecasting Agent
        async with MCPServerStdio(
            name="Weather Server",
            params={
                "command": "mcp",
                "args": ["run", "ecosync_logistics_agent/weather_server.py"]
            },
            cache_tools_list=True
        ) as weather_mcp_server:
            weather_agent = await create_weather_agent(weather_mcp_server)
            result = await Runner.run(weather_agent, query, run_config=config)
            return result.final_output
            
    elif "Forwarding to Routing Agent" in triage_response:
        # Process with Routing Agent
        routing_agent = await create_routing_agent()
        result = await Runner.run(routing_agent, query, run_config=config)
        return result.final_output
    
    else:
        # Return the triage agent's response (likely asking for clarification)
        return triage_response

if __name__ == "__main__":
    query = input("Enter your query: ")
    response = asyncio.run(run_triage_agent(query))
    print(f"\nResponse: {response}")