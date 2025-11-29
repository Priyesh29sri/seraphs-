"""
Agent 6: Knowledge Graph
Main agent for building and querying obligation graph.
"""

import json
from datetime import datetime
from typing import Dict, List
from agents.agent_6_kg import tools


class KnowledgeGraphAgent:
    """
    Agent 6: Knowledge Graph Builder
    
    Builds Neo4j graph from verified obligations, creating nodes and relationships
    for obligations, entities, policies, and sources.
    """
    
    def __init__(self):
        self.graph = tools.get_graph()
        print("[INFO] Agent 6 initialized (Knowledge Graph)")
        print("  Graph: Neo4j (simulated for demo)")
    
    def build_graph_from_debate_results(self, debate_results: List[Dict]) -> Dict:
        """
        Build knowledge graph from Agent 5 MAAD debate results.
        
        Args:
            debate_results: List of verified obligations from Agent 5
            
        Returns:
            Graph building result with statistics
        """
        print(f"\n{'='*80}")
        print(f"AGENT 6: Building Knowledge Graph")
        print(f"{'='*80}\n")
        
        print(f"[INFO] Processing {len(debate_results)} verified obligations")
        
        nodes_created = {
            "obligations": 0,
            "entities": 0,
            "sources": 0,
            "policies": 0
        }
        
        relationships_created = 0
        
        # Track created nodes to avoid duplicates
        created_sources = {}
        created_entities = {}
        
        for result in debate_results:
            try:
                # Get verified obligation
                verified_obl = result.get('verified_obligation', {})
                original_obl = result.get('original_obligation', {})
                
                # Use verified if available, fallback to original
                obligation = verified_obl if verified_obl else original_obl
                
                if not obligation:
                    continue
                
                # 1. Create Obligation node
                obl_node_id = tools.create_obligation_node(obligation)
                nodes_created["obligations"] += 1
                
                # 2. Extract and create Entity nodes
                affected_entities = obligation.get('affected_entities', [])
                if not affected_entities:
                    # Default entities based on obligation type
                    if obligation.get('type') in ['KYC', 'capital', 'reporting']:
                        affected_entities = ['Commercial Banks', 'NBFCs']
                
                for entity_name in affected_entities:
                    # Create entity if not exists
                    if entity_name not in created_entities:
                        entity_node_id = tools.create_entity_node(
                            entity_name,
                            entity_type="Financial Institution",
                            jurisdiction="India"
                        )
                        created_entities[entity_name] = entity_node_id
                        nodes_created["entities"] += 1
                    else:
                        entity_node_id = created_entities[entity_name]
                    
                    # Link: Obligation -[:AFFECTS]-> Entity
                    tools.link_obligation_to_entity(obl_node_id, entity_node_id)
                    relationships_created += 1
                
                # 3. Create Source node (if from Agent 5, extract source info)
                source_name = "Unknown Source"  # Would come from original snapshot
                
                if source_name not in created_sources:
                    source_node_id = tools.create_source_node({
                        "name": source_name,
                        "id": "src_demo",
                        "url": "https://example.com",
                        "authority": "regulatory_body",
                        "jurisdiction": "India"
                    })
                    created_sources[source_name] = source_node_id
                    nodes_created["sources"] += 1
                else:
                    source_node_id = created_sources[source_name]
                
                # Link: Obligation -[:FROM]-> Source
                tools.link_obligation_to_source(obl_node_id, source_node_id)
                relationships_created += 1
                
            except Exception as e:
                print(f"[ERROR] Failed to process obligation: {e}")
                continue
        
        # Get final statistics
        stats = tools.get_graph_statistics()
        
        result = {
            "agent": "agent-6-kg",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "nodes_created": nodes_created,
            "total_nodes": stats.get("nodes", 0),
            "relationships_created": relationships_created,
            "total_relationships": stats.get("relationships", 0),
            "graph_statistics": stats
        }
        
        print(f"\n[SUCCESS] Knowledge Graph built:")
        print(f"  Nodes created: {sum(nodes_created.values())}")
        print(f"  Relationships created: {relationships_created}")
        print(f"  Total nodes: {stats.get('nodes', 0)}")
        print(f"  Total relationships: {stats.get('relationships', 0)}")
        
        return result
    
    def query_policy_gaps(self) -> List[Dict]:
        """
        Find obligations without policy mappings.
        
        Returns:
            List of obligations requiring policy mapping
        """
        print(f"\n[KG] Querying policy gaps...")
        
        # Get all obligation nodes
        obligations = [n for n in self.graph.nodes if "Obligation" in n["labels"]]
        
        # Filter those without MAPPED_TO relationships
        gaps = []
        for obl_node in obligations:
            has_policy_mapping = any(
                rel["from"] == obl_node["id"] and rel["type"] == "MAPPED_TO"
                for rel in self.graph.relationships
            )
            
            if not has_policy_mapping:
                gaps.append(obl_node["properties"])
        
        print(f"[KG] Found {len(gaps)} obligations without policy mappings")
        
        return gaps
    
    def detect_conflicts(self) -> List[Dict]:
        """
        Find conflicting obligations.
        """
        return tools.detect_conflicts()
    
    def export_visualization(self) -> Dict:
        """
        Export graph for visualization.
        """
        return tools.export_subgraph("Obligation")
