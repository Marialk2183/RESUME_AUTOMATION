# ⚡ Quick Deploy to Vercel

## Fastest Way (GitHub Integration)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push
   ```

2. **Deploy via Vercel Dashboard**
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your GitHub repository
   - Click "Deploy" (settings are auto-detected)

3. **Done!** 🎉
   - Your app will be live at `https://your-project.vercel.app`

---

## Via CLI (Alternative)

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel

# Follow prompts, then:
vercel --prod
```

---

## ⚠️ Important Notes

1. **File Uploads**: Limited to 4.5MB (Vercel serverless limit)
2. **Temporary Storage**: Files stored in `/tmp` (deleted after function ends)
3. **First Request**: May be slow due to model loading (cold start)
4. **spaCy Model**: Will be downloaded during build

---

## 🔧 If Deployment Fails

1. **Check logs**: `vercel logs` or Vercel dashboard
2. **Test locally**: `vercel dev`
3. **Verify files**: Make sure `api/index.py` and `vercel.json` exist
4. **Check requirements.txt**: All dependencies listed?

---

## 📚 Full Guide

See `VERCEL_DEPLOYMENT.md` for detailed instructions and troubleshooting.

---

## 🚀 Alternative Platforms (Better for Flask)

If Vercel has limitations, consider:
- **Railway**: `railway up` (best for Flask)
- **Render**: Free tier, persistent storage
- **Fly.io**: Global deployment

See `VERCEL_DEPLOYMENT.md` for details.

