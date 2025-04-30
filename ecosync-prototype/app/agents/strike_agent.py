"""
Strike Agent for EcoSync
This module implements an agent that provides information about strikes and protests.
"""
import os
import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from agents.tool import function_tool
from tavily import TavilyClient
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

@function_tool("tavily_search")
def tavily_search(query: str):
    """Fetch the latest information from websites."""
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    response = tavily_client.search(query)

    # Extract and return all 'content' fields
    contents = [item['content'] for item in response.get('results', [])]
    return contents

async def create_strike_agent():
    """
    Creates a strike agent that provides information about strikes and protests.
    
    Returns:
        An Agent instance configured for strike information
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
        name="RoutingAgent",
        instructions="""
        You are a Strike Information Agent. Your primary role is to respond to user queries about strikes and protests based on a specified date.
        When you receive a query from a user, your process should be as follows:
           1.  **Identify the Date:** Carefully extract the specific date or date range mentioned in the user's query. If no clear date is provided, politely ask the user for a specific date to proceed. For example: "Could you please provide the specific date you are interested in for strike information?"
           2.  **Utilize the 'tavily_search' Tool:** Once you have a specific date or keywords related to a date, use the 'tavily_search' tool to find relevant information about strikes, protests, or significant events that occurred around that time. Formulate your search query to include the date and relevant keywords like "strike", "protest", "demonstration", etc.
           3.  **Summarize the Content:** After using the 'tavily_search' tool, you will receive content from various websites. Your task is to read through this content and identify individual instances of strikes or protests. For each distinct strike or protest you find, extract the following information:
                   * **City Name:** The city where the event took place.
                   * **Location:** The specific location within the city (if mentioned).
                   * **Reason for the Strike/Protest:** A brief explanation of why the event occurred.
           4.  **Format the Output:** Present the summarized information clearly, with each strike or protest described in one concise line. Ensure each line contains the city name, location (if available), and the reason for the event.
           5.  **Handle No Results:** If the 'tavily_search' tool does not return any relevant information for the specified date, inform the user that no strike information was found for that period.
        """,
        tools=[tavily_search],
        model=model
    )
    return agent

async def run_strike_agent(query: str):
    """
    Runs the strike agent with the given query.
    
    Args:
        query: The user's strike information query
        
    Returns:
        The agent's response to the query
    """
    config = RunConfig(
        model=None,  # Will be set in the agent
        tracing_disabled=True,
    )
    
    strike_agent = await create_strike_agent()
    result = await Runner.run(
        strike_agent,
        query,
        run_config=config
    )
    return result.final_output