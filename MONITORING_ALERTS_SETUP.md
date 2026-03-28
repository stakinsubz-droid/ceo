# 📊 MONITORING & ALERTING SETUP

**Complete Guide to Production Monitoring**

---

## 🎯 Overview

A production system needs eyes on it 24/7. This guide shows you how to set up monitoring so you know immediately when something breaks.

---

## 📈 What to Monitor

### Critical Metrics

| Metric | Target | Alert If | Why |
|--------|--------|----------|-----|
| **Backend Health** | 200 OK | Status ≠ 200 | Shows if API is alive |
| **Response Time** | <2s | >5s avg | Users see lag |
| **Error Rate** | <1% | >5% | Breaking user experience |
| **Database** | Connected | Disconnected | Core dependency |
| **API Uptime** | 99.9% | <99% | SLA breach |
| **API Rate Limit** | 100 req/min | Hits > 80% | Abuse detection |
| **Memory Usage** | <80% | >90% | Crash imminent |
| **Disk Usage** | <80% | >90% | Logs can't write |
| **Cost** | See budget | >$500/day | Runaway spend |

---

## 🔴 Alert Levels

### Level 1: CRITICAL 🚨
**Response: IMMEDIATE (< 5 min)**
- Backend completely down
- Database disconnected
- Data loss detected
- Security breach suspected
- All users affected

**Action:** Wake up DevOps, execute emergency procedures

---

### Level 2: HIGH ⚠️
**Response: URGENT (< 15 min)**
- Error rate > 10%
- Response time > 10s
- API key compromised
- Memory > 95%
- Cost > $1000/day

**Action:** Page on-call team, investigate immediately

---

### Level 3: MEDIUM 🟡
**Response: SOON (< 1 hour)**
- Error rate > 5%
- Response time > 5s
- Rate limit being hit frequently
- Disk > 85%
- Cost trending high

**Action:** Create ticket, schedule investigation

---

### Level 4: LOW 🟢
**Response: LATER (< 1 day)**
- Error rate 1-5%
- Response time 2-5s
- Minor issues observed
- Unusual traffic pattern

**Action:** Log and monitor, include in next review

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Production System               │
│  ┌──────────────┐    ┌──────────────┐  │
│  │  Backend     │    │  Frontend    │  │
│  │  (Render)    │    │  (Vercel)    │  │
│  └──────────────┘    └──────────────┘  │
│  ┌──────────────┐                      │
│  │  Database    │                      │
│  │  (MongoDB)   │                      │
│  └──────────────┘                      │
└─────────────────────────────────────────┘
        ↓ Metrics ↓
┌─────────────────────────────────────────┐
│      Monitoring Stack                   │
│  ┌────────┐ ┌────────┐ ┌────────────┐  │
│  │ Render │ │ Vercel │ │   MongoDB  │  │
│  │ Monitor│ │ Analytics│ │  Alerts  │  │
│  └────────┘ └────────┘ └────────────┘  │
└─────────────────────────────────────────┘
        ↓ Alerts ↓
┌─────────────────────────────────────────┐
│     Alert Channels                      │
│  ┌─────┐ ┌───────┐ ┌─────────────────┐ │
│  │Email│ │ Slack │ │  SMS/Phone Call │ │
│  └─────┘ └───────┘ └─────────────────┘ │
└─────────────────────────────────────────┘
```

---

## 🔧 Render Monitoring Setup

### Step 1: Health Check Configuration

**Already Configured In:**
- `backend/core/routes_v4_production.py` → `/api/health` endpoint

**Verify Endpoint:**

```bash
curl https://ceo-ai-backend.onrender.com/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-03-26T10:30:00",
  "database": "connected",
  "services": {
    "openai": "operational",
    "emergent_integrations": "operational"
  }
}
```

### Step 2: Configure Render Alerts

1. Go to: https://dashboard.render.com/
2. Select: **ceo-ai-backend** service
3. Click: **Settings**
4. Scroll to: **Alerts**
5. Configure:

```
Metric: CPU Usage
Threshold: > 80%
Duration: 2 minutes
Action: Send notification

Metric: Memory
Threshold: > 90%
Duration: 1 minute
Action: Send notification

Metric: Disk
Threshold: > 85%
Duration: 5 minutes
Action: Send notification

Metric: Build Failed
Threshold: Any
Duration: Immediate
Action: Send notification
```

### Step 3: Render Email Notifications

1. Dashboard → Settings → Notification Email
2. Add emails for alerts
3. Verify email addresses

**Recommended Recipients:**
- DevOps Lead
- CTO
- On-Call Engineer

---

## 🎨 Vercel Monitoring Setup

### Step 1: Analytics Dashboard

1. Go to: https://vercel.com/dashboard
2. Select: **ceo-frontend**
3. Click: **Analytics** tab
4. View:

```
- Core Web Vitals (LCP, FID, CLS)
- Rich Page Data
- Real User Monitoring
```

### Step 2: Configure Vercel Alerts

1. Dashboard → Settings → Monitoring
2. Configure thresholds:

```
Largest Contentful Paint (LCP):
  Threshold: > 2.5s
  Alert: HIGH

First Input Delay (FID):
  Threshold: > 100ms
  Alert: HIGH

Cumulative Layout Shift (CLS):
  Threshold: > 0.1
  Alert: MEDIUM
```

### Step 3: Deployment Monitoring

1. Dashboard → ceo-frontend → Deployments
2. Each deployment shows:
   - Build duration
   - Build status
   - Deployment URL
   - Performance score

**Set alerts for:**
- Build failures
- Performance regression
- Long build times

---

## 🍃 MongoDB Monitoring Setup

### Step 1: MongoDB Atlas Dashboard

1. Go to: https://cloud.mongodb.com/
2. Select: **ceo-ai** cluster
3. Click: **Monitoring**
4. View metrics:

```
- Connections
- Database Storage
- Query Performance
- Replication Lag
- Network I/O
```

### Step 2: Performance Alerts

1. Go to: **Alerts** → **Alert Settings**
2. Create:

```
Alert: Host is Down
Severity: Critical
Notification: Email + SMS

Alert: Replication Lag > 60s
Severity: High
Notification: Email

Alert: Storage > 80%
Severity: Medium
Notification: Email

Alert: Connection > 1000
Severity: Medium
Notification: Email
```

### Step 3: Backup Verification

1. Go to: **Backup** tab
2. Verify:
   - [ ] Backups running daily
   - [ ] Latest backup successful
   - [ ] Retention policy set

---

## 💰 Cost Monitoring

### Step 1: API Usage Tracking

**Track in backend logs:**
```python
# Already logged in server.py
db.error_logs.insert_one({
    "type": "api_call",
    "service": "openai",
    "cost_estimate": 0.02,
    "timestamp": datetime.utcnow()
})
```

### Step 2: Daily Cost Report

Create a scheduled task:

```bash
# Add to server.py startup
@app.on_event("startup")
async def schedule_cost_report():
    # Runs daily at midnight
    scheduler.add_job(
        send_daily_cost_report,
        'cron',
        hour=0,
        minute=0
    )
```

### Step 3: Cost Alerts

Set in each service:

**OpenAI:**
```
Budget limit: $100/day
Alert at: $80/day (80%)
Hard stop: $150/day
```

**Google Generative AI:**
```
Budget limit: $50/day
Alert at: $40/day (80%)
Hard stop: $75/day
```

---

## 📊 Custom Monitoring Dashboard

### Create Monitoring Dashboard

```html
<!-- monitoring-dashboard.html -->
<dashboard>
  <metric name="Backend Health">
    <source>https://ceo-ai-backend.onrender.com/api/health</source>
    <refresh>30s</refresh>
    <alert-if>status != healthy</alert-if>
  </metric>
  
  <metric name="API Response Time">
    <source>Backend logs</source>
    <threshold>2000ms</threshold>
    <alert-if>avg > 5000ms</alert-if>
  </metric>
  
  <metric name="Error Rate">
    <source>MongoDB error_logs</source>
    <threshold>1%</threshold>
    <alert-if>rate > 5%</alert-if>
  </metric>
  
  <metric name="Database Connections">
    <source>MongoDB cluster</source>
    <threshold>100</threshold>
    <alert-if>connections > 500</alert-if>
  </metric>
  
  <metric name="Daily Cost">
    <source>Backend cost_logs</source>
    <threshold>$100</threshold>
    <alert-if>accumulated > $500</alert-if>
  </metric>
</dashboard>
```

---

## 🔔 Alert Channels

### Email Alerts

**Configuration:**
```
Service: SendGrid
Recipient: devops@yourdomain.com
Subject: [ALERT] {metric} - {severity}
Body: Includes metric value, threshold, action items
```

### Slack Integration

**(Recommended - fastest response)**

1. Create Slack workspace: https://slack.com
2. Create channel: #monitoring-alerts
3. Get webhook: https://api.slack.com/apps → Create App → Webhooks
4. Add to backend:

```python
from slack_sdk.webhook import WebhookClient

def send_slack_alert(severity, message, metric):
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    client = WebhookClient(webhook_url)
    
    color = {
        'critical': '#FF0000',
        'high': '#FFA500',
        'medium': '#FFFF00',
        'low': '#00FF00'
    }[severity]
    
    response = client.send(
        text=f"[{severity.upper()}] {message}",
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{severity.upper()}*\n{message}"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"Metric: {metric} | Time: {datetime.utcnow()}"
                    }
                ]
            }
        ]
    )
    return response
```

### SMS/Phone Alerts

**For CRITICAL issues only:**

```python
from twilio.rest import Client

def send_sms_alert(phone, message):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        from_=os.getenv('TWILIO_PHONE'),
        to=phone,
        body=f"🚨 CRITICAL: {message}"
    )
    return message.sid
```

---

## 📋 Monitoring Checklist

**Daily (9 AM):**
- [ ] Check health dashboard
- [ ] Review error rates
- [ ] Check cost tracking
- [ ] Verify backups completed

**Weekly (Monday 9 AM):**
- [ ] Review performance trends
- [ ] Check for memory leaks
- [ ] Verify alert thresholds still appropriate
- [ ] Review logs for issues

**Monthly (1st of month):**
- [ ] Full monitoring audit
- [ ] Update baseline metrics
- [ ] Review cost trends
- [ ] Test alert system

**Quarterly:**
- [ ] Test monitoring failover
- [ ] Update alert contacts
- [ ] Disaster recovery drill
- [ ] Update escalation procedures

---

## 🧪 Test Your Alerts

### Test Email Alerts

```bash
# Trigger a test error
curl -X POST https://ceo-ai-backend.onrender.com/api/test-alert \
  -H "Content-Type: application/json" \
  -d '{"alert_type": "email", "severity": "high"}'
```

### Test Slack Integration

```python
import requests

def test_slack_alert():
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    response = requests.post(webhook_url, json={
        "text": "🧪 Test Alert - Monitoring System Online"
    })
    print(f"Slack test: {response.status_code}")
```

### Verify Alert Routes

```bash
# Test health check
curl https://ceo-ai-backend.onrender.com/api/health

# Test metrics endpoint
curl https://ceo-ai-backend.onrender.com/api/metrics

# Test error logging
curl -X POST https://ceo-ai-backend.onrender.com/api/test-error
```

---

## 🎯 Success Metrics

After monitoring is set up, you should have:

✅ Real-time visibility into system health  
✅ Alerts within 1 minute of issues  
✅ Under 5 minute response time for alerts  
✅ Zero unplanned downtime  
✅ Cost tracking preventing surprises  
✅ Performance baselines established  
✅ Clear escalation paths  
✅ Complete audit trail  

---

## 📞 Once Alerts Fire

**When you get an alert:**

1. **Read it carefully** - What's the issue?
2. **Check the dashboard** - Is it a false alarm?
3. **Reproduce if possible** - Can you trigger it again?
4. **Execute playbook** - Emergency rollback if critical
5. **Fix the root cause** - Don't just silence the alert
6. **Verify stability** - Make sure it's really fixed
7. **Document** - What was wrong? Why?
8. **Update systems** - Update monitoring/alerts

---

## 🔗 Quick Links

- **Render Dashboard:** https://dashboard.render.com
- **Vercel Dashboard:** https://vercel.com/dashboard
- **MongoDB Atlas:** https://cloud.mongodb.com
- **GitHub Logs:** https://github.com/stackinsubzinc-dev/ceo
- **Status Page:** [yourmonitoringurl.com]
- **Escalation Group:** [Slack or email]

---

**Remember:** Good monitoring is like good insurance - you hope you never need it, but you'll be glad it's there when you do. 🛡️

