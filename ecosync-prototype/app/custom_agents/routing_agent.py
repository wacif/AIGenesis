"""
Routing Agent Implementation for EcoSync Prototype

This module provides a specialized agent for handling logistics routing,
optimization, and route planning capabilities.
"""

from agents import Agent
import os
import json
from app.custom_agents.base_agent import BaseAgent, get_client_and_model, run_agent_with_query
from app.custom_tools.route_tools import optimize_route

class RoutingAgent(BaseAgent):
    """
    Routing specialized agent that handles logistics routing, optimization,
    and sustainable route planning capabilities.
    """
    
    def __init__(self):
        """Initialize the Routing Agent."""
        super().__init__("Routing Agent")
    
    async def process_query(self, query: str) -> str:
        """
        Process a routing-related query.
        
        Args:
            query (str): The routing-related query from the user
            
        Returns:
            str: The agent's response
        """
        cleaned_query = self._clean_query(query)
        
        # Create a Routing Agent instance
        agent = create_routing_agent()
        
        # Run the agent with the query
        response = await run_agent_with_query(agent, cleaned_query)
        
        # Add to history
        self._add_to_history(cleaned_query, response)
        
        return response

def create_routing_agent():
    """
    Create and return an instance of a Routing Agent.
    
    Returns:
        Agent: An Agent instance configured for routing-related queries
    """
    instructions = """You are a Routing Specialist agent for EcoSync Logistics. Your specialty is optimizing delivery routes, reducing carbon footprints, and helping logistics planners make efficient routing decisions.

CAPABILITIES:
- Suggest optimal routes between locations
- Calculate estimated delivery times and distances
- Optimize multi-stop delivery routes
- Evaluate carbon footprint of different transportation options
- Recommend sustainable shipping alternatives
- Balance speed, cost, and environmental impact in routing decisions

GUIDELINES:
1. Always prioritize sustainability when suggesting routes, unless urgent delivery is specified
2. Consider traffic patterns, weather conditions, and geographic constraints in routing recommendations
3. Provide clear explanations of trade-offs between speed, cost, and environmental impact
4. When optimizing multi-stop routes, explain the algorithm or approach used
5. Include carbon footprint estimates when comparing different routing options
6. Suggest alternative transportation modes (rail, water, electric vehicles) when appropriate

LIMITATIONS:
- You cannot provide real-time traffic conditions unless specifically provided with that data
- You do not have access to proprietary carrier pricing without the relevant data
- Your carbon footprint calculations are estimates based on standard industry values
- You cannot book or schedule actual deliveries

EXAMPLES:
- "What's the best route from Boston to Chicago?" → Provide options with sustainability focus
- "How can we reduce emissions for our LA to Seattle route?" → Suggest alternative transport modes
- "Optimize our delivery route through these 5 cities" → Provide an optimized sequence with rationale
- "Calculate carbon footprint difference between air and truck shipping" → Compare environmental impacts
- "What's our most efficient distribution pattern for the Northeast region?" → Analyze regional logistics

Respond in a helpful, conversational, and informative manner.
"""
    
    routing_agent = Agent(
        name="RoutingSpecialist",
        instructions=instructions
    )
    
    return routing_agent

async def run_routing_agent(query: str) -> str:
    """
    Run the routing agent with a user query.
    
    Args:
        query: The user's query string
        
    Returns:
        The agent's response string
    """
    agent = RoutingAgent()
    return await agent.process_query(query)