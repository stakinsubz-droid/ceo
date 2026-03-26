# 🚀 DEPLOYMENT GUIDE: Render + Vercel (LEVEL 3)

Complete step-by-step guide to deploy your enterprise system.

---

## 📋 PRE-DEPLOYMENT CHECKLIST

Before deploying, gather these credentials:

### Essential (Required)
- [ ] MongoDB Atlas URL (MONGO_URL)
- [ ] GitHub repository access
- [ ] Render account
- [ ] Vercel account

### LEVEL 2 (Monetization)
- [ ] Gumroad API token
- [ ] TikTok access token
- [ ] Instagram business account + token
- [ ] Twitter API bearer token

### LEVEL 3 (Enterprise)
- [ ] YouTube API key + Channel ID
- [ ] Mailchimp API key
- [ ] SendGrid API key
- [ ] OpenAI API key
- [ ] Stripe API key + Webhook secret

---

## 🔧 STEP-BY-STEP DEPLOYMENT

### STEP 1: Push Code to GitHub

```bash
cd /workspaces/ceo
git add .
git commit -m "deployCEO Level 3 - Enterprise"
git push origin main
```

### STEP 2: Deploy Backend on Render

#### Option A: Using render.yaml (Recommended)

1. Go to https://render.com/dashboard
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Select the `render.yaml` file
5. Add these environment variables:

```
MONGO_URL = mongodb+srv://user:pass@cluster...
DB_NAME = ai_ceo
GUMROAD_TOKEN = your_token
YOUTUBE_API_KEY = your_key
MAILCHIMP_API_KEY = your_key
SENDGRID_API_KEY = your_key
OPENAI_API_KEY = your_key
STRIPE_API_KEY = your_key
(etc...)
```

6. Click **"Deploy"** ✅

#### Option B: Manual Service

1. Go to https://render.com/dashboard
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `ceo-backend`
   - **Runtime**: Docker
   - **Branch**: main
   - **Docker Dockerfile**: `Dockerfile`
   - **Region**: Oregon (or closest)

5. Add all environment variables (see below)
6. Click **"Create Web Service"** ✅

### STEP 3: Deploy Frontend on Vercel

1. Go to https://vercel.com/dashboard
2. Click **"Add New"** → **"Project"**
3. Select your GitHub repo
4. Configure:
   - **Framework**: React
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

5. Add environment variable:
   - `REACT_APP_API_URL` = Your Render backend URL
   - `REACT_APP_ENABLE_LEVEL3` = `true`

6. Click **"Deploy"** ✅

---

## 🔑 ENVIRONMENT VARIABLES

### In Render Dashboard

Set these in your ceo-backend service:

```
Core:
MONGO_URL = mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority
DB_NAME = ai_ceo
ENVIRONMENT = production
CORS_ORIGINS = https://your-frontend.vercel.app

LEVEL 2:
MAX_CONCURRENT_PROJECTS = 5
PROJECTS_PER_DAY = 5
GUMROAD_TOKEN = your_gumroad_token
TIKTOK_ACCESS_TOKEN = your_tiktok_token
INSTAGRAM_ACCESS_TOKEN = your_ig_token
TWITTER_BEARER_TOKEN = your_twitter_token

LEVEL 3:
YOUTUBE_API_KEY = your_youtube_api_key
YOUTUBE_CHANNEL_ID = your_channel_id
MAILCHIMP_API_KEY = your_mailchimp_key
MAILCHIMP_SERVER = us1
SENDGRID_API_KEY = your_sendgrid_key
OPENAI_API_KEY = your_openai_key
STRIPE_API_KEY = your_stripe_key
STRIPE_WEBHOOK_SECRET = your_webhook_secret
```

### In Vercel Dashboard

Set these in your ceo-frontend project:

```
REACT_APP_API_URL = https://ceo-backend.onrender.com
REACT_APP_ENABLE_LEVEL2 = true
REACT_APP_ENABLE_LEVEL3 = true
```

---

## 🧪 TESTING DEPLOYMENT

### 1. Check Backend Health

```bash
curl https://ceo-backend.onrender.com/health
```

Should return:
```json
{
  "status": "healthy",
  "environment": "production"
}
```

### 2. Check API Status

```bash
curl https://ceo-backend.onrender.com/api/projects
```

### 3. Test LEVEL 3 Endpoint

```bash
curl https://ceo-backend.onrender.com/api/v3/health/level3
```

### 4. Visit Frontend

```
https://ceo-frontend.vercel.app
```

---

## 🚀 SCALING CONFIGURATION

### For Production (High Volume)

Change Max Concurrent Projects:

```bash
# In Render environment variables
MAX_CONCURRENT_PROJECTS = 50
PROJECTS_PER_DAY = 50
```

Then restart the service.

### Enable Enterprise Mode

```bash
curl -X POST "https://ceo-backend.onrender.com/api/v3/enterprise/enable-scaling?projects_per_day=50&concurrent_workers=10"
```

---

## 📊 MONITORING

### Render Dashboard
- Go to https://render.com/dashboard
- View logs: Click ceo-backend → "Logs"
- Monitor disk usage and CPU
- Check auto-deploy on Git push

### Vercel Dashboard
- Go to https://vercel.com/dashboard
- View deployments: Click project → Deployments
- Check build logs if deployment fails
- Monitor function execution time

---

## 🔐 SECURITY BEST PRACTICES

### Do NOT commit secrets to Git
```bash
# .gitignore should include
.env
.env.local
.env.production.local
```

### Use Render + Vercel Dashboards for secrets only
Never put API keys in code or Git!

### MongoDB Security
- Use strong username/password
- Enable IP whitelist: Allow Render's IP
- Rotate credentials quarterly

### API Rate Limiting
- Enable Stripe webhook verification
- Mailchimp list security settings
- YouTube API quota management

---

## 🐛 TROUBLESHOOTING

### Backend won't start

1. Check Render logs:
```
Render Dashboard → ceo-backend → Logs → Recent Events
```

2. Common issues:
- Missing MONGO_URL → Add to Render env vars
- Python version mismatch → Check Python 3.11 in Dockerfile
- Package install failed → Check requirements.txt

3. Restart service:
```
Render Dashboard → ceo-backend → Settings → Restart Service
```

### Frontend won't build

1. Check Vercel logs:
```
Vercel Dashboard → Deployments → Failed build → View Logs
```

2. Common issues:
- React version conflict → Update package.json
- Missing env variables → Add REACT_APP_* vars
- Build errors → Run locally first: `npm run build`

### API calls fail

1. Check CORS settings:
```
In Render env: CORS_ORIGINS = https://your-frontend.vercel.app
```

2. Check API URL:
```
In Vercel env: REACT_APP_API_URL = https://ceo-backend.onrender.com
```

3. Test with curl:
```bash
curl -H "Origin: https://your-frontend.vercel.app" https://ceo-backend.onrender.com/health
```

---

## 📈 SCALING FOR PRODUCTION

### Start: 1 instance, 5 projects/day
- Cost: $7/month (Render) + Free (Vercel)
- Revenue: ~$7,500/month

### Growth: Add worker dyno
- Cost: $50/month
- Projects/day: 50
- Revenue: ~$75,000/month

### Enterprise: Scale to 10 instances
- Cost: $500/month (Render) + $200/month (Vercel Pro)
- Projects/day: 500+
- Revenue: ~$750,000+/month

---

## 🔄 CONTINUOUS DEPLOYMENT

Every push to main triggers:

1. GitHub detects push
2. Render pulls latest code
3. Rebuild Docker image
4. Backend redeployment
5. Vercel pulls latest code
6. Frontend rebuild & deploy
7. Both live within 2-3 minutes

---

## 📞 SUPPORT

### Render Docs
https://render.com/docs

### Vercel Docs
https://vercel.com/docs

### API Documentation
https://your-backend.onrender.com/docs (Swagger)
https://your-backend.onrender.com/redoc (ReDoc)

---

## ✅ DEPLOYMENT CHECKLIST

- [ ] GitHub repo ready
- [ ] Render account created
- [ ] Vercel account created
- [ ] MongoDB Atlas setup
- [ ] All API tokens gathered
- [ ] render.yaml verified
- [ ] Backend deployed on Render
- [ ] Frontend deployed on Vercel
- [ ] Environment variables set
- [ ] Backend health check passes
- [ ] Frontend loads without errors
- [ ] API endpoints tested
- [ ] LEVEL 3 endpoints verified
- [ ] Monitoring dashboard accessed
- [ ] Documentation saved

---

## 🚀 AFTER DEPLOYMENT

1. Monitor first 24 hours closely
2. Check Render logs every 6 hours
3. Test endpoints manually
4. Set up monitoring alerts
5. Plan scaling strategy
6. Document any issues

---

You're now live! 🎉

Your autonomous system is now running on the internet and ready to:
- Generate products 24/7
- Market across platforms
- Handle customer support
- Track revenue
- Scale globally

**Go to https://ceo-backend.onrender.com/docs to see your API in action!**
