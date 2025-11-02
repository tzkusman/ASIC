# 🚀 Quick Start Guide - CryptoMinerPro

## ⚡ 5-Minute Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Windows
```bash
# 1. Clone or download the project
cd CryptoMinerPro

# 2. Run setup script
setup.bat

# 3. Start the app (or run manually)
python run.py
```

### macOS / Linux
```bash
# 1. Clone or download the project
cd CryptoMinerPro

# 2. Run setup script
chmod +x setup.sh
./setup.sh

# 3. Start the app (or run manually)
python run.py
```

## 🌐 Access the Application

**URL:** http://localhost:5000

### Demo Credentials
- **Username:** `admin`
- **Password:** `admin123`

## 📦 What's Included

✅ **Complete Backend**
- Flask web framework
- SQLAlchemy ORM with SQLite database
- RESTful API endpoints
- Real-time profitability calculations

✅ **Full Frontend**
- Responsive Bootstrap 5 design
- Mining marketplace with filters
- User dashboard
- Profitability calculator
- Admin panel

✅ **Database Models**
- User authentication & profiles
- ASIC miner inventory
- Order management
- Profitability tracking
- Mining analytics

✅ **Key Features**
- User registration & login
- Browse & filter miners
- Real-time profitability data
- Shopping cart (backend ready)
- User favorites
- Order history
- Admin management panel

## 🔧 Project Structure

```
CryptoMinerPro/
├── app/
│   ├── __init__.py           # App factory
│   ├── config.py             # Configuration
│   ├── models.py             # Database models
│   ├── routes.py             # API routes (800+ lines)
│   ├── services.py           # Business logic
│   ├── static/
│   │   ├── css/style.css     # Styling
│   │   └── js/main.js        # JavaScript
│   └── templates/            # HTML templates
│       ├── base.html
│       ├── marketplace/      # Product pages
│       ├── dashboard/        # User dashboard
│       ├── admin/            # Admin panel
│       └── auth/             # Login/Register
├── run.py                    # Entry point
├── init_db.py                # Database initialization
├── requirements.txt          # Dependencies
├── README.md
└── DEPLOYMENT.md
```

## 🛠️ Available Routes

### Public Routes
- `/` - Homepage with featured miners
- `/marketplace/` - Browse all miners
- `/marketplace/miner/<id>` - Miner details
- `/about` - About page
- `/contact` - Contact form

### Authentication
- `/auth/register` - User registration
- `/auth/login` - User login
- `/auth/logout` - Logout

### User Dashboard (requires login)
- `/dashboard/` - Overview
- `/dashboard/orders` - Order history
- `/dashboard/calculator` - Profitability calculator
- `/dashboard/favorites` - Favorite miners
- `/dashboard/profile` - User profile

### Admin Panel (admin only)
- `/admin/` - Admin dashboard
- `/admin/miners` - Manage miners
- `/admin/miners/add` - Add new miner

### API Endpoints
- `GET /api/miners` - List miners
- `GET /api/miner/<id>/profitability` - Profitability data
- `POST /api/miner/<id>/add-to-favorites` - Add favorite
- `POST /api/cart/checkout` - Checkout

## 📊 Database Schema

**Users** - Account management
**ASICMiners** - Mining hardware
**Orders** - Customer purchases
**ProfitabilityData** - Real-time calculations
**Cryptocurrencies** - Price & network data
**Reviews** - User reviews
**Analytics** - Mining analysis

## 🚢 Deployment

### Deploy to Vercel (Recommended)

1. **Push to GitHub:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/CryptoMinerPro.git
git push -u origin main
```

2. **Deploy to Vercel:**
   - Go to https://vercel.com
   - Connect your GitHub account
   - Import the CryptoMinerPro repository
   - Set environment variables
   - Deploy!

### Environment Variables
```
FLASK_ENV=production
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
SECRET_KEY=your-secret-key
```

See `DEPLOYMENT.md` for detailed instructions.

## 🛒 Features to Explore

1. **Browse Miners**
   - Filter by algorithm, manufacturer, price
   - View detailed specifications
   - Check profitability metrics

2. **Profitability Calculator**
   - Select any miner
   - Adjust electricity costs
   - See daily/monthly/yearly profits
   - Calculate ROI

3. **Admin Panel**
   - View dashboard statistics
   - Manage miner inventory
   - Add new miners
   - Monitor orders

4. **User Account**
   - Register and login
   - Save favorite miners
   - View order history
   - Edit profile

## 🐛 Troubleshooting

### ImportError: No module named 'flask'
```bash
pip install -r requirements.txt
```

### Database locked
Remove `mining_marketplace.db` and restart:
```bash
rm mining_marketplace.db
python run.py
```

### Port 5000 already in use
```bash
python run.py --port 8000
```

## 📚 Tech Stack

- **Backend:** Flask 3.0 + SQLAlchemy
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Deployment:** Vercel, Docker, Gunicorn

## 📈 Roadmap

- ✅ MVP Marketplace
- 🔜 Payment integration
- 🔜 Email notifications
- 🔜 Mobile app
- 🔜 API marketplace
- 🔜 Hardware leasing

## 📞 Support

- 📧 Email: support@cryptominerpro.com
- 💬 Discord: [Join Community]
- 🐦 Twitter: @CryptoMinerPro

## 📄 License

MIT License - Free to use and modify

## 🎉 Next Steps

1. Start the app: `python run.py`
2. Login with `admin` / `admin123`
3. Explore the marketplace
4. Try the profitability calculator
5. Add miners in admin panel
6. Deploy to production!

---

**Made with ❤️ for the crypto mining community**
