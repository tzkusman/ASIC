# CryptoMinerPro - ASIC Mining Equipment Marketplace

A comprehensive full-stack web application for buying, selling, and analyzing ASIC mining equipment with real-time profitability calculations.

## Features

- 🔍 **Advanced Marketplace** - Browse and compare ASIC miners with advanced filtering
- 📊 **Real-Time Profitability** - Calculate daily/monthly/yearly profits with live crypto data
- 💾 **User Authentication** - Secure registration and login system
- 🛒 **E-Commerce** - Complete shopping cart and order management
- 📈 **Analytics Dashboard** - Comprehensive mining analytics and ROI calculations
- ⭐ **Reviews & Ratings** - Community reviews for transparency
- 🌍 **Global Shipping** - International delivery with tracking
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile

## Tech Stack

### Backend
- **Framework**: Flask 3.0
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis for performance optimization
- **Task Queue**: Celery for background tasks
- **Authentication**: Flask-Login with password hashing

### Frontend
- **HTML5** & **CSS3** with Bootstrap 5
- **JavaScript** with jQuery
- **Chart.js** for data visualization
- **Responsive Design** with mobile-first approach

### DevOps
- **Containerization**: Docker & Docker Compose
- **Web Server**: Gunicorn
- **Reverse Proxy**: Nginx
- **Deployment**: Vercel / AWS / DigitalOcean

## Project Structure

```
CryptoMinerPro/
├── app/
│   ├── __init__.py           # App factory
│   ├── models.py             # Database models
│   ├── routes.py             # API routes
│   ├── services.py           # Business logic
│   ├── config.py             # Configuration
│   ├── static/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── images/
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── auth/
│       ├── marketplace/
│       ├── dashboard/
│       └── admin/
├── run.py                    # Entry point
├── requirements.txt          # Dependencies
├── docker-compose.yml        # Docker configuration
├── .env                      # Environment variables
└── README.md
```

## Installation

### Prerequisites
- Python 3.11+
- PostgreSQL 12+
- Redis 6+
- Docker & Docker Compose (optional)

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/CryptoMinerPro.git
cd CryptoMinerPro
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database**
```bash
flask --app run init-db
```

6. **Run the application**
```bash
python run.py
```

The application will be available at `http://localhost:5000`

### Docker Setup

```bash
docker-compose up -d
```

## Configuration

### Environment Variables (.env)
```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/mining_marketplace
REDIS_URL=redis://localhost:6379/0
COINGECKO_API_KEY=your-api-key
```

## Database Models

- **User** - User accounts and authentication
- **ASICMiner** - Mining hardware inventory
- **Order** - Customer orders
- **OrderItem** - Items within orders
- **ProfitabilityData** - Real-time profitability calculations
- **Cryptocurrency** - Crypto price and network data
- **MiningAnalytics** - User mining calculations
- **Review** - Product reviews and ratings
- **PriceAlert** - Price monitoring alerts

## API Endpoints

### Public
- `GET /` - Homepage
- `GET /marketplace/` - Browse miners
- `GET /marketplace/miner/<id>` - Miner details
- `GET /api/miners` - List miners (JSON)
- `GET /api/miner/<id>/profitability` - Profitability data

### Protected (Authentication Required)
- `POST /api/miner/<id>/add-to-favorites` - Add to favorites
- `POST /api/miner/<id>/remove-from-favorites` - Remove favorite
- `POST /api/cart/checkout` - Place order
- `GET /dashboard/` - User dashboard
- `GET /dashboard/orders` - Order history

### Admin
- `GET /admin/` - Admin dashboard
- `GET /admin/miners` - Manage miners
- `POST /admin/miners/add` - Add new miner

## Features Implementation

### Phase 1 (Current)
- ✅ User authentication and profiles
- ✅ Miner marketplace with search and filtering
- ✅ Real-time profitability calculations
- ✅ Shopping cart and orders
- ✅ User dashboard
- ✅ Admin panel basics

### Phase 2 (Planned)
- 🔄 Multi-currency support
- 🔄 Mining pool integration
- 🔄 Advanced analytics dashboard
- 🔄 Mobile app (React Native)
- 🔄 API for third-party integrations

### Phase 3 (Future)
- 🎯 Hardware leasing options
- 🎯 Secondary market for used equipment
- 🎯 Insurance options
- 🎯 Mining farm management tools

## Deployment

### Vercel Deployment
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

### Traditional Deployment
```bash
# Build with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app

# Use Nginx as reverse proxy
# Configure environment on server
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details

## Support

- 📧 Email: support@cryptominerpro.com
- 💬 Discord: [Join our community](https://discord.gg/cryptominerpro)
- 🐦 Twitter: [@CryptoMinerPro](https://twitter.com/cryptominerpro)

## Roadmap

- Q1 2024: Launch marketplace MVP
- Q2 2024: Mobile app beta
- Q3 2024: Pool integration
- Q4 2024: Global expansion

---

Made with ❤️ for the mining community
