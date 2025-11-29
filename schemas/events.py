"""
Pydantic schemas for all events in the Seraphs 2.0 system.

All agents communicate via standardized events published to Redis Streams.
These schemas enforce strict typing and validation.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, HttpUrl


class EventType(str, Enum):
    """All possible event types in the system"""
    INGESTION_SNAPSHOT = "INGESTION_SNAPSHOT"
    AUTH_PROOF_READY = "AUTH_PROOF_READY"
    CHANGE_EVENT = "CHANGE_EVENT"
    LEGAL_RESULT = "LEGAL_RESULT"
    DEBATE_RESULT = "DEBATE_RESULT"
    KG_RESULT = "KG_RESULT"
    REMEDIATION_PLAN = "REMEDIATION_PLAN"
    ZK_PROOF_READY = "ZK_PROOF_READY"
    WORKFLOW_ACTION = "WORKFLOW_ACTION"
    HITL_REQUIRED = "HITL_REQUIRED"


class EventEnvelope(BaseModel):
    """
    Universal event envelope for all inter-agent communication.
    Every event published to Redis must follow this schema.
    """
    event_id: str = Field(..., description="Unique event identifier (UUID)")
    event_type: EventType = Field(..., description="Type of event")
    payload: Dict[str, Any] = Field(..., description="Event-specific payload")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_agent: str = Field(..., description="Agent that published this event")
    trace_id: str = Field(..., description="Trace ID for distributed tracing")
    correlation_id: Optional[str] = Field(None, description="ID of related parent event")
    metadata: Dict[str, Any] = Field(default_factory=dict)


# =============================================================================
# AGENT 1: INGESTION SNAPSHOT
# =============================================================================

class SourceInfo(BaseModel):
    """Regulatory source information"""
    name: str
    url: HttpUrl
    type: str  # html | pdf | rss

class ContentData(BaseModel):
    """Fetched content data"""
    raw_html: Optional[str] = None
    raw_pdf: Optional[bytes] = None
    extracted_text: str
    content_type: str
    encoding: str = "utf-8"
    size_bytes: int

class HashData(BaseModel):
    """Cryptographic hashes"""
    sha256: str
    md5: Optional[str] = None

class StorageInfo(BaseModel):
    """Storage locations"""
    ipfs_cid: str
    ipfs_gateway_url: HttpUrl

class VersionInfo(BaseModel):
    """Version tracking"""
    is_new_version: bool
    previous_hash: Optional[str] = None
    change_detected: bool

class IngestionSnapshotPayload(BaseModel):
    """Payload for INGESTION_SNAPSHOT events"""
    snapshot_id: str
    source: SourceInfo
    fetched_at: datetime
    content: ContentData
    hashes: HashData
    storage: StorageInfo
    metadata: Dict[str, Any] = Field(default_factory=dict)
    version_info: VersionInfo


# =============================================================================
# AGENT 2: AUTH PROOF
# =============================================================================

class TLSProof(BaseModel):
    """TLS notary proof"""
    proof_type: str = "tls_notary"
    server_cert_fingerprint: str
    cipher_suite: str
    signature: str
    witness_data: Optional[str] = None
    verified: bool

class ConsensusData(BaseModel):
    """Multi-source consensus result"""
    sources_checked: int
    consensus_score: float = Field(..., ge=0.0, le=1.0)
    hashes: List[str]
    majority_hash: str

class TimestampProof(BaseModel):
    """RFC 3161 timestamp proof"""
    timestamp: datetime
    tsa_signature: str
    rfc3161_compliant: bool

class AuthProofPayload(BaseModel):
    """Payload for AUTH_PROOF_READY events"""
    snapshot_id: str
    authenticity: Dict[str, Any]
    tls_proof: TLSProof
    consensus: ConsensusData
    merkle_root: str
    timestamp_proof: TimestampProof
    storage: StorageInfo
    hitl_required: bool = False


# =============================================================================
# AGENT 3: CHANGE EVENT
# =============================================================================

class ChangeSeverity(str, Enum):
    """Change severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ChangeType(str, Enum):
    """Types of regulatory changes"""
    NEW_OBLIGATION = "new_obligation"
    AMENDMENT = "amendment"
    DELETION = "deletion"
    CLARIFICATION = "clarification"
    DEADLINE_CHANGE = "deadline_change"
    PENALTY_CHANGE = "penalty_change"
    SCOPE_CHANGE = "scope_change"
    FORMATTING = "formatting"

class SectionChange(BaseModel):
    """Individual section change"""
    section_id: str
    title: Optional[str] = None
    position: Optional[int] = None

class SemanticChange(BaseModel):
    """Semantic change details"""
    section_id: str
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    semantic_drift: Optional[str] = None

class ChangeEventPayload(BaseModel):
    """Payload for CHANGE_EVENT"""
    snapshot_id: str
    previous_snapshot_id: Optional[str] = None
    has_changes: bool
    structural_changes: Dict[str, List[SectionChange]] = Field(default_factory=dict)
    semantic_changes: List[SemanticChange] = Field(default_factory=list)
    classification: Dict[str, Any]
    summary: str
    highlighted_diff_html: Optional[str] = None
    metadata_changes: Dict[str, Any] = Field(default_factory=dict)


# =============================================================================
# AGENT 4: LEGAL RESULT
# =============================================================================

class Certainty(str, Enum):
    """Certainty levels for LLM extractions"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNCERTAIN = "UNCERTAIN"

class Obligation(BaseModel):
    """Regulatory obligation"""
    id: str
    text: str
    evidence_ref: str = Field(..., description="Must cite source section")
    deadline: Optional[str] = None
    penalty: Optional[str] = None
    scope: str
    certainty: Certainty

class LegalResultPayload(BaseModel):
    """Payload for LEGAL_RESULT events"""
    snapshot_id: str
    summary: str
    obligations: List[Obligation]
    penalties: List[Dict[str, Any]] = Field(default_factory=list)
    deadlines: List[Dict[str, Any]] = Field(default_factory=list)
    ambiguities: List[str] = Field(default_factory=list)
    contradictions: List[str] = Field(default_factory=list)
    impact_score: float = Field(..., ge=0.0, le=1.0)


# =============================================================================
# AGENT 5: DEBATE RESULT
# =============================================================================

class DebateResultPayload(BaseModel):
    """Payload for DEBATE_RESULT events"""
    snapshot_id: str
    original_legal_result: LegalResultPayload
    prosecutor_argument: str
    defender_argument: str
    judge_verdict: Dict[str, Any]
    divergence_score: float = Field(..., ge=0.0, le=1.0)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    refined_impact_score: float = Field(..., ge=0.0, le=1.0)
    hitl_required: bool
    debate_log: List[Dict[str, str]]


# =============================================================================
# AGENT 6: KNOWLEDGE GRAPH RESULT
# =============================================================================

class Mapping(BaseModel):
    """Obligation to policy mapping"""
    obligation_id: str
    matched_policies: List[str]
    matched_controls: List[str]
    justification: str
    confidence: float = Field(..., ge=0.0, le=1.0)

class Gap(BaseModel):
    """Compliance gap"""
    obligation_id: str
    reason: str
    risk_score: float = Field(..., ge=0.0, le=1.0)

class KGResultPayload(BaseModel):
    """Payload for KG_RESULT events"""
    snapshot_id: str
    mappings: List[Mapping]
    gaps: List[Gap]
    compliance_score: int = Field(..., ge=0, le=100)
    recommendations: List[str] = Field(default_factory=list)


# =============================================================================
# AGENT 9: ZK PROOF
# =============================================================================

class ZKProofPayload(BaseModel):
    """Payload for ZK_PROOF_READY events"""
    merkle_root: str
    zk_proof: str
    cardano_tx_hash: str
    nft_token_id: Optional[str] = None
    ipfs_proof_cid: str
    verified: bool


# =============================================================================
# HITL (Human-in-the-Loop)
# =============================================================================

class HITLReason(str, Enum):
    """Reasons for HITL escalation"""
    LOW_CONSENSUS = "low_consensus"
    AUTH_FAILED = "auth_failed"
    HIGH_DIVERGENCE = "high_divergence"
    AMBIGUITY_DETECTED = "ambiguity_detected"
    CRITICAL_CHANGE = "critical_change"
    HIGH_RISK_GAP = "high_risk_gap"

class HITLPayload(BaseModel):
    """Payload for HITL_REQUIRED events"""
    reason: HITLReason
    related_event_id: str
    related_event_type: EventType
    description: str
    data: Dict[str, Any]
    urgency: str = Field(..., pattern="^(low|medium|high|critical)$")
