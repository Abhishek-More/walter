#!/usr/bin/env python3
"""
Smart Event Search CLI

Command-line interface for weather-aware event search that combines
Exa search with National Weather Service data.
"""

import asyncio
import sys
import json
from smart_event_search import SmartEventSearch

def print_help():
    """Print help information"""
    print("""
🧠 Smart Event Search CLI - Weather-Aware Event Recommendations

Usage:
  python smart_event_cli.py <command> [options]

Commands:
  search <query> [location] [num_results]  - Search events with weather analysis
  weather <location>                        - Get current weather for a location
  help                                      - Show this help message

Examples:
  python smart_event_cli.py search "vintage events" "nyc" 10
  python smart_event_cli.py search "food festivals" "manhattan" 5
  python smart_event_cli.py search "art exhibitions" "brooklyn" 8
  python smart_event_cli.py weather "nyc"

Location Options:
  - nyc, manhattan, brooklyn, queens, bronx, staten island
  - Or use coordinates like "40.7128,-74.0060"
  - Or use any city name

Weather Integration:
  - Automatically analyzes weather conditions
  - Recommends indoor vs outdoor events
  - Provides weather-based event suggestions
  - Categorizes events by type and weather suitability

Help:
  python smart_event_cli.py help
""")

def print_weather_summary(weather_summary: dict):
    """Print formatted weather summary"""
    if not weather_summary:
        print("   🌤️ Weather: Data unavailable")
        return
    
    temp = weather_summary.get('temperature', 'Unknown')
    conditions = weather_summary.get('conditions', 'Unknown')
    wind = weather_summary.get('wind_speed', 'Unknown')
    humidity = weather_summary.get('humidity', 'Unknown')
    
    print(f"   🌤️ Weather: {temp}, {conditions}")
    print(f"   💨 Wind: {wind}")
    print(f"   💧 Humidity: {humidity}")

def print_event_recommendation(rec: dict, index: int):
    """Print formatted event recommendation"""
    print(f"\n{index}. {rec['title']}")
    print(f"   🏷️ Category: {rec['category']}")
    print(f"   🏠 Type: {rec['indoor_outdoor']}")
    print(f"   💡 Recommendation: {rec['weather_recommendation']}")
    print(f"   🎯 Confidence: {rec['confidence']}")
    print(f"   📝 Notes: {rec['notes']}")
    print(f"   🔗 URL: {rec['url']}")
    
    # Show preview if available
    if rec.get('preview'):
        preview = rec['preview'][:150] + "..." if len(rec['preview']) > 150 else rec['preview']
        print(f"   📖 Preview: {preview}")

async def search_events(query: str, location: str = "nyc", num_results: int = 10):
    """Search for events with weather analysis"""
    print(f"🔍 Smart Event Search")
    print(f"   Query: {query}")
    print(f"   Location: {location}")
    print(f"   Results: {num_results}")
    print(f"   🌤️ Including weather analysis...")
    
    smart_search = SmartEventSearch()
    
    try:
        results = await smart_search.get_weather_aware_recommendations(
            query, location, num_results
        )
        
        if not results["success"]:
            print(f"❌ Search failed: {results.get('error', 'Unknown error')}")
            return
        
        # Print summary
        print(f"\n✅ Search Complete!")
        print(f"📍 Location: {results['location']}")
        print_weather_summary(results.get('weather_summary', {}))
        print(f"🏠 Outdoor friendly: {'Yes' if results['outdoor_friendly'] else 'No'}")
        print(f"📊 Found {results['total_results']} events")
        
        # Print recommendations
        print(f"\n🎯 Event Recommendations:")
        for i, rec in enumerate(results["recommendations"], 1):
            print_event_recommendation(rec, i)
        
        # Print summary statistics
        outdoor_count = sum(1 for rec in results["recommendations"] if "Outdoor" in rec["indoor_outdoor"])
        indoor_count = sum(1 for rec in results["recommendations"] if "Indoor" in rec["indoor_outdoor"])
        unknown_count = results["total_results"] - outdoor_count - indoor_count
        
        print(f"\n📊 Summary:")
        print(f"   🏠 Indoor events: {indoor_count}")
        print(f"   🌳 Outdoor events: {outdoor_count}")
        print(f"   ❓ Unknown type: {unknown_count}")
        
        # Weather-based advice
        if results['outdoor_friendly']:
            print(f"\n💡 Weather Advice: Great conditions for outdoor events!")
        else:
            print(f"\n💡 Weather Advice: Consider indoor alternatives due to weather")
        
    except Exception as e:
        print(f"❌ Error during search: {str(e)}")
        import traceback
        traceback.print_exc()

async def get_weather(location: str):
    """Get current weather for a location"""
    print(f"🌤️ Getting weather for: {location}")
    
    smart_search = SmartEventSearch()
    
    try:
        coords = smart_search.get_location_coordinates(location)
        print(f"📍 Coordinates: {coords}")
        
        weather_result = await smart_search.weather_client.get_current_weather(coords)
        
        if not weather_result["success"]:
            print(f"❌ Weather failed: {weather_result['error']}")
            return
        
        weather_data = weather_result["weather"]
        weather_analysis = smart_search.weather_client.analyze_weather_for_events(weather_data)
        
        print(f"\n✅ Weather Data:")
        print(f"   📍 Location: {weather_data.get('location', 'Unknown')}")
        
        current = weather_data.get('current', {})
        if current:
            temp = current.get('temperature', {})
            temp_f = temp.get('fahrenheit', 'Unknown')
            temp_c = temp.get('celsius', 'Unknown')
            conditions = current.get('conditions', 'Unknown')
            humidity = current.get('humidity', 'Unknown')
            wind = current.get('windSpeed', {})
            wind_mph = wind.get('milesPerHour', 'Unknown')
            
            print(f"   🌡️ Temperature: {temp_f}°F ({temp_c}°C)")
            print(f"   🌤️ Conditions: {conditions}")
            print(f"   💨 Wind: {wind_mph} mph")
            print(f"   💧 Humidity: {humidity}%")
        
        print(f"\n📊 Event Planning Analysis:")
        print(f"   🏠 Outdoor friendly: {'Yes' if weather_analysis['is_outdoor_friendly'] else 'No'}")
        
        if weather_analysis['outdoor_reasons']:
            print(f"   ✅ Outdoor reasons: {', '.join(weather_analysis['outdoor_reasons'])}")
        
        if weather_analysis['indoor_reasons']:
            print(f"   ⚠️ Indoor reasons: {', '.join(weather_analysis['indoor_reasons'])}")
        
        print(f"\n💡 Recommendations:")
        if weather_analysis['is_outdoor_friendly']:
            print(f"   🌳 Great weather for outdoor events!")
        else:
            print(f"   🏠 Consider indoor alternatives")
        
    except Exception as e:
        print(f"❌ Error getting weather: {str(e)}")
        import traceback
        traceback.print_exc()

async def main():
    """Main CLI function"""
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        print_help()
        return
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("❌ Error: Search query required")
            print("Usage: python smart_event_cli.py search <query> [location] [num_results]")
            return
        
        query = sys.argv[2]
        location = sys.argv[3] if len(sys.argv) > 3 else "nyc"
        num_results = int(sys.argv[4]) if len(sys.argv) > 4 else 10
        
        await search_events(query, location, num_results)
    
    elif command == "weather":
        if len(sys.argv) < 3:
            print("❌ Error: Location required")
            print("Usage: python smart_event_cli.py weather <location>")
            return
        
        location = sys.argv[2]
        await get_weather(location)
    
    else:
        print(f"❌ Unknown command: {command}")
        print_help()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Search interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
