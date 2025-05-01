import asyncio
from custom_agents.base_agent import BaseAgent
from ecosync_logistics_agent.triage_agent import run_triage_agent
from ecosync_logistics_agent.forecasting_agent import create_weather_agent
from ecosync_logistics_agent.routing_agent import create_routing_agent
from agents.mcp import MCPServerStdio
from agents.run import Runner

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

class ForecastingAgentAdapter(BaseAgent):
    """
    Adapter class that connects directly to the forecasting agent.
    """
    
    def __init__(self):
        """Initialize the adapter with a name."""
        super().__init__(name="Weather & Forecasting Agent")
        self.history = []
    
    def process_message(self, message):
        """
        Process a message directly through the forecasting agent.
        
        Args:
            message (str): User's message
            
        Returns:
            str: Agent's response
        """
        # Store the message in history
        self.history.append({"role": "user", "content": message})
        
        # Define an async function to run the weather agent
        async def run_forecast_agent():
            async with MCPServerStdio(
                name="Weather Server",
                params={
                    "command": "mcp",
                    "args": ["run", "ecosync_logistics_agent/weather_server.py"]
                },
                cache_tools_list=True
            ) as weather_mcp_server:
                weather_agent = await create_weather_agent(weather_mcp_server)
                result = await Runner.run(weather_agent, message)
                return result.final_output
        
        # Run the async function in a synchronous context
        loop = asyncio.new_event_loop()
        response = loop.run_until_complete(run_forecast_agent())
        loop.close()
        
        # Store the response in history
        self.history.append({"role": "assistant", "content": response})
        
        return response

class RoutingAgentAdapter(BaseAgent):
    """
    Adapter class that connects directly to the routing agent.
    """
    
    def __init__(self):
        """Initialize the adapter with a name."""
        super().__init__(name="Routing & Traffic Agent")
        self.history = []
    
    def process_message(self, message):
        """
        Process a message directly through the routing agent.
        
        Args:
            message (str): User's message
            
        Returns:
            str: Agent's response
        """
        # Store the message in history
        self.history.append({"role": "user", "content": message})
        
        # Define an async function to run the routing agent
        async def run_routing_agent():
            routing_agent = await create_routing_agent()
            result = await Runner.run(routing_agent, message)
            return result.final_output
        
        # Run the async function in a synchronous context
        loop = asyncio.new_event_loop()
        response = loop.run_until_complete(run_routing_agent())
        loop.close()
        
        # Store the response in history
        self.history.append({"role": "assistant", "content": response})
        
        return response