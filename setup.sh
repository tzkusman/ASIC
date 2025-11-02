#!/bin/bash
# Quick setup script for CryptoMinerPro on Linux/Mac

echo "======================================="
echo "CryptoMinerPro - ASIC Mining Marketplace"
echo "Quick Setup Script"
echo "======================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.11+ from https://www.python.org"
    exit 1
fi

echo "[1/4] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "[2/4] Installing dependencies..."
pip install -r requirements.txt

echo "[3/4] Initializing database..."
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized!')"

echo "[4/4] Running database seeding..."
flask --app run init-db

echo
echo "======================================="
echo "Setup Complete!"
echo "======================================="
echo
echo "To start the application, run:"
echo "  python run.py"
echo
echo "The app will be available at:"
echo "  http://localhost:5000"
echo
echo "Login with these demo credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo
