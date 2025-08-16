from flask import Flask, request, jsonify
import asyncio
from main import MCPEnhancedAssistant
from text import sendText

app = Flask(__name__)

async def process_query_with_cleanup(query):
    """
    Wrapper function that ensures proper cleanup of the assistant
    """
    assistant = MCPEnhancedAssistant()
    result = await assistant.query_with_mcp_server(query)
    return result

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/sms', methods=['POST'])
def sms_reply():
    body = request.form.get('Body', '')
    from_number = request.form.get('From', '')
    
    print(f"Received SMS from {from_number}: {body}")
    
    try:
        # Use asyncio.run() which properly handles cleanup
        result = asyncio.run(process_query_with_cleanup(body))
        
        if result:
            response_text = result['response']
            sendText(response_text, from_number)
        else:
            response_text = "Sorry, I couldn't process your request right now."
            sendText(response_text, from_number)
            
    except Exception as e:
        print(f"Error processing SMS: {e}")
        response_text = "Sorry, there was an error processing your request."
        sendText(response_text, from_number)
    
    return {}

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
        
        # Use asyncio.run() which properly handles cleanup
        result = asyncio.run(process_query_with_cleanup(query))
        
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
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
