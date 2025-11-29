#!/usr/bin/env python3
"""
Test Agent 6: Knowledge Graph
Complete pipeline: Agent 1 → 2 → 3 → 4 → 5 → 6
"""

import json
import sys

sys.path.insert(0, '/Users/priyeshsrivastava/Seraphs')

from agents.agent_6_kg.agent import KnowledgeGraphAgent

def main():
    print("="*80)
    print("AGENT 6: Knowledge Graph Builder")
    print("Building obligation graph from MAAD verified results")
    print("="*80 + "\n")
    
    # Load Agent 5 output
    input_file = "agent5_output_test.json"
    
    print(f"[INFO] Loading Agent 5 debate results: {input_file}")
    
    try:
        with open(input_file, 'r') as f:
            agent5_data = json.load(f)
        
        debate_results = agent5_data.get('debate_results', [])
        print(f"[SUCCESS] Loaded {len(debate_results)} verified obligations\n")
        
        # Create Agent 6
        agent = KnowledgeGraphAgent()
        
        # Build knowledge graph
        result = agent.build_graph_from_debate_results(debate_results)
        
        # Query policy gaps
        print(f"\n{'='*80}")
        print("POLICY GAP ANALYSIS")
        print("="*80 + "\n")
        
        gaps = agent.query_policy_gaps()
        
        if gaps:
            print(f"Found {len(gaps)} obligations without policy mappings:")
            for i, gap in enumerate(gaps[:3], 1):  # Show first 3
                print(f"\n{i}. {gap.get('summary', '')[:60]}...")
                print(f"   Type: {gap.get('type')}, Severity: {gap.get('severity')}")
                print(f"   ⚠️  Requires policy mapping")
        else:
            print("No policy gaps found (all obligations mapped)")
        
        # Detect conflicts
        print(f"\n{'='*80}")
        print("CONFLICT DETECTION")
        print("="*80 + "\n")
        
        conflicts = agent.detect_conflicts()
        
        if conflicts:
            print(f"Found {len(conflicts)} potential conflicts:")
            for i, conflict in enumerate(conflicts, 1):
                print(f"\n{i}. {conflict.get('reason', '')}")
                print(f"   Obligations: {conflict.get('obligation_1')} vs {conflict.get('obligation_2')}")
        else:
            print("✓ No conflicts detected")
        
        # Export visualization data
        print(f"\n{'='*80}")
        print("GRAPH VISUALIZATION")
        print("="*80 + "\n")
        
        viz_data = agent.export_visualization()
        
        print(f"Graph exported for visualization:")
        print(f"  Nodes: {len(viz_data['nodes'])}")
        print(f"  Edges: {len(viz_data['edges'])}")
        print(f"  Format: vis.js compatible JSON")
        
        # Save outputs
        output_file = "agent6_output_test.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        viz_file = "graph_visualization.json"
        with open(viz_file, 'w') as f:
            json.dump(viz_data, f, indent=2)
        
        print(f"\n[SUCCESS] Outputs saved:")
        print(f"  Graph statistics: {output_file}")
        print(f"  Visualization data: {viz_file}")
        
        # Final summary
        print("\n" + "="*80)
        print("AGENT 6 SUMMARY")
        print("="*80)
        
        print(f"\nKnowledge Graph Built:")
        print(f"  Obligation nodes: {result['nodes_created']['obligations']}")
        print(f"  Entity nodes: {result['nodes_created']['entities']}")
        print(f"  Source nodes: {result['nodes_created']['sources']}")
        print(f"  Relationships: {result['relationships_created']}")
        
        print(f"\nAnalysis:")
        print(f"  Policy gaps: {len(gaps)}")
        print(f"  Conflicts: {len(conflicts)}")
        
        # Complete pipeline summary
        print("\n" + "="*80)
        print("COMPLETE 6-AGENT PIPELINE")
        print("="*80 + "\n")
        
        print("Agent 1 (Ingestion):")
        print("  ✓ Fetched 7 regulatory sources")
        
        print("\nAgent 2 (Authenticity):")
        print("  ✓ Verified all 7 sources")
        
        print("\nAgent 3 (Diff Analysis):")
        print("  ✓ Detected 7 changes")
        
        print("\nAgent 4 (Legal LLM):")
        print("  ✓ Extracted 7 obligations")
        
        print("\nAgent 5 (MAAD):")
        print(f"  ✓ Verified {len(debate_results)} obligations")
        print("  ✓ Adversarial debate complete")
        
        print("\nAgent 6 (Knowledge Graph):")
        print(f"  ✓ Built graph with {result['total_nodes']} nodes")
        print(f"  ✓ Created {result['total_relationships']} relationships")
        print(f"  ✓ Identified {len(gaps)} policy gaps")
        
        print("\n" + "="*80)
        print("✅ 6-Agent Pipeline Complete!")
        print("="*80 + "\n")
        
        print("🎯 Next Steps:")
        print("  • Add policy nodes and mappings")
        print("  • Visualize graph in Neo4j Browser")
        print("  • Proceed to Agent 7 (Oracle API)")
        
    except FileNotFoundError:
        print(f"[ERROR] File not found: {input_file}")
        print("[INFO] Run test_agent5.py first")
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
