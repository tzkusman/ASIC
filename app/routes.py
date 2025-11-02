from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import random
import string

from app.models import (
    db, User, ASICMiner, Order, OrderItem, Shipping, Review, 
    ProfitabilityData, MiningAnalytics, Inventory, PriceAlert
)
from app.services import ProfitabilityCalculator, CryptoPriceAPI

# Create blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
marketplace_bp = Blueprint('marketplace', __name__, url_prefix='/marketplace')
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
api_bp = Blueprint('api', __name__, url_prefix='/api')

# ==================== MAIN ROUTES ====================
@main_bp.route('/')
def index():
    """Homepage"""
    featured_miners = ASICMiner.query.filter_by(is_available=True).limit(6).all()
    top_profitable = (
        db.session.query(ASICMiner)
        .join(ProfitabilityData)
        .filter(ASICMiner.is_available == True)
        .order_by(ProfitabilityData.daily_profit_usd.desc())
        .limit(4)
        .all()
    )
    
    return render_template('index.html', featured_miners=featured_miners, top_profitable=top_profitable)

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page"""
    if request.method == 'POST':
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('main.index'))
    return render_template('contact.html')

# ==================== AUTH ROUTES ====================
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        company_name = request.form.get('company_name', '')
        country = request.form.get('country', '')
        phone = request.form.get('phone', '')
        
        # Validation
        if not all([username, email, password, confirm_password]):
            flash('Please fill in all required fields', 'error')
        elif password != confirm_password:
            flash('Passwords do not match', 'error')
        elif User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
        else:
            user = User(
                username=username,
                email=email,
                company_name=company_name,
                country=country,
                phone=phone,
                is_verified=True  # Auto-verify for demo
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=request.form.get('remember_me'))
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

# ==================== MARKETPLACE ROUTES ====================
@marketplace_bp.route('/')
def browse():
    """Browse miners marketplace"""
    page = request.args.get('page', 1, type=int)
    
    # Get filters
    algorithm = request.args.get('algorithm', '')
    manufacturer = request.args.get('manufacturer', '')
    min_price = request.args.get('min_price', '', type=float)
    max_price = request.args.get('max_price', '', type=float)
    sort_by = request.args.get('sort', 'newest')
    
    query = ASICMiner.query.filter_by(is_available=True)
    
    if algorithm:
        query = query.filter(ASICMiner.algorithm.ilike(f'%{algorithm}%'))
    if manufacturer:
        query = query.filter(ASICMiner.manufacturer.ilike(f'%{manufacturer}%'))
    if min_price:
        query = query.filter(ASICMiner.price_usd >= min_price)
    if max_price:
        query = query.filter(ASICMiner.price_usd <= max_price)
    
    # Sorting
    if sort_by == 'price_low':
        query = query.order_by(ASICMiner.price_usd.asc())
    elif sort_by == 'price_high':
        query = query.order_by(ASICMiner.price_usd.desc())
    elif sort_by == 'profitability':
        query = query.order_by(ASICMiner.profitability_score.desc())
    else:
        query = query.order_by(ASICMiner.created_at.desc())
    
    miners = query.paginate(page=page, per_page=12)
    
    algorithms = db.session.query(ASICMiner.algorithm).distinct().all()
    manufacturers = db.session.query(ASICMiner.manufacturer).distinct().all()
    
    return render_template(
        'marketplace/browse.html',
        miners=miners,
        algorithms=[a[0] for a in algorithms],
        manufacturers=[m[0] for m in manufacturers]
    )

@marketplace_bp.route('/miner/<int:miner_id>')
def miner_detail(miner_id):
    """Miner detail page"""
    miner = ASICMiner.query.get_or_404(miner_id)
    profitability = miner.get_latest_profitability()
    reviews = Review.query.filter_by(miner_id=miner_id).order_by(Review.created_at.desc()).all()
    related_miners = (
        ASICMiner.query
        .filter(ASICMiner.algorithm == miner.algorithm)
        .filter(ASICMiner.id != miner_id)
        .filter_by(is_available=True)
        .limit(4)
        .all()
    )
    
    return render_template(
        'marketplace/detail.html',
        miner=miner,
        profitability=profitability,
        reviews=reviews,
        related_miners=related_miners
    )

@marketplace_bp.route('/compare')
def compare():
    """Compare multiple miners"""
    miner_ids = request.args.getlist('miners', type=int)
    miners = ASICMiner.query.filter(ASICMiner.id.in_(miner_ids)).all() if miner_ids else []
    
    return render_template('marketplace/compare.html', miners=miners)

# ==================== DASHBOARD ROUTES ====================
@dashboard_bp.route('/')
@login_required
def overview():
    """User dashboard overview"""
    user_orders = Order.query.filter_by(user_id=current_user.id).count()
    favorite_miners = current_user.favorites.count()
    
    return render_template(
        'dashboard/overview.html',
        user_orders=user_orders,
        favorite_miners=favorite_miners
    )

@dashboard_bp.route('/orders')
@login_required
def my_orders():
    """View user orders"""
    page = request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(user_id=current_user.id).order_by(
        Order.created_at.desc()
    ).paginate(page=page, per_page=10)
    
    return render_template('dashboard/orders.html', orders=orders)

@dashboard_bp.route('/calculator')
@login_required
def profitability_calculator():
    """Profitability calculator"""
    miners = ASICMiner.query.filter_by(is_available=True).all()
    return render_template('dashboard/calculator.html', miners=miners)

@dashboard_bp.route('/profile')
@login_required
def profile():
    """User profile"""
    return render_template('dashboard/profile.html', user=current_user)

@dashboard_bp.route('/profile/edit', methods=['POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    current_user.company_name = request.form.get('company_name', '')
    current_user.country = request.form.get('country', '')
    current_user.phone = request.form.get('phone', '')
    db.session.commit()
    
    flash('Profile updated successfully', 'success')
    return redirect(url_for('dashboard.profile'))

@dashboard_bp.route('/favorites')
@login_required
def favorites():
    """User favorite miners"""
    page = request.args.get('page', 1, type=int)
    favorites = current_user.favorites.paginate(page=page, per_page=12)
    return render_template('dashboard/favorites.html', favorites=favorites)

# ==================== ADMIN ROUTES ====================
@admin_bp.route('/')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    if not current_user.is_admin:
        flash('You do not have permission to access this page', 'error')
        return redirect(url_for('main.index'))
    
    total_miners = ASICMiner.query.count()
    total_users = User.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    
    return render_template(
        'admin/dashboard.html',
        total_miners=total_miners,
        total_users=total_users,
        total_orders=total_orders,
        total_revenue=total_revenue
    )

@admin_bp.route('/miners')
@login_required
def manage_miners():
    """Manage miners"""
    if not current_user.is_admin:
        flash('You do not have permission to access this page', 'error')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    miners = ASICMiner.query.paginate(page=page, per_page=20)
    return render_template('admin/miners.html', miners=miners)

@admin_bp.route('/miners/add', methods=['GET', 'POST'])
@login_required
def add_miner():
    """Add new miner"""
    if not current_user.is_admin:
        flash('You do not have permission to access this page', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        miner = ASICMiner(
            name=request.form.get('name'),
            manufacturer=request.form.get('manufacturer'),
            model=request.form.get('model'),
            hash_rate=float(request.form.get('hash_rate', 0)),
            power_consumption=int(request.form.get('power_consumption', 0)),
            algorithm=request.form.get('algorithm'),
            price_usd=float(request.form.get('price_usd', 0)),
            stock_quantity=int(request.form.get('stock_quantity', 0)),
            description=request.form.get('description'),
            release_year=int(request.form.get('release_year', 0)) or None
        )
        db.session.add(miner)
        db.session.flush()
        
        # Create inventory record
        inventory = Inventory(
            miner_id=miner.id,
            quantity_available=int(request.form.get('stock_quantity', 0))
        )
        db.session.add(inventory)
        db.session.commit()
        
        flash('Miner added successfully', 'success')
        return redirect(url_for('admin.manage_miners'))
    
    return render_template('admin/add_miner.html')

# ==================== API ROUTES ====================
@api_bp.route('/miners')
def api_miners():
    """API endpoint for miners"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    
    query = ASICMiner.query.filter_by(is_available=True)
    
    algorithm = request.args.get('algorithm')
    if algorithm:
        query = query.filter(ASICMiner.algorithm.ilike(f'%{algorithm}%'))
    
    miners_page = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'success': True,
        'data': [{
            'id': m.id,
            'name': m.name,
            'manufacturer': m.manufacturer,
            'hash_rate': m.hash_rate,
            'power_consumption': m.power_consumption,
            'algorithm': m.algorithm,
            'price_usd': m.price_usd,
            'profitability_score': m.profitability_score
        } for m in miners_page.items],
        'pagination': {
            'page': miners_page.page,
            'per_page': miners_page.per_page,
            'total': miners_page.total,
            'pages': miners_page.pages
        }
    })

@api_bp.route('/miner/<int:miner_id>/profitability')
def api_miner_profitability(miner_id):
    """Get miner profitability data"""
    miner = ASICMiner.query.get_or_404(miner_id)
    
    electricity_cost = request.args.get('electricity_cost', 0.12, type=float)
    pool_fee = request.args.get('pool_fee', 0.01, type=float)
    
    profitability = ProfitabilityCalculator.calculate_miner_profitability(
        miner, electricity_cost, pool_fee
    )
    
    return jsonify({'success': True, 'data': profitability})

@api_bp.route('/miner/<int:miner_id>/add-to-favorites', methods=['POST'])
@login_required
def api_add_favorite(miner_id):
    """Add miner to favorites"""
    miner = ASICMiner.query.get_or_404(miner_id)
    
    if miner in current_user.favorites:
        return jsonify({'success': False, 'message': 'Already in favorites'}), 400
    
    current_user.favorites.append(miner)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Added to favorites'})

@api_bp.route('/miner/<int:miner_id>/remove-from-favorites', methods=['POST'])
@login_required
def api_remove_favorite(miner_id):
    """Remove miner from favorites"""
    miner = ASICMiner.query.get_or_404(miner_id)
    
    if miner not in current_user.favorites:
        return jsonify({'success': False, 'message': 'Not in favorites'}), 400
    
    current_user.favorites.remove(miner)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Removed from favorites'})

@api_bp.route('/cart/checkout', methods=['POST'])
@login_required
def api_checkout():
    """Checkout cart"""
    data = request.get_json()
    cart_items = data.get('items', [])
    shipping_info = data.get('shipping_info', {})
    
    if not cart_items:
        return jsonify({'success': False, 'message': 'Cart is empty'}), 400
    
    try:
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{random.randint(10000,99999)}"
        
        total_amount = 0
        order = Order(
            order_number=order_number,
            user_id=current_user.id,
            shipping_address=shipping_info.get('address', ''),
            billing_address=shipping_info.get('billing_address', shipping_info.get('address', '')),
            payment_method='credit_card'
        )
        db.session.add(order)
        db.session.flush()
        
        for item in cart_items:
            miner = ASICMiner.query.get(item['miner_id'])
            quantity = int(item['quantity'])
            
            if not miner or miner.stock_quantity < quantity:
                return jsonify({'success': False, 'message': f'Insufficient stock for {miner.name if miner else "item"}'}), 400
            
            item_total = miner.price_usd * quantity
            total_amount += item_total
            
            order_item = OrderItem(
                order_id=order.id,
                miner_id=miner.id,
                quantity=quantity,
                unit_price=miner.price_usd,
                total_price=item_total
            )
            db.session.add(order_item)
            miner.stock_quantity -= quantity
        
        order.total_amount = total_amount
        
        # Create shipping record
        shipping = Shipping(order_id=order.id)
        shipping.generate_tracking_number()
        db.session.add(shipping)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'order_id': order.id,
            'order_number': order.order_number,
            'total_amount': total_amount
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/crypto-prices')
def api_crypto_prices():
    """Get current cryptocurrency prices"""
    api = CryptoPriceAPI()
    prices = api.get_crypto_prices(['bitcoin', 'ethereum', 'litecoin', 'dogecoin'])
    
    return jsonify({'success': True, 'data': prices})
