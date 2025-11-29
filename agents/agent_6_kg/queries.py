"""
Agent 6: Knowledge Graph
Cypher query templates for Neo4j.
"""

# =============================================================================
# CYPHER QUERY TEMPLATES
# =============================================================================

# Find all KYC obligations affecting commercial banks
QUERY_KYC_FOR_BANKS = """
MATCH (o:Obligation {type: "KYC"})-[:AFFECTS]->(e:Entity {type: "Commercial Bank"})
RETURN o, e
ORDER BY o.severity DESC, o.deadline ASC
"""

# Find policy gaps (obligations without policy mappings)
QUERY_POLICY_GAPS = """
MATCH (o:Obligation)
WHERE NOT (o)-[:MAPPED_TO]->(:Policy)
RETURN o
ORDER BY o.severity DESC
"""

# Find all obligations from a specific source
QUERY_OBLIGATIONS_BY_SOURCE = """
MATCH (o:Obligation)-[:FROM]->(s:Source {name: $source_name})
RETURN o, s
ORDER BY o.created_at DESC
"""

# Find conflicting obligations
QUERY_CONFLICTS = """
MATCH (o1:Obligation)-[:CONFLICTS_WITH]->(o2:Obligation)
RETURN o1, o2
"""

# Temporal tracking - find superseded obligations
QUERY_SUPERSEDED = """
MATCH (old:Obligation)-[:SUPERSEDES]->(new:Obligation)
WHERE old.deadline < date()
RETURN old, new
ORDER BY new.created_at DESC
"""

# Find obligations by severity
QUERY_BY_SEVERITY = """
MATCH (o:Obligation {severity: $severity})
RETURN o
ORDER BY o.deadline ASC
"""

# Find all obligations affecting a specific entity
QUERY_OBLIGATIONS_FOR_ENTITY = """
MATCH (o:Obligation)-[:AFFECTS]->(e:Entity {name: $entity_name})
RETURN o
ORDER BY o.severity DESC, o.deadline ASC
"""

# Find obligations mapped to a policy
QUERY_OBLIGATIONS_FOR_POLICY = """
MATCH (o:Obligation)-[:MAPPED_TO]->(p:Policy {name: $policy_name})
RETURN o, p
"""

# Get full obligation network (1-hop from obligation)
QUERY_OBLIGATION_NETWORK = """
MATCH (o:Obligation {obligation_id: $obligation_id})
OPTIONAL MATCH (o)-[r1]->(n1)
OPTIONAL MATCH (o)<-[r2]-(n2)
RETURN o, r1, n1, r2, n2
"""

# Find obligations with approaching deadlines
QUERY_UPCOMING_DEADLINES = """
MATCH (o:Obligation)
WHERE o.deadline <> 'not specified' 
  AND date(o.deadline) > date() 
  AND date(o.deadline) < date() + duration({days: $days})
RETURN o
ORDER BY o.deadline ASC
"""

# Get graph overview statistics
QUERY_STATISTICS = """
MATCH (n)
WITH labels(n) AS label, count(*) AS count
RETURN label, count
ORDER BY count DESC
"""

# Find related obligations (same type, different sources)
QUERY_SIMILAR_OBLIGATIONS = """
MATCH (o1:Obligation {type: $obligation_type})
MATCH (o2:Obligation {type: $obligation_type})
WHERE o1 <> o2
RETURN o1, o2
LIMIT 10
"""

# Find entities without any obligations
QUERY_UNAFFECTED_ENTITIES = """
MATCH (e:Entity)
WHERE NOT (e)<-[:AFFECTS]-(:Obligation)
RETURN e
"""

# Get full compliance domain for an entity
QUERY_ENTITY_COMPLIANCE_DOMAIN = """
MATCH (e:Entity {name: $entity_name})<-[:AFFECTS]-(o:Obligation)-[:FROM]->(s:Source)
OPTIONAL MATCH (o)-[:MAPPED_TO]->(p:Policy)
RETURN e, o, s, p
"""

# Find obligations requiring HITL
QUERY_HITL_OBLIGATIONS = """
MATCH (o:Obligation)
WHERE o.confidence < $confidence_threshold
RETURN o
ORDER BY o.confidence ASC
"""
