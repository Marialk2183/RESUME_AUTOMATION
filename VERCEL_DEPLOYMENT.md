# 🚀 Deploying MIND-BRIDGE to Vercel

This guide will help you deploy your Flask application to Vercel.

## ⚠️ Important Considerations

**Vercel Limitations:**
- **File Uploads**: Vercel serverless functions have a 4.5MB request limit
- **Temporary Storage**: Uploaded files are stored in `/tmp` and are ephemeral (deleted after function execution)
- **Large Dependencies**: spaCy models are large (~50MB) - may need optimization
- **Cold Starts**: First request may be slow due to model loading

**Recommendations:**
- For production with file uploads, consider **Railway**, **Render**, or **Fly.io** (better for Flask apps)
- For demo/portfolio, Vercel works but with limitations

---

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install globally
   ```bash
   npm install -g vercel
   ```
3. **Git Repository**: Your code should be in a Git repo (GitHub, GitLab, or Bitbucket)

---

## 🔧 Step-by-Step Deployment

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Login to Vercel

```bash
vercel login
```

### Step 3: Update Requirements for Vercel

The spaCy model needs to be downloaded. Create a `vercel.json` build command or use a different approach:

**Option A: Pre-download model (Recommended)**

Create a script to download the model during build:

```bash
# Add to package.json or use build command
python -m spacy download en_core_web_sm
```

**Option B: Use smaller model or lazy loading**

The app already uses lazy loading, which helps.

### Step 4: Configure for Vercel

The following files are already created:
- ✅ `vercel.json` - Vercel configuration
- ✅ `api/index.py` - Serverless function entry point

### Step 5: Deploy

**Option A: Deploy via CLI**

```bash
# From project root
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? (your account)
# - Link to existing project? No (first time)
# - Project name? mind-bridge (or your choice)
# - Directory? ./
# - Override settings? No
```

**Option B: Deploy via GitHub Integration**

1. Push your code to GitHub
2. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
3. Click "Add New Project"
4. Import your GitHub repository
5. Vercel will auto-detect settings
6. Click "Deploy"

### Step 6: Environment Variables (if needed)

If you need environment variables:

```bash
vercel env add VARIABLE_NAME
```

Or set them in Vercel dashboard: Project → Settings → Environment Variables

---

## 📁 Project Structure for Vercel

```
MIND-BRIDGE/
├── api/
│   └── index.py          # Vercel serverless entry point
├── static/               # Static files (CSS, JS)
├── templates/            # HTML templates
├── app.py                # Flask application
├── resume_matcher.py     # Core matching logic
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
└── ...
```

---

## 🔍 Troubleshooting

### Issue: spaCy model not found

**Solution:**
```bash
# Add to vercel.json build command or use a build script
# Create build.sh:
#!/bin/bash
python -m spacy download en_core_web_sm
```

Or update `vercel.json`:
```json
{
  "buildCommand": "python -m spacy download en_core_web_sm"
}
```

### Issue: File uploads not working

**Solution:**
- Files are stored in `/tmp` (already configured)
- Files are deleted after function execution (ephemeral)
- Consider using external storage (S3, Cloudinary) for production

### Issue: Function timeout

**Solution:**
- Increase timeout in `vercel.json` (already set to 60s)
- Optimize model loading (use lazy loading - already implemented)
- Consider caching models

### Issue: Large deployment size

**Solution:**
- spaCy models are large (~50MB)
- Vercel has a 50MB limit for serverless functions
- Consider:
  - Using smaller spaCy model
  - Using alternative NLP library
  - Splitting into multiple functions

---

## 🎯 Alternative Deployment Options

### 1. **Railway** (Recommended for Flask)
- ✅ Better for Flask apps
- ✅ Persistent file storage
- ✅ No file size limits
- ✅ Easy deployment

**Deploy to Railway:**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize
railway init

# Deploy
railway up
```

### 2. **Render**
- ✅ Free tier available
- ✅ Persistent storage
- ✅ Good for Flask apps

**Deploy to Render:**
1. Connect GitHub repo
2. Select "Web Service"
3. Build command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
4. Start command: `python run_app.py`

### 3. **Fly.io**
- ✅ Great for Flask
- ✅ Global deployment
- ✅ Persistent volumes

### 4. **Heroku**
- ✅ Traditional Flask hosting
- ⚠️ Paid plans required (no free tier)

---

## 📝 Vercel Configuration Details

### vercel.json Explained

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"  // Uses Vercel's Python runtime
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"  // Serve static files directly
    },
    {
      "src": "/(.*)",
      "dest": "/api/index.py"  // All other routes go to Flask
    }
  ],
  "functions": {
    "api/index.py": {
      "maxDuration": 60,  // 60 second timeout
      "memory": 3008      // 3GB memory (max for Pro)
    }
  }
}
```

---

## ✅ Post-Deployment Checklist

- [ ] Test homepage loads
- [ ] Test file upload (remember: 4.5MB limit)
- [ ] Test resume matching
- [ ] Check console for errors
- [ ] Verify spaCy model loads correctly
- [ ] Test all API endpoints

---

## 🔗 Useful Links

- [Vercel Python Documentation](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)
- [Vercel CLI Documentation](https://vercel.com/docs/cli)
- [Flask on Vercel Guide](https://vercel.com/guides/deploying-flask-with-vercel)

---

## 💡 Tips

1. **Monitor Function Logs**: Use `vercel logs` or Vercel dashboard
2. **Test Locally**: Use `vercel dev` to test locally before deploying
3. **Optimize Cold Starts**: Consider using Vercel Pro for better performance
4. **File Storage**: For production, integrate with S3 or similar for file persistence

---

## 🎉 Success!

Once deployed, you'll get a URL like:
`https://mind-bridge.vercel.app`

Share it and show off your AI-powered resume matcher! 🚀

---

**Need Help?** Check Vercel's documentation or consider alternative platforms better suited for Flask applications with file uploads.

