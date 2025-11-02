"""WSGI entry point for Vercel deployment"""
import os
import sys
from flask import Flask, redirect

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Get backend URL from environment or use ngrok URL
BACKEND_URL = os.environ.get('BACKEND_URL', 'https://07dbabc61f8f.ngrok-free.app')

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def redirect_to_backend(path):
    """Redirect all requests to the ngrok backend"""
    return redirect(f'{BACKEND_URL}/{path}', code=307)

# For local development
if __name__ == '__main__':
    app.run()
