# Smart Event Search with Weather Integration

A Python application that combines Exa search with National Weather Service data to provide intelligent, weather-aware event recommendations. Perfect for planning events based on current weather conditions!

## 🌟 Features

### 🔍 **Smart Event Search**

- **Weather-Aware Recommendations**: Automatically analyzes weather conditions for event planning
- **Indoor vs Outdoor Classification**: Intelligently categorizes events based on weather suitability
- **Event Categorization**: Groups events by type (Vintage, Food, Arts, Entertainment, etc.)
- **Confidence Scoring**: Provides confidence levels for weather-based recommendations

### 🌤️ **Weather Integration**

- **Real-time Weather Data**: Connects to National Weather Service via MCP
- **Current Conditions**: Temperature, humidity, wind speed, and weather conditions
- **Event Planning Analysis**: Determines if weather is suitable for outdoor events
- **Location Support**: Works with city names, boroughs, or exact coordinates

### 🎯 **Event Discovery**

- **Exa Search Integration**: Powerful web search for events using Smithery AI
- **Multiple Search Types**: Web search, company research, URL crawling, LinkedIn search
- **Deep Research**: Start comprehensive AI-powered research tasks
- **Flexible Queries**: Search for any type of event in any location

## 🚀 Quick Start

### 1. **Installation**

```bash
# Clone or download this repository
cd walter

# Create a virtual environment (recommended)
python3 -m venv exa_env
source exa_env/bin/activate  # On macOS/Linux
# or
exa_env\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. **Smart Event Search**

```bash
# Search for vintage events in NYC with weather analysis
python smart_event_cli.py search "vintage events" "nyc" 10

# Search for food festivals in Manhattan
python smart_event_cli.py search "food festivals" "manhattan" 5

# Search for art exhibitions in Brooklyn
python smart_event_cli.py search "art exhibitions" "brooklyn" 8
```

### 3. **Weather Information**

```bash
# Get current weather for NYC
python smart_event_cli.py weather "nyc"

# Get weather for specific coordinates
python smart_event_cli.py weather "40.7128,-74.0060"
```

## 🔐 Google Calendar Integration

The application now includes Google Calendar integration for event scheduling and conflict checking. Credentials are managed securely using environment variables.

### **Environment Setup**

Create a `config.env` file in your project root:

```bash
# Google Calendar API Credentials
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_PROJECT_ID=your_project_id_here
GOOGLE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
GOOGLE_TOKEN_URI=https://oauth2.googleapis.com/token
GOOGLE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
GOOGLE_REDIRECT_URI=http://localhost
```

### **Testing Calendar Integration**

```bash
# Test environment variable setup
python test_env_calendar.py

# Test natural language calendar CLI
python natural_calendar_cli.py "find me vintage markets tomorrow"
```

## 🗣️ Natural Language Calendar CLI

The natural language calendar CLI understands complex queries and integrates multiple services:

### **Natural Language Examples**

```bash
# Find vintage markets for tomorrow
python natural_calendar_cli.py "find me vintage markets tomorrow"

# Search with location and travel constraints
python natural_calendar_cli.py "I want vintage popup shops this weekend, starting from 162 East 82nd Street, max 30 min travel"

# Check for conflicts
python natural_calendar_cli.py "show me vintage festivals that conflict with my current events this weekend"
```

### **Features**

- **Natural Language Parsing**: Understands complex queries like "vintage markets this weekend"
- **Calendar Integration**: Checks availability and conflicts
- **Travel Time Analysis**: Considers your starting location and travel constraints
- **Interactive Scheduling**: Choose events and schedule them with smart time suggestions
- **Multi-Service Integration**: Combines Exa Search, Weather, Maps, and Google Calendar

## 🧠 Smart Event Search CLI

### **Search Command**

```bash
python smart_event_cli.py search <query> [location] [num_results]
```

**Examples:**

- `python smart_event_cli.py search "vintage events" "nyc" 10`
- `python smart_event_cli.py search "food festivals" "manhattan" 5`
- `python smart_event_cli.py search "art exhibitions" "brooklyn" 8`

### **Weather Command**

```bash
python smart_event_cli.py weather <location>
```

**Examples:**

- `python smart_event_cli.py weather "nyc"`
- `python smart_event_cli.py weather "manhattan"`
- `python smart_event_cli.py weather "40.7128,-74.0060"`

### **Location Options**

- **NYC Boroughs**: `nyc`, `manhattan`, `brooklyn`, `queens`, `bronx`, `staten island`
- **Coordinates**: Use exact coordinates like `"40.7128,-74.0060"`
- **City Names**: Use any city name for automatic coordinate lookup

## 🔧 Architecture

The system combines multiple MCP servers for comprehensive functionality:

```
Smart Event Search
├── Exa Search MCP (Smithery AI)
│   ├── Web search for events
│   ├── Company research
│   ├── URL crawling
│   └── LinkedIn search
├── National Weather Service MCP (Smithery AI)
│   ├── Current weather conditions
│   ├── Weather forecasts
│   ├── Hourly forecasts
│   └── Weather alerts
└── Smart Analysis Engine
    ├── Event classification
    ├── Weather analysis
    ├── Indoor/outdoor recommendations
    └── Confidence scoring
```

## 📊 Output Example

Here's what you get from a smart event search:

```
🔍 Smart Event Search
   Query: vintage events
   Location: nyc
   Results: 5
   🌤️ Including weather analysis...

✅ Search Complete!
📍 Location: nyc
   🌤️ Weather: 70°F (21°C), Clear
   💨 Wind: 5 mph
   💧 Humidity: 50%
🏠 Outdoor friendly: Yes
📊 Found 5 events

🎯 Event Recommendations:

1. Jazz Age Lawn Party 2025
   🏷️ Category: Arts & Culture
   🏠 Type: Outdoor
   💡 Recommendation: Great weather for outdoor events!
   🎯 Confidence: High
   📝 Notes: Weather: 70°F (21°C), Clear
   🔗 URL: https://example.com/event

📊 Summary:
   🏠 Indoor events: 0
   🌳 Outdoor events: 4
   ❓ Unknown type: 1

💡 Weather Advice: Great conditions for outdoor events!
```

## 🎨 Event Categories

The system automatically categorizes events:

- **Vintage/Antique**: Flea markets, vintage shows, antique fairs
- **Food & Dining**: Restaurants, cafes, food festivals, food trucks
- **Arts & Culture**: Museums, galleries, exhibitions, performances
- **Entertainment**: Concerts, shows, movies, performances
- **Fitness & Sports**: Gyms, yoga, sports, athletic activities
- **General**: Other events not fitting specific categories

## 🌤️ Weather Analysis

The weather analysis considers multiple factors:

- **Temperature**: Optimal range 40°F - 95°F (4°C - 35°C)
- **Conditions**: Rain, snow, storms, fog, haze
- **Wind Speed**: High winds (>20 mph) may affect outdoor events
- **Humidity**: High humidity (>80%) noted for comfort

## 🔌 MCP Integration

### **Exa Search MCP**

- **Server**: `https://server.smithery.ai/exa/mcp`
- **Tools**: `web_search_exa`, `company_research_exa`, `crawling_exa`, `linkedin_search_exa`

### **National Weather Service MCP**

- **Server**: `https://server.smithery.ai/@smithery-ai/national-weather-service/mcp`
- **Tools**: `get_current_weather`, `get_weather_forecast`, `get_hourly_forecast`, `get_weather_alerts`

## 📁 File Structure

```
walter/
├── smart_event_search.py      # Main smart search engine
├── smart_event_cli.py         # CLI for smart event search
├── weather_client.py          # Weather MCP client
├── exa_search_app.py         # Exa search MCP client
├── exa_cli.py                # Basic Exa search CLI
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## 🚀 Advanced Usage

### **Python API**

```python
from smart_event_search import SmartEventSearch
import asyncio

async def main():
    smart_search = SmartEventSearch()

    # Get weather-aware recommendations
    results = await smart_search.get_weather_aware_recommendations(
        "vintage events", "nyc", 10
    )

    if results["success"]:
        print(f"Found {results['total_results']} events")
        print(f"Weather: {results['weather_summary']}")
        print(f"Outdoor friendly: {results['outdoor_friendly']}")

        for rec in results["recommendations"]:
            print(f"- {rec['title']}: {rec['weather_recommendation']}")

asyncio.run(main())
```

### **Weather Analysis**

```python
from weather_client import WeatherClient

async def analyze_weather():
    client = WeatherClient()
    weather = await client.get_current_weather("40.7128,-74.0060")
    analysis = client.analyze_weather_for_events(weather["weather"])

    print(f"Outdoor friendly: {analysis['is_outdoor_friendly']}")
    print(f"Temperature: {analysis['weather_summary']['temperature']}")

asyncio.run(analyze_weather())
```

## 🛠️ Troubleshooting

### **Common Issues**

1. **Python Version**: Ensure Python 3.10+ for MCP compatibility
2. **Virtual Environment**: Activate your virtual environment before running
3. **Dependencies**: Install all requirements with `pip install -r requirements.txt`
4. **API Limits**: Be aware of Smithery AI's rate limits

### **Error Messages**

- `ModuleNotFoundError: No module named 'mcp'`: Install MCP library or check Python version
- `Connection failed`: Check internet connection and Smithery AI server status
- `Weather data unavailable`: Weather service may be temporarily unavailable

## 🔮 Future Enhancements

- **Multi-day Weather Analysis**: Consider weather forecasts for future events
- **Event Time Integration**: Match event times with hourly weather forecasts
- **Alternative Event Suggestions**: Recommend indoor alternatives for bad weather
- **Weather Alerts**: Include severe weather warnings in recommendations
- **Historical Weather Data**: Analyze weather patterns for recurring events

## 📄 License

This project is provided as-is for educational and development purposes.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application!

## 📞 Support

For issues related to:

- **This application**: Check the troubleshooting section
- **MCP library**: Refer to the [MCP documentation](https://modelcontextprotocol.io/)
- **Smithery AI**: Contact Smithery AI support for server-related issues

---

**🎉 Now you can plan events with confidence, knowing the weather conditions!**
