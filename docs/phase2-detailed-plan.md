# Phase 2: Detailed Implementation Plan
## Authenticity & Oracle (Agent 2) + Diff/Change Classifier (Agent 3)

---

## 🎯 PHASE 2 OBJECTIVES

Build **two critical agents** that process the snapshots from Agent 1:

### **Agent 2: Authenticity & Oracle**
- Cryptographically prove content came from legitimate regulatory source
- Generate TLS notary proofs
- Perform multi-source consensus verification
- Compute Merkle roots for integrity
- Store proofs in IPFS
- Publish `AUTH_PROOF_READY` events

### **Agent 3: Diff & Change Classifier**
- Compare new snapshots with previous versions
- Detect structural changes (sections added/removed/moved)
- Detect semantic changes (meaning shifts)
- Classify change severity (critical/high/medium/low)
- Classify change type (new_obligation/amendment/deletion)
- Publish `CHANGE_EVENT` events

---

## 🔐 AGENT 2: AUTHENTICITY & ORACLE

### **Purpose**
In regulatory compliance, **provenance is everything**. You can't trust an AI saying "RBI published this" without cryptographic proof. Agent 2 solves this by:

1. **TLS Notary Proof**: Proves the content was served by rbi.org.in's TLS-certified server
2. **Certificate Chain Validation**: Verifies the SSL certificate is legitimate
3. **Multi-Source Consensus**: Fetches from multiple network locations and compares hashes
4. **Merkle Tree Aggregation**: Creates tamper-proof hash tree
5. **Timestamping**: Proves "when" the content was fetched

This makes it **impossible to fake** regulatory content in the system.

---

### **10 Core Tools**

#### **1. tls_notary_proof**
```python
def tls_notary_proof(url: str, content: bytes) -> TLSProof:
    """
    Generate TLS notarized proof that content came from URL
    
    Uses TLSNotary protocol to create cryptographic proof that:
    - Content was served by the domain's TLS certificate
    - Server's certificate chain is valid
    - No MITM attack occurred
    
    Args:
        url: Source URL
        content: Fetched content
        
    Returns:
        TLSProof object with signature, certificate, witness data
        
    Implementation:
        - Use tlsnotary-py library
        - Captures TLS handshake
        - Generates zero-knowledge proof
        - Returns witness data + signature
    """
```

**Example Output**:
```json
{
  "proof_type": "tls_notary",
  "url": "https://www.rbi.org.in/Scripts/NotificationUser.aspx",
  "tls_version": "TLS 1.3",
  "cipher_suite": "TLS_AES_256_GCM_SHA384",
  "server_cert_fingerprint": "SHA256:a3f7e2...",
  "cert_chain": ["cert1", "cert2", "cert3"],
  "signature": "0x...",
  "witness_data": "...",
  "timestamp": "2025-11-29T10:30:00Z",
  "verified": true
}
```

#### **2. cert_chain_verify**
```python
def cert_chain_verify(cert_chain: List[str]) -> CertValidation:
    """
    Verify SSL certificate chain validity
    
    Checks:
    - Certificate not expired
    - Chain of trust to root CA
    - Revocation status (OCSP/CRL)
    - Domain name matches
    
    Returns:
        CertValidation with validity status and details
    """
```

#### **3. multi_fetch_consensus**
```python
def multi_fetch_consensus(url: str, n: int = 3) -> ConsensusResult:
    """
    Fetch from multiple network locations and compare
    
    Strategy:
    - Fetch from local datacenter
    - Fetch via VPN (different geographic location)
    - Fetch via Tor (anonymized)
    - Compare SHA-256 hashes
    - Calculate consensus score
    
    Args:
        url: Target URL
        n: Number of independent fetches (default 3)
        
    Returns:
        ConsensusResult with:
        - consensus_score (0.0-1.0)
        - hashes from each source
        - majority hash
        - discrepancies (if any)
    """
```

**Consensus Logic**:
- If all 3 hashes match → `consensus_score = 1.0`
- If 2/3 match → `consensus_score = 0.67`
- If all different → `consensus_score = 0.0` → **HITL escalation**

#### **4. merkle_aggregate**
```python
def merkle_aggregate(data_hashes: List[str]) -> MerkleTree:
    """
    Build Merkle tree from content hashes
    
    Creates tamper-proof structure:
    - Leaf nodes: content hashes
    - Internal nodes: hash of children
    - Root: single hash representing all data
    
    Returns:
        MerkleTree with root, leaves, proof paths
    """
```

**Merkle Tree Structure**:
```
                Root Hash
               /         \
          H(AB)           H(CD)
         /    \          /    \
       H(A)  H(B)     H(C)   H(D)
        |     |        |      |
      Data1 Data2   Data3  Data4
```

#### **5. store_proof_ipfs**
```python
def store_proof_ipfs(proof: dict) -> str:
    """
    Store cryptographic proof in IPFS
    
    Returns: IPFS CID
    """
```

#### **6. timestamp_proof**
```python
def timestamp_proof(content: str) -> TimestampProof:
    """
    Generate trusted timestamp using RFC 3161
    
    Uses external timestamp authority to prove:
    - Content existed at specific time
    - Hash was created at specific time
    
    Options:
    - Use free TSA (freetsa.org)
    - Use paid TSA for production
    - Use blockchain timestamp (Bitcoin/Cardano)
    
    Returns:
        TimestampProof with TSA signature
    """
```

#### **7. dns_verification**
```python
def dns_verification(domain: str) -> DNSRecords:
    """
    Verify DNS records for domain authenticity
    
    Checks:
    - A/AAAA records
    - MX records
    - TXT records (SPF, DMARC)
    - DNSSEC validation
    
    Helps detect DNS spoofing
    """
```

#### **8. domain_authenticity_check**
```python
def domain_authenticity_check(domain: str) -> AuthScore:
    """
    Assess domain authenticity risk
    
    Checks:
    - Domain age (WHOIS)
    - SSL certificate history
    - Reputation databases
    - Typosquatting detection
    
    Returns:
        Risk score (0.0 = safe, 1.0 = suspicious)
    """
```

#### **9. compute_witness**
```python
def compute_witness(url: str, content: bytes) -> WitnessData:
    """
    Generate witness data for zero-knowledge proof
    
    Creates cryptographic commitment that can later prove:
    - Content was fetched from URL
    - At specific timestamp
    - Without revealing full content
    """
```

#### **10. verify_tls_signature**
```python
def verify_tls_signature(signature: str, cert: str) -> bool:
    """
    Verify TLS signature against certificate
    
    Returns: True if valid, False otherwise
    """
```

---

### **Agent 2 Workflow**

```
INPUT: INGESTION_SNAPSHOT event from Agent 1
  ↓
1. Extract URL and content from snapshot
  ↓
2. Generate TLS notary proof (tool #1)
  ↓
3. Verify certificate chain (tool #2)
  ↓
4. Perform multi-source consensus (tool #3)
  ↓
5. Check consensus_score:
   - If < 0.6 → ESCALATE TO HITL
   - If TLS proof fails → BLOCK EVENT
   - If ≥ 0.6 → Continue
  ↓
6. Compute Merkle root (tool #4)
  ↓
7. Generate timestamp proof (tool #6)
  ↓
8. Store proof bundle in IPFS (tool #5)
  ↓
9. Publish AUTH_PROOF_READY event
  ↓
OUTPUT: Cryptographically verified snapshot
```

---

### **Agent 2 Output Event**

```json
{
  "event_id": "uuid",
  "event_type": "AUTH_PROOF_READY",
  "trace_id": "trace-2025-11-29-001",
  "correlation_id": "snap-rbi-2025-11-29-103000",
  "timestamp": "2025-11-29T10:35:00Z",
  "source_agent": "agent-2-auth",
  "payload": {
    "snapshot_id": "snap-rbi-2025-11-29-103000",
    "authenticity": {
      "verified": true,
      "confidence_score": 0.95
    },
    "tls_proof": {
      "proof_type": "tls_notary",
      "server_cert_fingerprint": "SHA256:a3f7e2...",
      "cipher_suite": "TLS_AES_256_GCM_SHA384",
      "signature": "0x...",
      "verified": true
    },
    "consensus": {
      "sources_checked": 3,
      "consensus_score": 1.0,
      "hashes": [
        "a3c7f8e2...",
        "a3c7f8e2...",
        "a3c7f8e2..."
      ],
      "majority_hash": "a3c7f8e2..."
    },
    "merkle_root": "7f2d9a3c...",
    "timestamp_proof": {
      "timestamp": "2025-11-29T10:30:00Z",
      "tsa_signature": "0x...",
      "rfc3161_compliant": true
    },
    "storage": {
      "ipfs_proof_cid": "QmProof123...",
      "ipfs_gateway_url": "https://ipfs.io/ipfs/QmProof123..."
    },
    "hitl_required": false
  }
}
```

---

### **HITL Escalation Triggers**

Agent 2 escalates to human if:
1. **Consensus score < 0.6** → Different content from different sources
2. **TLS proof fails** → Certificate invalid or MITM attack suspected
3. **Domain authenticity risk > 0.7** → Suspicious domain
4. **Certificate recently changed** → Potential compromise

---

## 📊 AGENT 3: DIFF & CHANGE CLASSIFIER

### **Purpose**
Not every regulatory update matters equally. A typo fix vs. a new compliance obligation are vastly different.

Agent 3:
1. **Detects structural changes**: Sections added, removed, or reorganized
2. **Detects semantic changes**: Meaning shifts even if text is similar
3. **Classifies severity**: Critical (new penalties) vs. Low (formatting)
4. **Classifies type**: New obligation, amendment, deletion, clarification

This enables **intelligent routing** - critical changes go to Legal Agent immediately, minor changes can be batched.

---

### **12 Core Tools**

#### **1. section_chunk**
```python
def section_chunk(text: str, strategy: str = 'semantic') -> List[Chunk]:
    """
    Split document into logical sections
    
    Strategies:
    - 'semantic': Use embeddings to find semantic boundaries
    - 'structural': Use headings, numbering (Section 1, 2, 3)
    - 'hybrid': Combine both
    
    Returns:
        List of Chunk objects with:
        - section_id
        - title
        - content
        - start_offset, end_offset
    """
```

#### **2. hash_sections**
```python
def hash_sections(chunks: List[Chunk]) -> Dict[str, str]:
    """
    Compute hash for each section
    
    Returns: {section_id: sha256_hash}
    
    Use case: Quick comparison - if hashes match, section unchanged
    """
```

#### **3. structural_diff**
```python
def structural_diff(old_doc: Document, new_doc: Document) -> StructuralDiff:
    """
    Detect structural changes
    
    Detects:
    - Sections added
    - Sections removed
    - Sections moved/reordered
    - Sections merged/split
    
    Algorithm:
    - Diff old vs new section lists
    - Use longest common subsequence (LCS)
    - Track section IDs
    
    Returns:
        StructuralDiff with:
        - added_sections
        - removed_sections
        - moved_sections
        - modified_sections
    """
```

**Example**:
```json
{
  "added_sections": [
    {
      "section_id": "4.5",
      "title": "New KYC Requirements for Crypto",
      "content": "...",
      "position": 12
    }
  ],
  "removed_sections": [],
  "moved_sections": [
    {
      "section_id": "3.2",
      "old_position": 8,
      "new_position": 15
    }
  ],
  "modified_sections": ["2.1", "2.3", "4.1"]
}
```

#### **4. semantic_diff**
```python
def semantic_diff(old_text: str, new_text: str) -> SemanticDiff:
    """
    Detect semantic changes using embeddings
    
    Method:
    - Generate embeddings for old vs new (OpenAI/Sentence-Transformers)
    - Compute cosine similarity
    - If similarity < threshold → semantic change detected
    
    Returns:
        SemanticDiff with:
        - similarity_score (0.0-1.0)
        - changed_meaning: bool
        - semantic_drift_areas: List[str]
    """
```

**Similarity Thresholds**:
- `> 0.95`: No meaningful change
- `0.8 - 0.95`: Minor rewording
- `0.5 - 0.8`: Moderate semantic shift
- `< 0.5`: Major meaning change

#### **5. classify_change**
```python
def classify_change(diff: StructuralDiff, semantic: SemanticDiff) -> ChangeType:
    """
    Classify type of regulatory change
    
    Types:
    - NEW_OBLIGATION: New requirement added
    - AMENDMENT: Existing requirement modified
    - DELETION: Requirement removed
    - CLARIFICATION: Explanation added, no new obligations
    - DEADLINE_CHANGE: Timeline modified
    - PENALTY_CHANGE: Fines/penalties modified
    - SCOPE_CHANGE: Applicability changed
    - FORMATTING: Only formatting/typos
    
    Logic uses keyword matching + LLM classification
    """
```

#### **6. change_summary**
```python
def change_summary(diff: StructuralDiff) -> str:
    """
    Generate human-readable summary of changes
    
    Example output:
    "Added Section 4.5 on crypto KYC requirements. Modified Section 2.1 
    to extend deadline from Dec 2025 to Mar 2026. Removed outdated 
    Section 3.7 on legacy authentication."
    """
```

#### **7. impact_scorer**
```python
def impact_scorer(change: Change) -> float:
    """
    Score impact of change (0.0 - 1.0)
    
    Factors:
    - Severity keywords (must, shall, penalty, fine)
    - Deadline proximity
    - Section importance (title, body, appendix)
    - Scope (all entities vs. specific subset)
    
    Returns: Impact score
    """
```

**Scoring Logic**:
```python
score = 0.0

# Keywords
if "must" or "shall" in change: score += 0.3
if "penalty" or "fine" in change: score += 0.2
if "deadline" in change: score += 0.2

# Urgency
days_until_deadline = extract_deadline(change)
if days_until_deadline < 90: score += 0.3

# Scope
if "all financial institutions" in change: score += 0.2

return min(score, 1.0)
```

#### **8. highlight_changes**
```python
def highlight_changes(old_text: str, new_text: str) -> str:
    """
    Generate visual diff (HTML with highlights)
    
    Returns: HTML with:
    - Green highlights for additions
    - Red highlights for deletions
    - Yellow for modifications
    
    Use for UI display
    """
```

#### **9. detect_reorg**
```python
def detect_reorg(old_doc: Document, new_doc: Document) -> bool:
    """
    Detect if document was reorganized (but content unchanged)
    
    Returns: True if major reorganization detected
    """
```

#### **10. metadata_diff**
```python
def metadata_diff(old_meta: dict, new_meta: dict) -> MetadataDiff:
    """
    Compare document metadata
    
    Checks:
    - Title changes
    - Author changes
    - Publication date
    - Version number
    - Document ID
    
    Returns: MetadataDiff
    """
```

#### **11. section_mapper**
```python
def section_mapper(old_sections: List[Chunk], new_sections: List[Chunk]) -> Mapping:
    """
    Map sections from old doc to new doc
    
    Uses:
    - Section IDs (if stable)
    - Title similarity
    - Content similarity
    
    Returns: {old_section_id: new_section_id}
    """
```

#### **12. change_severity_classifier**
```python
def change_severity_classifier(change: Change) -> Severity:
    """
    Classify severity level
    
    Levels:
    - CRITICAL: New penalties, compliance deadlines <90 days
    - HIGH: New obligations, major scope changes
    - MEDIUM: Amendments to existing requirements
    - LOW: Clarifications, formatting, typos
    
    Uses LLM + rule-based logic
    """
```

---

### **Agent 3 Workflow**

```
INPUT: AUTH_PROOF_READY event from Agent 2
  ↓
1. Retrieve current snapshot
  ↓
2. Retrieve previous snapshot from database
  ↓
3. If no previous snapshot → Mark as "FIRST_VERSION" → Skip diff
  ↓
4. Chunk both documents into sections (tool #1)
  ↓
5. Hash each section (tool #2)
  ↓
6. Quick comparison: If all hashes match → NO CHANGE → End
  ↓
7. Perform structural diff (tool #3)
  ↓
8. Perform semantic diff on modified sections (tool #4)
  ↓
9. Classify change type (tool #5)
  ↓
10. Classify severity (tool #12)
  ↓
11. Score impact (tool #7)
  ↓
12. Generate change summary (tool #6)
  ↓
13. Publish CHANGE_EVENT
  ↓
OUTPUT: Structured change analysis
```

---

### **Agent 3 Output Event**

```json
{
  "event_id": "uuid",
  "event_type": "CHANGE_EVENT",
  "trace_id": "trace-2025-11-29-001",
  "correlation_id": "snap-rbi-2025-11-29-103000",
  "timestamp": "2025-11-29T10:40:00Z",
  "source_agent": "agent-3-diff",
  "payload": {
    "snapshot_id": "snap-rbi-2025-11-29-103000",
    "previous_snapshot_id": "snap-rbi-2025-11-28-103000",
    "has_changes": true,
    "structural_changes": {
      "added_sections": [
        {
          "section_id": "4.5",
          "title": "KYC Norms for Virtual Digital Assets",
          "position": 12
        }
      ],
      "removed_sections": [],
      "modified_sections": ["2.1", "3.4"]
    },
    "semantic_changes": [
      {
        "section_id": "2.1",
        "similarity_score": 0.72,
        "semantic_drift": "Deadline extended from Dec 2025 to Mar 2026"
      }
    ],
    "classification": {
      "type": "NEW_OBLIGATION",
      "severity": "HIGH",
      "impact_score": 0.85
    },
    "summary": "RBI introduced new KYC requirements for virtual digital assets (Section 4.5). Implementation deadline: March 31, 2026. Applies to all banks and NBFCs.",
    "highlighted_diff_html": "<html>...</html>",
    "metadata_changes": {
      "version_changed": true,
      "old_version": "1.2",
      "new_version": "1.3"
    }
  }
}
```

---

### **No Changes Scenario**

If no changes detected:
```json
{
  "event_type": "CHANGE_EVENT",
  "payload": {
    "snapshot_id": "snap-sebi-2025-11-29-120000",
    "has_changes": false,
    "all_hashes_match": true,
    "summary": "No changes detected"
  }
}
```

**Optimization**: Don't send to Legal Agent if no changes.

---

## 🔗 PHASE 2 INTEGRATION

### **Event Flow**
```
Agent 1 (Ingestion)
  → publishes: INGESTION_SNAPSHOT
  
Agent 2 (Authenticity)
  → subscribes to: INGESTION_SNAPSHOT
  → publishes: AUTH_PROOF_READY
  
Agent 3 (Diff)
  → subscribes to: AUTH_PROOF_READY
  → publishes: CHANGE_EVENT
```

### **Orchestrator Logic**
```python
# In LangGraph orchestrator

if event.type == "INGESTION_SNAPSHOT":
    route_to_agent_2(event)

if event.type == "AUTH_PROOF_READY":
    if event.payload.verified:
        route_to_agent_3(event)
    else:
        escalate_to_hitl(event, reason="Auth failed")

if event.type == "CHANGE_EVENT":
    if event.payload.has_changes:
        route_to_agent_4_legal(event)  # Phase 3
    else:
        log_no_change(event)
        end_flow(event)
```

---

## 🗄️ DATABASE SCHEMA (For Snapshots)

```sql
CREATE TABLE snapshots (
    id UUID PRIMARY KEY,
    source_id VARCHAR(50) NOT NULL,
    source_url TEXT NOT NULL,
    fetched_at TIMESTAMP NOT NULL,
    content_hash VARCHAR(64) NOT NULL,
    ipfs_cid VARCHAR(100),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE auth_proofs (
    id UUID PRIMARY KEY,
    snapshot_id UUID REFERENCES snapshots(id),
    verified BOOLEAN NOT NULL,
    consensus_score FLOAT,
    tls_proof JSONB,
    merkle_root VARCHAR(64),
    ipfs_proof_cid VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE changes (
    id UUID PRIMARY KEY,
    snapshot_id UUID REFERENCES snapshots(id),
    previous_snapshot_id UUID REFERENCES snapshots(id),
    has_changes BOOLEAN NOT NULL,
    severity VARCHAR(20),
    change_type VARCHAR(50),
    impact_score FLOAT,
    summary TEXT,
    structural_diff JSONB,
    semantic_diff JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_snapshots_source ON snapshots(source_id, fetched_at DESC);
CREATE INDEX idx_changes_severity ON changes(severity, created_at DESC);
```

---

## 🧪 TESTING STRATEGY

### **Agent 2 Tests**

1. **TLS Proof Test**:
   - Mock TLS handshake
   - Verify signature generation
   - Test certificate chain validation

2. **Consensus Test**:
   - Mock 3 fetches with same content → `consensus_score = 1.0`
   - Mock 2/3 match → `consensus_score = 0.67`
   - Mock all different → `consensus_score = 0.0` → HITL triggered

3. **Integration Test**:
   - Real fetch from RBI website
   - Generate real TLS proof
   - Store in local IPFS
   - Publish to Redis

### **Agent 3 Tests**

1. **Diff Detection Test**:
   ```python
   old_doc = load_fixture("rbi_circular_v1.html")
   new_doc = load_fixture("rbi_circular_v2.html")
   
   diff = structural_diff(old_doc, new_doc)
   
   assert len(diff.added_sections) == 1
   assert diff.added_sections[0].title == "New KYC Requirements"
   ```

2. **Severity Classification Test**:
   ```python
   change = Change(content="Must implement by Dec 31, 2025. Penalty: $1M")
   
   severity = change_severity_classifier(change)
   
   assert severity == "CRITICAL"
   ```

3. **No Change Test**:
   ```python
   old_doc = load_fixture("sebi_circular.pdf")
   new_doc = old_doc  # Same content
   
   event = agent_3_process(old_doc, new_doc)
   
   assert event.payload.has_changes == False
   ```

---

## 📦 ADDITIONAL DEPENDENCIES

```txt
# Phase 2 specific
tlsnotary-py>=0.1.0        # TLS notary proofs
cryptography>=41.0.0        # Certificate validation
python-merkle>=0.1.0        # Merkle trees
sentence-transformers>=2.2.0  # Semantic similarity
difflib>=3.9                # Text diffing
html-diff>=0.3.0           # HTML diff generation
```

---

## ⏱️ PHASE 2 TIMELINE

| Task | Duration | Dependency |
|------|----------|-----------|
| Agent 2 tool implementations | 4 hours | Phase 1 complete |
| Agent 2 core logic | 2 hours | Tools done |
| Agent 3 tool implementations | 3 hours | Phase 1 complete |
| Agent 3 core logic | 2 hours | Tools done |
| Database schema setup | 1 hour | - |
| Agent 2 unit tests | 2 hours | Agent 2 done |
| Agent 3 unit tests | 2 hours | Agent 3 done |
| Integration tests (2+3) | 2 hours | Both agents done |
| Docker setup | 1 hour | - |
| **Total** | **~19 hours** | - |

---

## 🎯 SUCCESS CRITERIA

- [ ] Agent 2 generates valid TLS proofs
- [ ] Consensus mechanism works (3-source comparison)
- [ ] Merkle roots computed correctly
- [ ] Proofs stored in IPFS
- [ ] AUTH_PROOF_READY events published
- [ ] Agent 3 detects structural changes accurately
- [ ] Agent 3 detects semantic changes using embeddings
- [ ] Severity classification matches expected results
- [ ] CHANGE_EVENT events published
- [ ] No-change scenarios handled (don't spam downstream)
- [ ] Database stores all snapshots, proofs, changes
- [ ] All tests pass (>80% coverage)

---

## 🚀 DEMO OUTPUT (After Phase 2)

```bash
# Start full pipeline
docker-compose up -d

# Agent 1 fetches RBI page
# Agent 2 verifies authenticity
# Agent 3 detects changes

# View all events
redis-cli XREAD STREAMS seraphs:events 0

# Query database
psql -d seraphs -c "SELECT * FROM changes WHERE severity='CRITICAL' ORDER BY created_at DESC LIMIT 10;"

# View stored proofs in IPFS
ipfs cat QmProof123...
```

---

## 📋 PHASE 2 DELIVERABLES

1. ✅ Agent 2 (Authenticity) fully functional
2. ✅ Agent 3 (Diff Classifier) fully functional
3. ✅ PostgreSQL schema created
4. ✅ TLS proof generation working
5. ✅ Multi-source consensus working
6. ✅ Structural + semantic diff working
7. ✅ Change classification working
8. ✅ All events flowing through Redis
9. ✅ Unit + integration tests passing
10. ✅ Docker containers for both agents

---

**Next**: Phase 3 will add **Agent 4 (Legal LLM Intelligence)** and **Agent 5 (MAAD Debate)** to extract obligations and verify them through adversarial reasoning.
