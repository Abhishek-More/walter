#!/usr/bin/env python3
"""
Enhanced Event Search with Google Maps Integration

This system combines:
- Exa Search MCP: Find events
- National Weather Service MCP: Weather analysis
- Google Maps MCP: Location, travel time, and directions
"""

import asyncio
import json
import re
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timedelta
from exa_search_app import ExaSearchClient
from weather_client import WeatherClient

class GoogleMapsClient:
    """
    Client for Google Maps MCP integration
    Note: This is a placeholder - you'll need to implement the actual MCP calls
    based on the tools available in your Google Maps MCP server
    """
    
    def __init__(self):
        """Initialize the Google Maps MCP client"""
        # You'll need to add your Google Maps MCP server details here
        self.smithery_api_key = "9775d396-48d3-4dd7-9a44-9fe04940ba16"
        self.smithery_profile = "grateful-crayfish-oQVqqO"
        # Update this URL to match your Google Maps MCP server
        self.url = f"https://server.smithery.ai/google-maps/mcp?api_key={self.smithery_api_key}&profile={self.smithery_profile}"
    
    async def geocode_address(self, address: str) -> Dict[str, Any]:
        """
        Convert address to coordinates
        
        Args:
            address: Address string
            
        Returns:
            Dictionary with coordinates and location info
        """
        # Placeholder - implement with actual Google Maps MCP tools
        try:
            # This would call the actual MCP tool like:
            # result = await session.call_tool("maps_geocode", {"address": address})
            
            # For now, return mock data
            return {
                "success": True,
                "address": address,
                "coordinates": "40.7589,-73.9851",  # Mock NYC coordinates
                "formatted_address": address,
                "location_type": "ROOFTOP"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Geocoding failed: {str(e)}"
            }
    
    async def get_travel_time(self, origin: str, destination: str, mode: str = "transit") -> Dict[str, Any]:
        """
        Get travel time between two locations
        
        Args:
            origin: Starting location (address or coordinates)
            destination: Destination location (address or coordinates)
            mode: Travel mode (transit, driving, walking, bicycling)
            
        Returns:
            Dictionary with travel time and route info
        """
        # Placeholder - implement with actual Google Maps MCP tools
        try:
            # This would call the actual MCP tool like:
            # result = await session.call_tool("maps_directions", {"origin": origin, "destination": destination, "mode": mode})
            
            # For now, return mock data
            return {
                "success": True,
                "origin": origin,
                "destination": destination,
                "mode": mode,
                "duration": "25 mins",
                "duration_seconds": 1500,
                "distance": "2.3 miles",
                "route_summary": f"Take subway from {origin} to {destination}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Travel time calculation failed: {str(e)}"
            }
    
    async def find_nearby_places(self, location: str, query: str, radius: int = 5000) -> Dict[str, Any]:
        """
        Find places near a location
        
        Args:
            location: Center location (address or coordinates)
            query: Search query
            radius: Search radius in meters
            
        Returns:
            Dictionary with nearby places
        """
        # Placeholder - implement with actual Google Maps MCP tools
        try:
            # This would call the actual MCP tool like:
            # result = await session.call_tool("maps_search_places", {"query": query, "location": location, "radius": radius})
            
            # For now, return mock data
            return {
                "success": True,
                "location": location,
                "query": query,
                "radius": radius,
                "places": [
                    {
                        "name": f"Mock {query} place 1",
                        "address": "123 Example St, NYC",
                        "rating": 4.5,
                        "types": ["establishment"]
                    }
                ]
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Nearby search failed: {str(e)}"
            }

class NaturalLanguageParser:
    """
    Parse natural language queries into structured search parameters
    """
    
    def __init__(self):
        """Initialize the natural language parser"""
        # Common event types and their keywords
        self.event_keywords = {
            "vintage": ["vintage", "antique", "retro", "flea market", "thrift", "collector"],
            "food": ["food", "restaurant", "cafe", "bar", "festival", "truck", "dining"],
            "art": ["art", "gallery", "museum", "exhibition", "show", "performance"],
            "music": ["music", "concert", "band", "dj", "live", "performance"],
            "fitness": ["fitness", "yoga", "gym", "workout", "sports", "athletic"],
            "culture": ["culture", "cultural", "heritage", "tradition", "festival"]
        }
        
        # Location patterns
        self.location_patterns = [
            r"in\s+([^,\n]+?)(?:\s+new\s+york|\s+nyc|\s+ny)?$",
            r"near\s+([^,\n]+?)(?:\s+new\s+york|\s+nyc|\s+ny)?$",
            r"around\s+([^,\n]+?)(?:\s+new\s+york|\s+nyc|\s+ny)?$",
            r"at\s+([^,\n]+?)(?:\s+new\s+york|\s+nyc|\s+ny)?$"
        ]
        
        # Time patterns
        self.time_patterns = [
            r"within\s+(\d+)\s*(?:mins?|minutes?)",
            r"(\d+)\s*(?:mins?|minutes?)\s+(?:away|travel|commute)",
            r"less\s+than\s+(\d+)\s*(?:mins?|minutes?)"
        ]
        
        # Transportation patterns
        self.transport_patterns = [
            r"by\s+(train|subway|bus|walking|car|bike)",
            r"on\s+(train|subway|bus|foot|bike)",
            r"via\s+(train|subway|bus|walking|car|bike)"
        ]
    
    def parse_query(self, query: str) -> Dict[str, Any]:
        """
        Parse a natural language query into structured parameters
        
        Args:
            query: Natural language query string
            
        Returns:
            Dictionary with parsed parameters
        """
        query_lower = query.lower()
        
        # Extract event type
        event_type = self._extract_event_type(query_lower)
        
        # Extract location
        location = self._extract_location(query_lower)
        
        # Extract time constraints
        max_time = self._extract_time_constraint(query_lower)
        
        # Extract transportation mode
        transport_mode = self._extract_transport_mode(query_lower)
        
        # Extract starting point (if mentioned)
        starting_point = self._extract_starting_point(query_lower)
        
        return {
            "event_type": event_type,
            "location": location,
            "max_travel_time": max_time,
            "transport_mode": transport_mode,
            "starting_point": starting_point,
            "original_query": query,
            "parsed": True
        }
    
    def _extract_event_type(self, query: str) -> str:
        """Extract event type from query"""
        for event_type, keywords in self.event_keywords.items():
            if any(keyword in query for keyword in keywords):
                return event_type
        
        # Default to general search
        return "events"
    
    def _extract_location(self, query: str) -> str:
        """Extract location from query"""
        # Check for specific NYC boroughs
        nyc_areas = ["manhattan", "brooklyn", "queens", "bronx", "staten island", "nyc", "new york"]
        for area in nyc_areas:
            if area in query:
                return area
        
        # Check for location patterns
        for pattern in self.location_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Default to NYC
        return "nyc"
    
    def _extract_time_constraint(self, query: str) -> Optional[int]:
        """Extract maximum travel time constraint"""
        for pattern in self.time_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return None
    
    def _extract_transport_mode(self, query: str) -> str:
        """Extract preferred transportation mode"""
        for pattern in self.transport_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                mode = match.group(1).lower()
                if mode in ["train", "subway"]:
                    return "transit"
                elif mode in ["walking", "foot"]:
                    return "walking"
                elif mode in ["bike", "bicycling"]:
                    return "bicycling"
                elif mode in ["car", "driving"]:
                    return "driving"
                elif mode in ["bus"]:
                    return "transit"
        
        # Default to transit for NYC
        return "transit"
    
    def _extract_starting_point(self, query: str) -> Optional[str]:
        """Extract starting point from query"""
        # Look for patterns like "starting at", "from", "I'm at"
        starting_patterns = [
            r"starting\s+at\s+([^,\n]+)",
            r"from\s+([^,\n]+)",
            r"i'm\s+at\s+([^,\n]+)",
            r"at\s+([^,\n]+?)(?:\s+street|\s+avenue|\s+road|\s+boulevard)"
        ]
        
        for pattern in starting_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None

class EnhancedEventSearch:
    """
    Enhanced event search that integrates location, weather, and travel time
    """
    
    def __init__(self):
        """Initialize the enhanced event search"""
        self.exa_client = ExaSearchClient()
        self.weather_client = WeatherClient()
        self.maps_client = GoogleMapsClient()
        self.parser = NaturalLanguageParser()
        
        # Common NYC locations with coordinates
        self.nyc_locations = {
            "nyc": "40.7128,-74.0060",
            "manhattan": "40.7589,-73.9851",
            "brooklyn": "40.6782,-73.9442",
            "queens": "40.7282,-73.7949",
            "bronx": "40.8448,-73.8648",
            "staten island": "40.5795,-74.1502"
        }
    
    async def search_natural_language(self, query: str, num_results: int = 10) -> Dict[str, Any]:
        """
        Search for events using natural language
        
        Args:
            query: Natural language query
            num_results: Number of results to return
            
        Returns:
            Dictionary with enhanced search results
        """
        print(f"🧠 Parsing query: '{query}'")
        
        # Parse the natural language query
        parsed = self.parser.parse_query(query)
        
        if not parsed["parsed"]:
            return {
                "success": False,
                "error": "Could not parse query",
                "original_query": query
            }
        
        print(f"✅ Parsed query:")
        print(f"   Event type: {parsed['event_type']}")
        print(f"   Location: {parsed['location']}")
        print(f"   Max travel time: {parsed['max_travel_time']} mins" if parsed['max_travel_time'] else "   Max travel time: None")
        print(f"   Transport mode: {parsed['transport_mode']}")
        print(f"   Starting point: {parsed['starting_point']}" if parsed['starting_point'] else "   Starting point: None")
        
        # Get starting coordinates if provided
        starting_coords = None
        if parsed["starting_point"]:
            print(f"📍 Geocoding starting point: {parsed['starting_point']}")
            geocode_result = await self.maps_client.geocode_address(parsed["starting_point"])
            if geocode_result["success"]:
                starting_coords = geocode_result["coordinates"]
                print(f"   Coordinates: {starting_coords}")
            else:
                print(f"   ⚠️ Geocoding failed: {geocode_result['error']}")
        
        # Search for events
        search_query = f"{parsed['event_type']} {parsed['location']}"
        print(f"🔍 Searching for: {search_query}")
        
        events_result = await self.exa_client.web_search(search_query, num_results)
        
        if not events_result["success"]:
            return {
                "success": False,
                "error": f"Event search failed: {events_result['error']}",
                "parsed_query": parsed
            }
        
        events = events_result["results"]
        print(f"✅ Found {len(events)} events")
        
        # Get weather data
        print(f"🌤️ Getting weather data...")
        location_coords = self.nyc_locations.get(parsed["location"], self.nyc_locations["nyc"])
        weather_result = await self.weather_client.get_current_weather(location_coords)
        
        weather_data = None
        weather_analysis = None
        if weather_result["success"]:
            weather_data = weather_result["weather"]
            weather_analysis = self.weather_client.analyze_weather_for_events(weather_data)
            print(f"✅ Weather analysis complete")
        else:
            print(f"⚠️ Weather data unavailable: {weather_result['error']}")
        
        # Enhance events with travel time and location data
        enhanced_events = []
        for event in events:
            enhanced_event = await self._enhance_event_with_location_data(
                event, starting_coords, parsed["transport_mode"], parsed["max_travel_time"]
            )
            enhanced_events.append(enhanced_event)
        
        # Sort events by travel time if available
        if starting_coords and any(e.get("travel_time") for e in enhanced_events):
            enhanced_events.sort(key=lambda x: x.get("travel_time") or float('inf'))
        
        return {
            "success": True,
            "original_query": query,
            "parsed_query": parsed,
            "events": enhanced_events,
            "weather": weather_data,
            "weather_analysis": weather_analysis,
            "starting_coordinates": starting_coords,
            "total_results": len(enhanced_events)
        }
    
    async def _enhance_event_with_location_data(self, event: Dict, starting_coords: Optional[str], 
                                              transport_mode: str, max_time: Optional[int]) -> Dict:
        """
        Enhance an event with location and travel time data
        
        Args:
            event: Event data
            starting_coords: Starting coordinates
            transport_mode: Preferred transport mode
            max_time: Maximum travel time
            
        Returns:
            Enhanced event data
        """
        enhanced_event = event.copy()
        
        # Try to extract location from event data
        event_location = self._extract_event_location(event)
        
        if event_location and starting_coords:
            # Get travel time
            travel_result = await self.maps_client.get_travel_time(
                starting_coords, event_location, transport_mode
            )
            
            if travel_result["success"]:
                enhanced_event["travel_time"] = travel_result["duration_seconds"]
                enhanced_event["travel_duration"] = travel_result["duration"]
                enhanced_event["travel_distance"] = travel_result["distance"]
                enhanced_event["route_summary"] = travel_result["route_summary"]
                
                # Check if within time constraint
                if max_time:
                    travel_minutes = travel_result["duration_seconds"] / 60
                    enhanced_event["within_time_limit"] = travel_minutes <= max_time
                else:
                    enhanced_event["within_time_limit"] = True
            else:
                enhanced_event["travel_time"] = None
                enhanced_event["within_time_limit"] = None
        else:
            enhanced_event["travel_time"] = None
            enhanced_event["within_time_limit"] = None
        
        return enhanced_event
    
    def _extract_event_location(self, event: Dict) -> Optional[str]:
        """Extract location information from event data"""
        # Try to extract address from various fields
        title = event.get("title", "").lower()
        url = event.get("url", "").lower()
        
        # Look for address patterns
        address_patterns = [
            r"(\d+\s+[a-z]+\s+(?:street|avenue|road|boulevard|st|ave|rd|blvd))",
            r"([a-z]+\s+(?:street|avenue|road|boulevard|st|ave|rd|blvd))",
            r"(\d+\s+[a-z]+\s+[a-z]+)"
        ]
        
        for pattern in address_patterns:
            match = re.search(pattern, title)
            if match:
                return match.group(1)
        
        # If no address found, return None
        return None

# Example usage and testing
async def main():
    """Main function to demonstrate Enhanced Event Search capabilities"""
    print("🚀 Starting Enhanced Event Search Demo...")
    
    enhanced_search = EnhancedEventSearch()
    
    # Test natural language queries
    test_queries = [
        "are there any vintage events in new york",
        "I'm starting at 162 east 82nd street new york, new york - can you find me vintage festivals near me or ones that are easy to get to on the train? within 40 mins of me?",
        "find art exhibitions in brooklyn within 30 minutes by subway",
        "vintage flea markets in manhattan this weekend"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {query}")
        print(f"{'='*60}")
        
        try:
            results = await enhanced_search.search_natural_language(query, 3)
            
            if results["success"]:
                print(f"\n✅ Search successful!")
                print(f"📊 Found {results['total_results']} events")
                
                if results.get("weather_analysis"):
                    weather = results["weather_analysis"]
                    print(f"🌤️ Weather: {weather.get('weather_summary', {}).get('temperature', 'Unknown')}")
                    print(f"🏠 Outdoor friendly: {weather.get('is_outdoor_friendly', 'Unknown')}")
                
                print(f"\n🎯 Top Events:")
                for j, event in enumerate(results["events"][:3], 1):
                    print(f"\n{j}. {event.get('title', 'No title')}")
                    print(f"   URL: {event.get('url', 'No URL')}")
                    
                    if event.get("travel_time"):
                        print(f"   🚇 Travel: {event.get('travel_duration', 'Unknown')} ({event.get('travel_distance', 'Unknown')})")
                        if event.get("within_time_limit") is not None:
                            status = "✅" if event["within_time_limit"] else "❌"
                            print(f"   {status} Within time limit: {event['within_time_limit']}")
                    
                    if event.get("route_summary"):
                        print(f"   🗺️ Route: {event['route_summary']}")
            else:
                print(f"❌ Search failed: {results.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Error during search: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print(f"\n🎉 Enhanced Event Search Demo Complete!")
    print("💡 You can now use natural language to find events with travel time analysis!")

if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
