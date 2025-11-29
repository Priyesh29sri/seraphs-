"""
Agent 2: Authenticity & Oracle - Simplified (No structured logging)
"""

import json
from datetime import datetime
from typing import Dict, List
from agents.agent_2_auth import tools


class AuthenticityAgent:
    """Agent 2: Authenticity & Oracle"""
    
    def __init__(self, consensus_threshold: float = 0.6):
        self.consensus_threshold = consensus_threshold
        print(f"[INFO] Agent 2 initialized (consensus threshold: {consensus_threshold})")
    
    def verify_snapshot(self, snapshot: Dict) -> Dict:
        """Verify authenticity of a snapshot"""
        snapshot_id = snapshot['snapshot_id']
        url = snapshot['url']
        content_hash = snapshot['sha256']
        
        print(f"\n[INFO] Verifying: {snapshot_id}")
        print(f"  Source: {snapshot['source']}")
        print(f"  URL: {url}")
        
        # TLS proof
        tls_proof_result = tools.tls_proof(url, content_hash)
        
        # Certificate verification
        cert_result = tools.cert_chain_verify(url)
        
        # Multi-source consensus
        consensus_result = tools.multi_fetch_consensus(url, n=3)
        
        # DNS verification
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        dns_result = tools.dns_verification(domain)
        
        # Domain authenticity
        auth_check = tools.domain_authenticity_check(domain)
        
        # Timestamp
        timestamp_result = tools.timestamp_proof(content_hash)
        
        # Witness
        witness = tools.compute_witness(url, content_hash.encode())
        
        # HITL check
        hitl_required = self._should_escalate_to_hitl(
            consensus_result,
            tls_proof_result,
            auth_check
        )
        
        # Calculate confidence
        confidence = self._calculate_confidence(
            consensus_result,
            tls_proof_result,
            cert_result,
            auth_check
        )
        
        auth_proof = {
            "snapshot_id": snapshot_id,
            "verified": tls_proof_result["verified"] and cert_result["valid"],
            "confidence_score": confidence,
            "tls_proof": tls_proof_result,
            "certificate": cert_result,
            "consensus": consensus_result,
            "dns": dns_result,
            "domain_check": auth_check,
            "timestamp": timestamp_result,
            "witness": witness,
            "hitl_required": hitl_required,
            "verified_at": datetime.utcnow().isoformat() + "Z"
        }
        
        print(f"[SUCCESS] Verified: {auth_proof['verified']}, Confidence: {confidence}, HITL: {hitl_required}")
        
        return auth_proof
    
    def _calculate_confidence(self, consensus, tls_proof, cert, domain_check) -> float:
        score = 0.0
        score += consensus["consensus_score"] * 0.4
        if tls_proof["verified"]:
            score += 0.3
        if cert["valid"]:
            score += 0.2
        if domain_check["is_legitimate"]:
            score += 0.1
        return round(score, 2)
    
    def _should_escalate_to_hitl(self, consensus, tls_proof, domain_check) -> bool:
        if consensus["consensus_score"] < self.consensus_threshold:
            print(f"[WARNING] HITL escalation: Low consensus ({consensus['consensus_score']})")
            return True
        if not tls_proof["verified"]:
            print(f"[WARNING] HITL escalation: TLS failed")
            return True
        if domain_check["risk_score"] > 0.7:
            print(f"[WARNING] HITL escalation: Suspicious domain")
            return True
        return False
    
    def verify_batch(self, snapshots: List[Dict]) -> Dict:
        """Verify batch of snapshots"""
        print(f"\n[INFO] Verifying batch of {len(snapshots)} snapshots...")
        
        results = []
        all_hashes = []
        
        for snapshot in snapshots:
            try:
                auth_proof = self.verify_snapshot(snapshot)
                results.append(auth_proof)
                all_hashes.append(snapshot["sha256"])
            except Exception as e:
                print(f"[ERROR] Verification failed for {snapshot.get('snapshot_id')}: {e}")
                results.append({
                    "snapshot_id": snapshot.get("snapshot_id"),
                    "verified": False,
                    "error": str(e),
                    "hitl_required": True
                })
        
        # Build Merkle tree
        merkle_result = tools.merkle_aggregate(all_hashes)
        
        # Store proof
        proof_bundle = {
            "verifications": results,
            "merkle_tree": merkle_result,
            "verified_at": datetime.utcnow().isoformat() + "Z"
        }
        
        ipfs_cid = tools.store_proof_ipfs(proof_bundle)
        
        output = {
            "agent": "agent-2-authenticity",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "total_snapshots": len(snapshots),
            "verified_count": sum(1 for r in results if r.get("verified", False)),
            "hitl_count": sum(1 for r in results if r.get("hitl_required", False)),
            "merkle_root": merkle_result["merkle_root"],
            "ipfs_proof_cid": ipfs_cid,
            "verifications": results
        }
        
        print(f"\n[SUCCESS] Batch verification complete:")
        print(f"  Total: {output['total_snapshots']}")
        print(f"  Verified: {output['verified_count']}")
        print(f"  Require HITL: {output['hitl_count']}")
        
        return output
