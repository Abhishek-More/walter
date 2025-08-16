#!/usr/bin/env python3
"""
Google Calendar MCP Client

This client integrates with Google Calendar via MCP to:
- Check calendar availability
- Add events to calendar
- Get calendar insights for event planning
"""

import asyncio
import json
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import mcp
from mcp.client.streamable_http import streamablehttp_client

class GoogleCalendarClient:
    """
    Client for interacting with Google Calendar MCP server
    """
    
    def __init__(self):
        """Initialize the Google Calendar MCP client"""
        # You'll need to add your Google Calendar MCP server details here
        self.smithery_api_key = "9775d396-48d3-4dd7-9a44-9fe04940ba16"
        self.smithery_profile = "grateful-crayfish-oQVqqO"
        # Update this URL to match your Google Calendar MCP server
        self.url = f"https://server.smithery.ai/@goldk3y/google-calendar-mcp/mcp?api_key={self.smithery_api_key}&profile={self.smithery_profile}"
    
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
                        # Try to parse the JSON text
                        try:
                            return json.loads(text_content.text)
                        except json.JSONDecodeError:
                            # If JSON parsing fails, return the raw text
                            return {"raw_content": text_content.text, "parsed": False}
            
            # Fallback: try to parse the result directly
            if isinstance(result, str):
                try:
                    return json.loads(result)
                except json.JSONDecodeError:
                    return {"raw_content": result, "parsed": False}
            
            # Return empty result if parsing fails
            return {"error": "Could not parse response", "parsed": False}
            
        except (AttributeError, IndexError) as e:
            return {"error": f"Parsing error: {str(e)}", "parsed": False}
    
    async def check_auth_status(self) -> Dict[str, Any]:
        """
        Check the current authentication status
        
        Returns:
            Dictionary with authentication status
        """
        try:
            async with streamablehttp_client(self.url) as (read_stream, write_stream, _):
                async with mcp.ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    
                    # Call the auth status tool
                    result = await session.call_tool("check_auth_status", {
                        "random_string": "check"
                    })
                    
                    content = self._parse_mcp_content(result)
                    
                    return {
                        "success": True,
                        "auth_status": content
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"Auth check failed: {str(e)}"
            }
    
    async def list_calendars(self, show_hidden: bool = False) -> Dict[str, Any]:
        """
        List all accessible calendars
        
        Args:
            show_hidden: Whether to show hidden calendars
            
        Returns:
            Dictionary with calendar list
        """
        try:
            async with streamablehttp_client(self.url) as (read_stream, write_stream, _):
                async with mcp.ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    
                    # Call the list calendars tool
                    result = await session.call_tool("list_calendars", {
                        "show_hidden": show_hidden
                    })
                    
                    content = self._parse_mcp_content(result)
                    
                    return {
                        "success": True,
                        "calendars": content
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"List calendars failed: {str(e)}"
            }
    
    async def list_events(self, calendar_id: str = "primary", 
                         time_min: Optional[str] = None,
                         time_max: Optional[str] = None,
                         max_results: int = 10) -> Dict[str, Any]:
        """
        List events from a calendar within a time range
        
        Args:
            calendar_id: Calendar ID (use 'primary' for main calendar)
            time_min: Start time (ISO 8601 format)
            time_max: End time (ISO 8601 format)
            max_results: Maximum number of events to return
            
        Returns:
            Dictionary with events list
        """
        try:
            async with streamablehttp_client(self.url) as (read_stream, write_stream, _):
                async with mcp.ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    
                    # Set default time range if not provided
                    if not time_min:
                        time_min = datetime.now().isoformat() + "Z"
                    if not time_max:
                        time_max = (datetime.now() + timedelta(days=7)).isoformat() + "Z"
                    
                    # Call the list events tool
                    result = await session.call_tool("list_events", {
                        "calendar_id": calendar_id,
                        "time_min": time_min,
                        "time_max": time_max,
                        "max_results": max_results,
                        "single_events": True,
                        "order_by": "startTime"
                    })
                    
                    content = self._parse_mcp_content(result)
                    
                    return {
                        "success": True,
                        "events": content,
                        "time_range": {"min": time_min, "max": time_max}
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"List events failed: {str(e)}"
            }
    
    async def create_event(self, calendar_id: str = "primary",
                          summary: str = "",
                          description: str = "",
                          start_time: str = "",
                          end_time: str = "",
                          location: str = "",
                          attendees: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Create a new calendar event
        
        Args:
            calendar_id: Calendar ID where to create the event
            summary: Event title/summary
            description: Event description
            start_time: Start time (ISO 8601 format)
            end_time: End time (ISO 8601 format)
            location: Event location
            attendees: List of attendee email addresses
            
        Returns:
            Dictionary with created event info
        """
        try:
            async with streamablehttp_client(self.url) as (read_stream, write_stream, _):
                async with mcp.ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    
                    # Prepare event data
                    event_data = {
                        "calendar_id": calendar_id,
                        "summary": summary,
                        "start_time": start_time,
                        "end_time": end_time
                    }
                    
                    if description:
                        event_data["description"] = description
                    if location:
                        event_data["location"] = location
                    if attendees:
                        event_data["attendees"] = attendees
                    
                    # Call the create event tool
                    result = await session.call_tool("create_event", event_data)
                    
                    content = self._parse_mcp_content(result)
                    
                    return {
                        "success": True,
                        "event": content,
                        "created": True
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"Create event failed: {str(e)}"
            }
    
    async def check_availability(self, calendar_id: str = "primary",
                               start_time: str = "",
                               end_time: str = "",
                               duration_minutes: int = 60) -> Dict[str, Any]:
        """
        Check calendar availability for a time slot
        
        Args:
            calendar_id: Calendar ID to check
            start_time: Start time to check (ISO 8601 format)
            end_time: End time to check (ISO 8601 format)
            duration_minutes: Minimum duration needed
            
        Returns:
            Dictionary with availability information
        """
        try:
            # Get events in the time range
            events_result = await self.list_events(
                calendar_id=calendar_id,
                time_min=start_time,
                time_max=end_time,
                max_results=50
            )
            
            if not events_result["success"]:
                return events_result
            
            events = events_result.get("events", [])
            
            # Check for conflicts
            conflicts = []
            available_slots = []
            
            # Simple availability check - can be enhanced
            if not events:
                available_slots.append({
                    "start": start_time,
                    "end": end_time,
                    "duration_minutes": duration_minutes
                })
            else:
                # Check if the requested time conflicts with existing events
                for event in events:
                    event_start = event.get("start", {}).get("dateTime", event.get("start", {}).get("date"))
                    event_end = event.get("end", {}).get("dateTime", event.get("end", {}).get("date"))
                    
                    if event_start and event_end:
                        # Check for overlap
                        if (start_time < event_end and end_time > event_start):
                            conflicts.append({
                                "summary": event.get("summary", "Unknown Event"),
                                "start": event_start,
                                "end": event_end
                            })
            
            return {
                "success": True,
                "available": len(conflicts) == 0,
                "conflicts": conflicts,
                "available_slots": available_slots,
                "requested_time": {
                    "start": start_time,
                    "end": end_time,
                    "duration_minutes": duration_minutes
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Availability check failed: {str(e)}"
            }
    
    async def suggest_event_time(self, calendar_id: str = "primary",
                                preferred_date: str = "",
                                duration_minutes: int = 60,
                                preferred_hours: tuple = (9, 17)) -> Dict[str, Any]:
        """
        Suggest available time slots for an event
        
        Args:
            calendar_id: Calendar ID to check
            preferred_date: Preferred date (YYYY-MM-DD format)
            duration_minutes: Event duration in minutes
            preferred_hours: Preferred time range (start_hour, end_hour)
            
        Returns:
            Dictionary with suggested time slots
        """
        try:
            # Convert date to datetime range
            date_obj = datetime.strptime(preferred_date, "%Y-%m-%d")
            start_of_day = date_obj.replace(hour=preferred_hours[0], minute=0, second=0, microsecond=0)
            end_of_day = date_obj.replace(hour=preferred_hours[1], minute=0, second=0, microsecond=0)
            
            # Check availability throughout the day
            time_slots = []
            current_time = start_of_day
            
            while current_time + timedelta(minutes=duration_minutes) <= end_of_day:
                slot_start = current_time.isoformat() + "Z"
                slot_end = (current_time + timedelta(minutes=duration_minutes)).isoformat() + "Z"
                
                # Check if this slot is available
                availability = await self.check_availability(
                    calendar_id=calendar_id,
                    start_time=slot_start,
                    end_time=slot_end,
                    duration_minutes=duration_minutes
                )
                
                if availability.get("available", False):
                    time_slots.append({
                        "start": slot_start,
                        "end": slot_end,
                        "start_time": current_time.strftime("%I:%M %p"),
                        "end_time": (current_time + timedelta(minutes=duration_minutes)).strftime("%I:%M %p")
                    })
                
                # Move to next slot (30-minute intervals)
                current_time += timedelta(minutes=30)
            
            return {
                "success": True,
                "preferred_date": preferred_date,
                "duration_minutes": duration_minutes,
                "available_slots": time_slots,
                "total_slots": len(time_slots)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Time suggestion failed: {str(e)}"
            }

# Example usage and testing
async def main():
    """Main function to demonstrate Google Calendar client capabilities"""
    print("📅 Starting Google Calendar MCP Client Demo...")
    
    client = GoogleCalendarClient()
    
    # Test 1: Check authentication status
    print("\n1️⃣ Testing Authentication Status...")
    auth_result = await client.check_auth_status()
    if auth_result["success"]:
        print(f"✅ Auth check successful!")
        print(f"   Status: {auth_result['auth_status']}")
    else:
        print(f"❌ Auth check failed: {auth_result['error']}")
    
    # Test 2: List calendars
    print("\n2️⃣ Testing Calendar List...")
    calendars_result = await client.list_calendars()
    if calendars_result["success"]:
        print(f"✅ Calendar list successful!")
        calendars = calendars_result.get("calendars", [])
        
        # Handle different response structures
        if isinstance(calendars, list):
            print(f"   Found {len(calendars)} calendars")
            for i, cal in enumerate(calendars[:3], 1):  # Show first 3
                if isinstance(cal, dict):
                    print(f"   - {cal.get('summary', 'Unknown')}: {cal.get('id', 'No ID')}")
                else:
                    print(f"   - Calendar {i}: {cal}")
        elif isinstance(calendars, dict):
            print(f"   Calendar data: {calendars}")
        else:
            print(f"   Raw response: {calendars}")
    else:
        print(f"❌ Calendar list failed: {calendars_result['error']}")
    
    # Test 3: Check availability
    print("\n3️⃣ Testing Availability Check...")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    availability_result = await client.suggest_event_time(
        preferred_date=tomorrow,
        duration_minutes=90
    )
    
    if availability_result["success"]:
        print(f"✅ Availability check successful!")
        print(f"   Date: {availability_result['preferred_date']}")
        print(f"   Duration: {availability_result['duration_minutes']} minutes")
        print(f"   Available slots: {availability_result['total_slots']}")
        
        if availability_result['available_slots']:
            print(f"   First slot: {availability_result['available_slots'][0]['start_time']} - {availability_result['available_slots'][0]['end_time']}")
    else:
        print(f"❌ Availability check failed: {availability_result['error']}")
    
    print("\n🎉 Google Calendar MCP Client Demo Complete!")
    print("💡 You can now integrate calendar functionality with event planning!")

if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
