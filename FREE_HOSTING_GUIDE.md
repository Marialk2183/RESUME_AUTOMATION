# 🆓 Free Hosting Guide - Deploy Your Resume Matcher for Free

## 🎯 Best Free Options for Flask Apps

Here are the best **completely free** options to host your application:

---

## 🥇 Option 1: Render (RECOMMENDED - Best for Flask)

### ✅ Why Render is Best:
- ✅ **Completely free tier** (with limitations)
- ✅ **No size limits** (spaCy models work!)
- ✅ **Persistent storage** (files stay)
- ✅ **Perfect for Flask**
- ✅ **Easy GitHub integration**
- ✅ **Free SSL certificate**

### ⚠️ Free Tier Limitations:
- App sleeps after 15 minutes of inactivity
- Takes ~30 seconds to wake up
- 750 hours/month free (enough for most use cases)
- 512MB RAM

### 🚀 How to Deploy (5 minutes):

1. **Push to GitHub** (if not already):
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push
   ```

2. **Go to Render**:
   - Visit [render.com](https://render.com)
   - Sign up with GitHub (free)

3. **Create Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Click "Connect"

4. **Configure**:
   - **Name**: `resume-matcher` (or your choice)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python -m spacy download en_core_web_sm
     ```
   - **Start Command**: 
     ```bash
     python run_app.py
     ```
   - **Environment**: `Python 3`

5. **Deploy**:
   - Click "Create Web Service"
   - Wait 3-5 minutes
   - Your URL: `https://resume-matcher.onrender.com`

### 📝 Your URL Format:
```
https://your-service-name.onrender.com
```

**That's it! Your app is live and free!** 🎉

---

## 🥈 Option 2: Railway (Great Alternative)

### ✅ Why Railway:
- ✅ **Free tier** with $5 credit/month
- ✅ **No sleep** (always on)
- ✅ **Easy deployment**
- ✅ **Great for Flask**

### 🚀 How to Deploy:

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login**:
   ```bash
   railway login
   ```

3. **Deploy**:
   ```bash
   railway init
   railway up
   ```

4. **Get URL**: Railway provides URL automatically

**Or use Railway Dashboard:**
- Go to [railway.app](https://railway.app)
- Sign up with GitHub
- New Project → Deploy from GitHub
- Select your repo
- Auto-detects Flask and deploys!

---

## 🥉 Option 3: Fly.io (Global Deployment)

### ✅ Why Fly.io:
- ✅ **Free tier** available
- ✅ **Global deployment** (fast worldwide)
- ✅ **No sleep** (always on)
- ✅ **Good for Flask**

### 🚀 How to Deploy:

1. **Install Fly CLI**:
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **Login**:
   ```bash
   fly auth login
   ```

3. **Create App**:
   ```bash
   fly launch
   ```

4. **Deploy**:
   ```bash
   fly deploy
   ```

---

## 🆓 Option 4: PythonAnywhere (Simple but Limited)

### ✅ Why PythonAnywhere:
- ✅ **Completely free** (with limitations)
- ✅ **Simple setup**
- ✅ **Good for learning**

### ⚠️ Limitations:
- Limited to 1 web app
- 512MB storage
- Can't install all packages
- May not work with spaCy models

### 🚀 How to Deploy:

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your files
3. Configure web app
4. Deploy

**Note**: May have issues with large dependencies like spaCy.

---

## 📊 Comparison Table

| Platform | Free Tier | Sleep? | Size Limit | Best For |
|----------|-----------|--------|------------|----------|
| **Render** | ✅ Yes | ⚠️ 15 min | ❌ None | **Flask apps** |
| **Railway** | ✅ $5 credit | ❌ No | ❌ None | Flask apps |
| **Fly.io** | ✅ Yes | ❌ No | ❌ None | Global deployment |
| **PythonAnywhere** | ✅ Yes | ❌ No | ⚠️ Limited | Simple apps |
| **Vercel** | ✅ Yes | ❌ No | ⚠️ 250MB | Serverless |

---

## 🎯 My Recommendation: **Render**

**Why?**
- ✅ Easiest to set up
- ✅ Works perfectly with Flask
- ✅ No size limits (spaCy works!)
- ✅ Persistent storage
- ✅ Free SSL
- ✅ GitHub integration

**The only downside**: App sleeps after 15 min inactivity (takes ~30 sec to wake up)

---

## 🚀 Quick Start with Render (Copy-Paste Ready)

### Step 1: Make sure you have `render.yaml` (I created this for you!)

Your `render.yaml` file is already configured. Render will use it automatically!

### Step 2: Deploy

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Select your repository
5. **OR** if you have `render.yaml`, select "Apply render.yaml"
6. Click "Create Web Service"
7. Wait 3-5 minutes
8. **Done!** Your app is live at `https://your-app.onrender.com`

---

## 🔧 Configuration Files Already Created

I've already created these for you:

✅ **`render.yaml`** - Auto-configuration for Render  
✅ **`run_app.py`** - Updated for production (uses PORT env var)  
✅ **`requirements.txt`** - All dependencies listed  

**You're ready to deploy!** Just push to GitHub and connect to Render.

---

## 📝 Step-by-Step: Render Deployment

### 1. Push Code to GitHub

```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 2. Go to Render Dashboard

- Visit [dashboard.render.com](https://dashboard.render.com)
- Sign up/Login with GitHub

### 3. Create New Web Service

- Click **"New +"** button (top right)
- Select **"Web Service"**
- Click **"Connect account"** if GitHub not connected
- Select your repository: `RESUME_AUTOMATION` (or your repo name)
- Click **"Connect"**

### 4. Configure (or use render.yaml)

**Option A: Use render.yaml (Easiest)**
- Select **"Apply render.yaml"**
- Render auto-configures everything!

**Option B: Manual Configuration**
- **Name**: `resume-matcher`
- **Region**: Choose closest (e.g., Oregon)
- **Branch**: `main`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt && python -m spacy download en_core_web_sm
  ```
- **Start Command**: 
  ```bash
  python run_app.py
  ```
- **Environment**: `Python 3`

### 5. Deploy

- Click **"Create Web Service"**
- Watch the build logs
- Wait 3-5 minutes
- **Success!** Your app is live!

### 6. Get Your URL

- Your URL will be: `https://resume-matcher.onrender.com`
- Or: `https://your-service-name.onrender.com`
- **Copy this URL!**

---

## 🎨 Custom Domain (Optional - Free)

You can add a custom domain for free:

1. In Render dashboard → Your service → Settings
2. Scroll to "Custom Domains"
3. Add your domain
4. Update DNS records (Render provides instructions)
5. Free SSL automatically!

---

## ⚡ Wake Up Time (Free Tier)

**Important**: On free tier, app sleeps after 15 minutes of inactivity.

- **First request**: Takes ~30 seconds (waking up)
- **Subsequent requests**: Fast (app is awake)

**Solution**: 
- Upgrade to paid ($7/month) for always-on
- Or accept the 30-second wake-up time (it's free!)

---

## 🔍 Troubleshooting

### Issue: Build Fails

**Check**:
- Build logs in Render dashboard
- Make sure `requirements.txt` is correct
- Check Python version compatibility

**Fix**:
- Update build command if needed
- Check for missing dependencies

### Issue: App Crashes

**Check**:
- Start command is correct: `python run_app.py`
- Port binding (Render uses PORT env var - already handled in `run_app.py`)

### Issue: spaCy Model Not Found

**Fix**: Make sure build command includes:
```bash
python -m spacy download en_core_web_sm
```

### Issue: File Uploads Not Working

**Fix**: 
- Render has persistent storage (unlike Vercel)
- Files stay in `uploads/` folder
- No changes needed!

---

## 📊 Free Tier Comparison

### Render Free Tier:
- ✅ 750 hours/month (enough for always-on)
- ✅ 512MB RAM
- ✅ Sleeps after 15 min inactivity
- ✅ Free SSL
- ✅ Unlimited bandwidth

### Railway Free Tier:
- ✅ $5 credit/month
- ✅ Always on (no sleep)
- ✅ 512MB RAM
- ✅ Free SSL

### Fly.io Free Tier:
- ✅ 3 shared VMs
- ✅ 3GB storage
- ✅ Always on
- ✅ Global deployment

---

## 🎯 Final Recommendation

**Use Render** - It's the best free option for your Flask app:

1. ✅ **Easiest setup** - Just connect GitHub
2. ✅ **No size limits** - spaCy models work
3. ✅ **Persistent storage** - Files stay
4. ✅ **Free SSL** - Secure by default
5. ✅ **Good documentation** - Easy to troubleshoot

**The only downside**: 30-second wake-up time on free tier (acceptable for free!)

---

## 🚀 Quick Deploy Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Web service created
- [ ] Build command set (or use render.yaml)
- [ ] Start command set: `python run_app.py`
- [ ] Service deployed
- [ ] URL copied: `https://your-app.onrender.com`
- [ ] App tested and working!

---

## 📝 Your Deployment URL

After deployment, your app will be live at:

```
https://your-service-name.onrender.com
```

**Share this URL in your LinkedIn post, portfolio, and resume!** 🎉

---

## 🆘 Need Help?

- See `RENDER_DEPLOYMENT.md` for detailed Render guide
- Check Render docs: [render.com/docs](https://render.com/docs)
- Check build logs in Render dashboard

---

**Your app can be live and free in 5 minutes!** 🚀

**Recommended: Use Render - it's perfect for your Flask app!**

