import requests
import os
import json
from anthropic import Anthropic
from prompts import MCP_EXTRACTION_PROMPT
from dotenv import load_dotenv

load_dotenv()

SMITHERY_API_KEY = os.getenv('SMITHERY_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

def extract_mcp_query(natural_text):
    """
    Use Claude to extract the most relevant search terms for finding MCP servers
    """
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    
    prompt = MCP_EXTRACTION_PROMPT.format(natural_text=natural_text)
    
    try:
        response = client.messages.create(
            model="claude-4-sonnet-20250514",
            max_tokens=50,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    except Exception as e:
        print(f"Error calling Claude: {e}")
        return natural_text

def fetchMCP(natural_query) -> dict:
    """
    Fetch MCP servers based on natural language query
    """
    print(f"Original query: {natural_query}")
    
    # Extract search terms using Claude
    search_query = extract_mcp_query(natural_query)
    print(f"Extracted search terms: {search_query}")
    
    url = "https://registry.smithery.ai/servers?q=" + search_query
    headers = {"Authorization": f"Bearer {SMITHERY_API_KEY}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return {} 
    
    serverJson = response.json()
    
    if not serverJson.get('servers') or len(serverJson['servers']) == 0:
        return {} 
    
    servers = serverJson['servers']
    
    sorted_servers = sorted(servers, key=lambda x: x.get('useCount', 0), reverse=True)
    
    top_server = sorted_servers[0]
    
    print(f"Found {len(servers)} servers, returning most popular:")
    print(f"Name: {top_server.get('displayName')}")
    print(f"Use Count: {top_server.get('useCount', 0)}")

    return top_server

if __name__ == "__main__":
    print("MCP Server Search Tool")
    print("Type your request in natural language, or 'quit' to exit")
    
    while True:
        user_input = input("\nEnter your request: ")
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
            
        if user_input.strip():
            try:
                best_server = fetchMCP(user_input)
                if isinstance(best_server, dict):
                    print(f"\nBest server JSON:")
                    print(json.dumps(best_server, indent=2))
                else:
                    print("No servers found or error occurred")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Please enter a valid request")
