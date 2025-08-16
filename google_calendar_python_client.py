#!/usr/bin/env python3
"""
Google Calendar Python Client

This client integrates with Google Calendar directly using the Google Calendar API
with OAuth2 authentication. No external MCP servers required.
"""

import os
import json
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleCalendarPythonClient:
    """
    Client for interacting with Google Calendar API directly
    """
    
    # OAuth2 scopes for Google Calendar
    SCOPES = [
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/calendar.events'
    ]
    
    def __init__(self, config_file: str = 'config.env', token_file: str = 'token.json'):
        """
        Initialize the Google Calendar client
        
        Args:
            config_file: Path to environment config file
            token_file: Path to store/load OAuth2 tokens
        """
        self.config_file = config_file
        self.token_file = token_file
        self.service = None
        self.creds = None
        
    def _create_credentials_file(self):
        """Create the credentials.json file from environment variables"""
        try:
            # Load environment variables
            from dotenv import load_dotenv
            load_dotenv(self.config_file)
            
            # Get credentials from environment variables
            client_id = os.getenv('GOOGLE_CLIENT_ID')
            client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
            project_id = os.getenv('GOOGLE_PROJECT_ID')
            auth_uri = os.getenv('GOOGLE_AUTH_URI')
            token_uri = os.getenv('GOOGLE_TOKEN_URI')
            auth_provider_x509_cert_url = os.getenv('GOOGLE_AUTH_PROVIDER_X509_CERT_URL')
            redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')
            
            # Validate required environment variables
            if not all([client_id, client_secret, project_id]):
                print("❌ Missing required environment variables. Please check your config.env file.")
                return False
            
            credentials_data = {
                "installed": {
                    "client_id": client_id,
                    "project_id": project_id,
                    "auth_uri": auth_uri or "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": token_uri or "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": auth_provider_x509_cert_url or "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": client_secret,
                    "redirect_uris": [redirect_uri or "http://localhost"]
                }
            }
            
            # Create a temporary credentials file for OAuth flow
            temp_credentials_file = 'temp_google_credentials.json'
            with open(temp_credentials_file, 'w') as f:
                json.dump(credentials_data, f, indent=2)
            
            print(f"✅ Created temporary credentials file from environment variables")
            return temp_credentials_file
            
        except Exception as e:
            print(f"❌ Failed to create credentials file: {str(e)}")
            return False
    
    def authenticate(self) -> bool:
        """
        Authenticate with Google Calendar API using OAuth2
        
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            # Create credentials file from environment variables
            credentials_file = self._create_credentials_file()
            if not credentials_file:
                return False
            
            # Load existing credentials
            if os.path.exists(self.token_file):
                self.creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
            
            # If no valid credentials available, let the user log in
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, self.SCOPES)
                    self.creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open(self.token_file, 'w') as token:
                    token.write(self.creds.to_json())
            
            # Clean up temporary credentials file
            if os.path.exists(credentials_file) and credentials_file.startswith('temp_'):
                try:
                    os.remove(credentials_file)
                except:
                    pass
            
            # Build the service
            self.service = build('calendar', 'v3', credentials=self.creds)
            print("✅ Google Calendar authentication successful!")
            return True
            
        except Exception as e:
            print(f"❌ Authentication failed: {str(e)}")
            return False
    
    def check_auth_status(self) -> Dict[str, Any]:
        """
        Check the current authentication status
        
        Returns:
            Dictionary with authentication status
        """
        try:
            if not self.service:
                if not self.authenticate():
                    return {"success": False, "error": "Authentication failed"}
            
            # Try to make a simple API call to verify authentication
            calendar_list = self.service.calendarList().list().execute()
            
            return {
                "success": True,
                "authenticated": True,
                "calendars_count": len(calendar_list.get('items', [])),
                "message": "Successfully authenticated with Google Calendar API"
            }
            
        except HttpError as e:
            if e.resp.status == 401:
                return {
                    "success": False,
                    "authenticated": False,
                    "error": "Authentication expired or invalid"
                }
            else:
                return {
                    "success": False,
                    "error": f"API error: {str(e)}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Authentication check failed: {str(e)}"
            }
    
    def list_calendars(self, show_hidden: bool = False) -> Dict[str, Any]:
        """
        List all accessible calendars
        
        Args:
            show_hidden: Whether to show hidden calendars
            
        Returns:
            Dictionary with calendar list
        """
        try:
            if not self.service:
                if not self.authenticate():
                    return {"success": False, "error": "Authentication failed"}
            
            # Get calendar list
            calendar_list = self.service.calendarList().list().execute()
            calendars = calendar_list.get('items', [])
            
            # Filter hidden calendars if requested
            if not show_hidden:
                calendars = [cal for cal in calendars if not cal.get('hidden', False)]
            
            # Format calendar data
            formatted_calendars = []
            for cal in calendars:
                formatted_calendars.append({
                    'id': cal.get('id'),
                    'summary': cal.get('summary'),
                    'description': cal.get('description'),
                    'location': cal.get('location'),
                    'timezone': cal.get('timeZone'),
                    'primary': cal.get('primary', False),
                    'access_role': cal.get('accessRole')
                })
            
            return {
                "success": True,
                "calendars": formatted_calendars,
                "total_count": len(formatted_calendars)
            }
            
        except HttpError as e:
            return {
                "success": False,
                "error": f"API error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"List calendars failed: {str(e)}"
            }
    
    def list_events(self, calendar_id: str = "primary", 
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
            if not self.service:
                if not self.authenticate():
                    return {"success": False, "error": "Authentication failed"}
            
            # Set default time range if not provided
            if not time_min:
                time_min = datetime.now().isoformat() + "Z"
            if not time_max:
                time_max = (datetime.now() + timedelta(days=7)).isoformat() + "Z"
            
            # Get events
            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            # Format event data
            formatted_events = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                
                formatted_events.append({
                    'id': event.get('id'),
                    'summary': event.get('summary'),
                    'description': event.get('description'),
                    'location': event.get('location'),
                    'start': start,
                    'end': end,
                    'all_day': 'date' in event['start'],
                    'attendees': [att.get('email') for att in event.get('attendees', [])],
                    'status': event.get('status')
                })
            
            return {
                "success": True,
                "events": formatted_events,
                "total_count": len(formatted_events),
                "time_range": {"min": time_min, "max": time_max}
            }
            
        except HttpError as e:
            return {
                "success": False,
                "error": f"API error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"List events failed: {str(e)}"
            }
    
    def create_event(self, calendar_id: str = "primary",
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
            if not self.service:
                if not self.authenticate():
                    return {"success": False, "error": "Authentication failed"}
            
            # Prepare event data
            event = {
                'summary': summary,
                'description': description,
                'location': location,
                'start': {
                    'dateTime': start_time,
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': 'UTC',
                }
            }
            
            # Add attendees if provided
            if attendees:
                event['attendees'] = [{'email': email} for email in attendees]
            
            # Create the event
            event_result = self.service.events().insert(
                calendarId=calendar_id,
                body=event
            ).execute()
            
            return {
                "success": True,
                "event": {
                    'id': event_result.get('id'),
                    'summary': event_result.get('summary'),
                    'start': event_result.get('start'),
                    'end': event_result.get('end'),
                    'html_link': event_result.get('htmlLink')
                },
                "created": True
            }
            
        except HttpError as e:
            return {
                "success": False,
                "error": f"API error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Create event failed: {str(e)}"
            }
    
    def check_availability(self, calendar_id: str = "primary",
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
            events_result = self.list_events(
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
                    event_start = event.get('start')
                    event_end = event.get('end')
                    
                    if event_start and event_end:
                        # Check for overlap
                        if (start_time < event_end and end_time > event_start):
                            conflicts.append({
                                "summary": event.get('summary', 'Unknown Event'),
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

# Example usage and testing
async def main():
    """Main function to demonstrate Google Calendar client capabilities"""
    print("📅 Starting Google Calendar Python Client Demo...")
    
    client = GoogleCalendarPythonClient()
    
    # Test 1: Check authentication status
    print("\n1️⃣ Testing Authentication Status...")
    auth_result = client.check_auth_status()
    if auth_result["success"]:
        print(f"✅ Auth check successful!")
        print(f"   Status: {auth_result}")
    else:
        print(f"❌ Auth check failed: {auth_result['error']}")
        return
    
    # Test 2: List calendars
    print("\n2️⃣ Testing Calendar List...")
    calendars_result = client.list_calendars()
    if calendars_result["success"]:
        print(f"✅ Calendar list successful!")
        calendars = calendars_result.get("calendars", [])
        print(f"   Found {len(calendars)} calendars")
        
        for i, cal in enumerate(calendars[:3], 1):  # Show first 3
            print(f"   - {cal.get('summary', 'Unknown')}: {cal.get('id', 'No ID')}")
    else:
        print(f"❌ Calendar list failed: {calendars_result['error']}")
    
    # Test 3: List events
    print("\n3️⃣ Testing Event List...")
    events_result = client.list_events(max_results=5)
    if events_result["success"]:
        print(f"✅ Event list successful!")
        events = events_result.get("events", [])
        print(f"   Found {len(events)} events")
        
        for i, event in enumerate(events[:3], 1):  # Show first 3
            print(f"   - {event.get('summary', 'Unknown')}: {event.get('start', 'No time')}")
    else:
        print(f"❌ Event list failed: {events_result['error']}")
    
    # Test 4: Check availability
    print("\n4️⃣ Testing Availability Check...")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    start_time = f"{tomorrow}T10:00:00Z"
    end_time = f"{tomorrow}T11:00:00Z"
    
    availability_result = client.check_availability(
        start_time=start_time,
        end_time=end_time,
        duration_minutes=60
    )
    
    if availability_result["success"]:
        print(f"✅ Availability check successful!")
        print(f"   Available: {availability_result['available']}")
        if availability_result['conflicts']:
            print(f"   Conflicts: {len(availability_result['conflicts'])}")
        if availability_result['available_slots']:
            print(f"   Available slots: {len(availability_result['available_slots'])}")
    else:
        print(f"❌ Availability check failed: {availability_result['error']}")
    
    print("\n🎉 Google Calendar Python Client Demo Complete!")
    print("💡 You can now integrate calendar functionality with event planning!")

if __name__ == "__main__":
    # Run the demo
    main()
