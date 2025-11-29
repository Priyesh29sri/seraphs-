#!/bin/bash
# Quick Dashboard Launcher

echo "=========================================="
echo "SERAPHS 2.0 - DASHBOARD LAUNCHER"
echo "=========================================="
echo ""

# Kill any existing dashboard
pkill -f dashboard.py 2>/dev/null

echo "Starting dashboard..."
cd /Users/priyeshsrivastava/Seraphs

# Start dashboard
python3 dashboard.py > dashboard.log 2>&1 &
DASHBOARD_PID=$!

echo "✅ Dashboard started (PID: $DASHBOARD_PID)"
echo ""
echo "Access at: http://localhost:5000"
echo ""
echo "To stop: kill $DASHBOARD_PID"
echo "Or run: pkill -f dashboard.py"
echo ""
echo "Logs: tail -f dashboard.log"
echo ""

# Wait and check
sleep 2
if curl -s http://localhost:5000 > /dev/null 2>&1; then
    echo "✅ Dashboard is running!"
    echo ""
    echo "Open in browser: http://localhost:5000"
else
    echo "⚠️  Dashboard may still be starting..."
    echo "   Wait 5 seconds and try: http://localhost:5000"
fi

echo ""
echo "=========================================="
