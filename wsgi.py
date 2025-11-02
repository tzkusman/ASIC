"""WSGI entry point for Vercel deployment - Proxies to local backend"""
import os
import sys
import urllib.request
import urllib.error
from flask import Flask, request, Response

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Backend URL - ngrok public tunnel
BACKEND_URL = 'https://f21eb9c64b5a.ngrok-free.app'

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
        
        # Prepare request body
        body = request.get_data()
        
        # Create request with headers
        req = urllib.request.Request(url, data=body, method=request.method)
        
        # Add headers from client
        for header, value in request.headers:
            if header.lower() not in ['host', 'connection']:
                req.add_header(header, value)
        
        # Make request to backend
        with urllib.request.urlopen(req, timeout=30) as resp:
            response_body = resp.read()
            status_code = resp.status
            response_headers = dict(resp.headers)
            
            # Add cache-busting headers
            response_headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response_headers['Pragma'] = 'no-cache'
            response_headers['Expires'] = '0'
            
            return Response(
                response_body,
                status=status_code,
                headers=response_headers
            )
    except urllib.error.URLError as e:
        return f"Backend offline: {str(e)}", 503
    except Exception as e:
        return f"Proxy error: {str(e)}", 502

# For local development
if __name__ == '__main__':
    app.run()
