from flask import render_template, jsonify, request
from app import app
import json
import asyncio
import os

# Import agent modules
from app.agents.weather_agent import run_weather_agent
from app.agents.strike_agent import run_strike_agent
from app.agents.triage_agent import run_triage_agent

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
        elif agent_type == 'strike':
            response = run_async(run_strike_agent(query))
            agent_name = "Strike Agent"
        else:
            response = "I'm not sure how to process your query. Could you please clarify what information you're looking for? You can ask about weather conditions in a specific city or about strikes/protests on a specific date."
            agent_name = "Triage Agent"
        
        return jsonify({
            "response": response,
            "agent": agent_name,
            "triage_message": triage_message
        })
    except Exception as e:
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

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/agent')
def agent_ui():
    return render_template('agent.html')