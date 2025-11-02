# Deployment Guide - CryptoMinerPro

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Create a repository named `CryptoMinerPro`
3. Choose "Public" if you want it publicly visible
4. Do NOT initialize with README (we already have one)

## Step 2: Push to GitHub

After creating the repository, run these commands:

```bash
cd g:\Openai\ASIC\CryptoMinerPro

# Add remote origin
git remote add origin https://github.com/YOUR_USERNAME/CryptoMinerPro.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 3: Deploy to Vercel

### Option A: Using Vercel CLI

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
cd g:\Openai\ASIC\CryptoMinerPro
vercel
```

3. Follow the interactive prompts to deploy

### Option B: Connect GitHub to Vercel

1. Go to https://vercel.com
2. Sign up with GitHub
3. Click "Import Project"
4. Select your CryptoMinerPro repository
5. Configure environment variables:
   - DATABASE_URL: Your PostgreSQL URL
   - REDIS_URL: Your Redis URL
   - SECRET_KEY: Your secret key
6. Click Deploy

## Step 4: Set Environment Variables on Vercel

In Vercel Dashboard:
1. Go to Settings → Environment Variables
2. Add the following:
   - `FLASK_ENV`: `production`
   - `DATABASE_URL`: Your PostgreSQL database URL
   - `REDIS_URL`: Your Redis URL
   - `SECRET_KEY`: A secure random string
   - `COINGECKO_API_KEY`: Optional, get from coingecko.com

## Step 5: Initialize Database (First Time Only)

After deployment, SSH into your server or use database client:

```bash
# SSH or Cloud Shell
python run.py

# In Flask shell:
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
...     # Then run init_db
```

Or use:
```bash
flask --app run init-db
```

## Database Setup

### PostgreSQL (Recommended for Production)

1. **DigitalOcean Managed PostgreSQL**:
   - Sign up at https://www.digitalocean.com
   - Create a managed PostgreSQL database
   - Copy connection string to `DATABASE_URL`

2. **Heroku Postgres** (if using Heroku):
   ```bash
   heroku addons:create heroku-postgresql:standard-0
   ```

3. **Self-hosted**:
   ```bash
   postgresql://user:password@host:5432/mining_marketplace
   ```

### Redis Setup

1. **DigitalOcean Managed Redis**:
   - Create managed Redis in your DO account
   - Copy connection string to `REDIS_URL`

2. **Redis Cloud** (https://redis.com):
   - Sign up free
   - Create database
   - Use connection string

## SSL/HTTPS

Vercel automatically provides HTTPS. For custom domains:

1. Add your domain to Vercel project
2. Update DNS records as instructed
3. SSL certificate is automatically provisioned

## Monitoring & Logging

### Vercel Logs
```bash
vercel logs
```

### Error Tracking (Optional)
Add Sentry for error tracking:
```bash
pip install sentry-sdk
```

Configure in `run.py`:
```python
import sentry_sdk
sentry_sdk.init("YOUR_SENTRY_DSN")
```

## Performance Optimization

1. **Enable CDN**: Already included with Vercel
2. **Database Connection Pooling**: Configured in `config.py`
3. **Redis Caching**: Enabled for frequently accessed data
4. **Compression**: Enable GZIP in Vercel settings

## Scaling

- **Compute**: Vercel automatically scales serverless functions
- **Database**: Upgrade PostgreSQL tier if needed
- **Cache**: Upgrade Redis tier if needed

## Troubleshooting

### Build Fails
- Check build logs in Vercel dashboard
- Verify all dependencies in requirements.txt
- Check Python version compatibility

### Database Connection Errors
- Verify DATABASE_URL environment variable
- Check network access rules in database provider
- Ensure firewall allows Vercel IPs

### Slow Performance
- Check database query logs
- Monitor Redis memory usage
- Review Vercel Analytics

## Continuous Deployment

Every push to main branch automatically triggers:
1. Vercel build
2. Database migrations (if applicable)
3. Deployment to production

To disable:
- Go to Project Settings → Git
- Modify deployment settings

## Backup Strategy

1. **Database**: Use managed backups from your provider
2. **Data Export**: Regular exports to cloud storage
3. **Code**: Backed up on GitHub

## Production Checklist

- [ ] Environment variables set correctly
- [ ] Database created and initialized
- [ ] Redis cache working
- [ ] HTTPS enabled
- [ ] Domain configured
- [ ] Backups enabled
- [ ] Monitoring active
- [ ] Logging configured
- [ ] Error tracking active
- [ ] Performance acceptable

## Support

For issues:
1. Check Vercel documentation: https://vercel.com/docs
2. Check Flask documentation: https://flask.palletsprojects.com
3. Check deployment provider docs

---

**🚀 Your CryptoMinerPro is now live!**
