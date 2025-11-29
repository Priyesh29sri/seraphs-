"""
Agent 6: Knowledge Graph
Tools for Neo4j graph database operations.
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional


# =============================================================================
# SIMULATED NEO4J (Demo Mode)
# Replace with real Neo4j driver in production: from neo4j import GraphDatabase
# =============================================================================

class SimulatedNeo4jGraph:
    """
    Simulated in-memory graph for demo.
    Replace with real Neo4j in production.
    """
    
    def __init__(self):
        self.nodes = []
        self.relationships = []
        print("[INFO] Using simulated Neo4j graph (in-memory)")
        print("[INFO] Install neo4j-driver for production: pip install neo4j")
    
    def create_node(self, labels: List[str], properties: Dict) -> str:
        """Create a node"""
        node_id = f"n{len(self.nodes)}"
        node = {
            "id": node_id,
            "labels": labels,
            "properties": properties
        }
        self.nodes.append(node)
        return node_id
    
    def create_relationship(self, from_id: str, to_id: str, rel_type: str, properties: Dict = None):
        """Create a relationship"""
        rel = {
            "from": from_id,
            "to": to_id,
            "type": rel_type,
            "properties": properties or {}
        }
        self.relationships.append(rel)
    
    def query(self, cypher: str, params: Dict = None) -> List[Dict]:
        """Execute Cypher query (simplified)"""
        # Simplified query execution for demo
        results = []
        
        if "MATCH" in cypher and "Obligation" in cypher:
            # Return obligations
            results = [n for n in self.nodes if "Obligation" in n["labels"]]
        elif "MATCH" in cypher and "Entity" in cypher:
            results = [n for n in self.nodes if "Entity" in n["labels"]]
        
        return results
    
    def get_stats(self) -> Dict:
        """Get graph statistics"""
        return {
            "nodes": len(self.nodes),
            "relationships": len(self.relationships),
            "node_types": list(set(label for node in self.nodes for label in node["labels"]))
        }


# Global graph instance
_graph = None

def get_graph() -> SimulatedNeo4jGraph:
    """Get singleton graph instance"""
    global _graph
    if _graph is None:
        _graph = SimulatedNeo4jGraph()
    return _graph


# =============================================================================
# KNOWLEDGE GRAPH TOOLS
# =============================================================================

def create_obligation_node(obligation: Dict) -> str:
    """
    Create Obligation node in graph.
    
    Args:
        obligation: Verified obligation from Agent 5
        
    Returns:
        Node ID
    """
    graph = get_graph()
    
    properties = {
        "obligation_id": obligation.get("obligation_id"),
        "text": obligation.get("text", ""),
        "summary": obligation.get("summary", ""),
        "type": obligation.get("type", ""),
        "severity": obligation.get("severity", ""),
        "confidence": obligation.get("confidence", 0),
        "deadline": obligation.get("deadline", "not specified"),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    node_id = graph.create_node(["Obligation"], properties)
    
    print(f"[KG] Created Obligation node: {node_id}")
    print(f"     Type: {properties['type']}, Severity: {properties['severity']}")
    
    return node_id


def create_entity_node(entity_name: str, entity_type: str, jurisdiction: str = "India") -> str:
    """
    Create Entity node (e.g., Commercial Bank, NBFC).
    
    Args:
        entity_name: Name of entity
        entity_type: Type (Commercial Bank, NBFC, etc.)
        jurisdiction: Geographic jurisdiction
        
    Returns:
        Node ID
    """
    graph = get_graph()
    
    properties = {
        "name": entity_name,
        "type": entity_type,
        "jurisdiction": jurisdiction,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    node_id = graph.create_node(["Entity"], properties)
    
    print(f"[KG] Created Entity node: {node_id} ({entity_name})")
    
    return node_id


def create_policy_node(policy_name: str, version: str, owner: str) -> str:
    """
    Create Policy node (internal company policy).
    
    Args:
        policy_name: Policy title
        version: Version number
        owner: Policy owner/department
        
    Returns:
        Node ID
    """
    graph = get_graph()
    
    properties = {
        "name": policy_name,
        "version": version,
        "owner": owner,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    node_id = graph.create_node(["Policy"], properties)
    
    print(f"[KG] Created Policy node: {node_id} ({policy_name} v{version})")
    
    return node_id


def create_source_node(source: Dict) -> str:
    """
    Create Source node (regulatory body).
    
    Args:
        source: Source metadata from config
        
    Returns:
        Node ID
    """
    graph = get_graph()
    
    properties = {
        "name": source.get("name", ""),
        "source_id": source.get("id", ""),
        "url": source.get("url", ""),
        "authority": source.get("authority", ""),
        "jurisdiction": source.get("jurisdiction", ""),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    node_id = graph.create_node(["Source"], properties)
    
    print(f"[KG] Created Source node: {node_id} ({properties['name']})")
    
    return node_id


def link_obligation_to_policy(obligation_id: str, policy_id: str, mapping_type: str = "IMPLEMENTS") -> None:
    """
    Create relationship: Obligation -> Policy.
    
    Args:
        obligation_id: Obligation node ID
        policy_id: Policy node ID
        mapping_type: Relationship type (IMPLEMENTS, CONFLICTS_WITH, etc.)
    """
    graph = get_graph()
    
    graph.create_relationship(
        obligation_id,
        policy_id,
        "MAPPED_TO",
        {"mapping_type": mapping_type, "created_at": datetime.utcnow().isoformat() + "Z"}
    )
    
    print(f"[KG] Linked: {obligation_id} -[MAPPED_TO]-> {policy_id}")


def link_obligation_to_entity(obligation_id: str, entity_id: str) -> None:
    """
    Create relationship: Obligation -> Entity.
    
    Args:
        obligation_id: Obligation node ID
        entity_id: Entity node ID
    """
    graph = get_graph()
    
    graph.create_relationship(
        obligation_id,
        entity_id,
        "AFFECTS",
        {"created_at": datetime.utcnow().isoformat() + "Z"}
    )
    
    print(f"[KG] Linked: {obligation_id} -[AFFECTS]-> {entity_id}")


def link_obligation_to_source(obligation_id: str, source_id: str) -> None:
    """
    Create relationship: Obligation -> Source.
    
    Args:
        obligation_id: Obligation node ID
        source_id: Source node ID
    """
    graph = get_graph()
    
    graph.create_relationship(
        obligation_id,
        source_id,
        "FROM",
        {"created_at": datetime.utcnow().isoformat() + "Z"}
    )
    
    print(f"[KG] Linked: {obligation_id} -[FROM]-> {source_id}")


def query_related_obligations(obligation_id: str, relationship_type: str = None) -> List[Dict]:
    """
    Find obligations related to given obligation.
    
    Args:
        obligation_id: Starting obligation
        relationship_type: Filter by relationship (RELATES_TO, CONFLICTS_WITH, etc.)
        
    Returns:
        List of related obligations
    """
    graph = get_graph()
    
    # Simplified query for demo
    related = []
    
    for rel in graph.relationships:
        if rel["from"] == obligation_id:
            if relationship_type is None or rel["type"] == relationship_type:
                # Find target node
                target = next((n for n in graph.nodes if n["id"] == rel["to"]), None)
                if target:
                    related.append(target)
    
    print(f"[KG] Found {len(related)} related obligations for {obligation_id}")
    
    return related


def detect_conflicts() -> List[Dict]:
    """
    Detect conflicting obligations in graph.
    
    Returns:
        List of conflict pairs
    """
    graph = get_graph()
    
    conflicts = []
    
    # Simplified conflict detection
    # In production: Use Cypher query to find contradictory obligations
    
    obligations = [n for n in graph.nodes if "Obligation" in n["labels"]]
    
    for i, obl1 in enumerate(obligations):
        for obl2 in obligations[i+1:]:
            # Check if same type but different requirements
            if (obl1["properties"].get("type") == obl2["properties"].get("type") and
                obl1["properties"].get("text") != obl2["properties"].get("text")):
                
                conflicts.append({
                    "obligation_1": obl1["properties"]["obligation_id"],
                    "obligation_2": obl2["properties"]["obligation_id"],
                    "type": "potential_conflict",
                    "reason": f"Different requirements for same type: {obl1['properties']['type']}"
                })
    
    print(f"[KG] Detected {len(conflicts)} potential conflicts")
    
    return conflicts


def export_subgraph(node_type: str = "Obligation") -> Dict:
    """
    Export subgraph for visualization.
    
    Args:
        node_type: Type of nodes to export
        
    Returns:
        Graph data in JSON format for vis.js
    """
    graph = get_graph()
    
    nodes = [n for n in graph.nodes if node_type in n["labels"]]
    
    # Get relationships involving these nodes
    node_ids = {n["id"] for n in nodes}
    edges = [r for r in graph.relationships if r["from"] in node_ids or r["to"] in node_ids]
    
    export_data = {
        "nodes": [
            {
                "id": n["id"],
                "label": n["properties"].get("summary", n["properties"].get("name", ""))[:50],
                "type": n["labels"][0],
                "properties": n["properties"]
            }
            for n in nodes
        ],
        "edges": [
            {
                "from": e["from"],
                "to": e["to"],
                "label": e["type"],
                "properties": e["properties"]
            }
            for e in edges
        ]
    }
    
    print(f"[KG] Exported subgraph: {len(export_data['nodes'])} nodes, {len(export_data['edges'])} edges")
    
    return export_data


def get_graph_statistics() -> Dict:
    """
    Get comprehensive graph statistics.
    
    Returns:
        Statistics dictionary
    """
    graph = get_graph()
    
    stats = graph.get_stats()
    
    # Count by node type
    node_counts = {}
    for node in graph.nodes:
        for label in node["labels"]:
            node_counts[label] = node_counts.get(label, 0) + 1
    
    # Count by relationship type
    rel_counts = {}
    for rel in graph.relationships:
        rel_type = rel["type"]
        rel_counts[rel_type] = rel_counts.get(rel_type, 0) + 1
    
    stats.update({
        "node_counts": node_counts,
        "relationship_counts": rel_counts
    })
    
    return stats
