@echo off
REM Quick setup script for CryptoMinerPro on Windows

echo ===============================================
echo CryptoMinerPro - ASIC Mining Marketplace
echo Quick Setup Script
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo [2/4] Installing dependencies...
pip install -r requirements.txt

echo [3/4] Initializing database...
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized!')"

echo [4/4] Running database seeding...
flask --app run init-db

echo.
echo ===============================================
echo Setup Complete!
echo ===============================================
echo.
echo To start the application, run:
echo   python run.py
echo.
echo The app will be available at:
echo   http://localhost:5000
echo.
echo Login with these demo credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo Press any key to continue...
pause
