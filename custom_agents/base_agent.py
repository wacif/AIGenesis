"""
Base Agent class that defines the interface for all agents in the system.
"""

class BaseAgent:
    def __init__(self, name="Base Agent"):
        """
        Initialize the base agent with a name.
        
        Args:
            name (str): Name of the agent
        """
        self.name = name
        self.history = []
    
    def process_message(self, message):
        """
        Process a message and return a response.
        
        Args:
            message (str): User's message
            
        Returns:
            str: Agent's response
        """
        # Store the message in history
        self.history.append({"role": "user", "content": message})
        
        # Basic implementation for the base agent
        response = f"Echo from {self.name}: {message}"
        
        # Store the response in history
        self.history.append({"role": "assistant", "content": response})
        
        return response
    
    def get_history(self):
        """
        Get the conversation history.
        
        Returns:
            list: List of conversation messages
        """
        return self.history
    
    def clear_history(self):
        """
        Clear the conversation history.
        """
        self.history = []