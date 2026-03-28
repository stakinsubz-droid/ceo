# 🆘 ROLLBACK & EMERGENCY PROCEDURES

**AI CEO System - Disaster Recovery & Rollback Plan**

---

## 🚨 Emergency Protocol

**IF SOMETHING GOES WRONG:**

1. **STOP:** Don't panic, don't push more code
2. **ASSESS:** Check what's broken (backend, frontend, DB, API)
3. **COMMUNICATE:** Notify team immediately
4. **EXECUTE:** Follow appropriate rollback procedure below
5. **MONITOR:** Watch for stability after rollback

---

## 🔴 Critical Issues & Immediate Response

### Issue: Backend Down

**Symptoms:**
- `/api/health` returns 500 error
- API requests timeout
- Render shows red status

**Immediate Action (1-5 min):**
```bash
# 1. Check logs
curl https://dashboard.render.com/logs

# 2. Check environment variables
# - All required env vars present?
# - Typos in variables?

# 3. Restart container
# In Render dashboard: Services → ceo-ai-backend → Manual Deploy button
```

**If doesn't fix (5-15 min):**
```bash
# Rollback to previous version
# In Render: Services → ceo-ai-backend → Logs
# Look for deployment history
# Click previous successful deployment and redeploy
```

**If still broken (15+ min):**
```bash
# Restore from backup
# 1. Switch to backup database
# 2. Redeploy backend from last known good commit
# See "FULL ROLLBACK" section below
```

---

### Issue: Frontend Down

**Symptoms:**
- Page won't load
- 404 errors
- Vercel shows deployment failed

**Immediate Action (1-5 min):**
```bash
# 1. Check Vercel logs
# Vercel Dashboard → Projects → ceo-frontend → Deployments

# 2. Check if build succeeded
# Did the build complete or fail?

# 3. Trigger rebuild
# Vercel Dashboard → ceo-frontend → Redeploy button
```

**If build failed (5-15 min):**
```bash
# Rollback to previous version
# Vercel Dashboard → Deployments → Find last successful build → Click "Restore"
```

---

### Issue: Database Down

**Symptoms:**
- Backend health check shows "database: disconnected"
- Database operations timeout
- MongoDB Atlas shows red status

**Immediate Action (1-5 min):**
```bash
# 1. Check MongoDB Atlas status
# Go to mongodb.com/cloud/atlas → Check cluster status

# 2. Verify connection string in Render
# Render Dashboard → ceo-ai-backend → Environment
# Verify MONGO_URL is correct

# 3. Check IP whitelist
# MongoDB Atlas → Security → Network Access
# Is Render's IP whitelisted?

# 4. Test connection manually
mongosh "your-connection-string"
```

**If connection string wrong (5-10 min):**
```bash
# Get correct connection string from MongoDB Atlas
# Copy new connection string
# Update MONGO_URL in Render environment variables
# Trigger redeploy
```

**If IP not whitelisted (10-15 min):**
```bash
# Add Render's IP to MongoDB whitelisting
# MongoDB Atlas → Security → Network Access → Add IP Address
# Add: 0.0.0.0/0 (allows all - more security risk but quick fix)
# Or add Render IP specifically (better security)
```

---

### Issue: API Rate Limiting Too Strict

**Symptoms:**
- Legitimate requests getting 429 errors
- Users can't use the app
- "/tmp/rate_limit_exceeded" errors

**Immediate Action:**
```bash
# Increase rate limits temporarily
# In Render environment:
RATE_LIMIT_REQUESTS=1000  # Increase from default 100
RATE_LIMIT_WINDOW=60      # Per 60 seconds

# Redeploy backend
# Monitor to see if helps
```

---

### Issue: High API Costs

**Symptoms:**
- OpenAI API usage spiking
- Gumroad API hitting limits
- Unexpected $500+ charges

**Immediate Action:**
```bash
# Disable AI features temporarily
# Set fake/debug API keys
# Or shut down affected endpoints

# Review logs for what's causing spike:
# - Runaway loop?
# - Rate limiting not working?
# - Hacked/unauthorized access?

# Fix the root cause
# Re-enable with fixes
```

---

## 🔄 Rollback Procedures

### Scenario 1: Code Bug Introduced

**Situation:** New code deployment broke something, need to revert

**Procedure:**

```bash
# Step 1: Identify last known good commit
git log --oneline | head -20
# Look for last working commit

# Step 2: Revert to that commit
git revert [commit-hash]
git push origin main

# Step 3: Render auto-deploys from main
# Monitor deployment in Render dashboard
# Should deploy automatically within 1-2 minutes

# Step 4: Verify working
curl https://ceo-ai-backend.onrender.com/api/health
# Should return 200 with "healthy"
```

**Estimated Time:** 5-10 minutes

---

### Scenario 2: Environment Variable Issue

**Situation:** Wrong environment variable value or missing variable

**Procedure:**

```bash
# Step 1: Check current environment
# Render Dashboard → ceo-ai-backend → Environment

# Step 2: Identify wrong variable
# Example: MONGO_URL pointing to staging instead of production

# Step 3: Fix variable value
# Edit in Render dashboard

# Step 4: Manually deploy
# Render Dashboard → Manual Deploy button
# Wait for deployment to complete

# Step 5: Verify
curl -I https://ceo-ai-backend.onrender.com/api/health
```

**Estimated Time:** 3-5 minutes

---

### Scenario 3: Database Corruption/Data Loss

**Situation:** Database corrupted or accidentally deleted important data

**Procedure:**

```bash
# Step 1: STOP all writes to database
# Disable write endpoints temporarily
# Point API to read-only mode if possible

# Step 2: Check MongoDB Atlas backups
# MongoDB Atlas → Backup → View Backups
# Look for backup before data was lost

# Step 3: Restore from backup
# MongoDB Atlas → Backup → [Backup Point] → Restore
# Choose "Restore to a New Atlas Cluster" 
# Name it: "ceo_db_restore_[date]"

# Step 4: Update connection string in Render
# Update MONGO_URL to point to restored cluster
# Trigger redeploy

# Step 5: Verify data restored
# Test critical operations work

# Step 6: Once verified, delete old corrupted cluster
```

**Estimated Time:** 30-60 minutes

---

### Scenario 4: Full System Rollback (Emergency)

**Situation:** Everything is broken, need to go back to previous stable state

**Procedure:**

```bash
# Step 1: Identify last known good commit
GOOD_COMMIT=$(git log --oneline | grep -i "stable\|release" | head -1 | awk '{print $1}')

# Step 2: Create rollback branch
git checkout -b emergency-rollback
git reset --hard $GOOD_COMMIT

# Step 3: Force push (CAREFUL!)
git push origin emergency-rollback --force

# Step 4: Update Render to deploy from rollback branch
# Render Dashboard → ceo-ai-backend → Settings → Repo Branch
# Change to: emergency-rollback
# Save and deploy

# Step 5: Monitor deployment
# Watch logs in Render dashboard

# Step 6: Once stable, merge back
git checkout main
git merge emergency-rollback
git push origin main

# Step 7: Update Render back to main branch
# Render Dashboard → ceo-ai-backend → Settings → Repo Branch
# Change back to: main
```

**Estimated Time:** 15-30 minutes

---

## 📊 Data Recovery

### Backup Strategy

**Current Backups:**
- MongoDB Atlas: Automatic daily backup
- GitHub: Version control (all code preserved)
- Vercel: Automatic deployment history

### Restore from Backup

**Latest Backup Location:**
- MongoDB Atlas: https://cloud.mongodb.com/v2
- GitHub: https://github.com/stackinsubzinc-dev/ceo
- Vercel: https://vercel.com/dashboard

**Recovery Steps:**

```bash
# 1. MongoDB restore
# See "Scenario 3: Database Corruption" above

# 2. Code restore
# See "Scenario 1: Code Bug" or "Scenario 4: Full Rollback"

# 3. Frontend restore
# Vercel automatically keeps deployment history
# Vercel Dashboard → Deployments → Select previous version → Restore
```

---

## 📋 Checklist: Before Declaring "Fixed"

After executing rollback:

- [ ] Health check returns 200 OK
- [ ] API authentication working
- [ ] Database connected
- [ ] No errors in logs
- [ ] Frontend loading
- [ ] Critical workflows tested
- [ ] No 500 errors
- [ ] Performance acceptable
- [ ] Rate limiting working
- [ ] All users can connect

---

## 🔍 Diagnostics Commands

Use these to understand what's wrong:

```bash
# Check backend health
curl -v https://ceo-ai-backend.onrender.com/api/health

# Check frontend loads
curl -I https://ceo-frontend.vercel.app

# Test API authentication
curl -H "x-api-key: test-key" \
  https://ceo-ai-backend.onrender.com/api/hot-products/find-trending

# Check rate limiting
for i in {1..5}; do
  curl -w "\n" https://ceo-ai-backend.onrender.com/api/health
done

# Monitor logs in real-time
# Use Render Dashboard → ceo-ai-backend → Logs (tail)
# Or Vercel Dashboard → Deployments → Logs
```

---

## 🚨 When to Escalate

**ESCALATE IMMEDIATELY if:**
- Data loss confirmed
- Security breach suspected
- Customer data exposed
- System down > 30 minutes
- Multiple critical services down
- Cannot identify root cause
- Rollback didn't fix issue

**Who to Contact:**
- **CTO:** [email] (Code & Architecture)
- **DevOps:** [email] (Deployment & Infrastructure)
- **Security:** [email] (Data & API Key breach)
- **Manager:** [email] (Business impact)

---

## 📞 Emergency Contacts

- **Support Line:** [phone]
- **On-Call Team:** [Slack #oncall]
- **GitHub Issues:** https://github.com/stackinsubzinc-dev/ceo/issues
- **Status Page:** https://status.yourdomain.com (if available)

---

## 📖 After-Action

Once system is stable:

1. **Document What Happened**
   - What went wrong?
   - Why did it happen?
   - How was it fixed?

2. **Root Cause Analysis**
   - What was the underlying cause?
   - How can we prevent this?
   - What process failed?

3. **Implement Preventive Measures**
   - Better monitoring?
   - More tests?
   - Better documentation?
   - Training needed?

4. **Update This Document**
   - Add new scenarios learned
   - Update contacts
   - Add new lessons

5. **Communicate to Team**
   - Incident summary
   - What we learned
   - Changes to prevent recurrence

---

## ✅ Regular Testing

**Monthly:**
- [ ] Test backup restoration
- [ ] Test rollback procedures
- [ ] Test database failover
- [ ] Review logs for issues

**Quarterly:**
- [ ] Full disaster recovery drill
- [ ] Test all rollback scenarios
- [ ] Update contact info
- [ ] Review and update procedures

---

## 🎯 Success Criteria

Rollback is successful when:
✅ System comes back online  
✅ No data loss  
✅ All users reconnected  
✅ No cascading failures  
✅ Performance normal  
✅ Monitoring shows green  
✅ Logs show no errors  

---

**Remember:** Staying calm and following procedures is key to a successful recovery. Don't rush.

**You've got this! 💪**

