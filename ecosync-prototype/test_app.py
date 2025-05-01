#!/usr/bin/env python3
"""
EcoSync Prototype Test Suite

This script tests the functionality of the EcoSync prototype application, including:
- Individual agents (weather, routing, strike, triage)
- Custom tools (weather_tools, route_tools)
- MCP servers
- Basic API endpoints

Run this script before starting the application to verify that everything is working correctly.
"""

import asyncio
import json
import os
import sys
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# Check if GEMINI_API_KEY is set
if not os.getenv('GEMINI_API_KEY'):
    print("⚠️  WARNING: GEMINI_API_KEY environment variable is not set.")
    print("    Agent tests will not work without an API key.")
    print("    Please set the GEMINI_API_KEY environment variable and try again.")
    print("    Continuing with other tests...\n")

# Add the project directory to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the necessary modules
try:
    # Import agent modules
    from app.custom_agents.weather_agent import run_weather_agent
    from app.custom_agents.routing_agent import run_routing_agent
    from app.custom_agents.strike_agent import run_strike_agent
    from app.custom_agents.triage_agent import run_triage_agent
    
    # Import custom tools
    from app.custom_tools.weather_tools import get_current_weather, predict_demand_from_weather
    from app.custom_tools.route_tools import optimize_route, check_for_disruptions
    
    print("✅ Successfully imported all required modules")
except ImportError as e:
    print(f"❌ Error importing modules: {str(e)}")
    print("   Make sure you have installed all requirements with:")
    print("   pip install -r requirements.txt")
    sys.exit(1)

# Create an async event loop for testing async functions
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

def test_weather_tools():
    """Test the weather tools"""
    print("\n🔍 Testing weather tools...")
    
    try:
        # Test get_current_weather
        print("  Testing get_current_weather()...")
        weather = get_current_weather("Lahore")
        print(f"  ✓ Current weather for Lahore: {weather.get('description', 'N/A')}, {weather.get('temperature', 'N/A')}°C")
        
        # Test predict_demand_from_weather
        print("  Testing predict_demand_from_weather()...")
        prediction = predict_demand_from_weather("Lahore", "Heater")
        print(f"  ✓ Prediction for Heaters in Lahore: {prediction.get('predicted_demand', 'N/A')} units")
        print(f"    Explanation: {prediction.get('explanation', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"  ❌ Error in weather tools: {str(e)}")
        return False

def test_route_tools():
    """Test the route tools"""
    print("\n🔍 Testing route tools...")
    
    try:
        # Test optimize_route
        print("  Testing optimize_route()...")
        route = optimize_route("Lahore", "Islamabad", True)
        print(f"  ✓ Optimized route: Emissions = {route.get('emissions_kg', 'N/A')} kg CO2")
        print(f"    Saved emissions: {route.get('emissions_saved_kg', 'N/A')} kg CO2")
        
        # Test check_for_disruptions
        print("  Testing check_for_disruptions()...")
        disruptions = check_for_disruptions("Lahore", "Islamabad")
        print(f"  ✓ Found {len(disruptions)} disruptions on route")
        for i, d in enumerate(disruptions, 1):
            print(f"    {i}. {d.get('type', 'Unknown')} at {d.get('location', 'Unknown')}")
        
        return True
    except Exception as e:
        print(f"  ❌ Error in route tools: {str(e)}")
        return False

async def test_agents():
    """Test all agents"""
    print("\n🔍 Testing agents...")
    
    if not os.getenv('GEMINI_API_KEY'):
        print("  ⚠️ Skipping agent tests due to missing API key")
        return False
    
    try:
        # Test weather agent
        print("  Testing weather agent...")
        weather_response = await run_weather_agent("What's the weather like in Lahore today?")
        print(f"  ✓ Weather agent response received ({len(weather_response)} chars)")
        
        # Test routing agent
        print("  Testing routing agent...")
        routing_response = await run_routing_agent("What's the best route from Lahore to Islamabad?")
        print(f"  ✓ Routing agent response received ({len(routing_response)} chars)")
        
        # Test strike agent
        print("  Testing strike agent...")
        strike_response = await run_strike_agent("Are there any protests in Lahore today?")
        print(f"  ✓ Strike agent response received ({len(strike_response)} chars)")
        
        # Test triage agent
        print("  Testing triage agent...")
        agent_type, triage_response = await run_triage_agent("I need to know about the weather in Karachi")
        print(f"  ✓ Triage agent identified query as '{agent_type}' type")
        print(f"    Triage message: {triage_response[:60]}...")
        
        return True
    except Exception as e:
        print(f"  ❌ Error in agents: {str(e)}")
        return False

def test_api_endpoints():
    """Test API endpoints using mock requests"""
    print("\n🔍 Testing API endpoints...")
    
    try:
        from app import app
        
        # Create a test client
        client = app.test_client()
        
        # Test forecast endpoint
        print("  Testing /api/forecast endpoint...")
        forecast_response = client.get('/api/forecast?city=Lahore&product=Heater')
        forecast_data = json.loads(forecast_response.data)
        print(f"  ✓ Forecast endpoint response status: {forecast_response.status_code}")
        print(f"    Units needed: {forecast_data.get('units_needed', 'N/A')}")
        
        # Test optimize endpoint
        print("  Testing /api/optimize endpoint...")
        optimize_response = client.get('/api/optimize?origin=Lahore&destination=Islamabad&eco_friendly=true')
        optimize_data = json.loads(optimize_response.data)
        print(f"  ✓ Optimize endpoint response status: {optimize_response.status_code}")
        print(f"    Emissions: {optimize_data.get('emissions_kg', 'N/A')} kg CO2")
        
        # Test dashboard endpoint
        print("  Testing /api/dashboard endpoint...")
        dashboard_response = client.get('/api/dashboard')
        dashboard_data = json.loads(dashboard_response.data)
        print(f"  ✓ Dashboard endpoint response status: {dashboard_response.status_code}")
        print(f"    Text: {dashboard_data.get('text', 'N/A')}")
        
        # Test chat endpoint with a POST request
        print("  Testing /api/chat endpoint...")
        chat_data = {'message': 'What\'s the weather in Lahore?'}
        chat_response = client.post('/api/chat', json=chat_data)
        chat_result = json.loads(chat_response.data)
        print(f"  ✓ Chat endpoint response status: {chat_response.status_code}")
        print(f"    Agent type: {chat_result.get('agent_type', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"  ❌ Error in API endpoints: {str(e)}")
        return False

def main():
    """Main function to run all tests"""
    print("🔬 Starting EcoSync Prototype Test Suite")
    print("=======================================")
    
    # Create a list to track test results
    results = []
    
    # Test weather tools
    results.append(("Weather Tools", test_weather_tools()))
    
    # Test route tools
    results.append(("Route Tools", test_route_tools()))
    
    # Test API endpoints
    results.append(("API Endpoints", test_api_endpoints()))
    
    # Test agents (async test)
    if os.getenv('GEMINI_API_KEY'):
        agent_result = loop.run_until_complete(test_agents())
        results.append(("Agents", agent_result))
    else:
        results.append(("Agents", "Skipped - No API key"))
    
    # Print summary
    print("\n📋 Test Results Summary")
    print("=====================")
    for name, result in results:
        if result is True:
            print(f"✅ {name}: PASS")
        elif result is False:
            print(f"❌ {name}: FAIL")
        else:
            print(f"⚠️ {name}: {result}")
    
    # Check if all tests passed
    all_passed = all(result is True for _, result in results if result != "Skipped - No API key")
    
    if all_passed:
        print("\n🎉 All tests PASSED! You can now run the application with:")
        print("   python run.py")
    else:
        print("\n⚠️ Some tests FAILED. Please fix the issues before running the application.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())