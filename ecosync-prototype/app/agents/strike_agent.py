"""
Strike Agent for EcoSync
This module implements a strike information agent that provides updates on strikes and protests.
"""
import os
import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled
set_tracing_disabled(True)
from agents.run import RunConfig
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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
    # This is a mock implementation that returns fake data
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
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    
    client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client
    )
    
    agent = Agent(
        name="Strike_Agent",
        instructions="""
        You are a Strike Information Agent providing up-to-date information about strikes, protests, and other events that might disrupt transportation and logistics.
        
        When a user asks about strikes or protests:
        1. Extract the specific location (city or country) from the query
        2. Extract the date from the query if provided (default to today if not specified)
        3. Use the get_strike_info tool to retrieve information about any strikes or protests
        4. If the location or date is unclear, politely ask for clarification
        5. Present the information in a clear, structured format with:
           - Strike/protest status (ongoing, scheduled, none reported)
           - Expected impact on transportation and logistics
           - Alternative suggestions if available
           - Source of the information (note that this is mock data for the prototype)
        6. Maintain a helpful, informative tone throughout
        
        Example query: "Are there any strikes in Paris on May 1, 2025?"
        Example response: "I've checked for strikes in Paris on May 1, 2025. There is a large transportation strike affecting metro and bus services. You should expect significant delays. Alternative options include using taxis, ride-sharing services, or walking for shorter distances."
        """,
        tools=[get_strike_info],
        model=model
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
    if not GEMINI_API_KEY:
        return "Strike agent is not available. Please check your API key configuration."
    
    config = RunConfig(
        model=None,  # Will be set in the agent
        tracing_disabled=True,
    )
    
    try:
        strike_agent = await create_strike_agent()
        result = await Runner.run(
            strike_agent,
            query,
            run_config=config
        )
        
        return result.final_output
    except Exception as e:
        return f"Error processing strike information request: {str(e)}"

# Initialize the agent on module load
try:
    agent = asyncio.get_event_loop().run_until_complete(create_strike_agent())
except Exception as e:
    print(f"Error initializing strike agent: {str(e)}")
    agent = None

async def main():
    """Simple CLI for testing the agent directly"""
    user_query = input("Enter your strike information request (e.g., Any strikes in Paris on May 1, 2025?): ")
    result = await run_strike_agent(user_query)
    print(f"\n\nFinal response:\n{result}")

if __name__ == "__main__":
    asyncio.run(main())