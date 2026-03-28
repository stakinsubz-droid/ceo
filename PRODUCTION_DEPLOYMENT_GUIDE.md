# 🚀 PRODUCTION DEPLOYMENT GUIDE

**AI CEO System - Launch to Render & Vercel**

---

## 📋 Pre-Deployment Checklist

### ✅ Code & Dependencies
- [x] All code committed to GitHub (main branch)
- [x] No API keys in code
- [x] All imports working
- [x] requirements.txt up to date
- [x] package.json up to date
- [x] .gitignore properly configured

### ✅ Security
- [x] API key authentication implemented
- [x] Rate limiting active
- [x] HTTPS configured
- [x] Environment variables secured
- [x] SSL certificates ready

### ✅ Documentation
- [x] README.md complete
- [x] API documentation complete
- [x] Deployment guide created
- [x] Privacy policy created
- [x] Terms of service created

---

## 🚢 Step 1: Deploy Backend to Render

### 1.1 Prepare Render Account

```bash
# Prerequisites:
# - Render account created (render.com)
# - GitHub account connected to Render
# - MongoDB Atlas account created
```

### 1.2 Create Render Web Service

**Settings:**
- **Name:** ceo-ai-backend
- **Repository:** stackinsubzinc-dev/ceo
- **Branch:** main
- **Root Directory:** backend
- **Runtime:** Python 3.11
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn -k uvicorn.workers.UvicornWorker server:app --bind 0.0.0.0:8000 --workers 3 --timeout 120`
- **Plan:** Standard (or Starter for testing)

### 1.3 Configure Environment Variables in Render

Go to **Dashboard → Environment → Environment Groups:**

```env
MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net/ceo_db?retryWrites=true&w=majority
DB_NAME=ceo_db
API_KEY=your-secure-api-key-here
ENVIRONMENT=production
CORS_ORIGINS=https://ceo-frontend.vercel.app,https://yourdomain.com
EMERGENT_LLM_KEY=your-emergent-llm-key
OPENAI_API_KEY=sk-xxx
GUMROAD_API_KEY=xxx
```

### 1.4 Deploy

1. Click **Create Web Service**
2. Render automatically deploys from GitHub (main branch)
3. Watch deployment logs
4. When complete, you'll get a live URL like: `https://ceo-ai-backend.onrender.com`

### 1.5 Test Backend

```bash
# Test health endpoint
curl -X GET https://ceo-ai-backend.onrender.com/api/health

# Expected response:
# {
#   "status": "healthy",
#   "database": "connected"
# }
```

---

## 🎨 Step 2: Deploy Frontend to Vercel

### 2.1 Prepare Vercel Account

```bash
# Prerequisites:
# - Vercel account created (vercel.com)
# - GitHub repository connected
```

### 2.2 Create Vercel Project

1. Go to **vercel.com/dashboard**
2. Click **New Project**
3. Select **stackinsubzinc-dev/ceo** repository
4. Configure:
   - **Framework Preset:** Create React App
   - **Root Directory:** frontend
   - **Build Command:** `npm run build`
   - **Start Command:** `npm start`

### 2.3 Set Environment Variables in Vercel

Go to **Settings → Environment Variables:**

```env
REACT_APP_API_URL=https://ceo-ai-backend.onrender.com
REACT_APP_API_KEY=your-api-key
NODE_ENV=production
```

### 2.4 Configure Vercel Settings

**Settings → Git:**
- Auto-deploy on push to main: ✓ Enabled

**Settings → Build & Development:**
- Ignore Build Step: Leave empty
- Build Cache: Enabled

### 2.5 Deploy

1. Click **Deploy**
2. Watch build logs
3. When complete, you'll get a live URL like: `https://ceo-frontend.vercel.app`

### 2.6 Test Frontend

```bash
# Visit URL
https://ceo-frontend.vercel.app

# Verify:
# - Page loads without errors
# - No console errors
# - Can connect to backend API
# - Dashboard displays correctly
```

---

## 🗄️ Step 3: Set Up MongoDB Atlas

### 3.1 Create MongoDB Cluster

1. Go to **mongodb.com/cloud/atlas**
2. Create free cluster (M0 tier)
3. Configure:
   - **Cloud Provider:** AWS
   - **Region:** US East
   - **Cluster Name:** ceo-production

### 3.2 Create Database & Collections

```javascript
// In MongoDB Atlas, create:

// Database: ceo_db

// Collections:
db.createCollection("users");
db.createCollection("products");
db.createCollection("tasks");
db.createCollection("revenue");
db.createCollection("affiliates");
db.createCollection("ad_campaigns");
db.createCollection("ad_performance");
db.createCollection("hot_products");
db.createCollection("errors");

// Create indexes:
db.products.createIndex({ "id": 1 });
db.revenue.createIndex({ "user_id": 1, "date": -1 });
db.ad_performance.createIndex({ "campaign_id": 1 });
```

### 3.3 Get Connection String

1. Cluster → **Connect**
2. Select **Connect your application**
3. Copy connection string: `mongodb+srv://...`
4. Add to Render environment as `MONGO_URL`

---

## 🔑 Step 4: Configure API Keys

### 4.1 Get Required Keys

1. **OpenAI API Key:**
   - Go to platform.openai.com/api-keys
   - Create new key
   - Copy to Render as `OPENAI_API_KEY`

2. **Gumroad API Key:**
   - Go to gumroad.com/settings/access_tokens
   - Create new token
   - Copy to Render as `GUMROAD_API_KEY`

3. **TikTok Business API:**
   - Go to ads.tiktok.com
   - Create app credentials
   - Copy to Render

4. **Your App's Master API Key:**
   - Generate random string: `openssl rand -hex 32`
   - Store securely as `API_KEY` in Render
   - Share with users who need API access

### 4.2 Verify Keys Work

```bash
# Test OpenAI
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models

# Test Gumroad
curl -H "Authorization: Bearer $GUMROAD_API_KEY" \
  https://api.gumroad.com/api/products

# Test your app's health
curl -X GET https://ceo-ai-backend.onrender.com/api/health
```

---

## 🧪 Step 5: End-to-End Testing

### 5.1 Smoke Tests (Critical Path)

```bash
# 1. Backend health
curl -X GET https://ceo-ai-backend.onrender.com/api/health
# Expected: 200 OK with "healthy" status

# 2. Frontend loads
curl -I https://ceo-frontend.vercel.app
# Expected: 200 OK

# 3. API authentication
curl -X POST https://ceo-ai-backend.onrender.com/api/hot-products/find-trending \
  -H "x-api-key: YOUR_API_KEY"
# Expected: 200 OK or appropriate error

# 4. Database connection
curl -X GET https://ceo-ai-backend.onrender.com/api/health
# Expected: database: "connected"
```

### 5.2 Complete Workflow Test

```bash
# 1. Find hot products
curl -X POST https://ceo-ai-backend.onrender.com/api/hot-products/find-trending \
  -H "x-api-key: YOUR_API_KEY"

# 2. Generate ad campaign
curl -X POST https://ceo-ai-backend.onrender.com/api/advertising/generate-campaign \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{"product_name": "AI Tool", "category": "AI", ...}'

# 3. Check dashboard
curl -X GET https://ceo-ai-backend.onrender.com/api/advertising/dashboard \
  -H "x-api-key: YOUR_API_KEY"

# 4. Track revenue
curl -X GET https://ceo-ai-backend.onrender.com/api/revenue/summary \
  -H "x-api-key: YOUR_API_KEY"
```

### 5.3 Frontend Testing

1. Open https://ceo-frontend.vercel.app
2. Verify dashboard loads
3. Check no console errors (F12 → Console)
4. Test API connection
5. Navigate all pages
6. Verify responsive design (mobile, tablet, desktop)

---

## 📊 Step 6: Monitoring & Alerts Setup

### 6.1 Render Monitoring

1. Dashboard → Select App
2. **Metrics:** Enable CPU, Memory, Network monitoring
3. **Logs:** Check real-time logs
4. **Alerts:** Set up critical alerts

### 6.2 Vercel Analytics

1. Dashboard → Project → Analytics
2. View performance metrics
3. Monitor Core Web Vitals
4. Check error tracking

### 6.3 Error Tracking (Optional)

```bash
# Install Sentry (error tracking)
pip install sentry-sdk==1.28.1

# In server.py:
import sentry_sdk
sentry_sdk.init(
    dsn="https://your-sentry-dsn@sentry.io/project",
    traces_sample_rate=1.0
)
```

### 6.4 Set Up Logging

All requests logged to MongoDB:
```javascript
db.logs.find({ level: "error" }).sort({ timestamp: -1 }).limit(10)
```

---

## 🔒 Step 7: Security Hardening

### 7.1 CORS Configuration

Already configured in server.py:
```python
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
```

Render env variable:
```env
CORS_ORIGINS=https://ceo-frontend.vercel.app,https://yourdomain.com
```

### 7.2 Rate Limiting

Already implemented in server.py:
- 100 requests per minute per user
- Configurable per endpoint

### 7.3 Security Headers

Add to Render response headers:
```
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
```

### 7.4 API Key Rotation

```bash
# Generate new key monthly
NEW_KEY=$(openssl rand -hex 32)
# Update in Render secrets
# Notify users to update their credentials
```

---

## 📈 Step 8: Performance Optimization

### 8.1 Backend Optimization

Already implemented:
- ✅ Async/await for non-blocking I/O
- ✅ Connection pooling for database
- ✅ Caching for frequently accessed data
- ✅ Background task queuing
- ✅ Request compression (gzip)

### 8.2 Frontend Optimization

Already implemented:
- ✅ Code splitting
- ✅ Lazy loading
- ✅ Image optimization
- ✅ Bundle minification
- ✅ CSS/JS compression

### 8.3 Database Optimization

Create indexes:
```javascript
// Fast lookups
db.products.createIndex({ created_at: -1 });
db.revenue.createIndex({ user_id: 1, date: -1 });
db.tasks.createIndex({ status: 1 });
db.ad_campaigns.createIndex({ status: 1, created_at: -1 });
```

---

## 🎯 Step 9: Launch Checklist

```
BEFORE GOING LIVE:

✅ Backend on Render (https://ceo-ai-backend.onrender.com)
✅ Frontend on Vercel (https://ceo-frontend.vercel.app)
✅ MongoDB Atlas connected
✅ All API keys configured
✅ Security tests passing
✅ Performance tests passing
✅ End-to-end workflow verified
✅ Monitoring configured
✅ Error tracking active
✅ Rate limiting tested
✅ Custom domain configured (optional)
✅ SSL/HTTPS working
✅ Database backups enabled
✅ Documentation complete
✅ Team trained on deployment
✅ Rollback plan documented

GOING LIVE:

✅ Deploy backend
✅ Deploy frontend
✅ Run post-deployment tests
✅ Monitor logs for errors
✅ Watch for unusual activity
✅ Check API costs
✅ Verify marketplace integrations
✅ Test affiliate links
✅ Monitor revenue accuracy
```

---

## 🆘 Troubleshooting

### Backend Not Starting

```bash
# Check logs
render logs --service ceo-ai-backend

# Common issues:
# - Missing environment variables
# - MongoDB connection failed
# - Port already in use
# - Missing dependencies
```

### Frontend Not Loading

```bash
# Check build logs in Vercel
# Common issues:
# - API URL misconfigured
# - Environment variables missing
# - Build command failed
# - Port conflict
```

### Database Connection Failed

```bash
# Test connection string
mongosh "your-connection-string"

# Verify:
# - IP whitelist includes Render IPs
# - Username/password correct
# - Cluster accessible
# - Network TTL appropriate
```

### API Slow/Timing Out

```bash
# Check:
# - Database query performance
# - API response times
# - Rate limiting not kicking in
# - External API latency
# - Gunicorn worker count (increase if needed)
```

---

## 📞 Support & Escalation

**Issue:** Backend down  
**Solution:** Check Render dashboard, view logs, restart container

**Issue:** API key not working  
**Solution:** Verify key in environment, check rate limiting, test with curl

**Issue:** Database slow  
**Solution:** Check indexes created, optimize queries, upgrade cluster tier

**Issue:** High API costs  
**Solution:** Review usage, adjust limits, implement caching

---

## 🎉 Deployment Complete!

Your AI CEO system is now live and ready to generate revenue!

**Next Steps:**
1. Share URLs with users
2. Generate their API keys
3. Start promoting products
4. Monitor dashboards
5. Scale to success!

---

**Deployment Date:** _____________  
**Live URL:** https://ceo-frontend.vercel.app  
**API URL:** https://ceo-ai-backend.onrender.com  
**Status:** 🟢 LIVE

