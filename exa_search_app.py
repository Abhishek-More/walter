#!/usr/bin/env python3
"""
Exa Search MCP Client Application

This application demonstrates how to use the Exa search MCP server
for web search, company research, and content crawling.
"""

import asyncio
import json
from typing import Optional, Dict, Any, List
from datetime import datetime
import mcp
from mcp.client.streamable_http import streamablehttp_client

class ExaSearchClient:
    """
    Client for interacting with Exa search MCP server via Smithery AI
    """
    
    def __init__(self):
        """Initialize the Exa MCP client with Smithery AI credentials"""
        self.smithery_api_key = "9775d396-48d3-4dd7-9a44-9fe04940ba16"
        self.smithery_profile = "grateful-crayfish-oQVqqO"
        self.url = f"https://server.smithery.ai/exa/mcp?api_key={self.smithery_api_key}&profile={self.smithery_profile}"
    
    def _parse_mcp_content(self, result) -> Dict[str, Any]:
        """
        Parse MCP response content into a dictionary
        
        Args:
            result: MCP CallToolResult object
            
        Returns:
            Parsed content as dictionary
        """
        try:
            if hasattr(result, 'content') and result.content:
                # Content is a list of TextContent objects
                if isinstance(result.content, list) and len(result.content) > 0:
                    # Get the text from the first TextContent item
                    text_content = result.content[0]
                    if hasattr(text_content, 'text'):
                        # Parse the JSON text
                        return json.loads(text_content.text)
            
            # Fallback: try to parse the result directly
            if isinstance(result, str):
                return json.loads(result)
            
            # Return empty result if parsing fails
            return {"results": [], "error": "Could not parse response"}
            
        except (json.JSONDecodeError, AttributeError, IndexError) as e:
            return {"results": [], "error": f"Parsing error: {str(e)}"}
    
    async def web_search(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Perform a web search using Exa
        
        Args:
            query: Search query
            num_results: Number of results to return (default: 5)
            
        Returns:
            Dictionary containing search results
        """
        try:
            # Connect to the server using HTTP client
            async with streamablehttp_client(self.url) as (read_stream, write_stream, _):
                async with mcp.ClientSession(read_stream, write_stream) as session:
                    # Initialize the connection
                    await session.initialize()
                    
                    # Call the web search tool
                    result = await session.call_tool("web_search_exa", {
                        "query": query,
                        "numResults": num_results
                    })
                    
                    # Parse the result
                    content = self._parse_mcp_content(result)
                    
                    return {
                        "success": True,
                        "query": query,
                        "results": content.get("results", []),
                        "search_time": content.get("searchTime", 0),
                        "cost": content.get("costDollars", {}),
                        "request_id": content.get("requestId", "")
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"Web search failed: {str(e)}"
            }
    
    async def company_research(self, company_name: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Research a company using Exa
        
        Args:
            company_name: Name of the company to research
            num_results: Number of results to return (default: 5)
            
        Returns:
            Dictionary containing company research results
        """
        try:
            # Connect to the server using HTTP client
            async with streamablehttp_client(self.url) as (read_stream, write_stream, _):
                async with mcp.ClientSession(read_stream, write_stream) as session:
                    # Initialize the connection
                    await session.initialize()
                    
                    # Call the company research tool
                    result = await session.call_tool("company_research_exa", {
                        "companyName": company_name,
                        "numResults": num_results
                    })
                    
                    # Parse the result
                    content = self._parse_mcp_content(result)
                    
                    return {
                        "success": True,
                        "company": company_name,
                        "results": content.get("results", []),
                        "search_time": content.get("searchTime", 0),
                        "cost": content.get("costDollars", {})
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"Company research failed: {str(e)}"
            }
    
    async def crawl_url(self, url: str, max_characters: int = 3000) -> Dict[str, Any]:
        """
        Crawl and extract content from a specific URL
        
        Args:
            url: URL to crawl
            max_characters: Maximum characters to extract (default: 3000)
            
        Returns:
            Dictionary containing crawled content
        """
        try:
            # Connect to the server using HTTP client
            async with streamablehttp_client(self.url) as (read_stream, write_stream, _):
                async with mcp.ClientSession(read_stream, write_stream) as session:
                    # Initialize the connection
                    await session.initialize()
                    
                    # Call the crawling tool
                    result = await session.call_tool("crawling_exa", {
                        "url": url,
                        "maxCharacters": max_characters
                    })
                    
                    # Parse the result
                    content = self._parse_mcp_content(result)
                    
                    return {
                        "success": True,
                        "url": url,
                        "content": content.get("content", ""),
                        "metadata": content.get("metadata", {}),
                        "cost": content.get("costDollars", {})
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"URL crawling failed: {str(e)}"
            }
    
    async def linkedin_search(self, query: str, search_type: str = "all", num_results: int = 5) -> Dict[str, Any]:
        """
        Search LinkedIn profiles and companies
        
        Args:
            query: Search query
            search_type: Type of search ("profiles", "companies", or "all")
            num_results: Number of results to return (default: 5)
            
        Returns:
            Dictionary containing LinkedIn search results
        """
        try:
            # Connect to the server using HTTP client
            async with streamablehttp_client(self.url) as (read_stream, write_stream, _):
                async with mcp.ClientSession(read_stream, write_stream) as session:
                    # Initialize the connection
                    await session.initialize()
                    
                    # Call the LinkedIn search tool
                    result = await session.call_tool("linkedin_search_exa", {
                        "query": query,
                        "searchType": search_type,
                        "numResults": num_results
                    })
                    
                    # Parse the result
                    content = self._parse_mcp_content(result)
                    
                    return {
                        "success": True,
                        "query": query,
                        "search_type": search_type,
                        "results": content.get("results", []),
                        "search_time": content.get("searchTime", 0),
                        "cost": content.get("costDollars", {})
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"LinkedIn search failed: {str(e)}"
            }
    
    async def deep_research(self, instructions: str, model: str = "exa-research") -> Dict[str, Any]:
        """
        Start a comprehensive deep research task
        
        Args:
            instructions: Detailed research instructions
            model: Research model ("exa-research" or "exa-research-pro")
            
        Returns:
            Dictionary containing research task information
        """
        try:
            # Connect to the server using HTTP client
            async with streamablehttp_client(self.url) as (read_stream, write_stream, _):
                async with mcp.ClientSession(read_stream, write_stream) as session:
                    # Initialize the connection
                    await session.initialize()
                    
                    # Call the deep research tool
                    result = await session.call_tool("deep_researcher_start", {
                        "instructions": instructions,
                        "model": model
                    })
                    
                    # Parse the result
                    content = self._parse_mcp_content(result)
                    
                    return {
                        "success": True,
                        "task_id": content.get("taskId", ""),
                        "instructions": instructions,
                        "model": model
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"Deep research failed: {str(e)}"
            }
    
    async def check_research_status(self, task_id: str) -> Dict[str, Any]:
        """
        Check the status of a deep research task
        
        Args:
            task_id: ID of the research task
            
        Returns:
            Dictionary containing task status and results
        """
        try:
            # Connect to the server using HTTP client
            async with streamablehttp_client(self.url) as (read_stream, write_stream, _):
                async with mcp.ClientSession(read_stream, write_stream) as session:
                    # Initialize the connection
                    await session.initialize()
                    
                    # Call the status check tool
                    result = await session.call_tool("deep_researcher_check", {
                        "taskId": task_id
                    })
                    
                    # Parse the result
                    content = self._parse_mcp_content(result)
                    
                    return {
                        "success": True,
                        "task_id": task_id,
                        "status": content.get("status", "unknown"),
                        "results": content.get("results", {}),
                        "progress": content.get("progress", {})
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"Status check failed: {str(e)}"
            }

# Example usage and testing
async def main():
    """Main function to demonstrate Exa search capabilities"""
    print("🔍 Starting Exa Search MCP Client Demo...")
    
    client = ExaSearchClient()
    
    # Test 1: Web Search
    print("\n1️⃣ Testing Web Search...")
    search_results = await client.web_search("Python programming tutorials", num_results=3)
    if search_results["success"]:
        print(f"✅ Web search successful! Found {len(search_results['results'])} results")
        for i, result in enumerate(search_results["results"][:2], 1):
            print(f"   {i}. {result.get('title', 'No title')}")
            print(f"      URL: {result.get('url', 'No URL')}")
    else:
        print(f"❌ Web search failed: {search_results['error']}")
    
    # Test 2: Company Research
    print("\n2️⃣ Testing Company Research...")
    company_results = await client.company_research("OpenAI", num_results=3)
    if company_results["success"]:
        print(f"✅ Company research successful! Found {len(company_results['results'])} results")
        for i, result in enumerate(company_results["results"][:2], 1):
            print(f"   {i}. {result.get('title', 'No title')}")
            print(f"      URL: {result.get('url', 'No URL')}")
    else:
        print(f"❌ Company research failed: {company_results['error']}")
    
    # Test 3: URL Crawling
    print("\n3️⃣ Testing URL Crawling...")
    if search_results["success"] and search_results["results"]:
        first_url = search_results["results"][0]["url"]
        crawl_results = await client.crawl_url(first_url, max_characters=1000)
        if crawl_results["success"]:
            print(f"✅ URL crawling successful!")
            print(f"   Content length: {len(crawl_results['content'])} characters")
            print(f"   Preview: {crawl_results['content'][:100]}...")
        else:
            print(f"❌ URL crawling failed: {crawl_results['error']}")
    
    # Test 4: LinkedIn Search
    print("\n4️⃣ Testing LinkedIn Search...")
    linkedin_results = await client.linkedin_search("Python developers", search_type="profiles", num_results=3)
    if linkedin_results["success"]:
        print(f"✅ LinkedIn search successful! Found {len(linkedin_results['results'])} results")
        for i, result in enumerate(linkedin_results["results"][:2], 1):
            print(f"   {i}. {result.get('title', 'No title')}")
            print(f"      URL: {result.get('url', 'No URL')}")
    else:
        print(f"❌ LinkedIn search failed: {linkedin_results['error']}")
    
    print("\n🎉 Exa Search MCP Client Demo Complete!")
    print("💡 You can now integrate these functions into your Python applications!")

if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
