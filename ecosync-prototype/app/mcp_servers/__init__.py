"""
Model Context Protocol (MCP) servers module for EcoSync Prototype.

This package contains MCP server implementations:
- routing_server: Handles routing optimization requests via MCP protocol
- weather_server: Handles weather-related requests via MCP protocol
"""

# Import server classes for easy access
from app.mcp_servers.routing_server import RoutingMCPServer
from app.mcp_servers.weather_server import WeatherMCPServer