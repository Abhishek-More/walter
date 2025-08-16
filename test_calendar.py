#!/usr/bin/env python3
"""
Test script for Google Calendar Python integration
"""

from google_calendar_python_client import GoogleCalendarPythonClient

def test_setup():
    """Test the Google Calendar setup"""
    print("🧪 Testing Google Calendar Python Setup...")
    
    client = GoogleCalendarPythonClient()
    
    try:
        # Test authentication
        print("1️⃣ Testing authentication...")
        auth_result = client.check_auth_status()
        print(f"Auth result: {auth_result}")
        
        if auth_result.get("success") and auth_result.get("authenticated"):
            print("✅ Authentication successful!")
            
            # Test calendar list
            print("2️⃣ Testing calendar list...")
            calendars_result = client.list_calendars()
            print(f"Calendars: {calendars_result}")
            
            # Test event list
            print("3️⃣ Testing event list...")
            events_result = client.list_events(max_results=3)
            print(f"Events: {events_result}")
            
        else:
            print("❌ Authentication failed!")
            print("💡 You may need to complete the OAuth2 flow in your browser")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_setup()
