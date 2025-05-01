"""
Agent registry module for AIGenesis.
This module manages the registration and loading of different AI agents.
"""
import asyncio

def register_agents(agent_registry):
    """
    Register all available agents into the provided registry.
    
    Args:
        agent_registry (dict): Dictionary to store agent objects
    """
    # First register the basic test agent
    from custom_agents.base_agent import BaseAgent
    test_agent = BaseAgent("Test Agent")
    agent_registry[test_agent.name] = test_agent
    
    # Register the main EcoSync Logistics agents
    from ecosync_logistics_agent.agent_adapter import TriageAgentAdapter
    from ecosync_logistics_agent.agent_adapter import ForecastingAgentAdapter
    from ecosync_logistics_agent.agent_adapter import RoutingAgentAdapter
    
    # Register the triage agent
    triage_agent = TriageAgentAdapter()
    agent_registry["EcoSync Logistics"] = triage_agent
    
    # Register specialized agents directly
    forecasting_agent = ForecastingAgentAdapter()
    agent_registry["Weather & Forecasting Agent"] = forecasting_agent
    
    routing_agent = RoutingAgentAdapter()
    agent_registry["Routing & Traffic Agent"] = routing_agent