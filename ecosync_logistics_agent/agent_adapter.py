import asyncio
from custom_agents.base_agent import BaseAgent
from ecosync_logistics_agent.triage_agent import run_triage_agent

class TriageAgentAdapter(BaseAgent):
    """
    Adapter class that connects our Flask web UI to the EcoSync Logistics triage agent system.
    Inherits from BaseAgent so it can be used with the existing UI infrastructure.
    """
    
    def __init__(self):
        """Initialize the adapter with a name."""
        super().__init__(name="EcoSync Logistics")
        self.history = []
        
    def process_message(self, message):
        """
        Process a message through the triage agent system.
        
        Args:
            message (str): User's message
            
        Returns:
            str: Agent's response
        """
        # Store the message in history
        self.history.append({"role": "user", "content": message})
        
        # Process the message through the triage agent system
        # We need to run the async function in a synchronous context
        loop = asyncio.new_event_loop()
        response = loop.run_until_complete(run_triage_agent(message))
        loop.close()
        
        # Store the response in history
        self.history.append({"role": "assistant", "content": response})
        
        return response