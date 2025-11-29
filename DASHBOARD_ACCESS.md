# SERAPHS 2.0 - Dashboard Access Guide

## 🎯 Quick Access

**Dashboard URL**: http://localhost:5000

---

## ✅ Current Status

Dashboard Process: Running (PID 6491)
Port: 5000
Auto-refresh: Every 5 seconds

---

## 🚀 How to Start Dashboard

### Option 1: Simple Launch Script
```bash
cd /Users/priyeshsrivastava/Seraphs
./launch_dashboard.sh
```

### Option 2: Manual Start
```bash
cd /Users/priyeshsrivastava/Seraphs
python3 dashboard.py
```

Then open: http://localhost:5000

---

## 🔍 Check if Running

```bash
# Check process
ps aux | grep dashboard

# Check port
lsof -i :5000

# Test connection
curl http://localhost:5000
```

---

## 🛑 Stop Dashboard

```bash
# Kill by name
pkill -f dashboard.py

# Or by PID
kill 6491
```

---

## 📊 Dashboard Features

- Shows all 12 agents status
- Real-time system metrics
- Auto-refreshes every 5 seconds
- Beautiful gradient UI
- Mobile responsive

---

## 🆘 Troubleshooting

**Can't connect?**
1. Check if Flask installed: `pip3 list | grep -i flask`
2. Install if needed: `pip3 install flask`
3. Restart: `./launch_dashboard.sh`

**Port already in use?**
```bash
# Find what's using port 5000
lsof -i :5000

# Kill it
kill -9 <PID>

# Restart dashboard
./launch_dashboard.sh
```

**Still not working?**
```bash
# Check logs
tail -f dashboard.log

# Try different port (edit dashboard.py, change 5000 to 8080)
```

---

## 📝 Access Log Location

Dashboard logs: `dashboard.log`
Monitoring logs: `monitoring.log`

---

**Dashboard should now be accessible at http://localhost:5000** 

Try opening in Chrome/Firefox instead of Safari if issues persist.
