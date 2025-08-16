#!/usr/bin/env python3
"""
Weather Client for National Weather Service MCP

This client connects to the National Weather Service MCP server via Smithery AI
to get weather information for event planning.
"""

import asyncio
import json
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import mcp
from mcp.client.streamable_http import streamablehttp_client

class WeatherClient:
    """
    Client for interacting with National Weather Service MCP server via Smithery AI
    """
    
    def __init__(self):
        """Initialize the Weather MCP client with Smithery AI credentials"""
        self.smithery_api_key = "9775d396-48d3-4dd7-9a44-9fe04940ba16"
        self.smithery_profile = "grateful-crayfish-oQVqqO"
        self.url = f"https://server.smithery.ai/@smithery-ai/national-weather-service/mcp?api_key={self.smithery_api_key}&profile={self.smithery_profile}"
    
    def _parse_mcp_content(self, result) -> Dict[str, Any]:
        """
        Parse MCP response content into a dictionary
        
        Args:
            result: MCP CallToolResult object
            
        Returns:
            Parsed content as dictionary
        """
        try:
            if hasattr(result, 'content') and result.content:
                # Content is a list of TextContent objects
                if isinstance(result.content, list) and len(result.content) > 0:
                    # Get the text from the first TextContent item
                    text_content = result.content[0]
                    if hasattr(text_content, 'text'):
                        # Parse the JSON text
                        return json.loads(text_content.text)
            
            # Fallback: try to parse the result directly
            if isinstance(result, str):
                return json.loads(result)
            
            # Return empty result if parsing fails
            return {"error": "Could not parse response"}
            
        except (json.JSONDecodeError, AttributeError, IndexError) as e:
            return {"error": f"Parsing error: {str(e)}"}
    
    async def get_current_weather(self, location: str) -> Dict[str, Any]:
        """
        Get current weather conditions for a location
        
        Args:
            location: Location as coordinates (lat,lng) or city name
            
        Returns:
            Dictionary containing current weather information
        """
        try:
            async with streamablehttp_client(self.url) as (read_stream, write_stream, _):
                async with mcp.ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    
                    # Call the current weather tool
                    result = await session.call_tool("get_current_weather", {
                        "location": location
                    })
                    
                    content = self._parse_mcp_content(result)
                    
                    return {
                        "success": True,
                        "location": location,
                        "weather": content
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"Current weather failed: {str(e)}"
            }
    
    async def get_weather_forecast(self, location: str, days: int = 7) -> Dict[str, Any]:
        """
        Get weather forecast for a location
        
        Args:
            location: Location as coordinates (lat,lng) or city name
            days: Number of days to forecast (1-7)
            
        Returns:
            Dictionary containing weather forecast
        """
        try:
            async with streamablehttp_client(self.url) as (read_stream, write_stream, _):
                async with mcp.ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    
                    # Call the weather forecast tool
                    result = await session.call_tool("get_weather_forecast", {
                        "location": location,
                        "days": days
                    })
                    
                    content = self._parse_mcp_content(result)
                    
                    return {
                        "success": True,
                        "location": location,
                        "forecast": content
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"Weather forecast failed: {str(e)}"
            }
    
    async def get_hourly_forecast(self, location: str, hours: int = 24) -> Dict[str, Any]:
        """
        Get hourly weather forecast for a location
        
        Args:
            location: Location as coordinates (lat,lng) or city name
            hours: Number of hours to forecast (1-48)
            
        Returns:
            Dictionary containing hourly weather forecast
        """
        try:
            async with streamablehttp_client(self.url) as (read_stream, write_stream, _):
                async with mcp.ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    
                    # Call the hourly forecast tool
                    result = await session.call_tool("get_hourly_forecast", {
                        "location": location,
                        "hours": hours
                    })
                    
                    content = self._parse_mcp_content(result)
                    
                    return {
                        "success": True,
                        "location": location,
                        "hourly_forecast": content
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"Hourly forecast failed: {str(e)}"
            }
    
    async def get_weather_alerts(self, location: str, severity: str = "all") -> Dict[str, Any]:
        """
        Get weather alerts for a location
        
        Args:
            location: Location as coordinates (lat,lng) or state code
            severity: Alert severity filter
            
        Returns:
            Dictionary containing weather alerts
        """
        try:
            async with streamablehttp_client(self.url) as (read_stream, write_stream, _):
                async with mcp.ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    
                    # Call the weather alerts tool
                    result = await session.call_tool("get_weather_alerts", {
                        "location": location,
                        "severity": severity
                    })
                    
                    content = self._parse_mcp_content(result)
                    
                    return {
                        "success": True,
                        "location": location,
                        "alerts": content
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"Weather alerts failed: {str(e)}"
            }
    
    def analyze_weather_for_events(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze weather data to provide event recommendations
        
        Args:
            weather_data: Weather data from any of the weather methods
            
        Returns:
            Dictionary with event recommendations based on weather
        """
        try:
            # Extract key weather information
            current_temp = weather_data.get('current', {}).get('temperature', {})
            temp_f = current_temp.get('fahrenheit', 70)
            temp_c = current_temp.get('celsius', 21)
            
            conditions = weather_data.get('current', {}).get('conditions', 'Clear')
            humidity = weather_data.get('current', {}).get('humidity', 50)
            wind_speed = weather_data.get('current', {}).get('windSpeed', {})
            wind_mph = wind_speed.get('milesPerHour', 5)
            
            # Determine if weather is suitable for outdoor events
            is_outdoor_friendly = True
            outdoor_reasons = []
            indoor_reasons = []
            
            # Temperature analysis
            if temp_f < 40 or temp_f > 95:
                is_outdoor_friendly = False
                indoor_reasons.append(f"Temperature is {temp_f}°F ({temp_c}°C)")
            
            # Weather conditions analysis
            bad_conditions = ['Rain', 'Snow', 'Storm', 'Thunder', 'Fog', 'Haze']
            if any(bad_condition in conditions for bad_condition in bad_conditions):
                is_outdoor_friendly = False
                indoor_reasons.append(f"Weather conditions: {conditions}")
            
            # Wind analysis
            if wind_mph > 20:
                is_outdoor_friendly = False
                outdoor_reasons.append(f"High winds: {wind_mph} mph")
            
            # Humidity analysis
            if humidity > 80:
                outdoor_reasons.append(f"High humidity: {humidity}%")
            
            # Generate recommendations
            if is_outdoor_friendly:
                outdoor_reasons = [
                    f"Temperature: {temp_f}°F ({temp_c}°C)",
                    f"Conditions: {conditions}",
                    f"Wind: {wind_mph} mph",
                    f"Humidity: {humidity}%"
                ]
            
            return {
                "is_outdoor_friendly": is_outdoor_friendly,
                "outdoor_reasons": outdoor_reasons,
                "indoor_reasons": indoor_reasons,
                "weather_summary": {
                    "temperature": f"{temp_f}°F ({temp_c}°C)",
                    "conditions": conditions,
                    "wind_speed": f"{wind_mph} mph",
                    "humidity": f"{humidity}%"
                },
                "recommendations": {
                    "outdoor_events": is_outdoor_friendly,
                    "indoor_events": not is_outdoor_friendly,
                    "weather_notes": "Consider weather conditions when planning events"
                }
            }
            
        except Exception as e:
            return {
                "error": f"Weather analysis failed: {str(e)}",
                "is_outdoor_friendly": False,
                "outdoor_reasons": [],
                "indoor_reasons": ["Weather data unavailable"],
                "weather_summary": {},
                "recommendations": {
                    "outdoor_events": False,
                    "indoor_events": True,
                    "weather_notes": "Unable to analyze weather - recommend indoor events"
                }
            }

# Example usage and testing
async def main():
    """Main function to demonstrate Weather client capabilities"""
    print("🌤️ Starting Weather MCP Client Demo...")
    
    client = WeatherClient()
    
    # Test coordinates for NYC (Manhattan)
    nyc_coords = "40.7128,-74.0060"
    
    # Test 1: Current Weather
    print("\n1️⃣ Testing Current Weather...")
    current_weather = await client.get_current_weather(nyc_coords)
    if current_weather["success"]:
        print(f"✅ Current weather successful!")
        weather_data = current_weather["weather"]
        print(f"   Location: {weather_data.get('location', 'Unknown')}")
        print(f"   Temperature: {weather_data.get('current', {}).get('temperature', {}).get('fahrenheit', 'Unknown')}°F")
        print(f"   Conditions: {weather_data.get('current', {}).get('conditions', 'Unknown')}")
        
        # Analyze weather for events
        analysis = client.analyze_weather_for_events(weather_data)
        print(f"\n📊 Weather Analysis for Events:")
        print(f"   Outdoor friendly: {analysis['is_outdoor_friendly']}")
        if analysis['outdoor_reasons']:
            print(f"   Outdoor reasons: {', '.join(analysis['outdoor_reasons'])}")
        if analysis['indoor_reasons']:
            print(f"   Indoor reasons: {', '.join(analysis['indoor_reasons'])}")
    else:
        print(f"❌ Current weather failed: {current_weather['error']}")
    
    # Test 2: Weather Forecast
    print("\n2️⃣ Testing Weather Forecast...")
    forecast = await client.get_weather_forecast(nyc_coords, days=3)
    if forecast["success"]:
        print(f"✅ Weather forecast successful!")
        forecast_data = forecast["forecast"]
        print(f"   Location: {forecast_data.get('location', 'Unknown')}")
        print(f"   Days forecasted: {len(forecast_data.get('forecast', []))}")
    else:
        print(f"❌ Weather forecast failed: {forecast['error']}")
    
    print("\n🎉 Weather MCP Client Demo Complete!")
    print("💡 You can now integrate weather data with event planning!")

if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
