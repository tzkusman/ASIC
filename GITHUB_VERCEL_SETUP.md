# 🚀 GitHub & Vercel Deployment Guide

## Step 1: Push to GitHub

### Create a GitHub Repository

1. Go to https://github.com/new
2. Repository name: `CryptoMinerPro`
3. Description: `Global ASIC Mining Equipment Marketplace with Real-Time Profitability Analytics`
4. Choose: **Public** (for visibility)
5. Do NOT check "Initialize with README" (we have files)
6. Click "Create repository"

### Push Your Code to GitHub

Run these commands in your CryptoMinerPro directory:

```bash
# Add remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/CryptoMinerPro.git

# Rename branch to main
git branch -M main

# Push all commits to GitHub
git push -u origin main
```

**That's it!** Your code is now on GitHub.

---

## Step 2: Deploy to Vercel

### Prerequisites
- Vercel account (free tier available)
- GitHub account (already done!)

### Deploy via Vercel Dashboard (Easiest)

1. **Go to Vercel**
   - Visit https://vercel.com
   - Click "Sign Up"
   - Choose "Continue with GitHub"
   - Authorize Vercel to access your GitHub repos

2. **Import Project**
   - Click "Add New..." → "Project"
   - Find and select "CryptoMinerPro"
   - Click "Import"

3. **Configure Project**
   - Framework Preset: "Other"
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: (leave blank)
   - Install Command: `pip install -r requirements.txt`

4. **Set Environment Variables**
   - Click "Environment Variables"
   - Add these variables:

```
FLASK_ENV           = production
SECRET_KEY          = your-very-secret-key-change-this-12345
DATABASE_URL        = sqlite:///mining_marketplace.db
DEBUG               = False
```

5. **Deploy**
   - Click "Deploy"
   - Wait for build to complete (2-3 minutes)
   - Get your Vercel URL!

---

## Step 3: Configure Vercel (Advanced)

### Add Custom Domain (Optional)

1. Go to Vercel Dashboard → Your Project
2. Settings → Domains
3. Add your custom domain
4. Update DNS records as instructed

### Enable Auto-Deployments

- **Automatic:** Every push to `main` automatically deploys
- Vercel → Settings → Git → Production Branch: `main`

### Monitor Deployments

- Vercel Dashboard shows all deployments
- View build logs for any errors
- Rollback to previous version if needed

---

## Troubleshooting

### Build Fails: "ModuleNotFoundError"
**Solution:** Verify all packages in `requirements.txt`
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Database Connection Error
**For production:** Use PostgreSQL instead of SQLite
- Sign up for DigitalOcean PostgreSQL or Heroku Postgres
- Set `DATABASE_URL` environment variable
- Migrate database

### Application Shows 404
- Check build logs in Vercel
- Verify `run.py` is correct
- Check all imports are valid

---

## Production Checklist

Before going live:

- [ ] Code pushed to GitHub
- [ ] Deployed to Vercel successfully
- [ ] Environment variables set correctly
- [ ] Database initialized
- [ ] HTTPS enabled (Vercel auto-provides)
- [ ] Custom domain configured (optional)
- [ ] All routes tested
- [ ] Admin credentials changed from default
- [ ] Monitoring enabled
- [ ] Backups configured

---

## Your Application is Live! 🎉

Once deployed, your app will be available at:
- **Vercel URL:** `https://cryptominerpro.vercel.app`
- **Or your custom domain:** `https://yourdomain.com`

---

## Git Commands Reference

```bash
# Check status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push

# View commit history
git log --oneline

# Switch branch
git checkout -b new-feature
```

---

## Next Steps

1. ✅ Push to GitHub
2. ✅ Deploy to Vercel
3. 📧 Share your live URL with others
4. 🔧 Monitor performance
5. 🚀 Add new features and push updates

**Automatic Deployments:** Every time you push to GitHub, Vercel automatically rebuilds and deploys!

---

**Need Help?**
- GitHub Docs: https://docs.github.com
- Vercel Docs: https://vercel.com/docs
- Flask Docs: https://flask.palletsprojects.com
