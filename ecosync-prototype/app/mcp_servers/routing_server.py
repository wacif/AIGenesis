"""
Routing MCP Server for EcoSync
This module implements a Model Context Protocol server for routing-related tools.
"""
from mcp.server.fastmcp import FastMCP
import requests
from datetime import datetime

# Create server
mcp = FastMCP("EcoSync Routing Server")

@mcp.tool()
def get_route_info(origin: str, destination: str, mode: str = "driving") -> str:
    """
    Get basic routing information between two locations.
    
    Args:
        origin: Starting location
        destination: Ending location
        mode: Transportation mode (driving, walking, transit, bicycling)
        
    Returns:
        A string with basic routing information and a Google Maps link
    """
    # Validate mode
    valid_modes = ["driving", "walking", "transit", "bicycling"]
    if mode.lower() not in valid_modes:
        mode = "driving"
    
    # Format origin and destination for URL
    origin_formatted = origin.replace(" ", "+")
    destination_formatted = destination.replace(" ", "+")
    
    # Generate Google Maps URL with the specified mode
    maps_url = f"https://www.google.com/maps/dir/?api=1&origin={origin_formatted}&destination={destination_formatted}&travelmode={mode}"
    
    # Mock distance and time calculation 
    # In a real implementation, this would come from a maps/routing API
    estimated_distance = "100-500 km"
    estimated_time = "1-5 hours"
    
    return f"""
Route Information:
- From: {origin}
- To: {destination}
- Mode: {mode.capitalize()}
- Estimated Distance: {estimated_distance} (approximate)
- Estimated Time: {estimated_time} (without traffic)

For precise directions and real-time traffic information, follow this link:
{maps_url}
"""

@mcp.tool()
def check_traffic_conditions(location: str) -> str:
    """
    Check current traffic conditions in a specific location.
    
    Args:
        location: The location to check traffic conditions for
        
    Returns:
        A string containing traffic information
    """
    # Mock traffic data - in a real implementation this would come from a traffic API
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Generate mock traffic conditions based on the location
    traffic_conditions = {
        "lahore": "Moderate traffic on main highways. Construction work on Ferozpur Road causing delays.",
        "karachi": "Heavy traffic in city center. Avoid Shahrah-e-Faisal during rush hours.",
        "islamabad": "Light traffic across most areas. Road maintenance on Kashmir Highway.",
        "new york": "Heavy congestion in Manhattan. Holland Tunnel experiencing delays.",
        "london": "Moderate traffic in central areas. Construction on M25 causing slowdowns.",
        "paris": "Heavy traffic on major boulevards. Avoid Arc de Triomphe roundabout."
    }
    
    location_lower = location.lower()
    
    if location_lower in traffic_conditions:
        return f"Traffic conditions in {location} as of {current_date}: {traffic_conditions[location_lower]}"
    else:
        return f"Traffic information for {location} as of {current_date}: Normal traffic conditions with moderate congestion during peak hours. No major incidents reported."

@mcp.tool()
def get_fuel_prices(location: str) -> str:
    """
    Get current fuel prices in a specific location.
    
    Args:
        location: The location to check fuel prices for
        
    Returns:
        A string containing fuel price information
    """
    # Mock fuel price data - in a real implementation this would come from a fuel price API
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Default prices
    petrol_price = "290 PKR"
    diesel_price = "280 PKR"
    
    # Location-specific prices
    price_data = {
        "pakistan": {"petrol": "290 PKR", "diesel": "280 PKR"},
        "lahore": {"petrol": "289 PKR", "diesel": "279 PKR"},
        "karachi": {"petrol": "291 PKR", "diesel": "281 PKR"},
        "usa": {"petrol": "$3.50", "diesel": "$3.75"},
        "uk": {"petrol": "£1.45", "diesel": "£1.50"}
    }
    
    location_lower = location.lower()
    
    if location_lower in price_data:
        petrol_price = price_data[location_lower]["petrol"]
        diesel_price = price_data[location_lower]["diesel"]
    
    return f"""
Fuel prices in {location} as of {current_date}:
- Petrol/Gasoline: {petrol_price} per liter
- Diesel: {diesel_price} per liter

Note: Prices may vary slightly between different stations and areas.
"""

# Run the server
if __name__ == "__main__":
    mcp.run()