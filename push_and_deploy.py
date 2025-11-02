#!/usr/bin/env python3
"""
One-command GitHub push and Vercel deployment
"""

import subprocess
import sys
import os

def run_command(cmd, description=""):
    """Run shell command"""
    if description:
        print(f"\n📌 {description}")
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=False)
    return result.returncode == 0

def main():
    print("\n" + "="*60)
    print("🚀 CryptoMinerPro - GitHub & Vercel Deployment")
    print("="*60)
    
    # Get GitHub username
    username = input("\n👤 Enter your GitHub username: ").strip()
    if not username:
        print("❌ GitHub username required!")
        return False
    
    print("\n" + "="*60)
    print("📤 STEP 1: Pushing to GitHub")
    print("="*60)
    
    # Set remote
    print("\n1️⃣  Setting GitHub remote...")
    subprocess.run(f'git remote remove origin 2>nul', shell=True, capture_output=True)
    subprocess.run(
        f'git remote add origin https://github.com/{username}/CryptoMinerPro.git',
        shell=True
    )
    print("✓ Remote configured")
    
    # Rename branch
    print("\n2️⃣  Setting main branch...")
    subprocess.run('git branch -M main', shell=True, capture_output=True)
    print("✓ Branch renamed to main")
    
    # Push to GitHub
    print("\n3️⃣  Pushing code to GitHub...")
    if run_command(f'git push -u origin main --force'):
        print("✅ Code pushed successfully!")
    else:
        print("⚠️  Push may have failed. Check GitHub permissions.")
    
    print("\n" + "="*60)
    print("🎉 GitHub Push Complete!")
    print("="*60)
    print(f"\n📋 Your repository: https://github.com/{username}/CryptoMinerPro")
    
    print("\n" + "="*60)
    print("🚀 STEP 2: Deploy to Vercel")
    print("="*60)
    print("\n✨ Next steps:")
    print("   1. Go to https://vercel.com")
    print("   2. Sign in with GitHub")
    print("   3. Click 'Add New' → 'Project'")
    print("   4. Select 'CryptoMinerPro'")
    print("   5. Set Environment Variables:")
    print("      - FLASK_ENV: production")
    print("      - SECRET_KEY: your-secure-random-key")
    print("   6. Click 'Deploy'")
    print("\n🎉 Your app will be live at:")
    print("   https://cryptominerpro.vercel.app")
    print("\n" + "="*60)
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
