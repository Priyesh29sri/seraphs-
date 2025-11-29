# Seraphs 2.0 - Real-time 24/7 Monitoring Guide
**Complete Setup for Continuous Regulatory Monitoring**

---

## 🎯 Overview

This guide explains how to set up Seraphs 2.0 for **real-time 24/7 monitoring** of regulatory changes.

---

## ✅ Step 1: Complete All 12 Agents (Current Status)

### Completed Agents (8):
1. ✅ Agent 1: Ingestion
2. ✅ Agent 2: Authenticity
3. ✅ Agent 3: Diff Analysis
4. ✅ Agent 4: Legal LLM
5. ✅ Agent 5: MAAD Debate
6. ✅ Agent 6: Knowledge Graph
7. ✅ Agent 7: Oracle API
8. ✅ Agent 8: Remediation

### Remaining (4):
- Agent 9: ZK + Cardano
- Agent 10: Workflow UI
- Agent 11: AgentOps
- Agent 12: Master Orchestrator

**We'll complete these first, then deploy for 24/7 operation.**

---

## 🔄 How Real-Time 24/7 Monitoring Works

### Architecture:

```
┌─────────────────────────────────────────────┐
│  SCHEDULER (APScheduler)                   │
│  Runs 24/7 in background                   │
│                                             │
│  Every 6 hours:                            │
│    → Agent 1: Fetch critical sources       │
│    → Agent 7: Fetch external data          │
│                                             │
│  Daily 9 AM:                               │
│    → Agent 1: Fetch high priority sources  │
│                                             │
│  When change detected:                     │
│    → Trigger Agents 2-8 pipeline          │
│    → Send alerts                           │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  REDIS EVENT BUS                           │
│  • Pub/Sub for agent communication         │
│  • Event queue for reliability             │
│  • Persistent storage                      │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  AGENT PIPELINE                            │
│  1 → 2 → 3 → 4 → 5 → 6 → 7 → 8           │
│  Processes every fetched change            │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  ALERTS & NOTIFICATIONS                    │
│  • WebSocket: Real-time UI updates         │
│  • Slack: Team notifications               │
│  • Email: Compliance team alerts           │
└─────────────────────────────────────────────┘
```

---

## 📋 Real-Time Setup Steps

### Step 1: API Key Configuration

Create `.env` file:
```bash
cd /Users/priyeshsrivastava/Seraphs
cp .env.example .env
```

Edit `.env`:
```bash
# YOUR Gemini API Key (you provided)
GOOGLE_API_KEY=AIzaSyBW_QmbdaMZn-IPTISNTYpPcSYYeYOM4kM

# Set Gemini as primary
LLM_PRIMARY_PROVIDER=gemini
LLM_PRIMARY_MODEL=gemini-1.5-pro

# For production (later)
REDIS_HOST=localhost
POSTGRES_HOST=localhost
BLOCKFROST_API_KEY=your_key_here
```

### Step 2: Install Dependencies

```bash
# Core dependencies
pip install google-generativeai  # Gemini
pip install apscheduler redis python-dotenv pyyaml

# Optional for production
pip install anthropic openai  # Fallback LLMs
pip install neo4j sentry-sdk
```

### Step 3: Start Scheduler

```bash
# Start 24/7 monitoring
python utils/scheduler.py

# Or run as background service
nohup python utils/scheduler.py > scheduler.log 2>&1 &
```

**This runs continuously**, fetching:
- Critical sources: Every 6 hours (RBI, SEBI, SEC)
- High priority: Daily at 9 AM
- Weekly sources: Monday 9 AM

### Step 4: Monitor Logs

```bash
# Watch real-time activity
tail -f scheduler.log

# You'll see:
[SCHEDULER] Fetching critical sources @ 2024-11-29 06:00:00
  Fetching: Reserve Bank of India
  Fetching: SEBI
  ... (automatic processing)
[AGENT-1] 3 new snapshots
[AGENT-2] Verification complete
[AGENT-3] 2 changes detected
[AGENT-4] 2 obligations extracted
[AGENT-5] MAAD debate: 2 verified
[AGENT-6] Graph updated

# Repeat every 6 hours, 24/7
```

---

## ⚙️ Production Deployment for 24/7

### Option A: Docker Compose (Recommended)

```yaml
# docker-compose.yml
version: '3.8'

services:
  seraphs:
    build: .
    env_file: .env
    volumes:
      - ./data:/app/data
    restart: always  # Auto-restart on failure
    
  redis:
    image: redis:7
    restart: always
    
  postgres:
    image: postgres:15
    env_file: .env
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

volumes:
  postgres_data:
```

Start:
```bash
docker-compose up -d  # Runs in background 24/7
```

### Option B: Systemd Service (Linux)

```ini
# /etc/systemd/system/seraphs.service
[Unit]
Description=Seraphs 2.0 Compliance Monitoring
After=network.target

[Service]
Type=simple
User=seraphs
WorkingDirectory=/opt/seraphs
ExecStart=/usr/bin/python3 utils/scheduler.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable seraphs
sudo systemctl start seraphs
sudo systemctl status seraphs  # Check running
```

### Option C: Cloud Deployment

**AWS/GCP/Azure**:
1. Deploy as containerized service
2. Use managed Redis/PostgreSQL
3. Enable auto-scaling
4. Set up monitoring

---

## 🔔 Real-Time Alerts Setup

### Slack Integration:

```python
# In utils/alerts.py
import requests

def send_slack_alert(message: str):
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    requests.post(webhook_url, json={"text": message})

# When new obligation detected:
send_slack_alert(f"🚨 New Obligation: {obligation['summary']}")
```

### Email Alerts:

```python
import smtplib

def send_email_alert(subject: str, body: str):
    # Send to compliance team
    # Triggered for CRITICAL obligations
```

### WebSocket Real-Time:

```python
# Agent 10 (UI) will have:
@app.websocket("/ws/compliance")
async def websocket_endpoint(websocket):
    # Push updates to browser in real-time
    await websocket.send_json(new_obligation)
```

---

## 📊 Monitoring Dashboard

### Agent 11 (AgentOps) provides:

**Grafana Dashboards**:
- Sources fetched/hour
- Obligations detected/day
- LLM costs/month
- Pipeline latency
- Error rates

**Alerts**:
- Pipeline failures
- High-priority obligations
- Cost thresholds exceeded

---

## ✅ Complete Setup Checklist

### Before 24/7 Deployment:

- [ ] Complete agents 9-12 (this week)
- [ ] Configure `.env` with your Gemini API key
- [ ] Install all dependencies
- [ ] Test scheduler manually
- [ ] Set up infrastructure (Redis, PostgreSQL)
- [ ] Configure alerts (Slack/Email)
- [ ] Test end-to-end pipeline
- [ ] Deploy to production server
- [ ] Enable systemd/Docker auto-restart
- [ ] Set up monitoring dashboard

### After Deployment:

- [ ] Verify scheduler running (check logs)
- [ ] Test alert notifications
- [ ] Monitor costs (Gemini API usage)
- [ ] Add more sources as needed
- [ ] Scale infrastructure if needed

---

## 💰 Cost for 24/7 Operation

### Monthly Costs:

| Component | Cost |
|-----------|------|
| **Gemini API** | ~$5-10 (80% cheaper than Claude) |
| **Infrastructure** | ~$50 (Redis, PostgreSQL, server) |
| **Cardano** | ~$3 (daily anchoring) |
| **Total** | **~$60/month** |

**vs Manual**: $10,000+/month (99.4% savings)

---

## 🚀 Launch Timeline

### This Week:
- Day 1-2: Complete agents 9-12
- Day 3: Integration testing
- Day 4: Set up infrastructure
- Day 5: Deploy to production

### Go Live:
**After agents 9-12 complete**, system runs 24/7 automatically!

---

## ✅ Yes, Deploy After All Agents Complete!

**Your approach is CORRECT**:
1. ✅ Finish agents 9-12 first
2. ✅ Test everything locally
3. ✅ Then deploy for 24/7 operation

**This ensures**:
- Complete functionality
- No missing features
- Stable 24/7 operation
- Full monitoring

---

## 🎯 Next Steps

1. **I'll complete agents 9-12 now** (2-3 days of work)
2. **You configure your Gemini API key** in `.env`
3. **We test the complete system**
4. **Deploy for 24/7 monitoring**

**System will then run automatically 24/7, monitoring 20 regulatory sources!** 🚀

Ready to complete agents 9-12?
