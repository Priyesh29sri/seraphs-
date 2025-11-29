"""
Agent 2: Authenticity & Oracle - Simplified Tools (No structured logging)
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List
from urllib.parse import urlparse
import requests


def tls_proof(url: str, content_hash: str) -> Dict:
    """Generate TLS proof (simplified for MVP)"""
    print(f"[INFO] Generating TLS proof for: {url}")
    
    try:
        response = requests.get(url, timeout=10, verify=True, stream=True)
        
        return {
            "verified": True,
            "method": "ssl_verification",
            "url": url,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status_code": response.status_code,
        }
    except Exception as e:
        print(f"[ERROR] TLS proof failed for {url}: {e}")
        return {
            "verified": False,
            "url": url,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }


def cert_chain_verify(url: str) -> Dict:
    """Verify SSL certificate"""
    try:
        requests.get(url, timeout=10, verify=True)
        return {
            "valid": True,
            "url": url,
            "verified_at": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        return {
            "valid": False,
            "url": url,
            "error": str(e)
        }


def multi_fetch_consensus(url: str, n: int = 3) -> Dict:
    """Fetch from multiple locations and compare hashes"""
    print(f"[INFO] Multi-fetch consensus ({n} attempts): {url}")
    
    hashes = []
    
    for i in range(n):
        try:
            if i > 0:
                time.sleep(0.5)
            
            response = requests.get(url, timeout=10)
            content_hash = hashlib.sha256(response.content).hexdigest()
            hashes.append(content_hash)
            print(f"  Attempt {i+1}: {content_hash[:16]}...")
            
        except Exception as e:
            print(f"  Attempt {i+1}: FAILED - {e}")
            hashes.append(None)
    
    valid_hashes = [h for h in hashes if h is not None]
    
    if not valid_hashes:
        return {
            "consensus_score": 0.0,
            "sources_checked": n,
            "successful_fetches": 0,
            "hashes": hashes,
            "majority_hash": None
        }
    
    from collections import Counter
    hash_counts = Counter(valid_hashes)
    majority_hash,count = hash_counts.most_common(1)[0]
    
    consensus_score = count / n
    
    print(f"[SUCCESS] Consensus score: {consensus_score}")
    
    return {
        "consensus_score": consensus_score,
        "sources_checked": n,
        "successful_fetches": len(valid_hashes),
        "hashes": hashes,
        "majority_hash": majority_hash,
        "all_match": len(set(valid_hashes)) == 1
    }


def merkle_aggregate(data_hashes: List[str]) -> Dict:
    """Build Merkle tree"""
    if not data_hashes:
        return {"merkle_root": None, "leaves": 0}
    
    current_level = data_hashes.copy()
    
    while len(current_level) > 1:
        next_level = []
        
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1] if i + 1 < len(current_level) else left
            
            combined = left + right
            parent_hash = hashlib.sha256(combined.encode()).hexdigest()
            next_level.append(parent_hash)
        
        current_level = next_level
    
    merkle_root = current_level[0]
    
    print(f"[SUCCESS] Merkle root: {merkle_root[:32]}...")
    
    return {
        "merkle_root": merkle_root,
        "leaves": len(data_hashes)
    }


def store_proof_ipfs(proof: dict) -> str:
    """Simulate IPFS storage"""
    proof_json = json.dumps(proof, sort_keys=True)
    proof_hash = hashlib.sha256(proof_json.encode()).hexdigest()
    
    cid = f"QmProof{proof_hash[:40]}"
    return cid


def timestamp_proof(content: str) -> Dict:
    """Generate timestamp proof"""
    timestamp = datetime.utcnow()
    
    return {
        "content_hash": hashlib.sha256(content.encode()).hexdigest(),
        "timestamp": timestamp.isoformat() + "Z",
        "timestamp_unix": int(timestamp.timestamp())
    }


def dns_verification(domain: str) -> Dict:
    """Verify DNS"""
    import socket
    
    try:
        ip_address = socket.gethostbyname(domain)
        return {
            "valid": True,
            "domain": domain,
            "ip_address": ip_address
        }
    except Exception as e:
        return {
            "valid": False,
            "domain": domain,
            "error": str(e)
        }


def domain_authenticity_check(domain: str) -> Dict:
    """Check domain authenticity"""
    KNOWN_LEGITIMATE = {
        'rbi.org.in', 'sebi.gov.in', 'sec.gov', 'mas.gov.sg',
        'fca.org.uk', 'federalregister.gov', 'dea.gov.in'
    }
    
    if domain in KNOWN_LEGITIMATE:
        risk_score = 0.0
        flags = ["known_legitimate"]
    elif domain.endswith('.gov') or domain.endswith('.gov.in'):
        risk_score = 0.1
        flags = ["government_tld"]
    else:
        risk_score = 0.5
        flags = ["unknown_domain"]
    
    return {
        "domain": domain,
        "risk_score": risk_score,
        "is_legitimate": risk_score < 0.3,
        "flags": flags
    }


def compute_witness(url: str, content: bytes) -> str:
    """Generate witness data"""
    if isinstance(content, str):
        content = content.encode()
    
    content_hash = hashlib.sha256(content).hexdigest()
    witness_data = f"{url}:{content_hash}"
    witness_hash = hashlib.sha256(witness_data.encode()).hexdigest()
    
    return witness_hash
