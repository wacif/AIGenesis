"""
Routing Agent for EcoSync
This module implements an intelligent routing agent that provides optimal routes with real-time information.
"""
import os
import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from agents.run import RunConfig
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

set_tracing_disabled(True)

# Try importing the custom tools
try:
    from ecosync_logistics_agent.custom_tools.route_planner_agent import agent as route_planner_agent_instance
    from ecosync_logistics_agent.custom_tools.live_search_agent import agent as live_search_agent_instance
    custom_tools_available = True
except ImportError:
    custom_tools_available = False
    print("Warning: Could not import custom routing tools. Using fallback implementation.")

load_dotenv(find_dotenv())

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_client_and_model():
    if GEMINI_API_KEY:
        client = AsyncOpenAI(
            api_key=GEMINI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        
        model = OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            openai_client=client
        )
        
        return client, model
    return None, None

client, model = get_client_and_model()

async def create_routing_agent():
    """
    Creates an intelligent routing agent that provides optimal routes with real-time information.
    
    Returns:
        An Agent instance configured for route planning
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    
    if not custom_tools_available:
        # Create a fallback agent if custom tools are not available
        routing_agent = Agent(
            name="Routing_Agent",
            instructions="""
            You are a sophisticated Routing Agent responsible for providing optimal routes between locations.
            Since your specialized tools are not available, you'll provide general routing guidance based on your knowledge.
            
            For any route request:
            1. Consider typical traffic patterns for the time of day
            2. Suggest alternative routes if available
            3. Mention any known points of interest or landmarks along the way
            4. Provide an estimated travel time and distance
            
            Format your response in a clear, structured manner with sections for:
            - Route Overview
            - Estimated Time & Distance
            - Key Waypoints
            - Travel Tips
            """,
            model=model
        )
        return routing_agent
    
    # If custom tools are available, create the full-featured routing agent
    routing_agent = Agent(
        name="Intelligent_Routing_Agent",
        instructions=f"""Your primary goal is to provide the best route from a user-specified source to a destination, considering real-time traffic, potential strikes, and generate a direct link to a Google Maps route showing step-by-step driving directions.

        You have access to the following tools:

        1. get_route: Generates a Google Maps link for the given route.
        2. get_real_time_info: Fetches real-time traffic, strikes, and petrol price information for a given location or route.

        Use these tools to fulfill the user's request. First, get the route link, then fetch real-time information relevant to that route to provide the best possible guidance. Finally, output the route link along with any important alerts and petrol price.
        """,
        tools=[
            route_planner_agent_instance.as_tool(
                tool_name="get_route",
                tool_description="Generates a Google Maps link for the given route (e.g., Lahore -> Karachi).",
            ),
            live_search_agent_instance.as_tool(
                tool_name="get_real_time_info",
                tool_description="Fetches real-time traffic, strikes, and petrol price information for a given location or route (e.g., traffic from Lahore to Karachi, strikes in Karachi today, petrol price in Pakistan).",
            ),
        ],
        model=model
    )
    return routing_agent

async def run_routing_agent(query: str):
    """
    Runs the routing agent with the given query.
    
    Args:
        query: The user's routing request, e.g., "I want to go from Lahore to Karachi"
        
    Returns:
        Route information with real-time updates and Google Maps link
    """
    if not GEMINI_API_KEY or not model:
        return "Routing agent is not available. Please check your API key configuration."
    
    config = RunConfig(
        model=model,
        tracing_disabled=True,
    )
    
    try:
        routing_agent = await create_routing_agent()
        result = await Runner.run(
            routing_agent,
            query,
            run_config=config
        )
        
        return result.final_output
    except Exception as e:
        return f"Error processing routing request: {str(e)}"

# Initialize the agent on module load
try:
    agent = asyncio.get_event_loop().run_until_complete(create_routing_agent())
except Exception as e:
    print(f"Error initializing routing agent: {str(e)}")
    agent = None

async def main():
    """Simple CLI for testing the agent directly"""
    user_query = input("Enter your route request (e.g., I want to go from Lahore to Karachi): ")
    result = await run_routing_agent(user_query)
    print(f"\n\nFinal response:\n{result}")

if __name__ == "__main__":
    asyncio.run(main())