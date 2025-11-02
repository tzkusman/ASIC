#!/bin/bash
# Automated deployment script for CryptoMinerPro to GitHub and Vercel

set -e  # Exit on error

echo "================================================"
echo "CryptoMinerPro - Automated Deployment Script"
echo "================================================"
echo

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ GitHub username is required"
    exit 1
fi

echo
echo "📦 Step 1: Preparing repository..."
git status

echo
echo "🔄 Step 2: Adding all changes..."
git add .

echo
echo "📝 Step 3: Creating commit..."
git commit -m "Final deployment commit - $(date +'%Y-%m-%d %H:%M:%S')" || true

echo
echo "🌐 Step 4: Setting GitHub remote..."
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/${GITHUB_USERNAME}/CryptoMinerPro.git"

echo
echo "📤 Step 5: Pushing to GitHub..."
git branch -M main
git push -u origin main --force || echo "⚠️  Push failed. Verify GitHub credentials."

echo
echo "================================================"
echo "✅ GitHub Push Complete!"
echo "================================================"
echo
echo "📋 Your repository is now at:"
echo "   https://github.com/${GITHUB_USERNAME}/CryptoMinerPro"
echo
echo "🚀 Next: Deploy to Vercel"
echo "================================================"
echo
echo "1. Go to: https://vercel.com"
echo "2. Click 'Add New' → 'Project'"
echo "3. Connect GitHub and import CryptoMinerPro"
echo "4. Set these environment variables:"
echo "   - FLASK_ENV: production"
echo "   - SECRET_KEY: your-secure-key"
echo "5. Click Deploy!"
echo
echo "Your app will be live at: https://cryptominerpro.vercel.app"
echo "================================================"
