# ⚡ Quick Render Deployment Guide

## 🚀 Fastest Way to Deploy

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for Render"
git push
```

### Step 2: Go to Render
1. Visit [render.com](https://render.com)
2. Sign up/Login with GitHub
3. Click **"New +"** → **"Web Service"**

### Step 3: Connect Repository
1. Select your GitHub repo
2. Click **"Connect"**

### Step 4: Configure (Copy These Settings)

**Name:** `resume-matcher` (or your choice)

**Build Command:**
```bash
pip install -r requirements.txt && python -m spacy download en_core_web_sm
```

**Start Command:**
```bash
python run_app.py
```

**Environment:** `Python 3`

### Step 5: Deploy
1. Click **"Create Web Service"**
2. Wait 3-5 minutes
3. Get your URL: `https://resume-matcher.onrender.com`

---

## ✅ That's It!

Your app will be live at: `https://your-service-name.onrender.com`

---

## 📝 Or Use render.yaml (Easier!)

I've created `render.yaml` for you. In Render:
1. Select **"Apply render.yaml"** instead of manual setup
2. It auto-configures everything!

---

## 🎯 Why Render?

- ✅ No size limits (spaCy works!)
- ✅ Persistent storage
- ✅ Perfect for Flask
- ✅ Free tier

---

**See `RENDER_DEPLOYMENT.md` for detailed guide!**

