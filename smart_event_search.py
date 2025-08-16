#!/usr/bin/env python3
"""
Smart Event Search Client

This client combines Exa search with weather data to provide intelligent
event recommendations based on weather conditions.
"""

import asyncio
import json
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from exa_search_app import ExaSearchClient
from weather_client import WeatherClient

class SmartEventSearch:
    """
    Smart event search that combines Exa search with weather data
    to recommend indoor vs outdoor events
    """
    
    def __init__(self):
        """Initialize the smart event search client"""
        self.exa_client = ExaSearchClient()
        self.weather_client = WeatherClient()
        
        # Common location coordinates
        self.location_coords = {
            "nyc": "40.7128,-74.0060",
            "manhattan": "40.7589,-73.9851",
            "brooklyn": "40.6782,-73.9442",
            "queens": "40.7282,-73.7949",
            "bronx": "40.8448,-73.8648",
            "staten island": "40.5795,-74.1502"
        }
    
    def get_location_coordinates(self, location: str) -> str:
        """
        Get coordinates for a location
        
        Args:
            location: Location name or coordinates
            
        Returns:
            Coordinates string
        """
        # If it's already coordinates, return as-is
        if "," in location and location.replace(".", "").replace("-", "").replace(",", "").isdigit():
            return location
        
        # Check if it's a known location
        location_lower = location.lower()
        for key, coords in self.location_coords.items():
            if key in location_lower:
                return coords
        
        # Default to NYC if location not found
        return self.location_coords["nyc"]
    
    async def search_events_with_weather(self, 
                                       query: str, 
                                       location: str = "nyc",
                                       num_results: int = 10,
                                       include_weather: bool = True) -> Dict[str, Any]:
        """
        Search for events and include weather recommendations
        
        Args:
            query: Search query for events
            location: Location name or coordinates
            num_results: Number of event results to return
            include_weather: Whether to include weather analysis
            
        Returns:
            Dictionary with events and weather recommendations
        """
        print(f"🔍 Searching for events: {query}")
        print(f"📍 Location: {location}")
        
        # Get events from Exa
        events_result = await self.exa_client.web_search(f"{query} {location}", num_results)
        
        if not events_result["success"]:
            return {
                "success": False,
                "error": f"Event search failed: {events_result['error']}",
                "events": [],
                "weather": None,
                "recommendations": []
            }
        
        events = events_result["results"]
        print(f"✅ Found {len(events)} events")
        
        # Get weather data if requested
        weather_data = None
        weather_analysis = None
        
        if include_weather:
            print(f"🌤️ Getting weather data for {location}...")
            coords = self.get_location_coordinates(location)
            weather_result = await self.weather_client.get_current_weather(coords)
            
            if weather_result["success"]:
                weather_data = weather_result["weather"]
                weather_analysis = self.weather_client.analyze_weather_for_events(weather_data)
                print(f"✅ Weather analysis complete")
            else:
                print(f"⚠️ Weather data unavailable: {weather_result['error']}")
        
        # Analyze events and provide recommendations
        recommendations = self._analyze_events_for_weather(events, weather_analysis)
        
        return {
            "success": True,
            "query": query,
            "location": location,
            "events": events,
            "weather": weather_data,
            "weather_analysis": weather_analysis,
            "recommendations": recommendations,
            "search_time": events_result.get("search_time", 0),
            "total_results": len(events)
        }
    
    def _analyze_events_for_weather(self, events: List[Dict], weather_analysis: Optional[Dict]) -> List[Dict]:
        """
        Analyze events and provide weather-based recommendations
        
        Args:
            events: List of event results
            weather_analysis: Weather analysis data
            
        Returns:
            List of event recommendations
        """
        recommendations = []
        
        if not weather_analysis:
            # No weather data available
            for event in events:
                recommendations.append({
                    "event": event,
                    "weather_recommendation": "Weather data unavailable",
                    "indoor_outdoor": "Unknown",
                    "confidence": "Low",
                    "notes": "Unable to determine if event is indoor/outdoor"
                })
            return recommendations
        
        is_outdoor_friendly = weather_analysis.get("is_outdoor_friendly", False)
        weather_summary = weather_analysis.get("weather_summary", {})
        
        for event in events:
            event_title = event.get("title", "").lower()
            event_url = event.get("url", "")
            
            # Analyze event type based on title and URL
            event_analysis = self._classify_event_type(event_title, event_url)
            
            # Provide weather-based recommendation
            if event_analysis["is_outdoor"]:
                if is_outdoor_friendly:
                    recommendation = "Great weather for outdoor events!"
                    confidence = "High"
                    notes = f"Weather: {weather_summary.get('temperature', 'Unknown')}, {weather_summary.get('conditions', 'Unknown')}"
                else:
                    recommendation = "Consider indoor alternatives due to weather"
                    confidence = "High"
                    notes = f"Weather: {weather_summary.get('temperature', 'Unknown')}, {weather_summary.get('conditions', 'Unknown')}"
            elif event_analysis["is_indoor"]:
                recommendation = "Indoor event - weather independent"
                confidence = "High"
                notes = "This event will not be affected by weather conditions"
            else:
                # Unknown event type
                if is_outdoor_friendly:
                    recommendation = "Weather looks good for outdoor activities"
                    confidence = "Medium"
                    notes = f"Weather: {weather_summary.get('temperature', 'Unknown')}, {weather_summary.get('conditions', 'Unknown')}"
                else:
                    recommendation = "Consider indoor alternatives due to weather"
                    confidence = "Medium"
                    notes = f"Weather: {weather_summary.get('temperature', 'Unknown')}, {weather_summary.get('conditions', 'Unknown')}"
            
            recommendations.append({
                "event": event,
                "weather_recommendation": recommendation,
                "indoor_outdoor": event_analysis["type"],
                "confidence": confidence,
                "notes": notes,
                "event_category": event_analysis["category"]
            })
        
        return recommendations
    
    def _classify_event_type(self, title: str, url: str) -> Dict[str, Any]:
        """
        Classify if an event is indoor or outdoor based on title and URL
        
        Args:
            title: Event title
            url: Event URL
            
        Returns:
            Dictionary with event classification
        """
        title_lower = title.lower()
        url_lower = url.lower()
        
        # Outdoor event indicators
        outdoor_keywords = [
            "outdoor", "outside", "park", "beach", "garden", "lawn", "street", "block party",
            "festival", "fair", "market", "flea market", "concert", "show", "walking tour",
            "hiking", "biking", "sports", "athletic", "fitness", "yoga", "meditation",
            "picnic", "bbq", "barbecue", "food truck", "food festival", "art walk",
            "parade", "march", "rally", "protest", "celebration", "ceremony"
        ]
        
        # Indoor event indicators
        indoor_keywords = [
            "indoor", "inside", "museum", "gallery", "theater", "cinema", "movie",
            "restaurant", "bar", "club", "lounge", "cafe", "coffee", "workshop",
            "class", "lecture", "seminar", "conference", "meeting", "presentation",
            "exhibition", "show", "performance", "concert", "dance", "fitness",
            "gym", "studio", "salon", "spa", "retail", "shopping", "mall"
        ]
        
        # Check for outdoor keywords
        outdoor_score = sum(1 for keyword in outdoor_keywords if keyword in title_lower)
        
        # Check for indoor keywords
        indoor_score = sum(1 for keyword in indoor_keywords if keyword in title_lower)
        
        # Determine event type
        if outdoor_score > indoor_score:
            event_type = "Outdoor"
            is_outdoor = True
            is_indoor = False
        elif indoor_score > outdoor_score:
            event_type = "Indoor"
            is_outdoor = False
            is_indoor = True
        else:
            event_type = "Unknown"
            is_outdoor = False
            is_indoor = False
        
        # Determine event category
        if any(word in title_lower for word in ["vintage", "antique", "retro", "flea market"]):
            category = "Vintage/Antique"
        elif any(word in title_lower for word in ["food", "restaurant", "cafe", "bar"]):
            category = "Food & Dining"
        elif any(word in title_lower for word in ["art", "gallery", "museum", "exhibition"]):
            category = "Arts & Culture"
        elif any(word in title_lower for word in ["music", "concert", "performance", "show"]):
            category = "Entertainment"
        elif any(word in title_lower for word in ["fitness", "yoga", "sports", "athletic"]):
            category = "Fitness & Sports"
        else:
            category = "General"
        
        return {
            "type": event_type,
            "is_outdoor": is_outdoor,
            "is_indoor": is_indoor,
            "category": category,
            "outdoor_score": outdoor_score,
            "indoor_score": indoor_score
        }
    
    async def get_weather_aware_recommendations(self, 
                                              query: str, 
                                              location: str = "nyc",
                                              num_results: int = 10) -> Dict[str, Any]:
        """
        Get weather-aware event recommendations
        
        Args:
            query: Search query for events
            location: Location name or coordinates
            num_results: Number of event results to return
            
        Returns:
            Dictionary with weather-aware recommendations
        """
        result = await self.search_events_with_weather(query, location, num_results, True)
        
        if not result["success"]:
            return result
        
        # Format the output for better readability
        formatted_recommendations = []
        
        for rec in result["recommendations"]:
            event = rec["event"]
            formatted_recommendations.append({
                "title": event.get("title", "No title"),
                "url": event.get("url", "No URL"),
                "preview": event.get("preview", "No preview"),
                "weather_recommendation": rec["weather_recommendation"],
                "indoor_outdoor": rec["indoor_outdoor"],
                "confidence": rec["confidence"],
                "category": rec["event_category"],
                "notes": rec["notes"]
            })
        
        return {
            "success": True,
            "query": result["query"],
            "location": result["location"],
            "weather_summary": result.get("weather_analysis", {}).get("weather_summary", {}),
            "outdoor_friendly": result.get("weather_analysis", {}).get("is_outdoor_friendly", False),
            "recommendations": formatted_recommendations,
            "total_results": result["total_results"]
        }

# Example usage and testing
async def main():
    """Main function to demonstrate Smart Event Search capabilities"""
    print("🧠 Starting Smart Event Search Demo...")
    
    smart_search = SmartEventSearch()
    
    # Test 1: Vintage events in NYC with weather
    print("\n1️⃣ Testing Vintage Events in NYC with Weather...")
    vintage_results = await smart_search.get_weather_aware_recommendations(
        "vintage events", "nyc", 5
    )
    
    if vintage_results["success"]:
        print(f"✅ Smart search successful!")
        print(f"📍 Location: {vintage_results['location']}")
        print(f"🌤️ Weather: {vintage_results.get('weather_summary', {}).get('temperature', 'Unknown')}")
        print(f"🏠 Outdoor friendly: {vintage_results['outdoor_friendly']}")
        print(f"📊 Found {vintage_results['total_results']} events")
        
        print(f"\n🎯 Top Recommendations:")
        for i, rec in enumerate(vintage_results["recommendations"][:3], 1):
            print(f"\n{i}. {rec['title']}")
            print(f"   Category: {rec['category']}")
            print(f"   Type: {rec['indoor_outdoor']}")
            print(f"   Weather: {rec['weather_recommendation']}")
            print(f"   Confidence: {rec['confidence']}")
            print(f"   URL: {rec['url']}")
    else:
        print(f"❌ Smart search failed: {vintage_results.get('error', 'Unknown error')}")
    
    print("\n🎉 Smart Event Search Demo Complete!")
    print("💡 You can now get weather-aware event recommendations!")

if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
