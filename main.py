import os
import asyncio
from anthropic import Anthropic
from dotenv import load_dotenv
from search import fetchMCP
from prompts import MCP_SYSTEM_PROMPT
import mcp
from mcp.client.streamable_http import streamablehttp_client

load_dotenv()

SMITHERY_API_KEY = os.getenv('SMITHERY_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')


class MCPEnhancedAssistant:
    def __init__(self):
        self.claude = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.smithery_api_key = SMITHERY_API_KEY 
        self.active_sessions = {}
    
    async def connect_to_mcp_server(self, mcp_server_info):
        """
        Connect to an MCP server from Smithery registry
        """
        # Extract connection info from the server
        server_id = mcp_server_info.get('id')
        server_url = mcp_server_info.get("homepage")
        
        url = f"{server_url}?api_key={self.smithery_api_key}"
        url = url.replace("https://", "https://server.")
        url = "https://server.smithery.ai/@jinkoso/jinko-mcp/mcp?api_key=bb25c9e0-2f85-4bb5-bccf-1adf14a41363&profile=witty-jackal-YJgUWC"
        
        print(f"Connecting to {url}")

        try:
            # Create the connection
            client_context = streamablehttp_client(url)
            print("HI")
            read_stream, write_stream, _ = await client_context.__aenter__()
            print("HEY")
            
            session = mcp.ClientSession(read_stream, write_stream)
            await session.__aenter__()
            print("THERE")
            
            # Initialize
            await session.initialize()

            print("Initialize")
            
            # Get available tools
            tools_result = await session.list_tools()
            tools = [{"name": t.name, "description": t.description} for t in tools_result.tools]
            
            print(f"Connected to {mcp_server_info.get('displayName')}!")
            print(f"Available tools: {', '.join([t['name'] for t in tools])}")
            
            return session, tools
            
        except Exception as e:
            print(f"Error connecting to MCP server: {e}")
            return None, None
    
    async def query_with_mcp_server(self, user_query):
        """
        Find the best MCP server for a query, connect to it, and use it with Claude
        """
        print(f"Finding MCP server for: {user_query}")
        
        # Find the best MCP server using your existing function
        best_server = fetchMCP(user_query)
        
        server_name = best_server.get('displayName', 'Unknown')
        
        print(f"\nUsing MCP server: {server_name}")
        
        # Connect to the actual MCP server
        session, tools = await self.connect_to_mcp_server(best_server)
        
        if not session:
            print("Failed to connect to MCP server")
            return None
        
        # Create system prompt with MCP context
        system_prompt = MCP_SYSTEM_PROMPT.format(
            server_name=server_name,
            server_description=best_server.get('description', ''),
            available_tools=', '.join([t['name'] for t in tools])
        )
        
        # Query Claude with MCP context
        try:
            response = self.claude.messages.create(
                model="claude-4-sonnet-20250514",
                max_tokens=1000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_query}]
            )
            
            # TODO: Parse Claude's response to see if it wants to call MCP tools
            # For now, just return the response
            
            return {
                "mcp_server": best_server,
                "session": session,
                "tools": tools,
                "response": response.content[0].text
            }
        
        except Exception as e:
            print(f"Error querying Claude: {e}")
            return None

async def main():
    """
    Async main function
    """
    assistant = MCPEnhancedAssistant()
    
    # user_input = input("Enter your query: ")
    user_input = "Find a hotel in New York City"

    if user_input.lower() in ['quit', 'exit', 'q']:
        print("Goodbye!")
        
    if user_input.strip():
        result = await assistant.query_with_mcp_server(user_input)
        
        if result:
            print(f"\n--- Response using {result['mcp_server']['displayName']} ---")
            print(result['response'])
            print("\n" + "="*50 + "\n")
        else:
            print("Failed to get a response\n")
    else:
        print("Please enter a valid query")

if __name__ == "__main__":
    asyncio.run(main())
