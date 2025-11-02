#!/usr/bin/env python
"""
CryptoMinerPro - ASIC Mining Equipment Marketplace
Direct runner script
"""

import os
import sys

# Set environment
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = '1'

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import User, ASICMiner

def main():
    """Run the application"""
    print("\n" + "="*60)
    print("🚀 CryptoMinerPro - ASIC Mining Marketplace")
    print("="*60)
    
    # Create app
    app = create_app()
    
    # Initialize database
    with app.app_context():
        db.create_all()
        
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("\n📝 Creating admin user...")
            admin = User(
                username='admin',
                email='admin@cryptominerpro.com',
                company_name='CryptoMinerPro',
                country='United States',
                is_verified=True,
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created")
        
        # Check if miners exist
        if ASICMiner.query.count() == 0:
            print("📦 Loading sample miners...")
            from app.models import Inventory
            
            miners_data = [
                {'name': 'Antminer S19 Pro', 'manufacturer': 'Bitmain', 'model': 'S19 Pro', 'hash_rate': 110.0, 'power_consumption': 1450, 'algorithm': 'SHA-256', 'price_usd': 6500, 'stock_quantity': 50},
                {'name': 'MicroBT Whatsminer M50S', 'manufacturer': 'MicroBT', 'model': 'M50S', 'hash_rate': 126.0, 'power_consumption': 1632, 'algorithm': 'SHA-256', 'price_usd': 7200, 'stock_quantity': 35},
                {'name': 'Antminer L7', 'manufacturer': 'Bitmain', 'model': 'L7', 'hash_rate': 9.5, 'power_consumption': 3425, 'algorithm': 'Scrypt', 'price_usd': 8500, 'stock_quantity': 20},
            ]
            
            for data in miners_data:
                miner = ASICMiner(**data)
                db.session.add(miner)
                db.session.flush()
                inv = Inventory(miner_id=miner.id, quantity_available=data['stock_quantity'])
                db.session.add(inv)
            
            db.session.commit()
            print(f"✓ {len(miners_data)} sample miners loaded")
    
    print("\n" + "="*60)
    print("✅ Application Ready!")
    print("="*60)
    print("\n📍 Access the app at: http://localhost:5000")
    print("\n🔐 Demo Credentials:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n" + "="*60)
    print("🌐 Starting server...\n")
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
