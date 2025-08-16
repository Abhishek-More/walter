#!/usr/bin/env python3
"""
Google Calendar CLI

Command-line interface for Google Calendar operations
"""

import asyncio
import sys
from datetime import datetime, timedelta
from google_calendar_client import GoogleCalendarClient

def print_help():
    """Print help information"""
    print("""
📅 Google Calendar CLI

Usage:
  python calendar_cli.py <command> [options]

Commands:
  auth                                    - Check authentication status
  calendars                               - List all calendars
  events [calendar_id] [days]             - List events (default: primary calendar, 7 days)
  check <date> <duration>                 - Check availability for a date
  suggest <date> <duration>               - Suggest available time slots
  create <title> <date> <time> <duration> - Create a new event
  help                                    - Show this help message

Examples:
  python calendar_cli.py auth
  python calendar_cli.py calendars
  python calendar_cli.py events primary 3
  python calendar_cli.py check 2025-08-15 90
  python calendar_cli.py suggest 2025-08-15 120
  python calendar_cli.py create "Vintage Market" 2025-08-15 "14:00" 180

Date Format: YYYY-MM-DD (e.g., 2025-08-15)
Time Format: HH:MM (e.g., 14:00 for 2:00 PM)
Duration: Minutes (e.g., 180 for 3 hours)

Help:
  python calendar_cli.py help
""")

def parse_datetime(date_str: str, time_str: str = "00:00") -> str:
    """
    Parse date and time into ISO format
    
    Args:
        date_str: Date in YYYY-MM-DD format
        time_str: Time in HH:MM format
        
    Returns:
        ISO formatted datetime string
    """
    try:
        # Parse date and time
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        time_obj = datetime.strptime(time_str, "%H:%M")
        
        # Combine date and time
        combined = date_obj.replace(
            hour=time_obj.hour,
            minute=time_obj.minute,
            second=0,
            microsecond=0
        )
        
        return combined.isoformat() + "Z"
    except ValueError as e:
        raise ValueError(f"Invalid date/time format: {e}")

async def check_auth():
    """Check authentication status"""
    print("🔐 Checking Google Calendar authentication...")
    
    client = GoogleCalendarClient()
    result = await client.check_auth_status()
    
    if result["success"]:
        print("✅ Authentication successful!")
        auth_status = result["auth_status"]
        print(f"   Status: {auth_status}")
    else:
        print(f"❌ Authentication failed: {result['error']}")
        print("💡 You may need to set up OAuth2 authentication")

async def list_calendars():
    """List all calendars"""
    print("📅 Listing Google Calendars...")
    
    client = GoogleCalendarClient()
    result = await client.list_calendars()
    
    if result["success"]:
        calendars = result.get("calendars", [])
        print(f"✅ Found {len(calendars)} calendars:")
        
        for i, cal in enumerate(calendars, 1):
            print(f"\n{i}. {cal.get('summary', 'Unknown Calendar')}")
            print(f"   ID: {cal.get('id', 'No ID')}")
            print(f"   Description: {cal.get('description', 'No description')}")
            print(f"   Primary: {'Yes' if cal.get('primary', False) else 'No'}")
    else:
        print(f"❌ Failed to list calendars: {result['error']}")

async def list_events(calendar_id: str = "primary", days: int = 7):
    """List events from a calendar"""
    print(f"📋 Listing events from calendar: {calendar_id}")
    print(f"📅 Time range: Next {days} days")
    
    client = GoogleCalendarClient()
    
    # Calculate time range
    now = datetime.now()
    time_min = now.isoformat() + "Z"
    time_max = (now + timedelta(days=days)).isoformat() + "Z"
    
    result = await client.list_events(
        calendar_id=calendar_id,
        time_min=time_min,
        time_max=time_max,
        max_results=20
    )
    
    if result["success"]:
        events = result.get("events", [])
        print(f"✅ Found {len(events)} events:")
        
        for i, event in enumerate(events, 1):
            print(f"\n{i}. {event.get('summary', 'No title')}")
            
            # Parse start time
            start = event.get("start", {})
            if start.get("dateTime"):
                start_time = datetime.fromisoformat(start["dateTime"].replace("Z", "+00:00"))
                print(f"   🕐 Start: {start_time.strftime('%Y-%m-%d %I:%M %p')}")
            elif start.get("date"):
                start_date = datetime.fromisoformat(start["date"])
                print(f"   📅 Date: {start_date.strftime('%Y-%m-%d')} (All day)")
            
            # Parse end time
            end = event.get("end", {})
            if end.get("dateTime"):
                end_time = datetime.fromisoformat(end["dateTime"].replace("Z", "+00:00"))
                print(f"   🕐 End: {end_time.strftime('%I:%M %p')}")
            
            # Show location if available
            if event.get("location"):
                print(f"   📍 Location: {event['location']}")
            
            # Show description if available
            if event.get("description"):
                desc = event["description"][:100] + "..." if len(event["description"]) > 100 else event["description"]
                print(f"   📝 Description: {desc}")
    else:
        print(f"❌ Failed to list events: {result['error']}")

async def check_availability(date_str: str, duration_minutes: int):
    """Check availability for a specific date and duration"""
    print(f"🔍 Checking availability for {date_str}")
    print(f"⏱️ Duration: {duration_minutes} minutes")
    
    client = GoogleCalendarClient()
    
    try:
        # Parse date and create time range
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        start_time = date_obj.replace(hour=9, minute=0, second=0, microsecond=0).isoformat() + "Z"
        end_time = date_obj.replace(hour=17, minute=0, second=0, microsecond=0).isoformat() + "Z"
        
        result = await client.check_availability(
            calendar_id="primary",
            start_time=start_time,
            end_time=end_time,
            duration_minutes=duration_minutes
        )
        
        if result["success"]:
            if result["available"]:
                print("✅ Time slot is available!")
            else:
                print("❌ Time slot has conflicts:")
                for conflict in result["conflicts"]:
                    print(f"   - {conflict['summary']}: {conflict['start']} to {conflict['end']}")
            
            print(f"\n📊 Summary:")
            print(f"   Available: {result['available']}")
            print(f"   Conflicts: {len(result['conflicts'])}")
            print(f"   Available slots: {len(result['available_slots'])}")
        else:
            print(f"❌ Availability check failed: {result['error']}")
            
    except ValueError as e:
        print(f"❌ Invalid date format: {e}")
        print("💡 Use YYYY-MM-DD format (e.g., 2025-08-15)")

async def suggest_times(date_str: str, duration_minutes: int):
    """Suggest available time slots for a date"""
    print(f"💡 Suggesting available times for {date_str}")
    print(f"⏱️ Duration needed: {duration_minutes} minutes")
    
    client = GoogleCalendarClient()
    
    try:
        result = await client.suggest_event_time(
            calendar_id="primary",
            preferred_date=date_str,
            duration_minutes=duration_minutes,
            preferred_hours=(9, 17)  # 9 AM to 5 PM
        )
        
        if result["success"]:
            slots = result["available_slots"]
            print(f"✅ Found {len(slots)} available time slots:")
            
            for i, slot in enumerate(slots[:10], 1):  # Show first 10 slots
                print(f"   {i}. {slot['start_time']} - {slot['end_time']}")
            
            if len(slots) > 10:
                print(f"   ... and {len(slots) - 10} more slots")
            
            print(f"\n📊 Summary:")
            print(f"   Date: {result['preferred_date']}")
            print(f"   Duration: {result['duration_minutes']} minutes")
            print(f"   Total available slots: {result['total_slots']}")
        else:
            print(f"❌ Time suggestion failed: {result['error']}")
            
    except ValueError as e:
        print(f"❌ Invalid date format: {e}")
        print("💡 Use YYYY-MM-DD format (e.g., 2025-08-15)")

async def create_event(title: str, date_str: str, time_str: str, duration_minutes: int):
    """Create a new calendar event"""
    print(f"➕ Creating new calendar event...")
    print(f"📝 Title: {title}")
    print(f"📅 Date: {date_str}")
    print(f"🕐 Time: {time_str}")
    print(f"⏱️ Duration: {duration_minutes} minutes")
    
    client = GoogleCalendarClient()
    
    try:
        # Parse start time
        start_time = parse_datetime(date_str, time_str)
        
        # Calculate end time
        start_obj = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
        end_obj = start_obj + timedelta(minutes=duration_minutes)
        end_time = end_obj.isoformat() + "Z"
        
        result = await client.create_event(
            calendar_id="primary",
            summary=title,
            start_time=start_time,
            end_time=end_time,
            description=f"Event created via CLI - Duration: {duration_minutes} minutes"
        )
        
        if result["success"]:
            print("✅ Event created successfully!")
            event = result["event"]
            print(f"   Event ID: {event.get('id', 'Unknown')}")
            print(f"   Start: {start_obj.strftime('%Y-%m-%d %I:%M %p')}")
            print(f"   End: {end_obj.strftime('%I:%M %p')}")
            print(f"   Calendar: primary")
        else:
            print(f"❌ Failed to create event: {result['error']}")
            
    except ValueError as e:
        print(f"❌ Error: {e}")

async def main():
    """Main CLI function"""
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        print_help()
        return
    
    elif command == "auth":
        await check_auth()
    
    elif command == "calendars":
        await list_calendars()
    
    elif command == "events":
        calendar_id = sys.argv[2] if len(sys.argv) > 2 else "primary"
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 7
        await list_events(calendar_id, days)
    
    elif command == "check":
        if len(sys.argv) < 4:
            print("❌ Error: Date and duration required")
            print("Usage: python calendar_cli.py check <date> <duration>")
            return
        
        date_str = sys.argv[2]
        duration = int(sys.argv[3])
        await check_availability(date_str, duration)
    
    elif command == "suggest":
        if len(sys.argv) < 4:
            print("❌ Error: Date and duration required")
            print("Usage: python calendar_cli.py suggest <date> <duration>")
            return
        
        date_str = sys.argv[2]
        duration = int(sys.argv[3])
        await suggest_times(date_str, duration)
    
    elif command == "create":
        if len(sys.argv) < 6:
            print("❌ Error: Title, date, time, and duration required")
            print("Usage: python calendar_cli.py create <title> <date> <time> <duration>")
            return
        
        title = sys.argv[2]
        date_str = sys.argv[3]
        time_str = sys.argv[4]
        duration = int(sys.argv[5])
        await create_event(title, date_str, time_str, duration)
    
    else:
        print(f"❌ Unknown command: {command}")
        print_help()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Calendar operation interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
