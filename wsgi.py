"""WSGI entry point for Vercel deployment"""
import os
from app import create_app, db
from app.models import User, ASICMiner

app = create_app(os.environ.get('FLASK_ENV', 'production'))

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'ASICMiner': ASICMiner}

if __name__ == '__main__':
    app.run()
