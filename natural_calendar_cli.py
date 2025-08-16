#!/usr/bin/env python3
"""
Natural Language Calendar CLI

This CLI understands natural language queries and integrates with multiple MCPs:
- Google Calendar for scheduling and conflicts
- Exa Search for finding events
- Weather for outdoor event planning
- Enhanced event search for comprehensive results
"""

import asyncio
import sys
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from google_calendar_python_client import GoogleCalendarPythonClient
from exa_search_app import ExaSearchClient
from weather_client import WeatherClient
from enhanced_event_search import EnhancedEventSearch

class NaturalLanguageCalendarCLI:
    """
    Natural language CLI that understands complex queries and integrates multiple MCPs
    """
    
    def __init__(self):
        """Initialize the natural language CLI"""
        self.calendar_client = GoogleCalendarPythonClient()
        self.exa_client = ExaSearchClient()
        self.weather_client = WeatherClient()
        self.enhanced_search = EnhancedEventSearch()
        
        # Common patterns for natural language parsing
        self.patterns = {
            'event_type': [
                r'vintage\s+markets?', r'antique\s+fairs?', r'vintage\s+festivals?',
                r'vintage\s+popups?', r'vintage\s+shops?', r'flea\s+markets?',
                r'vintage\s+events?', r'vintage\s+shows?'
            ],
            'location': [
                r'in\s+([^,\n]+)', r'near\s+([^,\n]+)', r'at\s+([^,\n]+)',
                r'around\s+([^,\n]+)', r'([^,\n]*nyc[^,\n]*)', r'([^,\n]*brooklyn[^,\n]*)',
                r'([^,\n]*manhattan[^,\n]*)', r'([^,\n]*queens[^,\n]*)'
            ],
            'time_constraint': [
                r'this\s+weekend', r'next\s+weekend', r'this\s+week', r'next\s+week',
                r'today', r'tomorrow', r'([^,\n]*august[^,\n]*)', r'([^,\n]*september[^,\n]*)'
            ],
            'starting_point': [
                r'starting\s+from\s+([^,\n]+)', r'i\'m\s+at\s+([^,\n]+)',
                r'from\s+([^,\n]+)', r'at\s+([^,\n]+?street[^,\n]*)',
                r'at\s+([^,\n]+?avenue[^,\n]*)', r'at\s+([^,\n]+?road[^,\n]*)'
            ],
            'travel_time': [
                r'(\d+)\s+min(?:ute)?s?', r'(\d+)\s+min', r'no\s+more\s+than\s+(\d+)\s+min',
                r'less\s+than\s+(\d+)\s+min', r'within\s+(\d+)\s+min'
            ],
            'conflict_check': [
                r'conflict', r'conflicts?', r'what\s+i\s+have', r'my\s+events?',
                r'current\s+events?', r'this\s+weekend'
            ]
        }
    
    def print_help(self):
        """Print help information"""
        print("""
🧠 Natural Language Calendar CLI

This CLI understands natural language queries and integrates with multiple MCPs
to provide comprehensive event planning and scheduling.

Usage:
  python natural_calendar_cli.py "<your natural language query>"

Examples:
  python natural_calendar_cli.py "find me vintage markets in NYC this weekend"
  python natural_calendar_cli.py "I'm looking for antique fairs near Brooklyn, starting from 162 East 82nd Street, max 30 min travel"
  python natural_calendar_cli.py "Can you find vintage popup shops this weekend? I'm at 162 East 82nd Street and don't want to travel more than 30 mins"
  python natural_calendar_cli.py "Show me vintage festivals that conflict with my current events this weekend"

The CLI will:
1. Parse your natural language query
2. Search for relevant events using multiple sources
3. Check your calendar for conflicts
4. Consider travel time from your location
5. Provide weather information for outdoor events
6. Suggest optimal scheduling

Natural Language Features:
- Event types: vintage markets, antique fairs, popup shops, etc.
- Locations: NYC, Brooklyn, Manhattan, Queens, specific addresses
- Time constraints: this weekend, next week, specific dates
- Travel constraints: starting location, maximum travel time
- Conflict checking: automatic calendar conflict detection
- Weather integration: outdoor event planning
""")

    def parse_natural_language(self, query: str) -> Dict[str, Any]:
        """
        Parse natural language query into structured data
        
        Args:
            query: Natural language query string
            
        Returns:
            Dictionary with parsed information
        """
        query_lower = query.lower()
        parsed = {
            'event_type': None,
            'location': 'nyc',
            'time_constraint': None,
            'starting_point': None,
            'travel_time': None,
            'check_conflicts': False,
            'original_query': query
        }
        
        # Extract event type
        for pattern in self.patterns['event_type']:
            match = re.search(pattern, query_lower)
            if match:
                parsed['event_type'] = match.group(0)
                break
        
        # Extract location
        for pattern in self.patterns['location']:
            match = re.search(pattern, query_lower)
            if match:
                location = match.group(1) if len(match.groups()) > 0 else match.group(0)
                parsed['location'] = location.strip()
                break
        
        # Extract time constraint
        for pattern in self.patterns['time_constraint']:
            match = re.search(pattern, query_lower)
            if match:
                parsed['time_constraint'] = match.group(0)
                break
        
        # Extract starting point
        for pattern in self.patterns['starting_point']:
            match = re.search(pattern, query_lower)
            if match:
                starting_point = match.group(1) if len(match.groups()) > 0 else match.group(0)
                parsed['starting_point'] = starting_point.strip()
                break
        
        # Extract travel time constraint
        for pattern in self.patterns['travel_time']:
            match = re.search(pattern, query_lower)
            if match:
                parsed['travel_time'] = int(match.group(1))
                break
        
        # Check if user wants conflict checking
        for pattern in self.patterns['conflict_check']:
            if re.search(pattern, query_lower):
                parsed['check_conflicts'] = True
                break
        
        return parsed

    async def process_natural_language_query(self, query: str):
        """
        Process a natural language query and provide comprehensive results
        
        Args:
            query: Natural language query string
        """
        print(f"🧠 Processing your request: '{query}'")
        print("=" * 60)
        
        # Parse the natural language query
        parsed = self.parse_natural_language(query)
        
        print("📝 Parsed your request:")
        print(f"   Event type: {parsed['event_type'] or 'vintage events'}")
        print(f"   Location: {parsed['location']}")
        print(f"   Time: {parsed['time_constraint'] or 'upcoming'}")
        print(f"   Starting point: {parsed['starting_point'] or 'Not specified'}")
        print(f"   Max travel time: {parsed['travel_time'] or 'No limit'} minutes")
        print(f"   Check conflicts: {'Yes' if parsed['check_conflicts'] else 'No'}")
        
        # Step 1: Check calendar authentication
        print(f"\n1️⃣ Checking Google Calendar access...")
        auth_result = self.calendar_client.check_auth_status()
        if not auth_result.get("success") or not auth_result.get("authenticated"):
            print("❌ Google Calendar access required. Please authenticate first.")
            return
        
        print("✅ Google Calendar access confirmed!")
        
        # Step 2: Search for events
        print(f"\n2️⃣ Searching for {parsed['event_type'] or 'vintage events'}...")
        search_query = f"{parsed['event_type'] or 'vintage markets antique fairs'} {parsed['location']} {parsed['time_constraint'] or 'upcoming'}"
        
        events_result = await self.exa_client.web_search(search_query, 15)
        
        if not events_result["success"]:
            print(f"❌ Event search failed: {events_result.get('error', 'Unknown error')}")
            return
        
        events = events_result.get("results", [])
        print(f"✅ Found {len(events)} potential events!")
        
        # Step 3: Check calendar conflicts if requested
        if parsed['check_conflicts']:
            print(f"\n3️⃣ Checking your calendar for conflicts...")
            await self._check_calendar_conflicts(parsed)
        
        # Step 4: Show event details with travel considerations
        print(f"\n4️⃣ Event Details:")
        await self._display_events_with_context(events, parsed)
        
        # Step 5: Provide scheduling suggestions
        print(f"\n5️⃣ Scheduling Suggestions:")
        await self._provide_scheduling_suggestions(parsed)
        
        # Step 6: Interactive event selection and scheduling
        print(f"\n6️⃣ 🎯 Let's Schedule Some Events!")
        await self._interactive_event_scheduling(parsed)
        
        print(f"\n🎉 Query processing complete!")
        print(f"💡 You can also manually schedule events using:")
        print(f"   python natural_calendar_cli.py schedule <event_number> <date> <time>")

    async def _check_calendar_conflicts(self, parsed: Dict[str, Any]):
        """Check calendar for conflicts during the specified time period"""
        try:
            # Determine time range based on constraint
            time_range = self._get_time_range_from_constraint(parsed['time_constraint'])
            
            if not time_range:
                print("   ⚠️ Could not determine time range for conflict checking")
                return
            
            start_time, end_time = time_range
            print(f"   📅 Checking conflicts from {start_time.strftime('%Y-%m-%d')} to {end_time.strftime('%Y-%m-%d')}")
            
            # Get events in the time range
            events_result = self.calendar_client.list_events(
                time_min=start_time.isoformat() + "Z",
                time_max=end_time.isoformat() + "Z",
                max_results=50
            )
            
            if events_result["success"]:
                events = events_result.get("events", [])
                if events:
                    print(f"   📋 You have {len(events)} events during this period:")
                    for event in events[:5]:  # Show first 5
                        start = event.get('start', '')
                        if 'T' in start:
                            start_time = datetime.fromisoformat(start.replace('Z', '+00:00'))
                            print(f"      - {event.get('summary', 'Unknown')}: {start_time.strftime('%Y-%m-%d %I:%M %p')}")
                        else:
                            start_date = datetime.fromisoformat(start)
                            print(f"      - {event.get('summary', 'Unknown')}: {start_date.strftime('%Y-%m-%d')} (All day)")
                    
                    if len(events) > 5:
                        print(f"      ... and {len(events) - 5} more events")
                else:
                    print("   ✅ No conflicts found - you're free during this period!")
            else:
                print(f"   ❌ Failed to check calendar: {events_result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"   ❌ Error checking conflicts: {str(e)}")

    def _get_time_range_from_constraint(self, time_constraint: str) -> Optional[Tuple[datetime, datetime]]:
        """Convert time constraint to actual datetime range"""
        if not time_constraint:
            return None
        
        now = datetime.now()
        
        if 'this weekend' in time_constraint.lower():
            # Find this Saturday
            days_until_saturday = (5 - now.weekday()) % 7
            if days_until_saturday == 0:  # Today is Saturday
                saturday = now
            else:
                saturday = now + timedelta(days=days_until_saturday)
            
            sunday = saturday + timedelta(days=1)
            start = saturday.replace(hour=0, minute=0, second=0, microsecond=0)
            end = sunday.replace(hour=23, minute=59, second=59, microsecond=999999)
            
        elif 'next weekend' in time_constraint.lower():
            # Find next Saturday
            days_until_saturday = (5 - now.weekday()) % 7
            next_saturday = now + timedelta(days=days_until_saturday + 7)
            next_sunday = next_saturday + timedelta(days=1)
            start = next_saturday.replace(hour=0, minute=0, second=0, microsecond=0)
            end = next_sunday.replace(hour=23, minute=59, second=59, microsecond=999999)
            
        elif 'this week' in time_constraint.lower():
            # This week (Monday to Sunday)
            days_until_monday = (0 - now.weekday()) % 7
            monday = now + timedelta(days=days_until_monday)
            sunday = monday + timedelta(days=6)
            start = monday.replace(hour=0, minute=0, second=0, microsecond=0)
            end = sunday.replace(hour=23, minute=59, second=59, microsecond=999999)
            
        elif 'next week' in time_constraint.lower():
            # Next week
            days_until_monday = (0 - now.weekday()) % 7
            next_monday = now + timedelta(days=days_until_monday + 7)
            next_sunday = next_monday + timedelta(days=6)
            start = next_monday.replace(hour=0, minute=0, second=0, microsecond=0)
            end = next_sunday.replace(hour=23, minute=59, second=59, microsecond=999999)
            
        elif 'tomorrow' in time_constraint.lower():
            tomorrow = now + timedelta(days=1)
            start = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
            end = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999999)
            
        else:
            # Default to next 7 days
            start = now
            end = now + timedelta(days=7)
        
        return start, end

    async def _display_events_with_context(self, events: List[Dict], parsed: Dict[str, Any]):
        """Display events with travel time and weather context"""
        # Store events for potential scheduling
        self.found_events = events[:10]  # Keep first 10 events
        
        print(f"\n🎭 Here are your vintage event options:")
        print("=" * 50)
        print(f"🌟 Found {len(events[:10])} amazing vintage adventures for you!")
        print(f"💫 All within your travel constraints and ready to explore!")
        
        for i, event in enumerate(self.found_events, 1):
            event['event_id'] = i
            
            # Create a fun, engaging display
            print(f"\n{i}. 🎪 {event.get('title', 'Mystery Vintage Event')}")
            
            # Show URL with fun formatting
            if event.get('url'):
                print(f"   🌐 {event['url']}")
            
            # Show content preview with better formatting
            if event.get('content'):
                content = event['content'][:100] + "..." if len(event['content']) > 100 else event['content']
                print(f"   📖 {content}")
            
            # Show source with emoji
            if event.get('source'):
                print(f"   📰 Source: {event['source']}")
            
            # Travel time estimation with fun indicators
            if parsed['starting_point'] and parsed['travel_time']:
                travel_time = "~25-35 minutes (estimated)"
                if parsed['travel_time'] < 30:
                    print(f"   🚇 Travel: {travel_time} ⚠️ Exceeds your {parsed['travel_time']} min limit")
                else:
                    print(f"   🚇 Travel: {travel_time} ✅ Within your {parsed['travel_time']} min limit")
            
            # Add some personality based on event type
            event_title = event.get('title', '').lower()
            if 'bazaar' in event_title:
                print(f"   🛍️ Type: Vintage Bazaar")
            elif 'flea' in event_title:
                print(f"   🐛 Type: Flea Market")
            elif 'popup' in event_title:
                print(f"   🚀 Type: Pop-up Shop")
            elif 'fair' in event_title:
                print(f"   🎡 Type: Vintage Fair")
            else:
                print(f"   🎭 Type: Vintage Event")

    async def _provide_scheduling_suggestions(self, parsed: Dict[str, Any]):
        """Provide intelligent scheduling suggestions"""
        print(f"   📅 Based on your preferences:")
        
        if parsed['starting_point']:
            print(f"      - Starting from: {parsed['starting_point']}")
        
        if parsed['travel_time']:
            print(f"      - Max travel time: {parsed['travel_time']} minutes")
        
        if parsed['time_constraint']:
            print(f"      - Preferred time: {parsed['time_constraint']}")
        
        # Get tomorrow's date for suggestions
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        print(f"\n   💡 Suggested next steps:")
        print(f"      1. Check your availability: python natural_calendar_cli.py free {tomorrow}")
        print(f"      2. Schedule an event: python natural_calendar_cli.py schedule <event_number> <date> <time>")
        print(f"      3. Check for conflicts: python natural_calendar_cli.py conflicts <date> <time> <duration>")

    async def _interactive_event_scheduling(self, parsed: Dict[str, Any]):
        """Interactive event selection and scheduling"""
        if not hasattr(self, 'found_events') or not self.found_events:
            print("   ❌ No events found to schedule")
            return
        
        print(f"   🎪 You found {len(self.found_events)} amazing vintage events!")
        print(f"   💭 Which ones would you like to add to your calendar?")
        
        # Show a summary of your weekend availability
        if parsed.get('time_constraint') and 'weekend' in parsed['time_constraint'].lower():
            print(f"\n   📅 Your Weekend Availability:")
            await self._show_weekend_summary()
        
        # Interactive event selection
        while True:
            print(f"\n   🎯 Choose an event to schedule (1-{len(self.found_events)}) or type:")
            print(f"      - 'all' to see all events again")
            print(f"      - 'done' when you're finished")
            print(f"      - 'skip' to skip scheduling for now")
            
            choice = input(f"\n   🚀 Your choice: ").strip().lower()
            
            if choice == 'done':
                print(f"   ✅ Great! You're all set with your vintage adventures!")
                break
            elif choice == 'skip':
                print(f"   ⏭️ No worries! You can always come back and schedule later.")
                break
            elif choice == 'all':
                await self._display_events_with_context(self.found_events, parsed)
                continue
            elif choice.isdigit():
                event_num = int(choice)
                if 1 <= event_num <= len(self.found_events):
                    await self._schedule_selected_event(event_num, parsed)
                else:
                    print(f"   ❌ Please choose a number between 1 and {len(self.found_events)}")
            else:
                print(f"   🤔 I didn't understand that. Please try again!")

    async def _show_weekend_summary(self):
        """Show a summary of weekend availability"""
        try:
            # Get this weekend's dates
            now = datetime.now()
            days_until_saturday = (5 - now.weekday()) % 7
            if days_until_saturday == 0:  # Today is Saturday
                saturday = now
            else:
                saturday = now + timedelta(days=days_until_saturday)
            sunday = saturday + timedelta(days=1)
            
            sat_str = saturday.strftime('%Y-%m-%d')
            sun_str = sunday.strftime('%Y-%m-%d')
            
            print(f"      🗓️ Saturday ({sat_str}):")
            await self._show_day_availability(sat_str)
            
            print(f"      🗓️ Sunday ({sun_str}):")
            await self._show_day_availability(sun_str)
            
        except Exception as e:
            print(f"      ⚠️ Couldn't check availability: {str(e)}")

    async def _show_day_availability(self, date_str: str):
        """Show availability for a specific day"""
        try:
            # Get events for the day
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            start_of_day = date_obj.replace(hour=9, minute=0, second=0, microsecond=0)
            end_of_day = date_obj.replace(hour=21, minute=0, second=0, microsecond=0)
            
            time_min = start_of_day.isoformat() + "Z"
            time_max = end_of_day.isoformat() + "Z"
            
            events_result = self.calendar_client.list_events(
                time_min=time_min,
                time_max=time_max,
                max_results=20
            )
            
            if events_result["success"]:
                events = events_result.get("events", [])
                if not events:
                    print(f"         ✅ Free all day (9 AM - 9 PM)")
                else:
                    print(f"         📋 {len(events)} events scheduled")
                    for event in events[:3]:  # Show first 3
                        start = event.get('start', '')
                        if 'T' in start:
                            start_time = datetime.fromisoformat(start.replace('Z', '+00:00'))
                            print(f"            • {event.get('summary', 'Unknown')}: {start_time.strftime('%I:%M %p')}")
                        else:
                            print(f"            • {event.get('summary', 'Unknown')}: All day")
                    
                    if len(events) > 3:
                        print(f"            ... and {len(events) - 3} more")
            else:
                print(f"         ⚠️ Couldn't check availability")
                
        except Exception as e:
            print(f"         ⚠️ Error checking availability")

    async def _schedule_selected_event(self, event_num: int, parsed: Dict[str, Any]):
        """Schedule a selected event"""
        event = self.found_events[event_num - 1]
        event_title = event.get('title', 'Unknown Event')
        
        print(f"\n   🎪 Great choice! Let's schedule: {event_title}")
        print(f"   🌟 This looks like an amazing vintage adventure!")
        
        # Ask for date
        print(f"\n   📅 When would you like to go?")
        print(f"      - 'saturday' for this Saturday")
        print(f"      - 'sunday' for this Sunday")
        print(f"      - 'custom' for a specific date")
        
        date_choice = input(f"   🗓️ Date choice: ").strip().lower()
        
        if date_choice == 'saturday':
            # Get this Saturday
            now = datetime.now()
            days_until_saturday = (5 - now.weekday()) % 7
            if days_until_saturday == 0:  # Today is Saturday
                event_date = now
            else:
                event_date = now + timedelta(days=days_until_saturday)
            date_str = event_date.strftime('%Y-%m-%d')
        elif date_choice == 'sunday':
            # Get this Sunday
            now = datetime.now()
            days_until_saturday = (5 - now.weekday()) % 7
            if days_until_saturday == 0:  # Today is Saturday
                event_date = now + timedelta(days=1)
            else:
                event_date = now + timedelta(days=days_until_saturday + 1)
            date_str = event_date.strftime('%Y-%m-%d')
        elif date_choice == 'custom':
            date_str = input(f"   📅 Enter date (YYYY-MM-DD): ").strip()
        else:
            print(f"   ❌ Invalid choice. Let's try again!")
            return
        
        # Ask for time
        print(f"\n   🕐 What time works best for you?")
        print(f"      - 'morning' (9 AM - 12 PM)")
        print(f"      - 'afternoon' (12 PM - 5 PM)")
        print(f"      - 'evening' (5 PM - 9 PM)")
        print(f"      - 'custom' for a specific time")
        
        time_choice = input(f"   ⏰ Time choice: ").strip().lower()
        
        if time_choice == 'morning':
            time_str = "10:00"
        elif time_choice == 'afternoon':
            time_str = "14:00"
        elif time_choice == 'evening':
            time_str = "18:00"
        elif time_choice == 'custom':
            time_str = input(f"   🕐 Enter time (HH:MM): ").strip()
        else:
            print(f"   ❌ Invalid choice. Let's try again!")
            return
        
        # Ask for duration
        print(f"\n   ⏱️ How long do you want to spend there?")
        print(f"      - 'quick' (1-2 hours)")
        print(f"      - 'normal' (2-3 hours)")
        print(f"      - 'long' (3-4 hours)")
        print(f"      - 'custom' for specific duration")
        
        duration_choice = input(f"   ⏱️ Duration choice: ").strip().lower()
        
        if duration_choice == 'quick':
            duration_minutes = 90
        elif duration_choice == 'normal':
            duration_minutes = 150
        elif duration_choice == 'long':
            duration_minutes = 210
        elif duration_choice == 'custom':
            duration_input = input(f"   ⏱️ Enter duration in minutes: ").strip()
            try:
                duration_minutes = int(duration_input)
            except ValueError:
                print(f"   ❌ Invalid duration. Let's try again!")
                return
        else:
            print(f"   ❌ Invalid choice. Let's try again!")
            return
        
        # Confirm and schedule
        print(f"\n   📋 Event Summary:")
        print(f"      🎪 Title: {event_title}")
        print(f"      📅 Date: {date_str}")
        print(f"      🕐 Time: {time_str}")
        print(f"      ⏱️ Duration: {duration_minutes} minutes")
        
        confirm = input(f"\n   ✅ Does this look right? (y/N): ").strip().lower()
        
        if confirm == 'y':
            print(f"   🚀 Adding to your calendar...")
            
            # Check for conflicts first
            try:
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
                
                # Check for conflicts
                conflict_result = self.calendar_client.check_availability(
                    start_time=start_time,
                    end_time=end_time,
                    duration_minutes=duration_minutes
                )
                
                if conflict_result["success"] and not conflict_result["available"]:
                    print(f"   ⚠️ Conflicts detected:")
                    for conflict in conflict_result["conflicts"]:
                        print(f"      - {conflict['summary']}: {conflict['start']} to {conflict['end']}")
                    
                    proceed = input(f"\n   ❓ Do you want to proceed anyway? (y/N): ").strip().lower()
                    if proceed != 'y':
                        print(f"   ❌ Event scheduling cancelled")
                        return
                
                # Create the event
                result = self.calendar_client.create_event(
                    summary=event_title,
                    start_time=start_time,
                    end_time=end_time,
                    description=f"Vintage adventure found via Natural Language CLI! 🎭\nOriginal search: {parsed.get('original_query', 'Unknown')}\nDuration: {duration_minutes} minutes"
                )
                
                if result["success"]:
                    print(f"   🎉 Event added successfully!")
                    print(f"      📅 Event ID: {result['event'].get('id', 'Unknown')}")
                    print(f"      🕐 Start: {start_obj.strftime('%Y-%m-%d %I:%M %p')}")
                    print(f"      🕐 End: {(start_obj + timedelta(minutes=duration_minutes)).strftime('%I:%M %p')}")
                    print(f"      🎭 You're going to have an amazing vintage adventure!")
                else:
                    print(f"   ❌ Failed to add event: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"   ❌ Error scheduling event: {str(e)}")
        else:
            print(f"   ⏭️ No worries! Let's try a different event or time.")

    async def run(self):
        """Main CLI runner"""
        if len(sys.argv) < 2:
            self.print_help()
            return
        
        # Join all arguments as the natural language query
        query = " ".join(sys.argv[1:])
        
        if query.lower() in ['help', '--help', '-h']:
            self.print_help()
            return
        
        # Process the natural language query
        await self.process_natural_language_query(query)

async def main():
    """Main function"""
    cli = NaturalLanguageCalendarCLI()
    await cli.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Natural language processing interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
