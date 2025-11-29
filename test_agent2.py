#!/usr/bin/env python3
"""
Test Agent 2: Authenticity & Oracle
Processes Agent 1 output and adds cryptographic verification
"""

import json
import sys

# Add parent to path
sys.path.insert(0, '/Users/priyeshsrivastava/Seraphs')

from agents.agent_2_auth.agent import AuthenticityAgent

def main():
    print("="*80)
    print("AGENT 2: Authenticity & Oracle - Test")
    print("Processing Agent 1 Output")
    print("="*80 + "\n")
    
    #Load Agent 1 output
    input_file = "agent1_output_20251129_052819.json"
    
    print(f"[INFO] Loading Agent 1 output: {input_file}")
    
    try:
        with open(input_file, 'r') as f:
            agent1_data = json.load(f)
        
        print(f"[SUCCESS] Loaded {agent1_data['total_snapshots']} snapshots\n")
        
        # Create Agent 2
        agent = AuthenticityAgent(consensus_threshold=0.6)
        
        # Verify all snapshots
        print("[INFO] Starting verification...\n")
        result = agent.verify_batch(agent1_data["snapshots"])
        
        # Print summary
        print("\n" + "="*80)
        print("AGENT 2 OUTPUT")
        print("="*80)
        print(f"Total Snapshots: {result['total_snapshots']}")
        print(f"Verified: {result['verified_count']}")
        print(f"Require HITL: {result['hitl_count']}")
        print(f"Merkle Root: {result['merkle_root'][:32]}...")
        print(f"IPFS Proof CID: {result['ipfs_proof_cid']}")
        
        # Show sample verification
        if result['verifications']:
            print("\n" + "="*80)
            print("SAMPLE VERIFICATION (First Snapshot)")
            print("="*80 + "\n")
            sample = result['verifications'][0]
            print(json.dumps(sample, indent=2))
        
        # Save output
        output_file = f"agent2_output_test.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"\n[SUCCESS] Full output saved to: {output_file}")
        
        print("\n" + "="*80)
        print("Agent 2 Complete - Ready for Agent 3 (Diff Analysis)")
        print("="*80 + "\n")
        
    except FileNotFoundError:
        print(f"[ERROR] File not found: {input_file}")
        print("[INFO] Run test_agent1_complete.py first to generate Agent 1 output")
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
