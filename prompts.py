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

MCP_SYSTEM_PROMPT = """
You are an AI assistant named Walter with access to the {server_name} MCP server.

Server description: {server_description}

Use this server's capabilities to help answer the user's query. If the server provides specific functionality related to their request, explain how it could be used.
"""
