from flask import Flask, render_template
from flask_login import LoginManager
from flask_cors import CORS
from app.models import db, User
from app.config import config
import os

def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.routes import main_bp, auth_bp, marketplace_bp, dashboard_bp, admin_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(marketplace_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return render_template('errors/500.html'), 500
    
    # Create database tables and seed initial data
    with app.app_context():
        db.create_all()
        # Seed initial data if needed
        _seed_initial_data()
    
    return app

def _seed_initial_data():
    """Seed initial data if tables are empty"""
    from app.models import User, ASICMiner, Inventory
    
    # Create admin user if doesn't exist
    if User.query.filter_by(username='admin').first() is None:
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
        print("✓ Admin user created")
    
    # Create sample miners if don't exist
    if ASICMiner.query.count() == 0:
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
        ]
        
        for miner_data in sample_miners:
            miner = ASICMiner(**miner_data)
            db.session.add(miner)
            db.session.flush()
            
            inventory = Inventory(
                miner_id=miner.id,
                quantity_available=miner_data['stock_quantity']
            )
            db.session.add(inventory)
        
        db.session.commit()
        print(f"✓ {len(sample_miners)} sample miners created")
