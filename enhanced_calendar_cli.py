#!/usr/bin/env python3
"""
Enhanced Calendar CLI with Vintage Event Search

This CLI combines:
- Vintage event search using Exa Search
- Google Calendar integration for availability checking
- Event scheduling and conflict detection
"""

import asyncio
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from google_calendar_python_client import GoogleCalendarPythonClient
from exa_search_app import ExaSearchClient

class EnhancedCalendarCLI:
    """
    Enhanced CLI that combines event search with calendar management
    """
    
    def __init__(self):
        """Initialize the enhanced CLI"""
        self.calendar_client = GoogleCalendarPythonClient()
        self.exa_client = ExaSearchClient()
        
    def print_help(self):
        """Print help information"""
        print("""
🎭 Enhanced Calendar CLI - Vintage Event Edition

Usage:
  python enhanced_calendar_cli.py <command> [options]

Commands:
  🔍 SEARCH & DISCOVERY:
    search <query>                    - Search for vintage events near you
    find <event_type> <location>      - Find specific type of events
    nearby <location>                  - Find events in a specific area
    
  📅 CALENDAR MANAGEMENT:
    auth                               - Check Google Calendar authentication
    calendars                          - List all calendars
    events [days]                      - List your upcoming events
    free <date>                        - Show when you're free on a date
    conflicts <date> <time> <duration> - Check for scheduling conflicts
    
  ➕ EVENT SCHEDULING:
    add <event_title> <date> <time> <duration> - Add event to calendar
    schedule <event_id> <date> <time>          - Schedule a found event
    
  💡 SMART FEATURES:
    suggest <event_type> <date>       - Suggest best times for event type
    plan <query>                       - Smart planning with search + calendar
    
Examples:
  python enhanced_calendar_cli.py search "vintage markets near brooklyn"
  python enhanced_calendar_cli.py find "antique fairs" "manhattan"
  python enhanced_calendar_cli.py free 2025-08-20
  python enhanced_calendar_cli.py add "Vintage Market" 2025-08-20 "14:00" 180
  python enhanced_calendar_cli.py plan "vintage popup shop this weekend"

Date Format: YYYY-MM-DD (e.g., 2025-08-20)
Time Format: HH:MM (e.g., 14:00 for 2:00 PM)
Duration: Minutes (e.g., 180 for 3 hours)

Help:
  python enhanced_calendar_cli.py help
""")

    async def check_auth(self):
        """Check Google Calendar authentication"""
        print("🔐 Checking Google Calendar authentication...")
        
        result = self.calendar_client.check_auth_status()
        
        if result["success"] and result.get("authenticated"):
            print("✅ Authentication successful!")
            print(f"   Calendars: {result.get('calendars_count', 0)}")
            print(f"   Message: {result.get('message', 'No message')}")
        else:
            print(f"❌ Authentication failed: {result.get('error', 'Unknown error')}")
            print("💡 You may need to complete the OAuth2 flow")

    async def search_vintage_events(self, query: str, num_results: int = 10):
        """Search for vintage events using natural language"""
        print(f"🔍 Searching for vintage events: '{query}'")
        print(f"📊 Results requested: {num_results}")
        
        try:
            # Search for events
            events_result = await self.exa_client.web_search(query, num_results)
            
            if events_result["success"]:
                events = events_result.get("results", [])
                print(f"✅ Found {len(events)} events:")
                
                for i, event in enumerate(events, 1):
                    print(f"\n{i}. {event.get('title', 'No title')}")
                    
                    # Show URL
                    if event.get('url'):
                        print(f"   🔗 {event['url']}")
                    
                    # Show content preview
                    if event.get('content'):
                        content = event['content'][:150] + "..." if len(event['content']) > 150 else event['content']
                        print(f"   📝 {content}")
                    
                    # Show source
                    if event.get('source'):
                        print(f"   📰 Source: {event['source']}")
                    
                    # Store event data for potential scheduling
                    event['event_id'] = i
                
                # Store events for later use
                self.found_events = events
                
                print(f"\n💡 To schedule any of these events, use:")
                print(f"   python enhanced_calendar_cli.py schedule <event_number> <date> <time>")
                
            else:
                print(f"❌ Search failed: {events_result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Search error: {str(e)}")

    async def find_specific_events(self, event_type: str, location: str, num_results: int = 8):
        """Find specific type of events in a location"""
        query = f"{event_type} {location} events upcoming"
        await self.search_vintage_events(query, num_results)

    async def find_nearby_events(self, location: str, num_results: int = 8):
        """Find events in a specific area"""
        query = f"vintage events markets fairs {location} upcoming"
        await self.search_vintage_events(query, num_results)

    async def list_calendars(self):
        """List all accessible calendars"""
        print("📅 Listing Google Calendars...")
        
        result = self.calendar_client.list_calendars()
        
        if result["success"]:
            calendars = result.get("calendars", [])
            print(f"✅ Found {len(calendars)} calendars:")
            
            for i, cal in enumerate(calendars, 1):
                print(f"\n{i}. {cal.get('summary', 'Unknown Calendar')}")
                print(f"   ID: {cal.get('id', 'No ID')}")
                print(f"   Description: {cal.get('description', 'No description')}")
                print(f"   Primary: {'Yes' if cal.get('primary', False) else 'No'}")
                print(f"   Timezone: {cal.get('timezone', 'Unknown')}")
        else:
            print(f"❌ Failed to list calendars: {result['error']}")

    async def list_events(self, days: int = 7):
        """List upcoming events from primary calendar"""
        print(f"📋 Listing events from primary calendar")
        print(f"📅 Time range: Next {days} days")
        
        # Calculate time range
        now = datetime.now()
        time_min = now.isoformat() + "Z"
        time_max = (now + timedelta(days=days)).isoformat() + "Z"
        
        result = self.calendar_client.list_events(
            time_min=time_min,
            time_max=time_max,
            max_results=20
        )
        
        if result["success"]:
            events = result.get("events", [])
            print(f"✅ Found {len(events)} events:")
            
            for i, event in enumerate(events, 1):
                print(f"\n{i}. {event.get('summary', 'No title')}")
                
                # Show start time
                start = event.get('start')
                if start:
                    if 'T' in start:  # Has time
                        start_time = datetime.fromisoformat(start.replace('Z', '+00:00'))
                        print(f"   🕐 Start: {start_time.strftime('%Y-%m-%d %I:%M %p')}")
                    else:  # All day
                        start_date = datetime.fromisoformat(start)
                        print(f"   📅 Date: {start_date.strftime('%Y-%m-%d')} (All day)")
                
                # Show end time
                end = event.get('end')
                if end and 'T' in end:
                    end_time = datetime.fromisoformat(end.replace('Z', '+00:00'))
                    print(f"   🕐 End: {end_time.strftime('%I:%M %p')}")
                
                # Show location
                if event.get('location'):
                    print(f"   📍 Location: {event['location']}")
                
                # Show description
                if event.get('description'):
                    desc = event['description'][:100] + "..." if len(event['description']) > 100 else event['description']
                    print(f"   📝 Description: {desc}")
        else:
            print(f"❌ Failed to list events: {result['error']}")

    async def show_free_times(self, date_str: str):
        """Show when you're free on a specific date"""
        print(f"🆓 Checking free times for {date_str}")
        
        try:
            # Parse date
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            
            # Check availability throughout the day (9 AM to 9 PM)
            start_of_day = date_obj.replace(hour=9, minute=0, second=0, microsecond=0)
            end_of_day = date_obj.replace(hour=21, minute=0, second=0, microsecond=0)
            
            # Get events for the day
            time_min = start_of_day.isoformat() + "Z"
            time_max = end_of_day.isoformat() + "Z"
            
            events_result = self.calendar_client.list_events(
                time_min=time_min,
                time_max=time_max,
                max_results=50
            )
            
            if events_result["success"]:
                events = events_result.get("events", [])
                
                if not events:
                    print("✅ You're completely free on this date!")
                    print(f"   Available: 9:00 AM - 9:00 PM")
                else:
                    print(f"📅 You have {len(events)} events on this date:")
                    
                    # Sort events by start time
                    sorted_events = sorted(events, key=lambda x: x.get('start', ''))
                    
                    # Show events and calculate free slots
                    free_slots = []
                    current_time = start_of_day
                    
                    for event in sorted_events:
                        event_start = event.get('start')
                        event_end = event.get('end')
                        
                        if event_start and event_end:
                            # Parse event times
                            if 'T' in event_start:
                                event_start_time = datetime.fromisoformat(event_start.replace('Z', '+00:00'))
                                event_end_time = datetime.fromisoformat(event_end.replace('Z', '+00:00'))
                                
                                # Check if there's free time before this event
                                if current_time < event_start_time:
                                    free_duration = (event_start_time - current_time).total_seconds() / 60
                                    if free_duration >= 30:  # Only show slots 30+ minutes
                                        free_slots.append({
                                            'start': current_time,
                                            'end': event_start_time,
                                            'duration': free_duration
                                        })
                                
                                current_time = event_end_time
                    
                    # Check if there's free time after the last event
                    if current_time < end_of_day:
                        free_duration = (end_of_day - current_time).total_seconds() / 60
                        if free_duration >= 30:
                            free_slots.append({
                                'start': current_time,
                                'end': end_of_day,
                                'duration': free_duration
                            })
                    
                    # Show free slots
                    if free_slots:
                        print(f"\n🆓 Free time slots:")
                        for i, slot in enumerate(free_slots, 1):
                            start_str = slot['start'].strftime('%I:%M %p')
                            end_str = slot['end'].strftime('%I:%M %p')
                            duration = int(slot['duration'])
                            print(f"   {i}. {start_str} - {end_str} ({duration} minutes)")
                    else:
                        print("❌ No significant free time slots found")
                        
            else:
                print(f"❌ Failed to check events: {events_result['error']}")
                
        except ValueError as e:
            print(f"❌ Invalid date format: {e}")
            print("💡 Use YYYY-MM-DD format (e.g., 2025-08-20)")

    async def check_conflicts(self, date_str: str, time_str: str, duration_minutes: int):
        """Check for scheduling conflicts"""
        print(f"🔍 Checking for conflicts on {date_str} at {time_str}")
        print(f"⏱️ Duration: {duration_minutes} minutes")
        
        try:
            # Parse date and time
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            time_obj = datetime.strptime(time_str, "%H:%M")
            
            # Create start and end times
            start_time = date_obj.replace(
                hour=time_obj.hour,
                minute=time_obj.minute,
                second=0,
                microsecond=0
            ).isoformat() + "Z"
            
            end_time = (start_time + timedelta(minutes=duration_minutes)).isoformat() + "Z"
            
            # Check availability
            result = self.calendar_client.check_availability(
                start_time=start_time,
                end_time=end_time,
                duration_minutes=duration_minutes
            )
            
            if result["success"]:
                if result["available"]:
                    print("✅ No conflicts! This time slot is available.")
                    print(f"   Start: {datetime.fromisoformat(start_time.replace('Z', '+00:00')).strftime('%Y-%m-%d %I:%M %p')}")
                    print(f"   End: {datetime.fromisoformat(end_time.replace('Z', '+00:00')).strftime('%I:%M %p')}")
                else:
                    print("❌ Conflicts found:")
                    for conflict in result["conflicts"]:
                        print(f"   - {conflict['summary']}: {conflict['start']} to {conflict['end']}")
                    
                    print(f"\n💡 Try using 'free {date_str}' to see available times")
            else:
                print(f"❌ Availability check failed: {result['error']}")
                
        except ValueError as e:
            print(f"❌ Error: {e}")

    async def add_event(self, title: str, date_str: str, time_str: str, duration_minutes: int):
        """Add a new event to calendar"""
        print(f"➕ Adding event to calendar...")
        print(f"📝 Title: {title}")
        print(f"📅 Date: {date_str}")
        print(f"🕐 Time: {time_str}")
        print(f"⏱️ Duration: {duration_minutes} minutes")
        
        try:
            # Parse start time
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            time_obj = datetime.strptime(time_str, "%H:%M")
            
            start_obj = date_obj.replace(
                hour=time_obj.hour,
                minute=time_obj.minute,
                second=0,
                microsecond=0
            )
            start_time = start_obj.isoformat() + "Z"
            
            end_time = (start_obj + timedelta(minutes=duration_minutes)).isoformat() + "Z"
            
            # Check for conflicts first
            print("🔍 Checking for conflicts...")
            conflict_result = self.calendar_client.check_availability(
                start_time=start_time,
                end_time=end_time,
                duration_minutes=duration_minutes
            )
            
            if conflict_result["success"] and not conflict_result["available"]:
                print("⚠️ Conflicts detected:")
                for conflict in conflict_result["conflicts"]:
                    print(f"   - {conflict['summary']}: {conflict['start']} to {conflict['end']}")
                
                proceed = input("\n❓ Do you want to proceed anyway? (y/N): ").strip().lower()
                if proceed != 'y':
                    print("❌ Event creation cancelled")
                    return
            
            # Create the event
            result = self.calendar_client.create_event(
                summary=title,
                start_time=start_time,
                end_time=end_time,
                description=f"Event created via Enhanced Calendar CLI - Duration: {duration_minutes} minutes"
            )
            
            if result["success"]:
                print("✅ Event created successfully!")
                event = result["event"]
                print(f"   Event ID: {event.get('id', 'Unknown')}")
                print(f"   Start: {datetime.fromisoformat(start_time.replace('Z', '+00:00')).strftime('%Y-%m-%d %I:%M %p')}")
                print(f"   End: {datetime.fromisoformat(end_time.replace('Z', '+00:00')).strftime('%I:%M %p')}")
                print(f"   Calendar: primary")
            else:
                print(f"❌ Failed to create event: {result['error']}")
                
        except ValueError as e:
            print(f"❌ Error: {e}")

    async def schedule_found_event(self, event_id: int, date_str: str, time_str: str):
        """Schedule a previously found event"""
        if not hasattr(self, 'found_events') or not self.found_events:
            print("❌ No events found. Please search for events first using 'search' command.")
            return
        
        try:
            event_id = int(event_id) - 1  # Convert to 0-based index
            if event_id < 0 or event_id >= len(self.found_events):
                print(f"❌ Invalid event ID. Please choose between 1 and {len(self.found_events)}")
                return
            
            event = self.found_events[event_id]
            print(f"📅 Scheduling event: {event.get('title', 'No title')}")
            
            # Ask for duration
            duration_input = input("⏱️ How long will this event take? (minutes): ").strip()
            try:
                duration_minutes = int(duration_input)
            except ValueError:
                print("❌ Invalid duration. Please enter a number of minutes.")
                return
            
            # Add the event
            await self.add_event(
                event.get('title', 'Found Event'),
                date_str,
                time_str,
                duration_minutes
            )
            
        except ValueError as e:
            print(f"❌ Error: {e}")

    async def smart_planning(self, query: str):
        """Smart planning that combines search and calendar"""
        print(f"🧠 Smart planning for: '{query}'")
        
        # First, search for events
        await self.search_vintage_events(query, 5)
        
        if hasattr(self, 'found_events') and self.found_events:
            print(f"\n📅 Now let's check your availability...")
            
            # Get tomorrow's date as default
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            print(f"🆓 Checking free times for tomorrow ({tomorrow}):")
            
            await self.show_free_times(tomorrow)
            
            print(f"\n💡 To schedule any of the found events:")
            print(f"   python enhanced_calendar_cli.py schedule <event_number> <date> <time>")
            print(f"   Example: python enhanced_calendar_cli.py schedule 1 {tomorrow} 14:00")

    async def run(self):
        """Main CLI runner"""
        if len(sys.argv) < 2:
            self.print_help()
            return
        
        command = sys.argv[1].lower()
        
        if command == "help":
            self.print_help()
            return
        
        elif command == "auth":
            await self.check_auth()
        
        elif command == "search":
            if len(sys.argv) < 3:
                print("❌ Error: Search query required")
                print("Usage: python enhanced_calendar_cli.py search <query>")
                return
            
            query = " ".join(sys.argv[2:])
            await self.search_vintage_events(query)
        
        elif command == "find":
            if len(sys.argv) < 4:
                print("❌ Error: Event type and location required")
                print("Usage: python enhanced_calendar_cli.py find <event_type> <location>")
                return
            
            event_type = sys.argv[2]
            location = sys.argv[3]
            await self.find_specific_events(event_type, location)
        
        elif command == "nearby":
            if len(sys.argv) < 3:
                print("❌ Error: Location required")
                print("Usage: python enhanced_calendar_cli.py nearby <location>")
                return
            
            location = sys.argv[2]
            await self.find_nearby_events(location)
        
        elif command == "calendars":
            await self.list_calendars()
        
        elif command == "events":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            await self.list_events(days)
        
        elif command == "free":
            if len(sys.argv) < 3:
                print("❌ Error: Date required")
                print("Usage: python enhanced_calendar_cli.py free <date>")
                return
            
            date_str = sys.argv[2]
            await self.show_free_times(date_str)
        
        elif command == "conflicts":
            if len(sys.argv) < 5:
                print("❌ Error: Date, time, and duration required")
                print("Usage: python enhanced_calendar_cli.py conflicts <date> <time> <duration>")
                return
            
            date_str = sys.argv[2]
            time_str = sys.argv[3]
            duration = int(sys.argv[4])
            await self.check_conflicts(date_str, time_str, duration)
        
        elif command == "add":
            if len(sys.argv) < 6:
                print("❌ Error: Title, date, time, and duration required")
                print("Usage: python enhanced_calendar_cli.py add <title> <date> <time> <duration>")
                return
            
            title = sys.argv[2]
            date_str = sys.argv[3]
            time_str = sys.argv[4]
            duration = int(sys.argv[5])
            await self.add_event(title, date_str, time_str, duration)
        
        elif command == "schedule":
            if len(sys.argv) < 5:
                print("❌ Error: Event ID, date, and time required")
                print("Usage: python enhanced_calendar_cli.py schedule <event_id> <date> <time>")
                return
            
            event_id = sys.argv[2]
            date_str = sys.argv[3]
            time_str = sys.argv[4]
            await self.schedule_found_event(event_id, date_str, time_str)
        
        elif command == "plan":
            if len(sys.argv) < 3:
                print("❌ Error: Planning query required")
                print("Usage: python enhanced_calendar_cli.py plan <query>")
                return
            
            query = " ".join(sys.argv[2:])
            await self.smart_planning(query)
        
        else:
            print(f"❌ Unknown command: {command}")
            self.print_help()

async def main():
    """Main function"""
    cli = EnhancedCalendarCLI()
    await cli.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Enhanced Calendar operation interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
