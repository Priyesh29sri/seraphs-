#!/usr/bin/env python3
"""
Live Demo Runner - Continuously fetches and processes regulatory data
Shows all 12 agents working in real-time
"""

import sys
import time
import json
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("="*80)
print("SERAPHS 2.0 - LIVE CONTINUOUS MONITORING")
print("="*80)
print("\nStarting continuous regulatory monitoring...")
print("Press Ctrl+C to stop\n")

iteration = 0

try:
    while True:
        iteration += 1
        print(f"\n{'='*80}")
        print(f"ITERATION {iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        # Agent 1: Fetch data
        print("▶ Agent 1: Fetching regulatory sources...")
        from agents.agent_1_ingestion.agent import IngestionAgent
        agent1 = IngestionAgent()
        
        # Fetch from a few sources
        sources_to_fetch = [
            {"name": "Reserve Bank of India", "url": "https://www.rbi.org.in"},
            {"name": "SEBI", "url": "https://www.sebi.gov.in"},
        ]
        
        snapshots = []
        for source in sources_to_fetch:
            try:
                result = agent1.fetch_source(source)
                snapshots.append(result)
                print(f"  ✓ Fetched: {source['name']} ({len(result.get('content', {}).get('extracted_text_preview', ''))} chars)")
            except Exception as e:
                print(f"  ✗ Error fetching {source['name']}: {e}")
        
        print(f"\n✓ Agent 1 Complete: {len(snapshots)} snapshots created\n")
        
        # Agent 2: Verify
        print("▶ Agent 2: Verifying authenticity...")
        from agents.agent_2_auth.agent import AuthAgent
        agent2 = AuthAgent()
        
        verified = []
        for snap in snapshots:
            result = agent2.verify_snapshot(snap)
            verified.append(result)
            print(f"  ✓ Verified: {snap['source']['name']} (confidence: {result.get('confidence', 0):.2f})")
        
        print(f"\n✓ Agent 2 Complete: {len(verified)} verified\n")
        
        # Agent 3: Detect changes
        print("▶ Agent 3: Detecting changes...")
        from agents.agent_3_diff.agent import DiffAgent
        agent3 = DiffAgent()
        
        changes = []
        for v in verified:
            result = agent3.detect_changes(v)
            if result.get('change_detected'):
                changes.append(result)
                print(f"  ✓ Change detected: {result.get('change_type')} (severity: {result.get('severity')})")
        
        if not changes:
            print("  ℹ No changes detected (all sources unchanged)")
            changes = verified  # Use verified data for demo
        
        print(f"\n✓ Agent 3 Complete: {len(changes)} changes analyzed\n")
        
        # Agent 4: Extract obligations
        print("▶ Agent 4: Extracting obligations (Gemini LLM)...")
        from agents.agent_4_legal.agent import LegalAgent
        agent4 = LegalAgent()
        
        obligations = []
        for change in changes[:2]:  # Process first 2 for demo
            result = agent4.extract_obligations(change)
            obligations.extend(result.get('obligations', []))
            print(f"  ✓ Extracted {len(result.get('obligations', []))} obligations")
        
        print(f"\n✓ Agent 4 Complete: {len(obligations)} total obligations\n")
        
        # Agent 5: MAAD verification
        print("▶ Agent 5: MAAD Adversarial Debate...")
        from agents.agent_5_maad.agent import MAADAgent
        agent5 = MAADAgent()
        
        verified_obligations = []
        for obl in obligations[:2]:  # Verify first 2
            result = agent5.verify_obligation(obl)
            verified_obligations.append(result)
            print(f"  ⚖️ Verdict: {result.get('verdict')} (confidence: {result.get('final_confidence', 0):.2f})")
        
        print(f"\n✓ Agent 5 Complete: {len(verified_obligations)} verified\n")
        
        # Agent 6: Build knowledge graph
        print("▶ Agent 6: Building knowledge graph...")
        from agents.agent_6_kg.agent import KnowledgeGraphAgent
        agent6 = KnowledgeGraphAgent()
        
        graph_result = agent6.build_graph(verified_obligations)
        print(f"  ✓ Nodes: {graph_result.get('nodes_created', 0)}")
        print(f"  ✓ Relationships: {graph_result.get('relationships_created', 0)}")
        print(f"  ✓ Policy gaps: {len(graph_result.get('policy_gaps', []))}")
        print(f"  ✓ Conflicts: {len(graph_result.get('conflicts', []))}")
        
        print(f"\n✓ Agent 6 Complete: Graph updated\n")
        
        # Save results
        output = {
            "iteration": iteration,
            "timestamp": datetime.now().isoformat(),
            "snapshots": len(snapshots),
            "verified": len(verified),
            "changes": len(changes),
            "obligations": len(obligations),
            "verified_obligations": len(verified_obligations),
            "graph": graph_result,
            "sample_obligation": obligations[0] if obligations else None
        }
        
        with open('live_monitoring_output.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"{'='*80}")
        print(f"✅ ITERATION {iteration} COMPLETE")
        print(f"{'='*80}")
        print(f"\nResults saved to: live_monitoring_output.json")
        print(f"Next iteration in 30 seconds...")
        print(f"Dashboard will auto-refresh to show latest data\n")
        
        # Wait before next iteration
        time.sleep(30)
        
except KeyboardInterrupt:
    print("\n\n⏹ Monitoring stopped by user")
    print(f"Completed {iteration} iterations")
    print("\n✅ System ready for next run\n")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
