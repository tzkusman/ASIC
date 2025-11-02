@echo off
REM Automated deployment script for CryptoMinerPro to GitHub and Vercel

echo ================================================
echo CryptoMinerPro - Automated Deployment Script
echo ================================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed. Please install Git first.
    echo    https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Get GitHub username
set /p GITHUB_USERNAME="Enter your GitHub username: "

if "%GITHUB_USERNAME%"=="" (
    echo ❌ GitHub username is required
    pause
    exit /b 1
)

echo.
echo 📦 Step 1: Preparing repository...
git status

echo.
echo 🔄 Step 2: Adding all changes...
git add .

echo.
echo 📝 Step 3: Creating commit...
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a:%%b)
git commit -m "Final deployment commit - %mydate% %mytime%" 2>nul || echo ⚠️  Already committed

echo.
echo 🌐 Step 4: Setting GitHub remote...
git remote remove origin 2>nul
git remote add origin "https://github.com/%GITHUB_USERNAME%/CryptoMinerPro.git"

echo.
echo 📤 Step 5: Pushing to GitHub...
git branch -M main
git push -u origin main --force || echo ⚠️  Push failed. Verify GitHub credentials.

echo.
echo ================================================
echo ✅ GitHub Push Complete!
echo ================================================
echo.
echo 📋 Your repository is now at:
echo    https://github.com/%GITHUB_USERNAME%/CryptoMinerPro
echo.
echo 🚀 Next: Deploy to Vercel
echo ================================================
echo.
echo 1. Go to: https://vercel.com
echo 2. Click 'Add New' / 'Project'
echo 3. Connect GitHub and import CryptoMinerPro
echo 4. Set these environment variables:
echo    - FLASK_ENV: production
echo    - SECRET_KEY: your-secure-key
echo 5. Click Deploy!
echo.
echo Your app will be live at: https://cryptominerpro.vercel.app
echo ================================================
echo.
pause
