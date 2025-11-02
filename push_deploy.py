#!/usr/bin/env python3
"""
Automated GitHub Push & Vercel Deploy for CryptoMinerPro
Run: python push_deploy.py
"""

import subprocess
import sys
import time

def run_command(cmd, description):
    """Run a shell command and print output"""
    print(f"\n{'='*60}")
    print(f"📦 {description}...")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        print(result.stdout)
        if result.stderr:
            print("⚠️ ", result.stderr)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("⏱️ Command timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🚀 CryptoMinerPro - GitHub Push & Vercel Deploy")
    print("="*60)
    
    # Get GitHub username
    github_user = input("\n👤 Enter your GitHub username: ").strip()
    if not github_user:
        print("❌ GitHub username required!")
        return False
    
    # Step 1: Push to GitHub
    print(f"\n📝 Repository URL: https://github.com/{github_user}/CryptoMinerPro")
    print("\n⚠️  Make sure you've created this repository on GitHub first!")
    input("Press Enter to continue...")
    
    # Configure git remote
    run_command(
        f'cd "g:\\Openai\\ASIC\\CryptoMinerPro" && git remote remove origin 2>nul || true',
        "Removing old remote"
    )
    
    time.sleep(1)
    
    run_command(
        f'cd "g:\\Openai\\ASIC\\CryptoMinerPro" && git remote add origin https://github.com/{github_user}/CryptoMinerPro.git',
        "Adding GitHub remote"
    )
    
    time.sleep(1)
    
    # Rename branch to main
    run_command(
        'cd "g:\\Openai\\ASIC\\CryptoMinerPro" && git branch -M main',
        "Renaming branch to main"
    )
    
    time.sleep(1)
    
    # Push to GitHub
    success = run_command(
        'cd "g:\\Openai\\ASIC\\CryptoMinerPro" && git push -u origin main --force',
        "Pushing to GitHub"
    )
    
    if success:
        print("\n" + "="*60)
        print("✅ Successfully pushed to GitHub!")
        print("="*60)
        print(f"\n📍 Your repository: https://github.com/{github_user}/CryptoMinerPro")
        print(f"📍 Clone command: git clone https://github.com/{github_user}/CryptoMinerPro.git")
    else:
        print("\n❌ GitHub push failed. Make sure:")
        print("   1. You created the repository on GitHub")
        print("   2. Git is configured with SSH or HTTPS")
        print("   3. You have internet connection")
        return False
    
    # Step 2: Vercel Deployment Instructions
    print("\n" + "="*60)
    print("🚀 Next: Deploy to Vercel")
    print("="*60)
    print("""
1. Go to https://vercel.com
2. Sign in with GitHub
3. Click "Add New" → "Project"
4. Select your CryptoMinerPro repository
5. Click "Import"
6. Configure:
   - Framework: Other
   - Build: pip install -r requirements.txt
7. Add Environment Variables:
   - FLASK_ENV = production
   - SECRET_KEY = your-secret-key-here
   - DATABASE_URL = sqlite:///mining_marketplace.db
8. Click "Deploy"

Your app will be live at: https://cryptominerpro.vercel.app
    """)
    
    print("\n✅ All done! Deployment prepared successfully!")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
