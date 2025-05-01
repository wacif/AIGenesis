"""
Routing Tools for EcoSync
This module provides utility functions for route planning and optimization.
"""
import json
import os
from datetime import datetime

def generate_maps_url(origin: str, destination: str, mode: str = "driving") -> str:
    """
    Generates a Google Maps URL for the given route.
    
    Args:
        origin: The starting point
        destination: The destination point
        mode: Transportation mode (driving, walking, transit, bicycling)
        
    Returns:
        A Google Maps URL string
    """
    # Format origin and destination for URL
    origin_formatted = origin.replace(" ", "+")
    destination_formatted = destination.replace(" ", "+")
    
    # Generate Google Maps URL
    return f"https://www.google.com/maps/dir/?api=1&origin={origin_formatted}&destination={destination_formatted}&travelmode={mode}"

def optimize_route(origin: str, destination: str, eco_friendly: bool = False) -> dict:
    """
    Optimizes a route based on various factors including eco-friendliness.
    
    Args:
        origin: The starting point
        destination: The destination point
        eco_friendly: Whether to prioritize eco-friendly routing
        
    Returns:
        A dictionary containing route optimization results
    """
    # This is a mock implementation - in a real system, this would call a routing API
    
    # Calculate mock carbon emissions savings
    base_emissions = 25.0  # kg CO2
    eco_savings = 10.0 if eco_friendly else 0.0
    
    # Generate route optimization result
    result = {
        "origin": origin,
        "destination": destination,
        "eco_mode": eco_friendly,
        "emissions_kg": base_emissions - eco_savings,
        "emissions_saved_kg": eco_savings if eco_friendly else 0.0,
        "maps_url": generate_maps_url(origin, destination),
        "timestamp": datetime.now().isoformat()
    }
    
    # Save route to data file
    try:
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
        routes_file = os.path.join(data_dir, "routes.json")
        
        # Load existing routes if file exists
        routes = []
        if os.path.exists(routes_file):
            try:
                with open(routes_file, "r") as f:
                    routes = json.load(f)
            except json.JSONDecodeError:
                routes = []
        
        # Add new route
        routes.append(result)
        
        # Write back to file
        with open(routes_file, "w") as f:
            json.dump(routes, f, indent=2)
    except Exception as e:
        print(f"Error saving route data: {str(e)}")
    
    return result

def check_for_disruptions(origin: str, destination: str) -> list:
    """
    Checks for known disruptions on a route.
    
    Args:
        origin: The starting point
        destination: The destination point
        
    Returns:
        A list of disruption dictionaries
    """
    # This is a mock implementation - in a real system, this would query a traffic API
    
    # Mock data for specific routes
    disruptions = []
    
    if ("lahore" in origin.lower() and "islamabad" in destination.lower()) or \
       ("islamabad" in origin.lower() and "lahore" in destination.lower()):
        disruptions.append({
            "type": "construction",
            "location": "M2 Motorway, near Kallar Kahar",
            "description": "Road maintenance causing lane closures",
            "delay_minutes": 15
        })
    
    elif ("karachi" in origin.lower() and "hyderabad" in destination.lower()) or \
         ("hyderabad" in origin.lower() and "karachi" in destination.lower()):
        disruptions.append({
            "type": "traffic",
            "location": "M9 Motorway, near Nooriabad",
            "description": "Heavy traffic due to accident",
            "delay_minutes": 30
        })
    
    # Check if today is May 1 (International Workers' Day) for potential strikes
    if datetime.now().strftime("%m-%d") == "05-01":
        disruptions.append({
            "type": "strike",
            "location": "Major cities",
            "description": "Labor day demonstrations may affect urban routes",
            "delay_minutes": 20
        })
    
    return disruptions