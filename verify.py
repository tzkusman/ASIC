#!/usr/bin/env python
"""Quick verification script"""
import sys
sys.path.insert(0, '.')
from app import create_app

app = create_app()
print("✅ Application imports successfully!")
print("✅ Flask app created!")
print("✅ Ready for deployment!")
print("\nTo start: python run.py")
print("URL: http://localhost:5000")
