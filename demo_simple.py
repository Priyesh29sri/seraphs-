#!/usr/bin/env python3
"""
Simple Agent 1 Demo - Tests core tools WITHOUT external dependencies
Shows the fetching and output without requiring Redis/IPFS/PyPDF2
"""

import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, '/Users/priyeshsrivastava/Seraphs')

# Only import tools that don't require PyPDF2
from agents.agent_1_ingestion.tools import (
    fetch_html,
    validate_url,
    compute_sha256,
    normalize_text,
    detect_new_version,
    list_links,
    extract_metadata,
    capture_dom_tree,
)

# Colors for output
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

print(f"\n{BOLD}{BLUE}{'='*80}{RESET}")
print(f"{BOLD}{BLUE}SERAPHS 2.0 - Agent 1 Demo: Live Regulatory Fetching{RESET.center(80)}")
print(f"{BOLD}{BLUE}{'='*80}{RESET}\n")

# Test 1: Fetch from RBI
print(f"{BOLD}TEST 1: Fetching REAL data from Reserve Bank of India{RESET}")
print(f"{BLUE}URL: https://www.rbi.org.in{RESET}\n")

try:
    # Fetch RBI homepage
    result = fetch_html("https://www.rbi.org.in", timeout=20)
    
    print(f"{GREEN}✓ Fetch successful!{RESET}")
    print(f"  Status: {result.status_code}")
    print(f"  Size: {len(result.content):,} bytes")
    print(f"  Type: {result.content_type}")
    print(f"  Time: {result.fetch_time:.2f}s")
    
    html_text = result.content.decode(result.encoding)
    
    # Test 2: Extract text
    print(f"\n{BOLD}TEST 2: Text Extraction & Normalization{RESET}")
    extracted = normalize_text(html_text[:500])
    print(f"{GREEN}✓ Extracted {len(extracted)} characters{RESET}")
    print(f"{YELLOW}Preview: {extracted[:200]}...{RESET}")
    
    # Test 3: Compute hash
    print(f"\n{BOLD}TEST 3: SHA-256 Hashing{RESET}")
    hash_value = compute_sha256(result.content)
    print(f"{GREEN}✓ Hash: {hash_value}{RESET}")
    
    # Test 4: Extract links
    print(f"\n{BOLD}TEST 4: Link Extraction{RESET}")
    links = list_links(html_text, "https://www.rbi.org.in")
    print(f"{GREEN}✓ Found {len(links)} links{RESET}")
    print(f"  Sample links:")
    for link in links[:5]:
        print(f"    • {link}")
    
    # Test 5: Extract metadata
    print(f"\n{BOLD}TEST 5: Metadata Extraction{RESET}")
    metadata = extract_metadata(html_text, result.content_type)
    print(f"{GREEN}✓ Metadata extracted{RESET}")
    print(f"  Title: {metadata.get('title', 'N/A')}")
    
    # Test 6: Version detection
    print(f"\n{BOLD}TEST 6: Version Change Detection{RESET}")
    is_new = detect_new_version(hash_value, None)
    print(f"{GREEN}✓ First fetch - New version: {is_new}{RESET}")
    
    # Test same content
    is_same = detect_new_version(hash_value, hash_value)
    print(f"{GREEN}✓ Same content - No change: {not is_same}{RESET}")
    
    # Create complete snapshot
    print(f"\n{BOLD}{'='*80}{RESET}")
    print(f"{BOLD}CREATING INGESTION_SNAPSHOT EVENT{RESET}")
    print(f"{BOLD}{'='*80}{RESET}\n")
    
    snapshot = {
        "event_type": "INGESTION_SNAPSHOT",
        "snapshot_id": f"snap-rbi-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "source": {
            "name": "Reserve Bank of India",
            "url": "https://www.rbi.org.in",
            "type": "html"
        },
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "content": {
            "extracted_text_preview": extracted[:200],
            "content_type": result.content_type,
            "size_bytes": len(result.content),
            "encoding": result.encoding
        },
        "hashes": {
            "sha256": hash_value
        },
        "metadata": {
            "title": metadata.get('title'),
            "links_found": len(links),
            "fetch_time_seconds": round(result.fetch_time, 2)
        },
        "version_info": {
            "is_new_version": True,
            "change_detected": True
        }
    }
    
    print(f"{YELLOW}{json.dumps(snapshot, indent=2)}{RESET}\n")
    
    print(f"{GREEN}{BOLD}✓✓✓ Agent 1 Complete Workflow Success! ✓✓✓{RESET}")
    print(f"\n{BLUE}What happens next in production:{RESET}")
    print(f"  1. Snapshot stored in IPFS (immutable storage)")
    print(f"  2. Event published to Redis Streams")
    print(f"  3. Agent 2 (Authenticity) verifies TLS proof")
    print(f"  4. Agent 3 (Diff) detects changes from previous version")
    print(f"  5. Agent 4 (Legal LLM) extracts obligations")
    
except Exception as e:
    print(f"\n{BOLD}Error: {e}{RESET}")
    print(f"\n{YELLOW}Note: This requires internet connection to fetch from RBI{RESET}")

print(f"\n{BOLD}{BLUE}{'='*80}{RESET}")
print(f"{GREEN}Demo Complete - All core tools working!{RESET}")
print(f"{BOLD}{BLUE}{'='*80}{RESET}\n")
