"""
Base Agent Implementation for EcoSync Prototype

This module provides a base class for all specialized agents to inherit from.
It contains common functionality and methods shared across agent types.
"""
import os
from typing import Dict, Any, List, Optional, Tuple
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from agents.run import RunConfig
from dotenv import load_dotenv, find_dotenv

# Disable tracing for better performance
set_tracing_disabled(True)

# Load environment variables
load_dotenv(find_dotenv())

# Get API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class BaseAgent:
    """Base class for all EcoSync agents."""
    
    def __init__(self, agent_name: str):
        """
        Initialize the base agent.
        
        Args:
            agent_name (str): The name of the agent
        """
        self.agent_name = agent_name
        self.history = []
    
    async def process_query(self, query: str) -> str:
        """
        Process a natural language query and return a response.
        This method should be overridden by subclasses.
        
        Args:
            query (str): The natural language query from the user
            
        Returns:
            str: The agent's response
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def _add_to_history(self, query: str, response: str):
        """
        Add the query and response to the agent's history.
        
        Args:
            query (str): The user's query
            response (str): The agent's response
        """
        self.history.append({
            "query": query,
            "response": response
        })
    
    @staticmethod
    def _clean_query(query: str) -> str:
        """
        Clean and normalize the input query.
        
        Args:
            query (str): The raw query from the user
            
        Returns:
            str: The cleaned query
        """
        # Remove extra whitespace and standardize quotes
        cleaned = query.strip()
        cleaned = " ".join(cleaned.split())
        
        return cleaned

def get_client_and_model():
    """
    Creates and returns OpenAI client and model instances.
    
    Returns:
        tuple: (client, model) if API key is available, (None, None) otherwise
    """
    if not GEMINI_API_KEY:
        return None, None
    
    client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client
    )
    
    return client, model

async def run_agent_with_query(agent, query):
    """
    Run an agent with a user query.
    
    Args:
        agent: The Agent instance to run
        query: The user's query string
        
    Returns:
        The agent's response string
    """
    if not GEMINI_API_KEY:
        return "API key not available. Please set the GEMINI_API_KEY environment variable."
    
    _, model = get_client_and_model()
    
    config = RunConfig(
        model=model,
        tracing_disabled=True,
    )
    
    try:
        runner = Runner(config=config)
        response = await runner.run_agent(agent=agent, user_message=query)
        return response
    except Exception as e:
        return f"Error running agent: {str(e)}"