"""
Prompts for various AI interactions
"""

MCP_EXTRACTION_PROMPT = """
Extract the main object or service the user wants to interact with from this request: "{natural_text}"

Return only the core noun that represents what they're looking for, in lowercase.

Examples:
"Find me Airbnbs in NYC" -> "airbnb"
"I want to find clothes" -> "clothes"  
"Search for restaurants" -> "restaurant"
"Connect to database" -> "database"
"Send an email" -> "email"
"Browse the web" -> "browser"

Request: "{natural_text}"
Core object:
"""
