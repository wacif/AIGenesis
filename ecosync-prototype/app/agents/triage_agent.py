"""
Triage Agent for EcoSync
This module implements a triage agent that routes queries to specialized agents.
"""
import os
import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from dotenv import load_dotenv, find_dotenv

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
        You are a sophisticated Triage Agent responsible for intelligently routing user queries to the most appropriate specialized agent from the following list:
        - Forecasting Agent: This agent specializes in providing real-time weather updates for specific cities. It can answer questions about current temperature, conditions, humidity, wind speed, etc., when a city is clearly mentioned in the query.
        - Real-Time Strike Updates Routing Agent: This agent analyzes user queries related to strikes and protests. It determines if the query includes a specific date or date range. If a specific date is present, it will route the query to the agent that can provide strike information for that date. If no specific date is mentioned, it will ask the user for clarification.

        When you receive a user query, follow these steps to determine the best agent for routing:

          1.  **Analyze for Weather Intent:** First, carefully analyze the user's query to determine if it is related to weather. Look for keywords such as "weather", "temperature", "forecast" (keeping in mind the Forecasting Agent provides *real-time* updates, not future forecasts), "humidity", "wind", and mentions of specific cities or locations.
          2.  **Route to Forecasting Agent:** If the user's query clearly expresses a need for current weather information and specifies a city, your final output should be a clear instruction to forward the query to the "Forecasting Agent". For example: "Forwarding to Forecasting Agent."
          3.  **Analyze for Strike Update Intent:** If the query is not clearly about weather, analyze it to see if it pertains to strikes, protests, or similar events. Look for keywords like "strike", "protest", "demonstration", "event", and any mentions of dates.
          4.  **Handle Ambiguous Queries:** If the user's query is unclear, doesn't fit neatly into either the weather or strike update categories, or if it asks for future weather forecasts (which the Forecasting Agent doesn't handle), politely ask the user for more clarification. For example: "Could you please clarify what information you are looking for?"
        """,
        model=model
    )
    return agent

async def run_triage_agent(query: str):
    """
    Runs the triage agent with the given query.
    
    Args:
        query: The user's query
        
    Returns:
        The agent's classification of the query type: 'weather', 'strike', or 'unknown'
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
    
    if any(kw in response for kw in ['weather', 'forecast', 'temperature']):
        return 'weather', result.final_output
    elif any(kw in response for kw in ['strike', 'protest', 'demonstration']):
        return 'strike', result.final_output
    else:
        return 'unknown', result.final_output