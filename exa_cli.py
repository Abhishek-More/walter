#!/usr/bin/env python3
"""
Exa Search Command Line Interface

Simple CLI for using Exa search MCP server from the terminal.
"""

import asyncio
import sys
import json
from exa_search_app import ExaSearchClient

def print_help():
    """Print help information"""
    print("""
🔍 Exa Search CLI - Command Line Interface

Usage:
  python3 exa_cli.py <command> [options]

Commands:
  search <query> [num_results]     - Web search (default: 5 results)
  company <name> [num_results]     - Company research (default: 5 results)
  crawl <url> [max_chars]         - Crawl URL content (default: 3000 chars)
  linkedin <query> [type] [num]   - LinkedIn search (types: profiles, companies, all)
  research <instructions> [model]  - Start deep research (models: exa-research, exa-research-pro)
  status <task_id>                - Check research task status

Examples:
  python3 exa_cli.py search "Python tutorials" 10
  python3 exa_cli.py company "OpenAI" 3
  python3 exa_cli.py crawl "https://example.com" 2000
  python3 exa_cli.py linkedin "Python developers" profiles 5
  python3 exa_cli.py research "What are the latest AI developments?" exa-research-pro
  python3 exa_cli.py status "task_123"

Help:
  python3 exa_cli.py help
""")

async def main():
    """Main CLI function"""
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        print_help()
        return
    
    client = ExaSearchClient()
    
    try:
        if command == "search":
            if len(sys.argv) < 3:
                print("❌ Error: Query required for search")
                print("Usage: python3 exa_cli.py search <query> [num_results]")
                return
            
            query = sys.argv[2]
            num_results = int(sys.argv[3]) if len(sys.argv) > 3 else 5
            
            print(f"🔍 Searching for: {query}")
            results = await client.web_search(query, num_results)
            
            if results["success"]:
                print(f"✅ Found {len(results['results'])} results:")
                for i, result in enumerate(results["results"], 1):
                    print(f"\n{i}. {result.get('title', 'No title')}")
                    print(f"   URL: {result.get('url', 'No URL')}")
                    if result.get('text'):
                        print(f"   Preview: {result.get('text', '')[:150]}...")
            else:
                print(f"❌ Search failed: {results['error']}")
        
        elif command == "company":
            if len(sys.argv) < 3:
                print("❌ Error: Company name required")
                print("Usage: python3 exa_cli.py company <name> [num_results]")
                return
            
            company_name = sys.argv[2]
            num_results = int(sys.argv[3]) if len(sys.argv) > 3 else 5
            
            print(f"🏢 Researching company: {company_name}")
            results = await client.company_research(company_name, num_results)
            
            if results["success"]:
                print(f"✅ Found {len(results['results'])} results:")
                for i, result in enumerate(results["results"], 1):
                    print(f"\n{i}. {result.get('title', 'No title')}")
                    print(f"   URL: {result.get('url', 'No URL')}")
                    if result.get('text'):
                        print(f"   Preview: {result.get('text', '')[:150]}...")
            else:
                print(f"❌ Company research failed: {results['error']}")
        
        elif command == "crawl":
            if len(sys.argv) < 3:
                print("❌ Error: URL required")
                print("Usage: python3 exa_cli.py crawl <url> [max_chars]")
                return
            
            url = sys.argv[2]
            max_chars = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
            
            print(f"🕷️ Crawling URL: {url}")
            results = await client.crawl_url(url, max_chars)
            
            if results["success"]:
                print(f"✅ Crawling successful!")
                print(f"Content length: {len(results['content'])} characters")
                print(f"\nContent preview:")
                print("-" * 50)
                print(results['content'][:500] + "..." if len(results['content']) > 500 else results['content'])
                print("-" * 50)
            else:
                print(f"❌ Crawling failed: {results['error']}")
        
        elif command == "linkedin":
            if len(sys.argv) < 3:
                print("❌ Error: Query required")
                print("Usage: python3 exa_cli.py linkedin <query> [type] [num_results]")
                return
            
            query = sys.argv[2]
            search_type = sys.argv[3] if len(sys.argv) > 3 else "all"
            num_results = int(sys.argv[4]) if len(sys.argv) > 4 else 5
            
            print(f"💼 LinkedIn search: {query} (type: {search_type})")
            results = await client.linkedin_search(query, search_type, num_results)
            
            if results["success"]:
                print(f"✅ Found {len(results['results'])} results:")
                for i, result in enumerate(results["results"], 1):
                    print(f"\n{i}. {result.get('title', 'No title')}")
                    print(f"   URL: {result.get('url', 'No URL')}")
                    if result.get('text'):
                        print(f"   Preview: {result.get('text', '')[:150]}...")
            else:
                print(f"❌ LinkedIn search failed: {results['error']}")
        
        elif command == "research":
            if len(sys.argv) < 3:
                print("❌ Error: Instructions required")
                print("Usage: python3 exa_cli.py research <instructions> [model]")
                return
            
            instructions = sys.argv[2]
            model = sys.argv[3] if len(sys.argv) > 3 else "exa-research"
            
            print(f"🔬 Starting deep research...")
            print(f"Instructions: {instructions}")
            print(f"Model: {model}")
            
            results = await client.deep_research(instructions, model)
            
            if results["success"]:
                print(f"✅ Research task started!")
                print(f"Task ID: {results['task_id']}")
                print(f"Status: {results['status']}")
                print(f"\nUse this command to check status:")
                print(f"python3 exa_cli.py status {results['task_id']}")
            else:
                print(f"❌ Research failed: {results['error']}")
        
        elif command == "status":
            if len(sys.argv) < 3:
                print("❌ Error: Task ID required")
                print("Usage: python3 exa_cli.py status <task_id>")
                return
            
            task_id = sys.argv[2]
            
            print(f"📊 Checking research task status: {task_id}")
            results = await client.check_research_status(task_id)
            
            if results["success"]:
                print(f"✅ Status check successful!")
                print(f"Task ID: {results['task_id']}")
                print(f"Status: {results['status']}")
                
                if results['status'] == 'completed':
                    print("🎉 Research completed!")
                    if results.get('results'):
                        print("\nResults:")
                        print(json.dumps(results['results'], indent=2))
                elif results['status'] == 'running':
                    print("⏳ Research still running...")
                    if results.get('progress'):
                        print(f"Progress: {results['progress']}")
                else:
                    print(f"Status: {results['status']}")
            else:
                print(f"❌ Status check failed: {results['error']}")
        
        else:
            print(f"❌ Unknown command: {command}")
            print_help()
    
    except KeyboardInterrupt:
        print("\n\n⏹️ Operation cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Try 'python3 exa_cli.py help' for usage information")

if __name__ == "__main__":
    asyncio.run(main())
