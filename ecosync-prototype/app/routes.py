from flask import render_template, jsonify
from app import app
import json

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

@app.route('/')
def index():
    return render_template('dashboard.html') 