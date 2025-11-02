import os
from app import create_app, db
from app.models import User, ASICMiner, Inventory, ProfitabilityData, Cryptocurrency
from app.services import ProfitabilityCalculator, CryptoPriceAPI

app = create_app(os.environ.get('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Register shell context"""
    return {
        'db': db,
        'User': User,
        'ASICMiner': ASICMiner,
        'ProfitabilityData': ProfitabilityData,
        'Cryptocurrency': Cryptocurrency,
        'ProfitabilityCalculator': ProfitabilityCalculator
    }

@app.cli.command()
def init_db():
    """Initialize database with sample data"""
    db.create_all()
    
    # Add admin user
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
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
        print("Admin user created: admin / admin123")
    
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
        {
            'name': 'Antminer E9',
            'manufacturer': 'Bitmain',
            'model': 'E9',
            'hash_rate': 2400.0,
            'power_consumption': 1920,
            'algorithm': 'Ethash',
            'price_usd': 9000,
            'stock_quantity': 15,
            'description': 'Ethereum mining ASIC with exceptional performance',
            'release_year': 2022
        }
    ]
    
    for miner_data in sample_miners:
        if not ASICMiner.query.filter_by(name=miner_data['name']).first():
            miner = ASICMiner(**miner_data)
            db.session.add(miner)
            db.session.flush()
            
            # Create inventory record
            inventory = Inventory(
                miner_id=miner.id,
                quantity_available=miner_data['stock_quantity']
            )
            db.session.add(inventory)
    
    db.session.commit()
    print("Database initialized with sample data")

@app.cli.command()
def update_profitability():
    """Update profitability data for all miners"""
    ProfitabilityCalculator.update_all_profitability_data()
    print("Profitability data updated")

@app.cli.command()
def update_crypto_prices():
    """Update cryptocurrency prices"""
    api = CryptoPriceAPI()
    api.update_crypto_data()
    print("Cryptocurrency prices updated")

if __name__ == '__main__':
    # Use use_reloader=False to prevent reload issues on Windows
    app.run(debug=False, host='0.0.0.0', port=5000)
