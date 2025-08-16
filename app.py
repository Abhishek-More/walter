from flask import Flask, request
from flask import Flask, request, jsonify
import asyncio
from main import MCPEnhancedAssistant

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/sms', methods=['POST'])
def sms_reply():
    body = request.form.get('Body', '')
    from_number = request.form.get('From', '')
    
    print(f"Received SMS from {from_number}: {body}")
    
    response_text = f"Processing: {body}"
    
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{response_text}</Message>
</Response>''', 200, {'Content-Type': 'text/xml'}

@app.route('/search', methods=['POST'])
def search_mcp():
    """
    Search for MCP servers and query Claude with the best match
    """
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Missing query parameter'}), 400
        
        query = data['query']
        
        # Create assistant and run async function
        assistant = MCPEnhancedAssistant()
        
        # Run the async function in a new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(assistant.query_with_mcp_server(query))
            
            if result:
                return jsonify({
                    'success': True,
                    'query': query,
                    'mcp_server': {
                        'name': result['mcp_server'].get('displayName'),
                        'description': result['mcp_server'].get('description'),
                        'useCount': result['mcp_server'].get('useCount')
                    },
                    'tools': result['tools'],
                    'response': result['response']
                })
            else:
                return jsonify({'error': 'Failed to process query'}), 500
                
        finally:
            loop.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)

