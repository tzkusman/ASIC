# 🚀 Backend on PC + Vercel Frontend Setup

Your PC runs the backend database, Vercel runs the frontend UI!

## ARCHITECTURE:
```
User Browser
     ↓
Vercel Frontend (UI)
     ↓
Your PC Backend (Database + API)
```

## ⚡ STEP 1: Get Your PC's IP Address

**Windows:**
```powershell
ipconfig
```
Look for "IPv4 Address" (usually starts with 192.168.x.x)

**Example:** `192.168.100.99`

## 📋 STEP 2: Run Backend on Your PC

Keep this running 24/7:

```bash
cd g:\Openai\ASIC\CryptoMinerPro
python backend.py
```

You'll see:
```
 * Running on http://0.0.0.0:5000
 * Running on http://192.168.100.99:5000
```

## 🌐 STEP 3: Update Vercel Environment Variables

1. Go to Vercel project settings
2. Add environment variable:
   - Key: `BACKEND_URL`
   - Value: `http://192.168.100.99:5000` (your PC IP)
3. Redeploy Vercel

## ✅ STEP 4: Everything Works!

- **Vercel URL:** Shows the UI
- **Backend:** Runs on your PC
- **Database:** SQLite on your PC
- **Data:** Persists on your PC

## 📊 Testing:

**Backend API:**
```
http://192.168.100.99:5000/api/miners
```

**Vercel Frontend:**
```
https://crypto-miner-31i7kcpia-tzkusmans-projects.vercel.app/
```

## ⚠️ IMPORTANT:
- Your PC must stay ON for the system to work
- Network must be stable
- Both devices on same network (or use ngrok for external access)

## 🔒 To Make Public (Optional):

If you want to access from anywhere (not just local network):

1. Install ngrok: https://ngrok.com/
2. Run: `ngrok http 5000`
3. Use ngrok URL in Vercel environment variables

That's it! Your app is live! 🎉
