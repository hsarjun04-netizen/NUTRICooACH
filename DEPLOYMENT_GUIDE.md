# 🚀 Deploy NutriCoach AI to Render - Step-by-Step Guide

## ✅ What's Already Done

Your project is now **fully configured** for Render deployment with:
- ✅ Updated `render.yaml` with proper build commands
- ✅ Database initialization in build process
- ✅ Recipe database seeding
- ✅ Health check endpoint (`/api/v1/health`)
- ✅ Production-ready WSGI server (Waitress)
- ✅ All environment variables configured
- ✅ Latest code pushed to GitHub

---

## 📋 Step-by-Step Deployment

### Step 1: Create Render Account

1. Go to **https://render.com**
2. Click **"Get Started for Free"**
3. Sign up using your **GitHub account** (recommended)
   - This gives Render access to your repositories

---

### Step 2: Create New Web Service

1. After logging in, click **"New +"** button
2. Select **"Web Service"**

---

### Step 3: Connect Repository

1. You'll see a list of your GitHub repositories
2. Find and select: **`hsarjun04-netizen/NUTRICooACH`**
3. If you don't see it:
   - Click **"Configure Account"** next to GitHub
   - Grant access to the NUTRICooACH repository
   - Refresh the page

---

### Step 4: Configure Web Service

Render will auto-detect your `render.yaml` file. Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `nutricoach-ai` (pre-filled) |
| **Region** | Oregon (pre-filled) |
| **Branch** | `main` |
| **Root Directory** | Leave blank |
| **Runtime** | Python (pre-filled) |
| **Plan** | **Free** |

**Build Command:** (pre-filled from render.yaml)
```bash
cd nutricoach/backend
pip install -r requirements.txt
python init_db.py
python seed_recipes.py
cd ../frontend
npm install
npm run build
```

**Start Command:** (pre-filled from render.yaml)
```bash
cd nutricoach/backend && python wsgi.py
```

---

### Step 5: Environment Variables

These are already configured in `render.yaml`:
- ✅ `PYTHON_VERSION` = 3.11.0
- ✅ `NODE_VERSION` = 20.11.0
- ✅ `FLASK_ENV` = production
- ✅ `JWT_SECRET_KEY` = (auto-generated)
- ✅ `PORT` = 5000

**No need to add manually!**

---

### Step 6: Deploy!

1. Click **"Create Web Service"** button
2. Wait for deployment (2-5 minutes)
3. Watch the build logs in real-time

---

### Step 7: Get Your Live URL

Once deployment completes:
1. You'll see a success message
2. Your live URL will be: **`https://nutricoach-ai-xxxx.onrender.com`**
   - The `xxxx` is a unique identifier assigned by Render
3. Copy this URL - it's accessible from **any device, anywhere!**

---

## 🎉 You're Live!

Your application is now running on:
```
https://nutricoach-ai-xxxx.onrender.com
```

**Test it:**
1. Open the URL in any browser
2. Register a new account
3. Complete profile setup
4. Start using all features!

---

## 🔧 Post-Deployment Checklist

### ✅ Verify Deployment
- [ ] Visit your Render URL
- [ ] Check health endpoint: `https://YOUR-URL.onrender.com/api/v1/health`
- [ ] Register a new user
- [ ] Complete profile setup
- [ ] Test meal plan generation
- [ ] Test food logging
- [ ] Test dashboard

### ✅ Check Render Dashboard
- [ ] Go to https://dashboard.render.com
- [ ] Click on your service
- [ ] Check logs for any errors
- [ ] Monitor resource usage

---

## 🔄 Auto-Deploy on Git Push

**Great news!** Render is configured for **automatic deployments**:

Every time you push to the `main` branch:
```bash
git push origin main
```

Render will automatically:
1. Detect the new commit
2. Rebuild your application
3. Deploy the updated version
4. Zero downtime!

---

## 📊 Free Tier Limits

Render's free tier includes:
- ✅ **750 hours/month** of runtime (enough for 24/7)
- ✅ **512 MB RAM**
- ✅ **0.1 CPU**
- ✅ **100 GB bandwidth/month**
- ✅ **Automatic HTTPS**
- ✅ **Custom domains** (optional)

**Note:** Free services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds to wake up
- This is normal for free tier

---

## 🐛 Troubleshooting

### Build Fails?

**Check logs in Render dashboard:**
1. Go to your service
2. Click "Logs" tab
3. Look for error messages

**Common issues:**
- Missing dependencies → Check `requirements.txt`
- Build command errors → Verify paths in `render.yaml`
- Node version mismatch → Update `NODE_VERSION`

### Application Crashes?

**Check application logs:**
```
Render Dashboard → Your Service → Logs
```

**Common fixes:**
- Database errors → Ensure `init_db.py` runs in build
- Import errors → Check Python paths
- Port conflicts → PORT env var is set to 5000

### Can't Access After Deployment?

1. **Wait 2-5 minutes** after deployment completes
2. **Check the URL** - should be `https://nutricoach-ai-xxxx.onrender.com`
3. **Test health endpoint**: `/api/v1/health`
4. **Check Render logs** for errors

---

## 🌐 Custom Domain (Optional)

Want a custom domain like `nutricoach.yourdomain.com`?

1. Go to Render Dashboard → Your Service
2. Click "Settings"
3. Scroll to "Custom Domains"
4. Click "Add Custom Domain"
5. Follow the DNS configuration instructions

---

## 📱 Share Your App!

Your app is now accessible worldwide! Share the URL:
- 📧 Email to friends
- 💬 Share on social media
- 💼 Add to your portfolio
- 📱 Access from any device

---

## 🔄 Future Updates

To update your live application:

1. **Make changes locally:**
   ```bash
   # Edit your code
   git add -A
   git commit -m "Your update message"
   git push origin main
   ```

2. **Render auto-deploys!**
   - Watch deployment progress in Render dashboard
   - Takes 2-5 minutes
   - Zero downtime

---

## 📞 Support Resources

- **Render Docs:** https://render.com/docs
- **Render Support:** https://render.com/support
- **Your Repository:** https://github.com/hsarjun04-netizen/NUTRICooACH

---

## 🎯 Next Steps After Deployment

1. ✅ Test all features thoroughly
2. ✅ Share the URL with others for feedback
3. ✅ Monitor usage in Render dashboard
4. ✅ Consider upgrading to paid plan if needed (starts at $7/month)
5. ✅ Add custom domain (optional)
6. ✅ Set up monitoring/alerts

---

## 💡 Pro Tips

1. **Monitor Logs:** Regularly check Render logs for errors
2. **Database Backup:** SQLite is file-based; consider PostgreSQL for production
3. **Environment Variables:** Never commit secrets; use Render's env var UI
4. **Performance:** Free tier has limitations; upgrade for production use
5. **SSL:** Render provides free HTTPS automatically

---

**Congratulations! Your NutriCoach AI is now live and accessible from anywhere! 🎉**

**Your Live URL:** `https://nutricoach-ai-xxxx.onrender.com`

Replace `xxxx` with the unique ID assigned by Render.
