# ⚡ Quick Free Deployment - 5 Minutes!

## 🎯 Best Option: Render (Recommended)

**Why?** Easiest, works perfectly with Flask, completely free!

---

## 🚀 5-Minute Deployment Steps

### Step 1: Push to GitHub (if not already)
```bash
git add .
git commit -m "Ready for deployment"
git push
```

### Step 2: Go to Render
1. Visit [render.com](https://render.com)
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (easiest)

### Step 3: Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Click **"Connect account"** (if GitHub not connected)
3. Select your repository
4. Click **"Connect"**

### Step 4: Configure (OR use render.yaml)

**EASIEST WAY - Use render.yaml:**
- Select **"Apply render.yaml"** 
- Render auto-configures everything!
- Click **"Create Web Service"**
- **Done!** ✅

**OR Manual Setup:**
- **Name**: `resume-matcher`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt && python -m spacy download en_core_web_sm
  ```
- **Start Command**: 
  ```bash
  python run_app.py
  ```
- **Environment**: `Python 3`
- Click **"Create Web Service"**

### Step 5: Wait & Get URL
- Wait 3-5 minutes for build
- Your URL: `https://resume-matcher.onrender.com`
- **Copy and share!** 🎉

---

## ✅ That's It!

Your app is now live and **completely free** at:
```
https://your-service-name.onrender.com
```

---

## ⚠️ Free Tier Note

- App sleeps after 15 minutes of inactivity
- First request takes ~30 seconds (waking up)
- Subsequent requests are fast
- **Still completely free!**

---

## 🎯 Alternative: Railway

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. New Project → Deploy from GitHub
4. Select your repo
5. Auto-deploys!

---

## 📝 Your Deployment Checklist

- [ ] Code on GitHub
- [ ] Render account created
- [ ] Web service created
- [ ] App deployed
- [ ] URL copied
- [ ] Tested and working!

---

**See `FREE_HOSTING_GUIDE.md` for detailed guide and alternatives!**

**Your app can be live in 5 minutes!** 🚀

