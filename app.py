from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
           template_folder='AIGenesis/templates',
           static_folder='AIGenesis/static')

# Dictionary to store available agents
agents = {}

# Import agent modules
from custom_agents import register_agents
register_agents(agents)

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html', agents=list(agents.keys()))

@app.route('/chat', methods=['POST'])
def chat():
    """Process a message and get a response from the selected agent"""
    data = request.json
    message = data.get('message', '')
    agent_name = data.get('agent', '')
    
    if not message:
        return jsonify({"error": "No message provided"}), 400
    
    if agent_name not in agents:
        return jsonify({"error": f"Agent '{agent_name}' not found"}), 404
    
    # Get response from the selected agent
    try:
        response = agents[agent_name].process_message(message)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)