"""WSGI entry point for Vercel deployment"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import User, ASICMiner

# Create app for Vercel
app = create_app(os.environ.get('FLASK_ENV', 'production'))

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'ASICMiner': ASICMiner}

# For local development
if __name__ == '__main__':
    app.run()
