### Hackathon Prototype: EcoSync Logistics Agent (Python, OpenAI Agents SDK, No Blockchain)

#### 1. Prototype Scope
To balance ease and competitiveness, the prototype includes:
- **Four Agents** (using OpenAI Agents SDK):
  - **Routing Agent**: Optimizes routes in real-time, incorporating **Real-Time Routing Optimization** and **Exception Management** for traffic/weather disruptions.
  - **Collaboration Agent**: Generates an emotion-aware dashboard with **Sustainability Storytelling**, adapting to user stress.
  - **Reward Agent**: Tracks eco-friendly points in-memory, tied to **GreenSync Mode**.
  - **Forecasting Agent**: Implements **Dynamic Demand Forecasting** to predict stock needs, influencing routing decisions.
- **Key Features**:
  - **Real-Time Route Optimization**: Reroutes shipments using mock traffic/weather data, with exception handling for delays.
  - **GreenSync Mode**: Prioritizes low-emission routes, calculates carbon savings.
  - **Dynamic Demand Forecasting**: Updates stock predictions based on mock sales/weather data.
  - **Emotion-Aware Dashboard**: Adapts UI for high-stress users, includes storytelling (e.g., “This route saved 10 trees!”).
  - **Reward System**: Assigns points for green routes, displayed on a leaderboard.
  - **3D Route Visualization**: Uses Plotly for AR-like visuals.
  - **Disruption Simulator**: Button to trigger mock disruptions (e.g., traffic jam).
- **Demo Scenario**:
  - Simulate a shipment from Warehouse A to Customer B, with a mock sales spike (from Forecasting Agent) and traffic jam (Exception Management).
  - Show the Routing Agent rerouting in GreenSync Mode, Collaboration Agent updating the dashboard with storytelling, and Reward Agent assigning points.
  - Display 3D visuals, leaderboard, and metrics (e.g., “15% CO2 saved, 5 points earned”).

**Notes on Suggested Features**:
- **Autonomous Procurement Agents**: Excluded from the prototype due to hackathon time constraints (requires complex supplier negotiation logic). Mentioned in the presentation as a future feature.
- **Smart Warehouses**: Simplified to inventory insights from the Forecasting Agent, as robot coordination is too complex for a 1-3 day build. Future scope noted in presentation.

#### 2. Why It Wins
- **Innovation**: Combines OpenAI Agents SDK for autonomous routing, forecasting, and exception handling, a cutting-edge logistics application.
- **Impact**: Reduces costs/emissions (e.g., 15% CO2 savings in demo) and improves resilience.
- **Wow Factor**: 3D visuals, storytelling, leaderboard, and disruption simulator captivate judges.
- **Ease**: Mock data and Python (Flask, Plotly) ensure a fast build.
- **Polish**: Sleek dashboard with metrics (cost, emissions, points) and multimedia storytelling (aligning with your interest).

#### 3. Mock Data Strategy
Mock data (JSON) simplifies development:
- **Supply Chain**:
  - 5 suppliers, 3 warehouses, 10 routes (graph nodes/edges).
  - Mock IoT: GPS coordinates, shipment statuses.
- **External Data**:
  - Mock traffic: Delays on Route 1.
  - Mock weather: Storm on Route 2.
  - Mock X posts: “Traffic jam on Route 1.”
- **Demand Data**:
  - Mock sales: Daily units sold per product.
  - Mock weather: Temperature affecting demand (e.g., cold weather boosts heater sales).
- **Sustainability**:
  - Emissions: 0.5 kg CO2/km per route.
  - Supplier ESG scores: 80/100 for green suppliers.
- **Human Inputs**:
  - Mock feedback: “Urgent delivery needed.”
  - Mock stress: “High” during disruption.
- **Rewards**:
  - Mock points: 1 point per 2 kg CO2 saved, stored in-memory.
  - Mock leaderboard: Top 5 drivers by points.

#### 4. Agentic AI with OpenAI Agents SDK
The OpenAI Agents SDK enables multi-agent workflows with:
- **Agents**: LLMs with instructions and tools.
- **Handoffs**: Task delegation between agents.
- **Tools**: Python functions for actions (e.g., routing, forecasting).
- **Tracing**: Debugging via OpenAI Dashboard.

We’ll use GPT-4o for reasoning, keeping it lightweight.

##### Agentic Framework
- **Multi-Agent System**: Four agents (Routing, Collaboration, Reward, Forecasting) coordinated via SDK’s `Runner`.
- **Autonomy**: Agents process inputs and act independently.
- **Adaptability**: Handoffs handle disruptions and demand changes.
- **Collaboration**: Collaboration Agent aligns outputs with human needs.
- **Transparency**: SDK tracing and GPT-4o explanations ensure XAI.

##### Agent Details
1. **Routing Agent**:
   - **Perception**: Reads mock routes/traffic/weather via tools.
   - **Reasoning**: Optimizes routes for emissions (GreenSync Mode), handles exceptions (e.g., delays), using GPT-4o.
   - **Action**: Outputs route ID, carbon savings, and exception alerts.
   - **SDK Role**: Tool-calling for routing, handoff to Collaboration/Forecasting.

2. **Collaboration Agent**:
   - **Perception**: Reads mock user inputs/stress and route data.
   - **Reasoning**: Generates emotion-aware dashboard with storytelling (e.g., “Saved 10 trees!”).
   - **Action**: Outputs text, visuals, and leaderboard data.
   - **SDK Role**: Processes handoffs, outputs structured data.

3. **Reward Agent**:
   - **Perception**: Monitors green routes.
   - **Reasoning**: Calculates points (1 per 2 kg CO2 saved).
   - **Action**: Updates in-memory leaderboard.
   - **SDK Role**: Handles reward logic, handoffs to dashboard.

4. **Forecasting Agent**:
   - **Perception**: Reads mock sales/weather data.
   - **Reasoning**: Predicts stock needs, influences routing priorities.
   - **Action**: Outputs demand forecasts.
   - **SDK Role**: Tool-calling for forecasting, handoff to Routing.

##### SDK Integration
- **Setup**: `pip install openai-agents`.
- **Tools**: Functions for routing, user inputs, forecasting, and rewards.
- **Handoffs**: Forecasting → Routing → Collaboration → Reward.
- **Tracing**: OpenAI Dashboard for debugging.
- **API Key**: Store in `.env`.

#### 5. Technical Implementation
##### Tech Stack
- **Backend**: Python, Flask, `openai-agents`.
- **Frontend**: Flask templates, Plotly for 3D visuals.
- **Data**: JSON for mock data.
- **AI**: OpenAI Agents SDK with GPT-4o.
- **Rewards**: In-memory dictionary.

##### Prototype Structure
```
/ecosync-prototype
├── /app
│   ├── __init__.py
│   ├── routes.py
│   ├── agents/
│   │   ├── routing.py
│   │   ├── collaboration.py
│   │   ├── reward.py
│   │   ├── forecasting.py
├── /data
│   ├── routes.json
│   ├── traffic.json
│   ├── weather.json
│   ├── user.json
│   ├── sales.json
├── /templates
│   ├── dashboard.html
├── requirements.txt
├── run.py
```

##### Mock Data (data/routes.json)
```json
[
  {
    "id": 1,
    "from": "Warehouse A",
    "to": "Customer B",
    "distance_km": 100,
    "time_min": 60,
    "cost_usd": 50,
    "emissions_kg": 20
  },
  {
    "id": 2,
    "from": "Warehouse A",
    "to": "Customer B",
    "distance_km": 120,
    "time_min": 70,
    "cost_usd": 45,
    "emissions_kg": 15
  }
]
```

##### Mock Data (data/sales.json)
```json
[
  {
    "product": "Heater",
    "date": "2025-04-26",
    "units_sold": 100,
    "weather": "cold"
  },
  {
    "product": "Heater",
    "date": "2025-04-27",
    "units_sold": 120,
    "weather": "cold"
  }
]
```

##### Key Code Snippets
1. **Main App (app/routes.py)**:
   ```python
   from flask import Flask, render_template, jsonify
   from app.agents.routing import routing_agent
   from app.agents.collaboration import collaboration_agent
   from app.agents.reward import reward_agent
   from app.agents.forecasting import forecasting_agent
   from agents import Runner
   import json

   app = Flask(__name__)

   @app.route('/api/forecast', methods=['GET'])
   async def forecast():
       result = await Runner.run(forecasting_agent, input="Predict stock needs")
       return jsonify(result.final_output.dict())

   @app.route('/api/optimize', methods=['GET'])
   async def optimize():
       forecast = (await Runner.run(forecasting_agent, input="Predict stock needs")).final_output
       result = await Runner.run(routing_agent, input=f"Optimize route in GreenSync Mode with forecast: {forecast.dict()}")
       return jsonify(result.final_output.dict())

   @app.route('/api/dashboard', methods=['GET'])
   async def dashboard():
       route = (await Runner.run(routing_agent, input="Optimize route in GreenSync Mode")).final_output
       result = await Runner.run(collaboration_agent, input=f"Generate dashboard for route: {route.dict()}, stress: high")
       return jsonify(result.final_output.dict())

   @app.route('/api/reward', methods=['GET'])
   async def reward():
       route = (await Runner.run(routing_agent, input="Optimize route in GreenSync Mode")).final_output
       result = await Runner.run(reward_agent, input=f"Issue points for route: {route.dict()}")
       return jsonify(result.final_output.dict())

   @app.route('/api/disrupt', methods=['POST'])
   def disrupt():
       with open('data/traffic.json', 'w') as f:
           json.dump({"route_id": 1, "delay_min": 30}, f)
       return jsonify({"status": "Traffic jam added"})

   @app.route('/')
   def index():
       return render_template('dashboard.html')
   ```

2. **Routing Agent (app/agents/routing.py)**:
   ```python
   from agents import Agent, function_tool
   from pydantic import BaseModel
   import json

   class RouteOutput(BaseModel):
       route_id: int
       explanation: str
       emissions_kg: float

   @function_tool
   def get_routes():
       with open('data/routes.json', 'r') as f:
           return json.load(f)

   @function_tool
   def get_traffic():
       try:
           with open('data/traffic.json', 'r') as f:
               return json.load(f)
       except FileNotFoundError:
           return {}

   routing_agent = Agent(
       name="RoutingAgent",
       instructions="Optimize routes for emissions in GreenSync Mode, handle traffic delays. Use get_routes and get_traffic tools.",
       tools=[get_routes, get_traffic],
       output_type=RouteOutput
   )
   ```

3. **Collaboration Agent (app/agents/collaboration.py)**:
   ```python
   from agents import Agent, function_tool
   from pydantic import BaseModel
   import json

   class DashboardOutput(BaseModel):
       text: str
       story: str
       points: int

   @function_tool
   def get_user():
       with open('data/user.json', 'r') as f:
           return json.load(f)

   @function_tool
   def get_leaderboard():
       return [
           {"driver": "Alice", "points": 50},
           {"driver": "Bob", "points": 40}
       ]

   collaboration_agent = Agent(
       name="CollaborationAgent",
       instructions="Generate dashboard text and sustainability story (e.g., 'Saved 10 trees') for high-stress users. Include leaderboard. Use get_user and get_leaderboard tools.",
       tools=[get_user, get_leaderboard],
       output_type=DashboardOutput
   )
   ```

4. **Reward Agent (app/agents/reward.py)**:
   ```python
   from agents import Agent, function_tool
   from pydantic import BaseModel

   class RewardOutput(BaseModel):
       points: int
       message: str

   @function_tool
   def issue_points(emissions_kg: float):
       points = int(emissions_kg / 2)
       return {"points": points, "message": f"Earned {points} points for saving {emissions_kg} kg CO2"}

   reward_agent = Agent(
       name="RewardAgent",
       instructions="Issue points for emissions saved (1 point per 2 kg). Use issue_points tool.",
       tools=[issue_points],
       output_type=RewardOutput
   )
   ```

5. **Forecasting Agent (app/agents/forecasting.py)**:
   ```python
   from agents import Agent, function_tool
   from pydantic import BaseModel
   import json

   class ForecastOutput(BaseModel):
       product: str
       units_needed: int
       explanation: str

   @function_tool
   def get_sales():
       with open('data/sales.json', 'r') as f:
           return json.load(f)

   @function_tool
   def get_weather():
       return {"date": "2025-04-27", "condition": "cold"}

   forecasting_agent = Agent(
       name="ForecastingAgent",
       instructions="Predict stock needs based on sales and weather. Use get_sales and get_weather tools.",
       tools=[get_sales, get_weather],
       output_type=ForecastOutput
   )
   ```

6. **Dashboard Template (templates/dashboard.html)**:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <title>EcoSync Dashboard</title>
       <script src="https://cdn.tailwindcss.com"></script>
       <script src="https://cdn.plotly.io/plotly-2.14.0.min.js"></script>
   </head>
   <body class="bg-gray-100 p-4">
       <h1 class="text-2xl font-bold">EcoSync Dashboard</h1>
       <button id="disrupt" class="bg-red-500 text-white px-4 py-2 rounded">Simulate Traffic Jam</button>
       <div id="dashboard-text" class="my-4"></div>
       <div id="story" class="my-4 text-green-600"></div>
       <div id="route-visual" class="w-full h-64"></div>
       <p id="carbon-saved"></p>
       <p id="points-earned"></p>
       <div id="leaderboard" class="my-4">
           <h2 class="text-xl">Leaderboard</h2>
           <ul id="leaderboard-list"></ul>
       </div>

       <script>
           function updateDashboard() {
               fetch('/api/forecast').then(res => res.json()).then(forecast => {
                   fetch('/api/optimize').then(res => res.json()).then(route => {
                       fetch('/api/dashboard').then(res => res.json()).then(dashboard => {
                           fetch('/api/reward').then(res => res.json()).then(reward => {
                               document.getElementById('dashboard-text').innerText = dashboard.text || 'Loading...';
                               document.getElementById('story').innerText = dashboard.story || '';
                               document.getElementById('carbon-saved').innerText = `Carbon Saved: ${route.emissions_kg || 0} kg`;
                               document.getElementById('points-earned').innerText = `Points Earned: ${reward.points || 0}`;
                               document.getElementById('leaderboard-list').innerHTML = dashboard.leaderboard?.map(d => `<li>${d.driver}: ${d.points}</li>`).join('') || '';

                               // 3D route visualization
                               const trace = {
                                   x: [0, 100], y: [0, 50], z: [0, 10],
                                   type: 'scatter3d',
                                   mode: 'lines+markers',
                                   marker: { size: 5, color: 'green' }
                               };
                               Plotly.newPlot('route-visual', [trace], {
                                   scene: { xaxis: { title: 'X' }, yaxis: { title: 'Y' }, zaxis: { title: 'Z' } }
                               });
                           });
                       });
                   });
               });
           }
           updateDashboard();
           document.getElementById('disrupt').addEventListener('click', () => {
               fetch('/api/disrupt', { method: 'POST' }).then(updateDashboard);
           });
       </script>
   </body>
   </html>
   ```

7. **Requirements (requirements.txt)**:
   ```
   flask==2.0.1
   openai-agents==0.1.0
   plotly==5.10.0
   pydantic==1.10.7
   ```

##### Development Timeline (1-3 Days)
- **Day 1**:
  - Set up Flask, mock JSON data, and OpenAI Agents SDK.
  - Implement Routing and Forecasting Agents.
  - Create basic dashboard with Plotly.
- **Day 2**:
  - Build Collaboration and Reward Agents.
  - Add disruption simulator and leaderboard.
  - Test routing, forecasting, and visuals.
- **Day 3**:
  - Polish dashboard with storytelling and Tailwind CSS.
  - Simulate demo scenario (rerouting, points).
  - Prepare presentation.

#### 6. Additional Functionalities (Refined)
Incorporating your suggestions, here are the prioritized features (beyond those included):
1. **Predictive Delay Alerts**:
   - **What**: Routing Agent predicts delays using mock X post sentiment (e.g., “Traffic reported”).
   - **Why**: Enhances Exception Management, shows SDK’s NLP power.
   - **How**: Add a tool to parse mock X posts; integrate with Routing Agent.
   - **Effort**: 3 hours.
   - **Impact**: Medium.
2. **Voice Input Mock**:
   - **What**: Simulate voice commands (e.g., “Show green routes”) via text inputs.
   - **Why**: Adds interactivity, mimics Grok 3’s voice mode.
   - **How**: Add form input to dashboard; process with Collaboration Agent.
   - **Effort**: 3 hours.
   - **Impact**: Medium.
3. **Healthcare Logistics Teaser**:
   - **What**: Mock a vaccine delivery scenario in the presentation.
   - **Why**: Shows cross-industry potential.
   - **How**: Add slide and mock JSON for vaccine routes.
   - **Effort**: 1 hour.
   - **Impact**: High.

**Excluded Suggestions (for Presentation)**:
- **Autonomous Procurement Agents**: “Future scope: AI agents will negotiate supplier contracts autonomously, optimizing for price and ESG scores.”
- **Smart Warehouses**: “Future vision: Coordinate warehouse robots for picking and audits, integrated with EcoSync’s forecasting.”

#### 7. Presentation Strategy
- **Demo Flow**:
  - Pitch (30 seconds): “EcoSync leverages OpenAI’s Agents SDK to optimize logistics, forecasting demand, and saving emissions with autonomous AI.”
  - Simulate a sales spike and traffic jam; show rerouting, dashboard with storytelling, and leaderboard.
  - Click disruption button to highlight Exception Management.
  - Show metrics: “15% CO2 saved, 5 points earned.”
- **Slides**:
  - **Problem**: Logistics inefficiencies, emissions, disruptions.
  - **Solution**: Agentic AI with forecasting, routing, and collaboration.
  - **Tech**: Python, Flask, Plotly, OpenAI Agents SDK.
  - **Demo**: Live rerouting, storytelling, leaderboard.
  - **Impact**: 20% cost reduction, 15% CO2 savings (simulated).
  - **Future**: Procurement agents, smart warehouses, blockchain (e.g., Solana).
- **Judges’ Questions**:
  - **Tech**: “OpenAI Agents SDK enables autonomous routing and forecasting with tool-calling.”
  - **Scalability**: “Extensible to SAP, Oracle, and blockchain like Solana.”
  - **Impact**: “15% emission reduction, gamified points drive adoption.”

#### 8. Blockchain in Presentation
- **Mention**: “EcoSync is ready for blockchain integration with Solana, offering 65,000 TPS and $0.00025 fees for scalable, transparent rewards.”
- **Why**: Shows vision without hackathon complexity.
- **Slide**: “Future Vision: Solana for eco-friendly rewards, aligning with ESG goals.”

---

```python
```python
# EcoSync Logistics Agent Prototype
# Hackathon demo with mock data, OpenAI Agents SDK, no blockchain
# Directory: /ecosync-prototype

# app/__init__.py
from flask import Flask

app = Flask(__name__)
from app import routes

# app/routes.py
from flask import Flask, render_template, jsonify
from app.agents.routing import routing_agent
from app.agents.collaboration import collaboration_agent
from app.agents.reward import reward_agent
from app.agents.forecasting import forecasting_agent
from agents import Runner
import json

app = Flask(__name__)

@app.route('/api/forecast', methods=['GET'])
async def forecast():
    result = await Runner.run(forecasting_agent, input="Predict stock needs")
    return jsonify(result.final_output.dict())

@app.route('/api/optimize', methods=['GET'])
async def optimize():
    forecast = (await Runner.run(forecasting_agent, input="Predict stock needs")).final_output
    result = await Runner.run(routing_agent, input=f"Optimize route in GreenSync Mode with forecast: {forecast.dict()}")
    return jsonify(result.final_output.dict())

@app.route('/api/dashboard', methods=['GET'])
async def dashboard():
    route = (await Runner.run(routing_agent, input="Optimize route in GreenSync Mode")).final_output
    result = await Runner.run(collaboration_agent, input=f"Generate dashboard for route: {route.dict()}, stress: high")
    return jsonify(result.final_output.dict())

@app.route('/api/reward', methods=['GET'])
async def reward():
    route = (await Runner.run(routing_agent, input="Optimize route in GreenSync Mode")).final_output
    result = await Runner.run(reward_agent, input=f"Issue points for route: {route.dict()}")
    return jsonify(result.final_output.dict())

@app.route('/api/disrupt', methods=['POST'])
def disrupt():
    with open('data/traffic.json', 'w') as f:
        json.dump({"route_id": 1, "delay_min": 30}, f)
    return jsonify({"status": "Traffic jam added"})

@app.route('/')
def index():
    return render_template('dashboard.html')

# app/agents/routing.py
from agents import Agent, function_tool
from pydantic import BaseModel
import json

class RouteOutput(BaseModel):
    route_id: int
    explanation: str
    emissions_kg: float

@function_tool
def get_routes():
    with open('data/routes.json', 'r') as f:
        return json.load(f)

@function_tool
def get_traffic():
    try:
        with open('data/traffic.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

routing_agent = Agent(
    name="RoutingAgent",
    instructions="Optimize routes for emissions in GreenSync Mode, handle traffic delays. Use get_routes and get_traffic tools.",
    tools=[get_routes, get_traffic],
    output_type=RouteOutput
)

# app/agents/collaboration.py
from agents import Agent, function_tool
from pydantic import BaseModel
import json

class DashboardOutput(BaseModel):
    text: str
    story: str
    points: int
    leaderboard: list

@function_tool
def get_user():
    with open('data/user.json', 'r') as f:
        return json.load(f)

@function_tool
def get_leaderboard():
    return [
        {"driver": "Alice", "points": 50},
        {"driver": "Bob", "points": 40}
    ]

collaboration_agent = Agent(
    name="CollaborationAgent",
    instructions="Generate dashboard text and sustainability story (e.g., 'Saved 10 trees') for high-stress users. Include leaderboard. Use get_user and get_leaderboard tools.",
    tools=[get_user, get_leaderboard],
    output_type=DashboardOutput
)

# app/agents/reward.py
from agents import Agent, function_tool
from pydantic import BaseModel

class RewardOutput(BaseModel):
    points: int
    message: str

@function_tool
def issue_points(emissions_kg: float):
    points = int(emissions_kg / 2)
    return {"points": points, "message": f"Earned {points} points for saving {emissions_kg} kg CO2"}

reward_agent = Agent(
    name="RewardAgent",
    instructions="Issue points for emissions saved (1 point per 2 kg). Use issue_points tool.",
    tools=[issue_points],
    output_type=RewardOutput
)

# app/agents/forecasting.py
from agents import Agent, function_tool
from pydantic import BaseModel
import json

class ForecastOutput(BaseModel):
    product: str
    units_needed: int
    explanation: str

@function_tool
def get_sales():
    with open('data/sales.json', 'r') as f:
        return json.load(f)

@function_tool
def get_weather():
    return {"date": "2025-04-27", "condition": "cold"}

forecasting_agent = Agent(
    name="ForecastingAgent",
    instructions="Predict stock needs based on sales and weather. Use get_sales and get_weather tools.",
    tools=[get_sales, get_weather],
    output_type=ForecastOutput
)

# run.py
from app import app

if __name__ == '__main__':
    app.run(debug=True)

# data/routes.json
[
  {
    "id": 1,
    "from": "Warehouse A",
    "to": "Customer B",
    "distance_km": 100,
    "time_min": 60,
    "cost_usd": 50,
    "emissions_kg": 20
  },
  {
    "id": 2,
    "from": "Warehouse A",
    "to": "Customer B",
    "distance_km": 120,
    "time_min": 70,
    "cost_usd": 45,
    "emissions_kg": 15
  }
]

# data/user.json
{
  "role": "logistics_manager",
  "stress": "high",
  "feedback": "urgent delivery needed"
}

# data/traffic.json
{
  "route_id": 1,
  "delay_min": 0
}

# data/sales.json
[
  {
    "product": "Heater",
    "date": "2025-04-26",
    "units_sold": 100,
    "weather": "cold"
  },
  {
    "product": "Heater",
    "date": "2025-04-27",
    "units_sold": 120,
    "weather": "cold"
  }
]

# templates/dashboard.html
<!DOCTYPE html>
<html>
<head>
    <title>EcoSync Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.plotly.io/plotly-2.14.0.min.js"></script>
</head>
<body class="bg-gray-100 p-4">
    <h1 class="text-2xl font-bold">EcoSync Dashboard</h1>
    <button id="disrupt" class="bg-red-500 text-white px-4 py-2 rounded">Simulate Traffic Jam</button>
    <div id="dashboard-text" class="my-4"></div>
    <div id="story" class="my-4 text-green-600"></div>
    <div id="route-visual" class="w-full h-64"></div>
    <p id="carbon-saved"></p>
    <p id="points-earned"></p>
    <div id="leaderboard" class="my-4">
        <h2 class="text-xl">Leaderboard</h2>
        <ul id="leaderboard-list"></ul>
    </div>

    <script>
        function updateDashboard() {
            fetch('/api/forecast').then(res => res.json()).then(forecast => {
                fetch('/api/optimize').then(res => res.json()).then(route => {
                    fetch('/api/dashboard').then(res => res.json()).then(dashboard => {
                        fetch('/api/reward').then(res => res.json()).then(reward => {
                            document.getElementById('dashboard-text').innerText = dashboard.text || 'Loading...';
                            document.getElementById('story').innerText = dashboard.story || '';
                            document.getElementById('carbon-saved').innerText = `Carbon Saved: ${route.emissions_kg || 0} kg`;
                            document.getElementById('points-earned').innerText = `Points Earned: ${reward.points || 0}`;
                            document.getElementById('leaderboard-list').innerHTML = dashboard.leaderboard?.map(d => `<li>${d.driver}: ${d.points}</li>`).join('') || '';

                            // 3D route visualization
                            const trace = {
                                x: [0, 100], y: [0, 50], z: [0, 10],
                                type: 'scatter3d',
                                mode: 'lines+markers',
                                marker: { size: 5, color: 'green' }
                            };
                            Plotly.newPlot('route-visual', [trace], {
                                scene: { xaxis: { title: 'X' }, yaxis: { title: 'Y' }, zaxis: { title: 'Z' } }
                            });
                        });
                    });
                });
            });
        }
        updateDashboard();
        document.getElementById('disrupt').addEventListener('click', () => {
            fetch('/api/disrupt', { method: 'POST' }).then(updateDashboard);
        });
    </script>
</body>
</html>

# requirements.txt
flask==2.0.1
openai-agents==0.1.0
plotly==5.10.0
pydantic==1.10.7
```

```
