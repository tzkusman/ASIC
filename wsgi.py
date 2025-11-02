"""WSGI entry point for Vercel deployment - Proxies to local backend"""
import os
import sys
from flask import Flask, request, Response
import requests

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Backend URL - ngrok public tunnel
BACKEND_URL = 'https://07dbabc61f8f.ngrok-free.app'

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
def proxy(path):
    """Proxy all requests to backend"""
    try:
        # Build URL
        url = f'{BACKEND_URL}/{path}'
        if request.query_string:
            url = f'{url}?{request.query_string.decode()}'
        
        # Prepare headers
        headers = {}
        for header, value in request.headers:
            if header.lower() not in ['host', 'connection']:
                headers[header] = value
        
        # Make request to backend
        resp = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            timeout=30
        )
        
        # Return response with cache-busting headers
        response_headers = dict(resp.headers)
        response_headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response_headers['Pragma'] = 'no-cache'
        response_headers['Expires'] = '0'
        
        return Response(
            resp.content,
            status=resp.status_code,
            headers=response_headers
        )
    except requests.exceptions.ConnectionError:
        return "Backend offline. Make sure your PC is running.", 503
    except Exception as e:
        return f"Proxy error: {str(e)}", 502

# For local development
if __name__ == '__main__':
    app.run()
