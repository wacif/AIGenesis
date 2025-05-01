#!/usr/bin/env python3
"""
Basic EcoSync Prototype Test

This script performs basic tests on EcoSync components to identify any issues.
"""

import sys
import os

# Add the project directory to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

print("Starting basic EcoSync tests...")

# Test 1: Import the route_tools module
try:
    print("Test 1: Importing route_tools module...")
    from app.custom_tools.route_tools import optimize_route, check_for_disruptions
    print("✅ Successfully imported route_tools")
except ImportError as e:
    print(f"❌ Error importing route_tools: {str(e)}")
    print("Stack trace:")
    import traceback
    traceback.print_exc()

# Test 2: Import the weather_tools module
try:
    print("\nTest 2: Importing weather_tools module...")
    from app.custom_tools.weather_tools import get_current_weather, predict_demand_from_weather
    print("✅ Successfully imported weather_tools")
except ImportError as e:
    print(f"❌ Error importing weather_tools: {str(e)}")
    print("Stack trace:")
    import traceback
    traceback.print_exc()

# Test 3: Import all agent modules
try:
    print("\nTest 3: Importing agent modules...")
    from app.custom_agents.weather_agent import run_weather_agent
    from app.custom_agents.routing_agent import run_routing_agent
    from app.custom_agents.strike_agent import run_strike_agent
    from app.custom_agents.triage_agent import run_triage_agent
    print("✅ Successfully imported agent modules")
except ImportError as e:
    print(f"❌ Error importing agent modules: {str(e)}")
    print("Stack trace:")
    import traceback
    traceback.print_exc()