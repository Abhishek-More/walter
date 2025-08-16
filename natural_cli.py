#!/usr/bin/env python3
"""
Natural Language Event Search CLI

Simple interface for searching events using natural language
"""

import asyncio
import sys
from enhanced_event_search import EnhancedEventSearch

def print_help():
    """Print help information"""
    print("""
🧠 Natural Language Event Search CLI

Usage:
  python natural_cli.py "<your natural language query>"

Examples:
  python natural_cli.py "are there any vintage events in new york"
  python natural_cli.py "I'm starting at 162 east 82nd street new york - find me vintage festivals within 40 mins by train"
  python natural_cli.py "find art exhibitions in brooklyn within 30 minutes by subway"
  python natural_cli.py "vintage flea markets in manhattan this weekend"

Features:
  - Natural language queries
  - Automatic location detection
  - Travel time analysis
  - Weather integration
  - Event categorization

Help:
  python natural_cli.py help
""")

async def search_events(query: str):
    """Search for events using natural language"""
    print(f"🔍 Searching for: '{query}'")
    print(f"{'='*60}")
    
    enhanced_search = EnhancedEventSearch()
    
    try:
        results = await enhanced_search.search_natural_language(query, 5)
        
        if not results["success"]:
            print(f"❌ Search failed: {results.get('error', 'Unknown error')}")
            return
        
        print(f"\n✅ Search Complete!")
        print(f"📊 Found {results['total_results']} events")
        
        # Show weather info if available
        if results.get("weather_analysis"):
            weather = results["weather_analysis"]
            print(f"🌤️ Weather: {weather.get('weather_summary', {}).get('temperature', 'Unknown')}")
            print(f"🏠 Outdoor friendly: {'Yes' if weather.get('is_outdoor_friendly') else 'No'}")
        
        # Show starting point if provided
        if results.get("starting_coordinates"):
            print(f"📍 Starting from: {results['starting_coordinates']}")
        
        # Show events
        print(f"\n🎯 Events Found:")
        for i, event in enumerate(results["events"], 1):
            print(f"\n{i}. {event.get('title', 'No title')}")
            print(f"   🔗 URL: {event.get('url', 'No URL')}")
            
            # Show travel info if available
            if event.get("travel_time"):
                print(f"   🚇 Travel: {event.get('travel_duration', 'Unknown')} ({event.get('travel_distance', 'Unknown')})")
                if event.get("within_time_limit") is not None:
                    status = "✅" if event["within_time_limit"] else "❌"
                    limit_text = f"Within time limit" if event["within_time_limit"] else "Exceeds time limit"
                    print(f"   {status} {limit_text}")
            
            if event.get("route_summary"):
                print(f"   🗺️ Route: {event['route_summary']}")
        
        # Show summary
        if results.get("starting_coordinates"):
            within_limit = sum(1 for e in results["events"] if e.get("within_time_limit") is True)
            exceeds_limit = sum(1 for e in results["events"] if e.get("within_time_limit") is False)
            unknown_time = len(results["events"]) - within_limit - exceeds_limit
            
            print(f"\n📊 Travel Summary:")
            print(f"   ✅ Within time limit: {within_limit}")
            print(f"   ❌ Exceeds time limit: {exceeds_limit}")
            print(f"   ❓ Unknown travel time: {unknown_time}")
        
    except Exception as e:
        print(f"❌ Error during search: {str(e)}")
        import traceback
        traceback.print_exc()

async def main():
    """Main CLI function"""
    if len(sys.argv) < 2:
        print_help()
        return
    
    query = sys.argv[1]
    
    if query.lower() == "help":
        print_help()
        return
    
    await search_events(query)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Search interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
