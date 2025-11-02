"""WSGI entry point for Vercel deployment - Proxies to local backend"""
import os
import sys
import urllib.request
import urllib.error
import time
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
        # Build URL with cache-busting timestamp
        url = f'{BACKEND_URL}/{path}'
        if request.query_string:
            url = f'{url}?{request.query_string.decode()}&t={int(time.time())}'
        else:
            # Add timestamp for cache busting on GET requests
            if request.method == 'GET':
                url = f'{url}?t={int(time.time())}'
        
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
            
            # Remove Cache-Control from backend response (override it)
            if 'Cache-Control' in response_headers:
                del response_headers['Cache-Control']
            
            # Add aggressive cache-busting headers
            response_headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0, public'
            response_headers['Pragma'] = 'no-cache'
            response_headers['Expires'] = '0'
            response_headers['X-Vercel-Cache'] = 'BYPASS'
            response_headers['CDN-Cache-Control'] = 'no-cache'
            
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
