from flask import render_template, jsonify, request
from app import app
import json
import asyncio
import os
import time  # Added for timestamp generation

# Import agent modules
from app.agents.weather_agent import run_weather_agent
from app.agents.strike_agent import run_strike_agent
from app.agents.triage_agent import run_triage_agent
from app.agents.routing_agent import run_routing_agent

# Create a helper function to run async functions
def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

@app.route('/api/forecast', methods=['GET'])
def forecast():
    # Mock response until we implement the agent
    forecast_response = {
        "product": "Heater",
        "units_needed": 150,
        "explanation": "Based on cold weather forecast and previous sales trends"
    }
    return jsonify(forecast_response)

@app.route('/api/optimize', methods=['GET'])
def optimize():
    # Mock response until we implement the agent
    route_response = {
        "route_id": 2,
        "explanation": "Selected greener route due to GreenSync Mode",
        "emissions_kg": 15.0
    }
    return jsonify(route_response)

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    # Mock response until we implement the agent
    dashboard_response = {
        "text": "Your shipment is on an optimized green route",
        "story": "This route choice saved the equivalent of 5 trees!",
        "points": 7,
        "leaderboard": [
            {"driver": "Alice", "points": 50},
            {"driver": "Bob", "points": 40}
        ]
    }
    return jsonify(dashboard_response)

@app.route('/api/reward', methods=['GET'])
def reward():
    # Mock response until we implement the agent
    reward_response = {
        "points": 7,
        "message": "Earned 7 points for saving 15 kg CO2"
    }
    return jsonify(reward_response)

@app.route('/api/disrupt', methods=['POST'])
def disrupt():
    with open('data/traffic.json', 'w') as f:
        json.dump({"route_id": 1, "delay_min": 30}, f)
    return jsonify({"status": "Traffic jam added"})

@app.route('/api/agent/query', methods=['POST'])
def agent_query():
    """
    Process a user query through the triage agent and route to the appropriate specialized agent.
    """
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400
    
    query = data['query']
    
    try:
        # First, use the triage agent to determine which specialized agent to use
        agent_type, triage_message = run_async(run_triage_agent(query))
        
        # Based on the triage result, route to the appropriate agent
        if agent_type == 'weather':
            response = run_async(run_weather_agent(query))
            agent_name = "Weather Agent"
        elif agent_type == 'routing':
            response = run_async(run_routing_agent(query))
            agent_name = "Routing Agent"
        elif agent_type == 'strike':
            response = run_async(run_strike_agent(query))
            agent_name = "Strike Updates Agent"
        else:
            response = "I'm not sure how to process your query. Could you please clarify what information you're looking for? You can ask about weather conditions in a specific city, routes between locations, or about strikes/protests on a specific date."
            agent_name = "Triage Agent"
        
        return jsonify({
            "response": response,
            "agent": agent_name,
            "triage_message": triage_message
        })
    except Exception as e:
        app.logger.error(f"Error in agent query: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/agent/weather', methods=['POST'])
def agent_weather():
    """
    Process a weather query directly through the weather agent.
    """
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400
    
    query = data['query']
    
    try:
        response = run_async(run_weather_agent(query))
        return jsonify({"response": response})
    except Exception as e:
        app.logger.error(f"Error in weather agent: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/agent/strike', methods=['POST'])
def agent_strike():
    """
    Process a strike query directly through the strike agent.
    """
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400
    
    query = data['query']
    
    try:
        response = run_async(run_strike_agent(query))
        return jsonify({"response": response})
    except Exception as e:
        app.logger.error(f"Error in strike agent: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def handle_chat():
    """
    Process a chat message through the triage agent and route to the appropriate specialized agent.
    Returns both the response and which agent type provided the response.
    """
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "Missing 'message' in request body"}), 400
    
    message = data['message']
    
    try:
        # Use the triage agent to determine which specialized agent to use
        agent_type, triage_message = run_async(run_triage_agent(message))
        
        # Based on the triage result, route to the appropriate agent
        if agent_type == 'weather':
            response = run_async(run_weather_agent(message))
        elif agent_type == 'routing':
            response = run_async(run_routing_agent(message))
        elif agent_type == 'strike':
            response = run_async(run_strike_agent(message))
        else:
            # If the triage agent couldn't determine a specific agent, use its message
            response = triage_message
            agent_type = 'triage'
        
        return jsonify({
            "response": response,
            "agent_type": agent_type
        })
    except Exception as e:
        app.logger.error(f"Error in chat processing: {str(e)}")
        return jsonify({
            "response": "I'm sorry, I encountered an error processing your request. Please try again.",
            "agent_type": "triage"
        }), 500

@app.route('/api/shipment', methods=['POST'])
def process_shipment():
    """
    Process shipment data from the form and pass it to the triage agent.
    Returns a response with route optimization and sustainability suggestions.
    """
    data = request.json
    if not data:
        return jsonify({"error": "Missing shipment details in request body"}), 400
    
    try:
        # Create a natural language query from the shipment data
        origin = data.get('origin', 'unknown location')
        destination = data.get('destination', 'unknown location')
        cargo_type = data.get('cargo_type', 'goods')
        weight = data.get('weight', 'unknown weight')
        volume = data.get('volume', 'unknown volume')
        transport_method = data.get('transport_method', 'unknown method')
        priority = data.get('priority', 'standard')
        deadline = data.get('deadline', 'unspecified date')
        
        # Build special requirements string
        special_reqs = []
        if data.get('hazardous'):
            special_reqs.append('hazardous materials')
        if data.get('fragile'):
            special_reqs.append('fragile items')
        if data.get('eco_friendly'):
            special_reqs.append('eco-friendly routing')
        if data.get('insurance'):
            special_reqs.append('insurance required')
        
        special_requirements = ', '.join(special_reqs) if special_reqs else 'none'
        
        # Format temperature requirement
        temp_req = data.get('temperature', 'ambient')
        
        # Format notes
        notes = data.get('notes', '')
        notes_text = f" Additional notes: {notes}" if notes else ""
        
        # Create natural language query for the triage agent
        query = (f"I need to optimize a shipping route for {cargo_type} from {origin} to {destination} "
                f"using {transport_method} transport. The shipment weighs {weight}kg with volume {volume}m³. "
                f"Priority is {priority} with delivery deadline {deadline}. "
                f"Special requirements: {special_requirements}. Temperature requirements: {temp_req}.{notes_text} "
                f"Please provide route optimization considering weather conditions and potential strikes along the route.")
        
        # First, use the routing agent directly for shipment route optimization
        routing_response = run_async(run_routing_agent(
            f"Find optimal route from {origin} to {destination} for {transport_method} transport with {special_requirements}"
        ))
        
        # Store shipment data in a JSON file for future reference
        try:
            with open('data/shipment.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            app.logger.error(f"Error saving shipment data: {str(e)}")
        
        # Build a comprehensive response with the routing information
        response = {
            "response": routing_response,
            "agent_type": "routing",
            "shipment_id": f"SH-{int(time.time())}", # Generate a unique shipment ID
            "status": "Processing",
            "message": f"Your shipment from {origin} to {destination} has been received and is being optimized."
        }
        
        return jsonify(response)
    except Exception as e:
        app.logger.error(f"Error in shipment processing: {str(e)}")
        return jsonify({
            "response": "I'm sorry, I encountered an error processing your shipment details. Please verify your information and try again.",
            "agent_type": "triage",
            "status": "Error"
        }), 500

@app.route('/api/route', methods=['POST'])
def route_planning():
    """
    Process a route planning request through the intelligent routing agent.
    
    Expects a JSON body with:
    - origin: starting location
    - destination: ending location
    
    Returns routing information with real-time updates.
    """
    data = request.json
    if not data or 'origin' not in data or 'destination' not in data:
        return jsonify({"error": "Missing 'origin' or 'destination' in request body"}), 400
    
    origin = data['origin']
    destination = data['destination']
    
    # Additional parameters that might be passed
    transport_method = data.get('transport_method', '')
    special_requirements = []
    if data.get('eco_friendly'):
        special_requirements.append('eco-friendly')
    if data.get('hazardous'):
        special_requirements.append('hazardous materials')
    
    # Construct the query for the routing agent
    query = f"I want to go from {origin} to {destination}"
    if transport_method:
        query += f" using {transport_method}"
    if special_requirements:
        query += f" with {', '.join(special_requirements)} considerations"
    
    try:
        # Process the routing request asynchronously
        route_response = run_async(run_routing_agent(query))
        
        return jsonify({
            "response": route_response,
            "origin": origin,
            "destination": destination,
            "request_id": f"ROUTE-{int(time.time())}",
            "status": "success"
        })
    except Exception as e:
        app.logger.error(f"Error in route processing: {str(e)}")
        return jsonify({
            "error": "Failed to process routing request",
            "message": str(e)
        }), 500

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/agent')
def agent_ui():
    return render_template('agent.html')