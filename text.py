import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def sendText(text, to_number=None):
    """
    Send SMS using Twilio
    """
    try:
        # Get Twilio credentials from environment variables
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if not all([account_sid, auth_token, from_number]):
            raise ValueError("Missing required Twilio environment variables")
        
        # Default to number if not provided
        if not to_number:
            to_number = "+18777804236" 
            
        if not to_number:
            raise ValueError("No recipient phone number provided")
        
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Send the message
        message = client.messages.create(
            body=text,
            from_=from_number,
            to=to_number
        )
        
        print(f"Message sent successfully! SID: {message.sid}")
        return message.sid
        
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
        return None

sendText("Hello, this is a test message.")
