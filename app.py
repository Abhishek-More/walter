from flask import Flask, request
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

if __name__ == '__main__':
    app.run(debug=True, port=5001)
