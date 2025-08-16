#!/usr/bin/env python3
"""
Demo script for Enhanced Calendar CLI

This script demonstrates the key features of the enhanced CLI
"""

import asyncio
from enhanced_calendar_cli import EnhancedCalendarCLI

async def demo():
    """Demonstrate the enhanced CLI features"""
    print("🎭 Enhanced Calendar CLI Demo")
    print("=" * 50)
    
    cli = EnhancedCalendarCLI()
    
    # Demo 1: Check authentication
    print("\n1️⃣ Checking Google Calendar authentication...")
    await cli.check_auth()
    
    # Demo 2: Show your calendars
    print("\n2️⃣ Listing your calendars...")
    await cli.list_calendars()
    
    # Demo 3: Show upcoming events
    print("\n3️⃣ Showing your upcoming events...")
    await cli.list_events(7)  # Next 7 days
    
    # Demo 4: Check when you're free tomorrow
    print("\n4️⃣ Checking your availability for tomorrow...")
    from datetime import datetime, timedelta
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    await cli.show_free_times(tomorrow)
    
    # Demo 5: Search for vintage events
    print("\n5️⃣ Searching for vintage events near you...")
    await cli.search_vintage_events("vintage markets antique fairs brooklyn manhattan", 5)
    
    print("\n🎉 Demo complete!")
    print("\n💡 Try these commands:")
    print("   python enhanced_calendar_cli.py help")
    print("   python enhanced_calendar_cli.py search 'vintage popup shops'")
    print("   python enhanced_calendar_cli.py free 2025-08-20")
    print("   python enhanced_calendar_cli.py plan 'vintage markets this weekend'")

if __name__ == "__main__":
    asyncio.run(demo())
