"""
Real-time scheduling for automated regulatory monitoring.
Uses APScheduler for cron-style scheduling.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import asyncio
import yaml
from pathlib import Path


class ComplianceScheduler:
    """
    Automated scheduler for regulatory fetching.
    
    Features:
    - Critical sources: Every 6 hours
    - High priority: Daily at 9 AM
    - Medium/weekly: Weekly on Monday
    - Blockchain anchoring: Daily at 11 PM
    """
    
    def __init__(self, config_path: str = "config/sources.yaml"):
        self.scheduler = AsyncIOScheduler()
        self.config_path = config_path
        self.sources = self._load_sources()
        
        # Organize by frequency
        self.critical_sources = [s for s in self.sources if s.get('priority') == 'critical']
        self.daily_sources = [s for s in self.sources if s.get('frequency') == 'daily']
        self.weekly_sources = [s for s in self.sources if s.get('frequency') == 'weekly']
        
        print(f"[INFO] Scheduler initialized")
        print(f"  Critical sources (6h): {len(self.critical_sources)}")
        print(f"  Daily sources: {len(self.daily_sources)}")
        print(f"  Weekly sources: {len(self.weekly_sources)}")
    
    def _load_sources(self):
        """Load sources from YAML config"""
        config_file = Path(self.config_path)
        
        if not config_file.exists():
            print(f"[WARNING] Config not found: {self.config_path}")
            return []
        
        with open(config_file) as f:
            config = yaml.safe_load(f)
        
        return config.get('sources', [])
    
    def setup_jobs(self):
        """Set up all scheduled jobs"""
        
        # Critical sources: Every 6 hours (0, 6, 12, 18)
        self.scheduler.add_job(
            self.fetch_critical_sources,
            CronTrigger(hour='0,6,12,18', minute=0),
            id='fetch_critical',
            name='Fetch Critical Sources (RBI, SEBI, SEC)',
            replace_existing=True
        )
        
        # Daily sources: 9 AM UTC
        self.scheduler.add_job(
            self.fetch_daily_sources,
            CronTrigger(hour=9, minute=0),
            id='fetch_daily',
            name='Fetch Daily Sources',
            replace_existing=True
        )
        
        # Weekly sources: Monday 9 AM
        self.scheduler.add_job(
            self.fetch_weekly_sources,
            CronTrigger(day_of_week='mon', hour=9, minute=0),
            id='fetch_weekly',
            name='Fetch Weekly Sources',
            replace_existing=True
        )
        
        # Blockchain anchoring: Daily at 11 PM
        self.scheduler.add_job(
            self.daily_blockchain_anchor,
            CronTrigger(hour=23, minute=0),
            id='blockchain_anchor',
            name='Daily Cardano Anchoring',
            replace_existing=True
        )
        
        print(f"[SUCCESS] {len(self.scheduler.get_jobs())} jobs scheduled")
    
    async def fetch_critical_sources(self):
        """Fetch critical priority sources (every 6 hours)"""
        print(f"\n[SCHEDULER] Fetching critical sources @ {datetime.now()}")
        
        for source in self.critical_sources:
            try:
                print(f"  Fetching: {source['name']}")
                await self._run_agent_1(source)
            except Exception as e:
                print(f"  [ERROR] {source['id']}: {e}")
    
    async def fetch_daily_sources(self):
        """Fetch daily sources (9 AM)"""
        print(f"\n[SCHEDULER] Fetching daily sources @ {datetime.now()}")
        
        for source in self.daily_sources:
            try:
                print(f"  Fetching: {source['name']}")
                await self._run_agent_1(source)
            except Exception as e:
                print(f"  [ERROR] {source['id']}: {e}")
    
    async def fetch_weekly_sources(self):
        """Fetch weekly sources (Monday)"""
        print(f"\n[SCHEDULER] Fetching weekly sources @ {datetime.now()}")
        
        for source in self.weekly_sources:
            try:
                print(f"  Fetching: {source['name']}")
                await self._run_agent_1(source)
            except Exception as e:
                print(f"  [ERROR] {source['id']}: {e}")
    
    async def daily_blockchain_anchor(self):
        """Anchor daily Merkle root to Cardano"""
        print(f"\n[SCHEDULER] Blockchain anchoring @ {datetime.now()}")
        
        try:
            # Compute daily Merkle root
            # merkle_root = compute_daily_merkle_root()
            
            # Anchor to Cardano
            # tx_hash = anchor_to_cardano(merkle_root)
            
            print(f"  [INFO] Blockchain anchoring placeholder")
            print(f"  [TODO] Integrate Cardano/Midnight anchoring")
        except Exception as e:
            print(f"  [ERROR] Anchoring failed: {e}")
    
    async def _run_agent_1(self, source: dict):
        """Run Agent 1 for a source (placeholder)"""
        # In production, import and run actual Agent 1
        print(f"    [PLACEHOLDER] Would fetch from {source['url']}")
        
        # TODO: Actual implementation
        # from agents.agent_1_ingestion.agent import IngestionAgent
        # agent = IngestionAgent()
        # snapshot = agent.fetch_source(source)
        # publish_event(snapshot)
    
    def start(self):
        """Start the scheduler"""
        self.setup_jobs()
        self.scheduler.start()
        print(f"\n[SUCCESS] Scheduler started - running in background")
        print(f"  Press Ctrl+C to stop\n")
    
    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()
        print(f"[INFO] Scheduler stopped")
    
    def list_jobs(self):
        """List all scheduled jobs"""
        jobs = self.scheduler.get_jobs()
        
        print(f"\n{'='*80}")
        print(f"SCHEDULED JOBS ({len(jobs)} total)")
        print(f"{'='*80}\n")
        
        for job in jobs:
            print(f"  {job.name}")
            print(f"    ID: {job.id}")
            print(f"    Next run: {job.next_run_time}")
            print()


# Standalone execution
if __name__ == "__main__":
    import sys
    
    scheduler = ComplianceScheduler()
    
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        # Just list jobs
        scheduler.setup_jobs()
        scheduler.list_jobs()
    else:
        # Run scheduler
        scheduler.start()
        
        try:
            # Keep running
            asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            print("\n[INFO] Shutting down...")
            scheduler.stop()
