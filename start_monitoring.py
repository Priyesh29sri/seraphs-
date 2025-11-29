#!/usr/bin/env python3
"""
Start 24/7 Compliance Monitoring
Runs continuously in background
"""

import sys
import os
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment
from dotenv import load_dotenv
load_dotenv()

print("="*80)
print("SERAPHS 2.0 - 24/7 MONITORING STARTING")
print("="*80 + "\n")

# Verify Gemini API
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("❌ ERROR: GOOGLE_API_KEY not found in .env")
    print("Run: python deploy.py first")
    sys.exit(1)

print(f"✅ Gemini API: Configured")
print(f"✅ Model: {os.getenv('LLM_PRIMARY_MODEL', 'gemini-2.0-flash-exp')}")
print(f"✅ Environment: {os.getenv('ENVIRONMENT', 'production')}")
print(f"✅ Timezone: {os.getenv('SCHEDULER_TIMEZONE', 'Asia/Kolkata')}\n")

# Import scheduler
try:
    from utils.scheduler import ComplianceScheduler
    
    # Create and start scheduler
    scheduler = ComplianceScheduler()
    scheduler.setup_jobs()
    scheduler.start()
    
    print("="*80)
    print("✅ SCHEDULER RUNNING - 24/7 MONITORING ACTIVE")
    print("="*80 + "\n")
    
    print("Monitoring Schedule:")
    print("  • Every 6 hours: Critical sources (RBI, SEBI, SEC)")
    print("  • Daily 9 AM: High priority sources")
    print("  • Weekly Monday: Standard sources")
    print("  • Daily 11 PM: Blockchain anchoring\n")
    
    print("Press Ctrl+C to stop\n")
    
    # Keep running
    import time
    while True:
        time.sleep(60)
        
except KeyboardInterrupt:
    print("\n\n Stopping scheduler...")
    print("✅ Shutdown complete\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
