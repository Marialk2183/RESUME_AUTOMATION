# 🚀 Deploy to Render - Step-by-Step Guide

Render is **perfect** for Flask apps! No size limits, persistent storage, and easy deployment.

---

## ✅ Why Render is Better for This App

- ✅ **No size limits** (spaCy models work fine!)
- ✅ **Persistent file storage** (uploads stay)
- ✅ **Free tier available**
- ✅ **Perfect for Flask**
- ✅ **Easy GitHub integration**

---

## 📋 Prerequisites

1. **GitHub Account** (your code should be on GitHub)
2. **Render Account** (free to sign up)
3. **Your code pushed to GitHub**

---

## 🎯 Step-by-Step Deployment

### Step 1: Push Code to GitHub

Make sure your code is on GitHub:

```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

---

### Step 2: Sign Up / Login to Render

1. Go to [render.com](https://render.com)
2. Click **"Get Started for Free"** or **"Sign In"**
3. Sign up with GitHub (easiest way)

---

### Step 3: Create New Web Service

1. In Render dashboard, click **"New +"** button
2. Select **"Web Service"**
3. Click **"Connect account"** if not connected to GitHub
4. Select your repository: `RESUME_AUTOMATION` (or your repo name)
5. Click **"Connect"**

---

### Step 4: Configure Your Service

Fill in the settings:

#### Basic Settings:
- **Name**: `resume-matcher` (or your choice)
- **Region**: Choose closest to you (e.g., `Oregon (US West)`)
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave empty (or `.` if needed)

#### Build & Deploy:
- **Runtime**: `Python 3`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt && python -m spacy download en_core_web_sm
  ```
- **Start Command**: 
  ```bash
  python run_app.py
  ```

#### Environment:
- **Environment**: `Python 3`
- **Python Version**: `3.12` (or latest)

#### Advanced (Optional):
- **Auto-Deploy**: `Yes` (deploys on every push)

---

### Step 5: Add Environment Variables (Optional)

If needed, click **"Advanced"** → **"Add Environment Variable"**:

- `PYTHONUNBUFFERED`: `1`
- `FLASK_ENV`: `production`

(Usually not needed, but good to have)

---

### Step 6: Create Service

1. Scroll down
2. Click **"Create Web Service"**
3. Render will start building!

---

### Step 7: Wait for Deployment

- Build takes **3-5 minutes** (first time)
- You'll see build logs in real-time
- Watch for: "Your service is live at..."

---

### Step 8: Get Your URL

Once deployed:
- Your URL will be: `https://resume-matcher.onrender.com`
- Or: `https://your-service-name.onrender.com`
- **Copy this URL!**

---

## 🔧 Configuration Details

### Build Command:
```bash
pip install -r requirements.txt && python -m spacy download en_core_web_sm
```

### Start Command:
```bash
python run_app.py
```

### Alternative Start Command (if run_app.py doesn't work):
```bash
gunicorn app:app
```

If using gunicorn, add to `requirements.txt`:
```
gunicorn>=21.2.0
```

---

## 📝 Create render.yaml (Optional but Recommended)

Create a `render.yaml` file in your project root for easier setup:

```yaml
services:
  - type: web
    name: resume-matcher
    env: python
    buildCommand: pip install -r requirements.txt && python -m spacy download en_core_web_sm
    startCommand: python run_app.py
    envVars:
      - key: PYTHONUNBUFFERED
        value: 1
```

Then in Render dashboard, select **"Apply render.yaml"** instead of manual setup.

---

## 🛠️ Troubleshooting

### Issue: Build Fails

**Check:**
1. Build logs in Render dashboard
2. Make sure `requirements.txt` is correct
3. Check Python version compatibility

**Fix:**
- Update build command if needed
- Check for missing dependencies

### Issue: App Crashes on Start

**Check:**
1. Start command is correct
2. Port binding (Render uses port from `PORT` env var)

**Fix:**
Update `run_app.py` to use Render's port:

```python
import os
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### Issue: spaCy Model Not Found

**Fix:**
Make sure build command includes:
```bash
python -m spacy download en_core_web_sm
```

### Issue: File Uploads Not Working

**Fix:**
- Render has persistent storage (unlike Vercel)
- Files will stay in `uploads/` folder
- No changes needed!

---

## 🔄 Update run_app.py for Render

Update `run_app.py` to work with Render's port:

```python
import os

# ... existing code ...

# At the end, change:
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port, debug=False)
```

---

## 📊 Render vs Vercel

| Feature | Render | Vercel |
|---------|--------|--------|
| Size Limit | None ✅ | 250MB ❌ |
| File Storage | Persistent ✅ | Ephemeral ❌ |
| Flask Support | Excellent ✅ | Limited ⚠️ |
| Free Tier | Yes ✅ | Yes ✅ |
| spaCy Models | Works ✅ | Too Large ❌ |

**Render is better for this app!** 🎯

---

## 🎉 After Deployment

1. **Test your app**: Visit the URL
2. **Share it**: Add to portfolio/resume
3. **Monitor**: Check logs in Render dashboard
4. **Update**: Auto-deploys on every git push!

---

## 🔗 Useful Links

- [Render Dashboard](https://dashboard.render.com)
- [Render Docs](https://render.com/docs)
- [Python on Render](https://render.com/docs/python)

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Web service created
- [ ] Build command set
- [ ] Start command set
- [ ] Service deployed
- [ ] URL copied
- [ ] App tested

---

**Your app is now live on Render!** 🚀

