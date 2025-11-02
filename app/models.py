from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
import string

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and profile management"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255))
    company_name = db.Column(db.String(200))
    country = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    is_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    orders = db.relationship('Order', backref='customer', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='author', lazy=True, cascade='all, delete-orphan')
    mining_analytics = db.relationship('MiningAnalytics', backref='user', lazy=True, cascade='all, delete-orphan')
    favorites = db.relationship('ASICMiner', secondary='user_favorites', backref=db.backref('favorited_by', lazy='dynamic'))
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

# Association table for user favorites
user_favorites = db.Table(
    'user_favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('miner_id', db.Integer, db.ForeignKey('asic_miner.id'), primary_key=True)
)

class ASICMiner(db.Model):
    """ASIC Mining hardware model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    manufacturer = db.Column(db.String(100), nullable=False, index=True)  # Bitmain, MicroBT, etc.
    model = db.Column(db.String(100), nullable=False)
    hash_rate = db.Column(db.Float, nullable=False)  # TH/s
    power_consumption = db.Column(db.Integer, nullable=False)  # Watts
    algorithm = db.Column(db.String(50), nullable=False, index=True)  # SHA-256, Scrypt, etc.
    price_usd = db.Column(db.Float, nullable=False, index=True)
    stock_quantity = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500))
    description = db.Column(db.Text)
    release_year = db.Column(db.Integer)
    profitability_score = db.Column(db.Float, default=0.0)  # Calculated field
    efficiency_rating = db.Column(db.Float, default=0.0)  # J/GH
    is_available = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('OrderItem', backref='miner', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='miner', lazy=True, cascade='all, delete-orphan')
    profitability_data = db.relationship('ProfitabilityData', backref='miner', lazy=True, cascade='all, delete-orphan')
    inventory = db.relationship('Inventory', backref='asic_miner', lazy=True, uselist=False, cascade='all, delete-orphan')
    
    def get_average_rating(self):
        """Calculate average rating from reviews"""
        if not self.reviews:
            return 0
        return sum(r.rating for r in self.reviews) / len(self.reviews)
    
    def get_latest_profitability(self):
        """Get most recent profitability data"""
        return ProfitabilityData.query.filter_by(miner_id=self.id).order_by(ProfitabilityData.timestamp.desc()).first()
    
    def __repr__(self):
        return f'<ASICMiner {self.name}>'

class Inventory(db.Model):
    """Inventory tracking for miners"""
    id = db.Column(db.Integer, primary_key=True)
    miner_id = db.Column(db.Integer, db.ForeignKey('asic_miner.id'), nullable=False, unique=True)
    warehouse_location = db.Column(db.String(100), default='Main Warehouse')
    quantity_available = db.Column(db.Integer, default=0)
    reserved_quantity = db.Column(db.Integer, default=0)
    last_restock = db.Column(db.DateTime)
    next_restock_expected = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_available_quantity(self):
        """Get available quantity minus reserved"""
        return max(0, self.quantity_available - self.reserved_quantity)
    
    def __repr__(self):
        return f'<Inventory {self.miner_id}: {self.quantity_available} units>'

class Order(db.Model):
    """Customer orders"""
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending', index=True)  # pending, confirmed, shipped, delivered, cancelled
    shipping_address = db.Column(db.Text, nullable=False)
    billing_address = db.Column(db.Text, nullable=False)
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(50), default='pending', index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    shipping = db.relationship('Shipping', backref='order', uselist=False, cascade='all, delete-orphan')
    
    def get_total_items(self):
        """Get total number of items in order"""
        return sum(item.quantity for item in self.items)
    
    def __repr__(self):
        return f'<Order {self.order_number}>'

class OrderItem(db.Model):
    """Individual items in an order"""
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    miner_id = db.Column(db.Integer, db.ForeignKey('asic_miner.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<OrderItem {self.order_id}-{self.miner_id}>'

class Shipping(db.Model):
    """Shipping information for orders"""
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False, unique=True)
    tracking_number = db.Column(db.String(100), unique=True)
    carrier = db.Column(db.String(100), default='DHL')
    shipping_cost = db.Column(db.Float, default=0.0)
    estimated_delivery = db.Column(db.DateTime)
    actual_delivery = db.Column(db.DateTime)
    shipping_status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def generate_tracking_number(self):
        """Generate unique tracking number"""
        self.tracking_number = 'CMP' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    def __repr__(self):
        return f'<Shipping {self.tracking_number}>'

class Review(db.Model):
    """Customer reviews for miners"""
    id = db.Column(db.Integer, primary_key=True)
    miner_id = db.Column(db.Integer, db.ForeignKey('asic_miner.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    verified_purchase = db.Column(db.Boolean, default=False)
    helpful_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Review {self.id}: {self.rating}★>'

class ProfitabilityData(db.Model):
    """Real-time profitability data for miners"""
    id = db.Column(db.Integer, primary_key=True)
    miner_id = db.Column(db.Integer, db.ForeignKey('asic_miner.id'), nullable=False, index=True)
    daily_profit_usd = db.Column(db.Float, default=0.0)
    monthly_profit_usd = db.Column(db.Float, default=0.0)
    yearly_profit_usd = db.Column(db.Float, default=0.0)
    electricity_cost = db.Column(db.Float, default=0.12)  # $ per kWh
    net_profit_daily = db.Column(db.Float, default=0.0)
    roi_days = db.Column(db.Float, default=0.0)  # Return on Investment calculation
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    data_source = db.Column(db.String(100), default='internal')  # miningnow.com, whattomine.com, etc.
    
    def __repr__(self):
        return f'<ProfitabilityData {self.miner_id}: ${self.daily_profit_usd:.2f}/day>'

class Cryptocurrency(db.Model):
    """Cryptocurrency data"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    symbol = db.Column(db.String(20), nullable=False, unique=True, index=True)
    current_price = db.Column(db.Float, default=0.0)
    market_cap = db.Column(db.Float)
    algorithm = db.Column(db.String(50), index=True)
    network_difficulty = db.Column(db.Float)
    block_reward = db.Column(db.Float)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Cryptocurrency {self.symbol}: ${self.current_price:.2f}>'

class MiningAnalytics(db.Model):
    """User's mining analytics and calculations"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    miner_id = db.Column(db.Integer, db.ForeignKey('asic_miner.id'), nullable=False, index=True)
    electricity_rate = db.Column(db.Float, default=0.12)  # Default $0.12 per kWh
    mining_pool_fee = db.Column(db.Float, default=0.01)  # 1% pool fee
    calculated_profitability = db.Column(db.Float, default=0.0)
    last_calculated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MiningAnalytics {self.user_id}: ${self.calculated_profitability:.2f}>'

class PriceAlert(db.Model):
    """Price alerts for users"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    miner_id = db.Column(db.Integer, db.ForeignKey('asic_miner.id'), nullable=False)
    target_price = db.Column(db.Float, nullable=False)
    alert_type = db.Column(db.String(20), default='drops_to')  # drops_to, rises_to
    is_active = db.Column(db.Boolean, default=True)
    triggered = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    triggered_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<PriceAlert {self.miner_id}: {self.alert_type} ${self.target_price}>'
