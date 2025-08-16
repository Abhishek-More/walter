#!/usr/bin/env python3
"""
Exa Search Web Application

A Flask web app that demonstrates how to use the Exa search MCP server
for web search, company research, and content crawling.
"""

from flask import Flask, render_template, request, jsonify
import asyncio
import json
from exa_search_app import ExaSearchClient

app = Flask(__name__)

# Initialize the Exa search client
exa_client = ExaSearchClient()

# Helper function to run async MCP calls in Flask
def run_async_exa(func, *args, **kwargs):
    """Helper function to run async Exa MCP calls in Flask"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(func(*args, **kwargs))
        loop.close()
        return result
    except Exception as e:
        return {"error": f"Async execution failed: {str(e)}"}

@app.route('/')
def index():
    return render_template('exa_index.html')

@app.route('/api/web_search', methods=['POST'])
def web_search():
    """Perform a web search using Exa"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        num_results = int(data.get('num_results', 5))
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query is required'
            }), 400
        
        # Call the Exa web search
        results = run_async_exa(
            exa_client.web_search,
            query=query,
            num_results=num_results
        )
        
        if "error" in results:
            return jsonify({
                'success': False,
                'error': results["error"]
            }), 400
        
        return jsonify({
            'success': True,
            'results': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/company_research', methods=['POST'])
def company_research():
    """Research a company using Exa"""
    try:
        data = request.get_json()
        company_name = data.get('company_name', '')
        num_results = int(data.get('num_results', 5))
        
        if not company_name:
            return jsonify({
                'success': False,
                'error': 'Company name is required'
            }), 400
        
        # Call the Exa company research
        results = run_async_exa(
            exa_client.company_research,
            company_name=company_name,
            num_results=num_results
        )
        
        if "error" in results:
            return jsonify({
                'success': False,
                'error': results["error"]
            }), 400
        
        return jsonify({
            'success': True,
            'results': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/crawl_url', methods=['POST'])
def crawl_url():
    """Crawl and extract content from a URL using Exa"""
    try:
        data = request.get_json()
        url = data.get('url', '')
        max_characters = int(data.get('max_characters', 3000))
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL is required'
            }), 400
        
        # Call the Exa URL crawling
        results = run_async_exa(
            exa_client.crawl_url,
            url=url,
            max_characters=max_characters
        )
        
        if "error" in results:
            return jsonify({
                'success': False,
                'error': results["error"]
            }), 400
        
        return jsonify({
            'success': True,
            'results': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/linkedin_search', methods=['POST'])
def linkedin_search():
    """Search LinkedIn using Exa"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        search_type = data.get('search_type', 'all')
        num_results = int(data.get('num_results', 5))
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query is required'
            }), 400
        
        # Call the Exa LinkedIn search
        results = run_async_exa(
            exa_client.linkedin_search,
            query=query,
            search_type=search_type,
            num_results=num_results
        )
        
        if "error" in results:
            return jsonify({
                'success': False,
                'error': results["error"]
            }), 400
        
        return jsonify({
            'success': True,
            'results': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/deep_research', methods=['POST'])
def deep_research():
    """Start a deep research task using Exa"""
    try:
        data = request.get_json()
        instructions = data.get('instructions', '')
        model = data.get('model', 'exa-research')
        
        if not instructions:
            return jsonify({
                'success': False,
                'error': 'Instructions are required'
            }), 400
        
        # Call the Exa deep research
        results = run_async_exa(
            exa_client.deep_research,
            instructions=instructions,
            model=model
        )
        
        if "error" in results:
            return jsonify({
                'success': False,
                'error': results["error"]
            }), 400
        
        return jsonify({
            'success': True,
            'results': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/check_research_status', methods=['POST'])
def check_research_status():
    """Check the status of a deep research task"""
    try:
        data = request.get_json()
        task_id = data.get('task_id', '')
        
        if not task_id:
            return jsonify({
                'success': False,
                'error': 'Task ID is required'
            }), 400
        
        # Call the Exa status check
        results = run_async_exa(
            exa_client.check_research_status,
            task_id=task_id
        )
        
        if "error" in results:
            return jsonify({
                'success': False,
                'error': results["error"]
            }), 400
        
        return jsonify({
            'success': True,
            'results': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    print("🔍 Starting Exa Search Web Application...")
    print("🌐 Visit http://localhost:5000 to use the Exa search interface!")
    print("🚀 Starting Flask server...\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
