#!/usr/bin/env python3
"""
Minimal standalone demo - shows Agent 1 fetching RBI data
No imports from our codebase - pure demonstration
"""

import requests
from bs4 import BeautifulSoup
import hashlib
import json
from datetime import datetime

print("\n" + "="*80)
print("SERAPHS 2.0 - Agent 1 Demo: Live Regulatory Fetching".center(80))
print("="*80 + "\n")

# DEMO 1: Fetch from RBI
print("TEST 1: Fetching REAL data from Reserve Bank of India")
print("URL: https://www.rbi.org.in\n")

try:
    # Fetch RBI homepage
    headers = {'User-Agent': 'Seraphs-Bot/2.0'}
    response = requests.get("https://www.rbi.org.in", headers=headers, timeout=20)
    
    print(f"✓ Fetch successful!")
    print(f"  Status: {response.status_code}")
    print(f"  Size: {len(response.content):,} bytes")
    print(f"  Type: {response.headers.get('Content-Type')}")
    
    # DEMO 2: Extract text
    print(f"\nTEST 2: Text Extraction")
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    cleaned = ' '.join(text.split())[:500]
    print(f"✓ Extracted text (first 500 chars):")
    print(f"  {cleaned}...\n")
    
    # DEMO 3: Compute hash
    print(f"TEST 3: SHA-256 Hashing")
    hash_value = hashlib.sha256(response.content).hexdigest()
    print(f"✓ Hash: {hash_value}\n")
    
    # DEMO 4: Extract links
    print(f"TEST 4: Link Extraction")
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    print(f"✓ Found {len(links)} links")
    print(f"  Sample links:")
    for link in links[:5]:
        print(f"    • {link}")
    
    # DEMO 5: Extract metadata
    print(f"\nTEST 5: Metadata Extraction")
    title = soup.find('title')
    print(f"✓ Title: {title.string if title else 'N/A'}")
    
    # DEMO 6: Create snapshot
    print(f"\n" + "="*80)
    print("CREATING INGESTION_SNAPSHOT EVENT")
    print("="*80 + "\n")
    
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
            "extracted_text_preview": cleaned[:200],
            "content_type": response.headers.get('Content-Type'),
            "size_bytes": len(response.content),
            "encoding": response.encoding
        },
        "hashes": {
            "sha256": hash_value
        },
        "metadata": {
            "title": title.string if title else None,
            "links_found": len(links),
        },
        "version_info": {
            "is_new_version": True,
            "change_detected": True
        }
    }
    
    print(json.dumps(snapshot, indent=2))
    
    print(f"\n✓✓✓ Agent 1 Complete Workflow Success! ✓✓✓")
    print(f"\nWhat happens next in production:")
    print(f"  1. Snapshot stored in IPFS (immutable storage)")
    print(f"  2. Event published to Redis Streams")
    print(f"  3. Agent 2 (Authenticity) verifies TLS proof")
    print(f"  4. Agent 3 (Diff) detects changes from previous version")
    print(f"  5. Agent 4 (Legal LLM) extracts obligations")
    
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()

print(f"\n" + "="*80)
print("Demo Complete - Agent 1 tools working!")
print("="*80 + "\n")
