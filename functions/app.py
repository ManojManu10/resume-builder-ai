from flask import Flask, request
from flask.helpers import send_from_directory
import os
import json
from generate_resume import generate_resume_content

app = Flask(__name__)

def handler(event, context):
    # Get HTTP method and path
    method = event['httpMethod']
    path = event['path']
    
    # Get query parameters and body
    query_params = event.get('queryStringParameters', {}) or {}
    body = {}
    if event.get('body'):
        if isinstance(event['body'], str):
            body = json.loads(event['body'])
        else:
            body = event['body']

    # Create a mock request context
    with app.test_request_context(
        path=path,
        method=method,
        query_string=query_params,
        data=json.dumps(body) if body else None,
        headers=event.get('headers', {})
    ):
        try:
            # Get the Flask response
            response = app.full_dispatch_request()
            
            # Convert Flask response to Netlify format
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data(as_text=True)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': str(e)
            }

# Flask routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Handle form submission
            form_data = request.form.to_dict()
            resume_content = generate_resume_content(form_data)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'resume_content': resume_content,
                    'form_data': form_data
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': str(e)
            }
    
    return send_from_directory('../', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('../static', path)

@app.route('/templates/<path:path>')
def serve_template(path):
    return send_from_directory('../templates', path)
