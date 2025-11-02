"""
Backend Server - Run this on your PC
Exposes all data as REST API
Vercel frontend will call this API
"""
import os
from app import create_app, db
from app.models import User, ASICMiner

# Create app with production config (uses local SQLite)
app = create_app(os.environ.get('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'ASICMiner': ASICMiner}

if __name__ == '__main__':
    # Run on port 5000, accessible from everywhere
    # Your PC IP will be: http://<YOUR_PC_IP>:5000
    app.run(
        host='0.0.0.0',  # Listen on all network interfaces
        port=5000,
        debug=False,
        use_reloader=False
    )
