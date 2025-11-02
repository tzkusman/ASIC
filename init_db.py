#!/usr/bin/env python
"""
Database initialization script for CryptoMinerPro
"""

from app import create_app, db
from app.models import User, ASICMiner, Inventory, ProfitabilityData

def init_database():
    """Initialize database with tables and sample data"""
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    
    print("🔧 Initializing database...")
    db.create_all()
    print("✓ Database tables created!")
    
    # Add admin user
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@cryptominerpro.com',
            company_name='CryptoMinerPro',
            country='United States',
            phone='+1 (555) 123-4567',
            is_verified=True,
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✓ Admin user created!")
        print("  Username: admin")
        print("  Password: admin123")
    else:
        print("✓ Admin user already exists")
    
    # Add sample miners
    sample_miners = [
        {
            'name': 'Antminer S19 Pro',
            'manufacturer': 'Bitmain',
            'model': 'S19 Pro',
            'hash_rate': 110.0,
            'power_consumption': 1450,
            'algorithm': 'SHA-256',
            'price_usd': 6500,
            'stock_quantity': 50,
            'description': 'High-performance Bitcoin ASIC miner with excellent efficiency',
            'release_year': 2022
        },
        {
            'name': 'Antminer S19j Pro',
            'manufacturer': 'Bitmain',
            'model': 'S19j Pro',
            'hash_rate': 100.0,
            'power_consumption': 1320,
            'algorithm': 'SHA-256',
            'price_usd': 5500,
            'stock_quantity': 40,
            'description': 'Efficient Bitcoin mining with improved power consumption',
            'release_year': 2021
        },
        {
            'name': 'MicroBT Whatsminer M50S',
            'manufacturer': 'MicroBT',
            'model': 'M50S',
            'hash_rate': 126.0,
            'power_consumption': 1632,
            'algorithm': 'SHA-256',
            'price_usd': 7200,
            'stock_quantity': 35,
            'description': 'High hashrate Bitcoin miner for professional operations',
            'release_year': 2023
        },
        {
            'name': 'Antminer L7',
            'manufacturer': 'Bitmain',
            'model': 'L7',
            'hash_rate': 9.5,
            'power_consumption': 3425,
            'algorithm': 'Scrypt',
            'price_usd': 8500,
            'stock_quantity': 20,
            'description': 'Professional Litecoin and Dogecoin mining hardware',
            'release_year': 2022
        },
        {
            'name': 'Iceriver KS0 Pro',
            'manufacturer': 'Iceriver',
            'model': 'KS0 Pro',
            'hash_rate': 2.0,
            'power_consumption': 450,
            'algorithm': 'Kheavyhash',
            'price_usd': 2500,
            'stock_quantity': 60,
            'description': 'Compact Kaspa mining ASIC with low power consumption',
            'release_year': 2023
        },
    ]
    
    added_count = 0
    for miner_data in sample_miners:
        if not ASICMiner.query.filter_by(name=miner_data['name']).first():
            miner = ASICMiner(**miner_data)
            db.session.add(miner)
            db.session.flush()
            
            inventory = Inventory(
                miner_id=miner.id,
                quantity_available=miner_data['stock_quantity']
            )
            db.session.add(inventory)
            added_count += 1
    
    db.session.commit()
    if added_count > 0:
        print(f"✓ {added_count} sample miners added!")
    else:
        print("✓ Sample miners already exist")
    
    print("\n" + "="*50)
    print("✅ Database initialization complete!")
    print("="*50)
    print("\n📌 Demo Credentials:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n🚀 To start the application, run:")
    print("   python run.py")
    print("\n🌐 The app will be available at:")
    print("   http://localhost:5000")
    print("\n" + "="*50)

if __name__ == '__main__':
    init_database()
