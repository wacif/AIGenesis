"""
Weather Tools for EcoSync
This module provides utility functions for weather forecasting and analysis.
"""
import json
import os
import requests
from datetime import datetime, timedelta

def get_current_weather(city: str) -> dict:
    """
    Gets current weather information for a city.
    
    Args:
        city: The name of the city to get weather for
        
    Returns:
        A dictionary containing weather information
    """
    try:
        # Use wttr.in API for weather data
        endpoint = "https://wttr.in"
        response = requests.get(f"{endpoint}/{city}?format=j1")
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract relevant information
            current = data["current_condition"][0]
            
            return {
                "city": city,
                "temperature_c": current["temp_C"],
                "temperature_f": current["temp_F"],
                "condition": current["weatherDesc"][0]["value"],
                "humidity": current["humidity"],
                "wind_speed_kmph": current["windspeedKmph"],
                "wind_direction": current["winddir16Point"],
                "precipitation_mm": current["precipMM"],
                "visibility": current["visibility"],
                "pressure": current["pressure"],
                "timestamp": datetime.now().isoformat()
            }
        else:
            # Return mock data as fallback
            return generate_mock_weather(city)
    except Exception as e:
        print(f"Error fetching weather data: {str(e)}")
        # Return mock data on error
        return generate_mock_weather(city)

def generate_mock_weather(city: str) -> dict:
    """
    Generates mock weather data for a city when API is unavailable.
    
    Args:
        city: The name of the city to generate weather for
        
    Returns:
        A dictionary containing mock weather information
    """
    # Create deterministic but different weather for different cities
    city_hash = sum(ord(c) for c in city.lower())
    
    # Use the hash to create variations in temperature
    temp_base = 25  # Base temperature in Celsius
    temp_variation = city_hash % 15 - 7  # -7 to +7 variation
    
    # Create mock weather data
    conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Heavy Rain"]
    condition_index = city_hash % len(conditions)
    
    return {
        "city": city,
        "temperature_c": str(temp_base + temp_variation),
        "temperature_f": str(int((temp_base + temp_variation) * 9/5 + 32)),
        "condition": conditions[condition_index],
        "humidity": str(60 + city_hash % 30),
        "wind_speed_kmph": str(5 + city_hash % 20),
        "wind_direction": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"][city_hash % 8],
        "precipitation_mm": "0" if condition_index < 3 else str((condition_index - 2) * 2),
        "visibility": str(10 - (2 if condition_index > 2 else 0)),
        "pressure": str(1010 + city_hash % 20),
        "timestamp": datetime.now().isoformat(),
        "is_mock_data": True
    }

def predict_demand_from_weather(city: str, product_category: str) -> dict:
    """
    Predicts product demand based on weather conditions.
    
    Args:
        city: The city to predict demand for
        product_category: The category of product
        
    Returns:
        A dictionary with demand prediction information
    """
    # Get weather data for the city
    weather = get_current_weather(city)
    
    # Convert temperature to number for calculations
    temp_c = float(weather["temperature_c"])
    
    # Define product categories and their demand factors based on temperature
    demand_factors = {
        "heaters": max(0, (15 - temp_c) / 10),  # Higher demand in cold weather
        "coolers": max(0, (temp_c - 25) / 10),  # Higher demand in hot weather
        "umbrellas": 0.8 if "rain" in weather["condition"].lower() else 0.2,  # Higher in rain
        "sunglasses": 0.8 if "sunny" in weather["condition"].lower() else 0.3,  # Higher in sun
        "beverages": min(1.0, max(0.3, (temp_c - 15) / 15))  # Higher in hot weather
    }
    
    # Default factor if category not in our list
    demand_factor = demand_factors.get(product_category.lower(), 0.5)
    
    # Calculate base demand (1-100 scale)
    base_demand = 50
    
    # Apply weather factor
    predicted_demand = int(base_demand * (0.5 + demand_factor))
    
    # Clamp to reasonable range
    predicted_demand = max(10, min(100, predicted_demand))
    
    return {
        "city": city,
        "product_category": product_category,
        "predicted_demand": predicted_demand,
        "demand_level": "High" if predicted_demand > 70 else "Medium" if predicted_demand > 40 else "Low",
        "weather_condition": weather["condition"],
        "temperature_c": weather["temperature_c"],
        "explanation": f"Based on the current {'high' if temp_c > 25 else 'low' if temp_c < 15 else 'moderate'} temperature of {temp_c}°C and {weather['condition']} conditions",
        "timestamp": datetime.now().isoformat()
    }