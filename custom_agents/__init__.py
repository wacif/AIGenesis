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
    
    # Now register our EcoSync Logistics agents
    from ecosync_logistics_agent.agent_adapter import TriageAgentAdapter
    
    triage_agent = TriageAgentAdapter()
    agent_registry["EcoSync Logistics"] = triage_agent