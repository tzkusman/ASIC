"""
Vercel Frontend - Calls your PC backend
All UI served from Vercel
All data from your PC
"""
import os
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Your PC backend URL (update with your PC's IP address)
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://192.168.100.99:5000')

@app.route('/')
def index():
    """Home page - fetches data from backend"""
    try:
        miners_response = requests.get(f'{BACKEND_URL}/api/miners', timeout=5)
        miners = miners_response.json() if miners_response.status_code == 200 else []
        return render_template('index.html', featured_miners=miners[:6], top_profitable=miners[:4])
    except:
        return render_template('index.html', featured_miners=[], top_profitable=[])

@app.route('/marketplace/')
def marketplace():
    """Marketplace page"""
    try:
        miners_response = requests.get(f'{BACKEND_URL}/api/miners', timeout=5)
        miners = miners_response.json() if miners_response.status_code == 200 else []
        return render_template('marketplace/browse.html', miners=miners)
    except:
        return render_template('marketplace/browse.html', miners=[])

@app.route('/api/proxy/<path:endpoint>')
def api_proxy(endpoint):
    """Proxy all API requests to backend"""
    try:
        backend_url = f'{BACKEND_URL}/api/{endpoint}'
        
        if request.method == 'GET':
            response = requests.get(backend_url, params=request.args, timeout=5)
        elif request.method == 'POST':
            response = requests.post(backend_url, json=request.get_json(), timeout=5)
        else:
            return jsonify({'error': 'Method not allowed'}), 405
        
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
