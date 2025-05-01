"""
Routing Agent for EcoSync
This module implements an intelligent routing agent that provides optimal routes.
"""
import os
import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def create_routing_agent():
    """
    Creates an intelligent routing agent that provides optimal routes with real-time information.
    
    Returns:
        An Agent instance configured for route planning
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
    
    # Create a fallback agent since custom tools might not be available
    routing_agent = Agent(
        name="Routing_Agent",
        instructions="""
        You are a sophisticated Routing Agent responsible for providing optimal routes between locations.
        
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