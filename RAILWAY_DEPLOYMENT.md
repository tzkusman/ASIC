# 🚀 Railway Deployment Guide - CryptoMinerPro

Your Flask app with PostgreSQL database is ready to deploy on Railway!

## ✅ What's Ready:
- ✓ Flask backend configured for PostgreSQL
- ✓ Procfile for Gunicorn WSGI server
- ✓ Database migration scripts
- ✓ Environment variables configured
- ✓ All code pushed to GitHub

## 📋 Deployment Steps (5 minutes):

### Step 1: Create Railway Account
1. Go to https://railway.app/
2. Click "Start Project"
3. Sign in with GitHub

### Step 2: Create New Project
1. Click "New Project"
2. Select "GitHub Repo"
3. Authorize Railway to access GitHub
4. Select repository: **tzkusman/ASIC**
5. Click "Deploy"

### Step 3: Add PostgreSQL Database
1. In Railway dashboard, click "Add Service"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically create one!

### Step 4: Configure Environment Variables
Railway will auto-detect:
- `DATABASE_URL` - PostgreSQL connection string (automatic)
- `FLASK_ENV` - Set to `production`

To manually add:
1. In Railway project, go to "Variables"
2. Add: `FLASK_ENV` = `production`
3. Add: `SECRET_KEY` = (your secret key)

### Step 5: Deploy!
1. Railway will auto-build your app
2. It automatically runs Python/PostgreSQL
3. Your app will be live in ~2 minutes!

## 📊 What You Get:
- ✅ Free PostgreSQL database (PostgreSQL 14)
- ✅ 5GB storage free tier
- ✅ Full Flask app running
- ✅ Custom domain (railway.app subdomain)
- ✅ Automatic deployments on GitHub push

## 🔗 Access Your App:
1. After deployment, Railway shows your public URL
2. It looks like: `https://cryptominerpro-production.railway.app/`
3. Database automatically persists!

## 💾 Database Initialization:
1. Railway runs migrations automatically
2. Admin user will be created on first run
3. Sample miners loaded into database

## 🆕 Future Deployments:
Any push to `main` branch automatically redeploys on Railway!

```bash
git push origin main  # Automatic deployment!
```

## 📞 Support:
- Railway Docs: https://docs.railway.app/
- Flask + PostgreSQL: Works perfectly on Railway
- Custom domain: Available in paid plans

---

**Ready? Visit https://railway.app/ and connect your GitHub repo!** 🚀
