#!/usr/bin/env python3
"""
Google Calendar OAuth2 Setup Script

This script helps you set up authentication for Google Calendar MCP
"""

import asyncio
import mcp
from mcp.client.streamable_http import streamablehttp_client

async def setup_calendar_auth():
    """Set up Google Calendar OAuth2 authentication"""
    print("🔐 Setting up Google Calendar OAuth2 Authentication...")
    
    # Your MCP server details
    smithery_api_key = "9775d396-48d3-4dd7-9a44-9fe04940ba16"
    smithery_profile = "grateful-crayfish-oQVqqO"
    url = f"https://server.smithery.ai/@goldk3y/google-calendar-mcp/mcp?api_key={smithery_api_key}&profile={smithery_profile}"
    
    try:
        async with streamablehttp_client(url) as (read_stream, write_stream, _):
            async with mcp.ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                print("✅ Connected to Google Calendar MCP server")
                
                # Step 1: Generate OAuth URL
                print("\n1️⃣ Generating OAuth2 authorization URL...")
                try:
                    oauth_result = await session.call_tool("generate_oauth_url", {
                        "scopes": ["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/calendar.events"],
                        "access_type": "offline"
                    })
                    
                    if hasattr(oauth_result, 'content') and oauth_result.content:
                        oauth_url = oauth_result.content[0].text
                        print(f"✅ OAuth URL generated!")
                        print(f"🔗 Please visit this URL to authorize:")
                        print(f"   {oauth_url}")
                        print(f"\n📝 After authorization, you'll get a code to exchange for tokens")
                        
                        # Step 2: Get authorization code from user
                        auth_code = input("\n🔑 Enter the authorization code you received: ").strip()
                        
                        if auth_code:
                            print(f"\n2️⃣ Exchanging authorization code for tokens...")
                            
                            # Step 3: Exchange code for tokens
                            token_result = await session.call_tool("exchange_auth_code", {
                                "auth_code": auth_code
                            })
                            
                            if hasattr(token_result, 'content') and token_result.content:
                                token_response = token_result.content[0].text
                                print(f"✅ Token exchange successful!")
                                print(f"📋 Response: {token_response}")
                                
                                # Step 4: Check auth status
                                print(f"\n3️⃣ Checking authentication status...")
                                auth_check = await session.call_tool("check_auth_status", {
                                    "random_string": "check"
                                })
                                
                                if hasattr(auth_check, 'content') and auth_check.content:
                                    auth_status = auth_check.content[0].text
                                    print(f"📊 Auth status: {auth_status}")
                                    
                                    if "authenticated" in auth_status.lower():
                                        print("🎉 Authentication setup complete!")
                                        print("💡 You can now use Google Calendar features")
                                    else:
                                        print("⚠️ Authentication may not be complete")
                                else:
                                    print("❌ Could not check auth status")
                            else:
                                print("❌ Token exchange failed")
                        else:
                            print("❌ No authorization code provided")
                    else:
                        print("❌ Could not generate OAuth URL")
                        
                except Exception as e:
                    print(f"❌ OAuth setup failed: {str(e)}")
                    print("💡 Make sure the MCP server supports OAuth2 tools")
                
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")

if __name__ == "__main__":
    print("🚀 Google Calendar OAuth2 Setup")
    print("=" * 50)
    
    try:
        asyncio.run(setup_calendar_auth())
    except KeyboardInterrupt:
        print("\n👋 Setup interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
