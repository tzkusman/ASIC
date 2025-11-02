"""
Complete Flask App - Backend + Frontend
Run this on your PC - everything works!
Access from: http://your-pc-ip:5000
"""
import os
from app import create_app, db
from app.models import User, ASICMiner

# Create complete app (with frontend + backend)
app = create_app(os.environ.get('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'ASICMiner': ASICMiner}

if __name__ == '__main__':
    # Run on port 5000, accessible from everywhere on your network
    # Your PC will be accessible at: http://<YOUR_PC_IP>:5000
    # Find your IP: run "ipconfig" in PowerShell
    app.run(
        host='0.0.0.0',  # Listen on all network interfaces
        port=5000,
        debug=False,
        use_reloader=False
    )
