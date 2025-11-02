"""WSGI entry point for Vercel deployment"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import User, ASICMiner

# Create app for Vercel - with error handling for serverless
try:
    app = create_app(os.environ.get('FLASK_ENV', 'production'))
except Exception as e:
    print(f"Error creating app: {e}")
    # Fallback for Vercel issues
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mining_marketplace.db'
    
    @app.route('/')
    def home():
        return "Server starting...", 503

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'ASICMiner': ASICMiner}

# For local development
if __name__ == '__main__':
    app.run()
