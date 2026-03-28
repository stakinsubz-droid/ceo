# 📖 OPERATIONS RUNBOOK

**AI CEO System - Complete Production Operations Guide**

---

## 🎯 Purpose

This runbook is your single source of truth for running the AI CEO system in production. It references specialized guides for specific scenarios.

---

## 🗂️ Document Map

```
OPERATIONS RUNBOOK (you are here)
│
├─ 🚀 GETTING STARTED
│  └─ PRODUCTION_DEPLOYMENT_GUIDE.md
│     (Step-by-step: Deploy to Render/Vercel/MongoDB)
│
├─ ✅ BEFORE GOING LIVE
│  ├─ DEPLOYMENT_SECURITY_CHECKLIST.md
│  │  (Security & compliance audit - 94% ready score)
│  │
│  └─ GO_LIVE_FINAL_CHECKLIST.md
│     (100+ verification items - sign-off)
│
├─ 📊 DURING PRODUCTION
│  ├─ MONITORING_ALERTS_SETUP.md
│  │  (24/7 monitoring dashboard & alerts)
│  │
│  └─ HOT_PRODUCTS_GUIDE.md
│     (API reference for monetization features)
│
├─ 🆘 WHEN SOMETHING BREAKS
│  └─ EMERGENCY_ROLLBACK_PLAN.md
│     (Troubleshooting & disaster recovery)
│
└─ 📚 REFERENCE
   ├─ README.md (System overview)
   ├─ SYSTEM_OVERVIEW.md (Architecture)
   └─ backend/HOT_PRODUCTS_README.md (Monetization details)
```

---

## 🚀 Quick Start Paths

### Path 1: First Time Deployment (2-4 hours)

**Goal:** Deploy system to production for the first time

**Steps:**
1. ✅ Review: DEPLOYMENT_SECURITY_CHECKLIST.md (10 min)
   - Understand security requirements
   - Know what will be checked

2. ✅ Configure: PRODUCTION_DEPLOYMENT_GUIDE.md (45 min)
   - Set up Render backend
   - Set up Vercel frontend
   - Set up MongoDB Atlas

3. ✅ Prepare: GO_LIVE_FINAL_CHECKLIST.md (30 min)
   - Gather all API keys
   - Prepare environment variables
   - Create test plan

4. ✅ Deploy: Follow PRODUCTION_DEPLOYMENT_GUIDE.md (60 min)
   - Deploy backend to Render
   - Deploy frontend to Vercel
   - Configure database

5. ✅ Verify: GO_LIVE_FINAL_CHECKLIST.md (60 min)
   - Run all verification tests
   - Performance tests
   - E2E workflow test

6. ✅ Monitor: MONITORING_ALERTS_SETUP.md (30 min)
   - Enable Render alerts
   - Enable Vercel monitoring
   - Enable MongoDB alerts

**When done:** System is live and monitored

---

### Path 2: Something is Broken (5-30 min)

**Goal:** Restore service quickly

**Steps:**

1. 🚨 **STAY CALM** (30 seconds)
   - Don't panic, don't push code
   - It's probably recoverable

2. 🔍 **ASSESS** (1-5 min)
   ```bash
   # What's actually broken?
   curl https://ceo-ai-backend.onrender.com/api/health
   # Status: ?
   
   # Check frontend
   curl -I https://ceo-frontend.vercel.app
   # Status: ?
   
   # Check database
   mongosh "your-connection-string"
   # Can you connect? Yes/No?
   ```

3. 📋 **IDENTIFY** (1-2 min)
   - Is it backend? → See "Backend Down" in EMERGENCY_ROLLBACK_PLAN.md
   - Is it frontend? → See "Frontend Down" in EMERGENCY_ROLLBACK_PLAN.md
   - Is it database? → See "Database Down" in EMERGENCY_ROLLBACK_PLAN.md

4. ⚡ **FIX** (Follow appropriate section, 5-20 min)
   - Execute the procedure for your issue type
   - Use Render/Vercel dashboards
   - Follow rollback if needed

5. ✅ **VERIFY** (1-2 min)
   ```bash
   curl https://ceo-ai-backend.onrender.com/api/health
   # Should see: "status": "healthy"
   ```

**See:** EMERGENCY_ROLLBACK_PLAN.md for detailed procedures

---

### Path 3: Performance Issues (10-30 min)

**Goal:** Make the system faster

**Symptoms:**
- API responses > 5 seconds
- Frontend slow to load
- Users complaining about lag

**Quick Checks:**
```bash
# Time an API call
time curl https://ceo-ai-backend.onrender.com/api/health

# Check current load
# Render Dashboard → ceo-ai-backend → Metrics
# Look for: CPU, Memory, Network

# Check database
# MongoDB Atlas → Monitoring
# Look for: slow queries, connection count
```

**Solutions (by severity):**

1. **Response time > 10s** (CRITICAL)
   - Likely database issue
   - Check: Database connections > 500?
   - Fix: Restart database connection pool
   ```bash
   # Render Dashboard → Manual Deploy
   ```

2. **Response time 5-10s** (HIGH)
   - Likely too many requests
   - Check: Is rate limiting working?
   - Fix: Increase rate limits temporarily
   ```bash
   # Render → Environment
   # RATE_LIMIT_REQUESTS=1000
   # Redeploy
   ```

3. **Response time 2-5s** (NORMAL)
   - Acceptable performance
   - Monitor and move on

**See:** MONITORING_ALERTS_SETUP.md for performance baselines

---

### Path 4: High Costs (15 min)

**Goal:** Stop bleeding money

**Symptoms:**
- Bill > expected budget
- API costs spiking
- Unexpected charges

**Quick Fixes:**
```bash
# Step 1: Find what's expensive
# Check backend logs:
# MongoDB → error_logs collection
# Look for: "cost_estimate" > 1.0

# Step 2: Identify culprit
# Is it OpenAI? Gumroad? Google?
# Filter logs by "service"

# Step 3: Disable or limit
# Set fake API key temporarily
# Or reduce rate limits

# Step 4: Fix root cause
# Is there a loop? A bug? Abuse?
# Fix and re-enable
```

**Emergency Actions:**
```bash
# Set all API keys to dummy values
# Render → Environment
# OPENAI_API_KEY=disabled
# GOOGLE_API_KEY=disabled
# Redeploy

# This stops all AI calls until you fix
```

**See:** PRODUCTION_DEPLOYMENT_GUIDE.md for API key configuration

---

### Path 5: Security Alert (immediate)

**Goal:** Investigate and contain

**Symptoms:**
- Suspicious activity in logs
- Unexpected API calls
- Credentials possibly exposed

**Immediate Actions:**
```bash
# Step 1: REVOKE all API keys
# Get new keys from:
# - OpenAI Dashboard
# - Gumroad Settings
# - MongoDB Atlas
# - Google Cloud Console

# Step 2: UPDATE environment variables
# Render Dashboard → Environment
# Replace all API keys with new ones
# DO NOT commit to GitHub

# Step 3: REDEPLOY
# Render → Manual Deploy

# Step 4: ROTATE credentials
# Generate new keys
# Update all services
```

**See:** DEPLOYMENT_SECURITY_CHECKLIST.md for security procedures

---

## 📊 Daily Operations Checklist

**Every morning (9 AM):**

```
☐ Health check: curl health endpoint
  Expected: status=healthy, database=connected
  
☐ Error rate check: MongoDB error_logs
  Expected: < 10 errors in last 24 hours
  
☐ Cost check: MongoDB cost_logs
  Expected: < 80% of daily budget
  
☐ Backup check: MongoDB Atlas → Backup
  Expected: Latest backup < 24 hours old
  
☐ Uptime check: Render/Vercel dashboards
  Expected: 100% uptime
  
☐ User feedback: Check Slack/email/support
  Expected: No critical complaints
```

---

## 🔔 When Alerts Fire

**Alert received?** Follow this flow:

```
Is it CRITICAL? (Red alert)
├─ YES → Execute EMERGENCY_ROLLBACK_PLAN.md → See "Critical Issues"
└─ NO → Go to next question

Is it HIGH? (Orange alert)
├─ YES → Investigate within 15 minutes → Log issue → Fix today
└─ NO → Go to next question

Is it MEDIUM? (Yellow alert)
├─ YES → Investigate today → Plan fix
└─ NO → Go to next question

Is it LOW? (Green alert)
├─ YES → Log for next review
└─ NO → Probably false alarm, move on
```

**See:** MONITORING_ALERTS_SETUP.md

---

## 📈 Key Metrics to Track

**Every Hour:**
- Backend health status (✅/❌)
- API response time average (target: < 2s)
- Error count in logs (target: 0-2/hour)

**Every Day:**
- Daily API calls processed
- Daily revenue generated
- Daily cost incurred
- Backup status

**Every Week:**
- User feedback sentiment
- Top error types
- Performance trend
- Cost trend

**Every Month:**
- SLA uptime % (target: >99.9%)
- Cost per request ratio
- Revenue vs cost ratio
- User growth

**See:** MONITORING_ALERTS_SETUP.md for setup

---

## 🔄 Release Process

**When deploying new code:**

1. **Pre-deployment** (5 min)
   - [ ] All tests passing locally
   - [ ] Code reviewed
   - [ ] Backup of database taken
   - [ ] Rollback plan ready

2. **Deployment** (5 min)
   ```bash
   git commit -m "Your change"
   git push origin main
   # Render auto-deploys from main branch
   # Wait for deployment in dashboard
   ```

3. **Verification** (5 min)
   - [ ] Build succeeded in Render
   - [ ] Health check: 200 OK
   - [ ] No new errors in logs
   - [ ] Performance normal

4. **Post-deployment** (ongoing)
   - Monitor for next 1 hour
   - Watch error rates
   - Check user feedback
   - Ready to rollback if needed

**If something breaks:** See Path 2 (Something is Broken)

---

## 👥 Team Responsibilities

### DevOps Engineer
- [ ] Deploy code to production
- [ ] Configure infrastructure (Render/Vercel/MongoDB)
- [ ] Monitor system health
- [ ] Execute rollbacks
- [ ] Respond to critical alerts

### Security Lead
- [ ] Audit API keys and credentials
- [ ] Review DEPLOYMENT_SECURITY_CHECKLIST.md
- [ ] Approve production deployment
- [ ] Investigate security incidents
- [ ] Rotate credentials periodically

### CTO/Backend Lead
- [ ] Review code before deployment
- [ ] Define performance SLAs
- [ ] Optimize database queries
- [ ] Plan capacity scaling
- [ ] Owner of GO_LIVE_FINAL_CHECKLIST.md

### Product/Manager
- [ ] Define success metrics
- [ ] Monitor user feedback
- [ ] Report status to stakeholders
- [ ] Approve major changes
- [ ] Business continuity planning

---

## 🎯 SLAs (Service Level Agreements)

**We commit to:**

| Metric | Target | Penalty |
|--------|--------|---------|
| Uptime | 99.9% (43 min/month) | $100/hour |
| Response Time | < 2s avg | $50 per hour over 5s |
| Error Rate | < 1% | Alert & investigate |
| Data Loss | 0 | Emergency response |
| Recovery Time | < 15 min | Escalate immediately |

---

## 🚦 Status Indicators

**Green (All Good)** ✅
- Health check: 200 OK
- Error rate: < 1%
- Response time: < 2s
- Backup: < 24h old
- No alerts

**Yellow (Watch)** 🟡
- Error rate: 1-5%
- Response time: 2-5s
- Approaching alert thresholds
- Non-critical issue logged
- **Action:** Investigate today

**Red (Critical)** 🔴
- Health check: Error/timeout
- Error rate: > 10%
- Response time: > 10s
- Database: Disconnected
- **Action:** Execute emergency procedures immediately

**See:** Current status in Render/Vercel/MongoDB dashboards

---

## 📞 Who to Contact

**24/7 Issues:**
- **On-Call:** [Slack #oncall]
- **Phone:** [emergency #]

**During Business Hours:**
- **DevOps:** [email]
- **CTO:** [email]
- **Security:** [email]

**Non-Urgent:**
- **Tickets:** [GitHub issues]
- **Email:** [support@]

---

## 🎓 Learning Resources

**New team member? Start here:**
1. Read: SYSTEM_OVERVIEW.md (understand architecture)
2. Read: PRODUCTION_DEPLOYMENT_GUIDE.md (understand deployment)
3. Read: MONITORING_ALERTS_SETUP.md (understand monitoring)
4. Watch: Backend demo video (if available)
5. Practice: Deploy to staging environment
6. Pair: Shadow senior engineer on production task

---

## 📝 Incident Reporting

**When something goes wrong:**

```markdown
# Incident Report

**Severity:** [CRITICAL/HIGH/MEDIUM/LOW]
**Start Time:** [when problem began]
**Impact:** [what users were affected]
**Root Cause:** [what actually went wrong]
**Resolution Steps:** [what you did to fix it]
**Prevention:** [how to prevent next time]
**Post-Incident Actions:**
- [ ] Fix root cause
- [ ] Update monitoring
- [ ] Update documentation
- [ ] Team training
```

**File location:** GitHub Issues → New Issue → Incident template

---

## ✅ Monthly Audit Checklist

**First Monday of each month:**

- [ ] Review all logs from previous month
- [ ] Update baseline metrics
- [ ] Review cost trends
- [ ] Update alert thresholds if needed
- [ ] Test disaster recovery procedures
- [ ] Verify backups restorable
- [ ] Check security compliance
- [ ] Review team capacity
- [ ] Plan upcoming maintenance
- [ ] Update SLAs if needed

---

## 🎯 30/60/90 Day Plan

### 30 Days: Stabilization
- ✅ System running in production
- ✅ No critical issues
- ✅ All monitoring configured
- ✅ Team trained on procedures
- **Goal:** Prove stability

### 60 Days: Optimization
- ✅ Response times < 1.5s
- ✅ Error rate < 0.1%
- ✅ Cost within budget
- ✅ Zero unplanned downtime
- **Goal:** Optimize performance

### 90 Days: Scale
- ✅ Ready for 10x traffic
- ✅ Load test passed
- ✅ Capacity plan documented
- ✅ Auto-scaling configured
- **Goal:** Prepare for growth

---

## 🏁 Success Metrics

After 90 days in production:

✅ **Reliability:** 99.9% uptime  
✅ **Performance:** < 1.5s average response time  
✅ **Cost Control:** Actual spend < budget + 20%  
✅ **User Satisfaction:** > 90% positive feedback  
✅ **Team Readiness:** Can respond to issues < 5 min  
✅ **Zero:** Unauthorized access, data loss, compliance violations  

---

## 🔗 Quick Links

| Link | Purpose |
|------|---------|
| [Render Dashboard](https://dashboard.render.com) | Backend hosting |
| [Vercel Dashboard](https://vercel.com/dashboard) | Frontend hosting |
| [MongoDB Atlas](https://cloud.mongodb.com) | Database |
| [GitHub Repo](https://github.com/stackinsubzinc-dev/ceo) | Source code |
| [OpenAI API](https://platform.openai.com) | AI API |
| [Server Health](https://ceo-ai-backend.onrender.com/api/health) | Live status |

---

## 📚 All Documentation Files

| File | Purpose | When to Use |
|------|---------|------------|
| **PRODUCTION_DEPLOYMENT_GUIDE.md** | Step-by-step deployment | First deployment |
| **DEPLOYMENT_SECURITY_CHECKLIST.md** | Security audit | Before going live |
| **GO_LIVE_FINAL_CHECKLIST.md** | Launch verification | Day of launch |
| **EMERGENCY_ROLLBACK_PLAN.md** | Disaster recovery | Something breaks |
| **MONITORING_ALERTS_SETUP.md** | Monitoring setup | After deployment |
| **OPERATIONS_RUNBOOK.md** | This file | Daily reference |

---

## 🎯 Your Next Steps

1. **Today:**
   - [ ] Read all documentation
   - [ ] Gather API keys
   - [ ] Prepare environment

2. **Tomorrow:**
   - [ ] Begin deployment following PRODUCTION_DEPLOYMENT_GUIDE.md
   - [ ] Set up monitoring
   - [ ] Run verification tests

3. **Next Week:**
   - [ ] Monitor production
   - [ ] Fix any issues
   - [ ] Document lessons learned

---

**Remember:** 
- *Preparation prevents problems*
- *Monitoring catches issues early*
- *Documentation prevents panic*
- *Teamwork makes it work*

**You've got this! 🚀**

