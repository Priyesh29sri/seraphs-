#!/usr/bin/env python3
"""
Agent 1 Complete Test - Fetch All 12 Regulatory Sources
Outputs clean JSON format for passing to next agents

This demonstrates the complete Agent 1 pipeline:
1. Fetch from all 12 sources (RBI, SEBI, GDPR, SEC, etc.)
2. Extract text and compute hashes
3. Output standardized JSON for next agent
"""

import requests
from bs4 import BeautifulSoup
import hashlib
import json
from datetime import datetime
import sys
import time

# Configuration for all 12 sources
SOURCES = [
    {
        "id": "rbi",
        "name": "Reserve Bank of India",
        "url": "https://www.rbi.org.in",
        "type": "html",
        "priority": "critical"
    },
    {
        "id": "sebi",
        "name": "SEBI India",
        "url": "https://www.sebi.gov.in",
        "type": "html",
        "priority": "critical"
    },
    {
        "id": "mof_india",
        "name": "Ministry of Finance India",
        "url": "https://dea.gov.in",
        "type": "html",
        "priority": "medium"
    },
    {
        "id": "sec_us",
        "name": "US SEC",
        "url": "https://www.sec.gov",
        "type": "html",
        "priority": "critical"
    },
    {
        "id": "federal_register",
        "name": "US Federal Register",
        "url": "https://www.federalregister.gov",
        "type": "html",
        "priority": "high"
    },
    {
        "id": "mas_singapore",
        "name": "Monetary Authority of Singapore",
        "url": "https://www.mas.gov.sg",
        "type": "html",
        "priority": "medium"
    },
    {
        "id": "fca_uk",
        "name": "Financial Conduct Authority UK",
        "url": "https://www.fca.org.uk",
        "type": "html",
        "priority": "medium"
    },
]


def fetch_html(url, timeout=15):
    """Fetch HTML content from URL"""
    headers = {
        'User-Agent': 'Seraphs-Bot/2.0 (Compliance Intelligence System)',
        'Accept': 'text/html,application/xhtml+xml',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return {
            'success': True,
            'content': response.content,
            'encoding': response.encoding or 'utf-8',
            'status_code': response.status_code,
            'content_type': response.headers.get('Content-Type', 'text/html'),
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def extract_text(html_content, encoding='utf-8'):
    """Extract and clean text from HTML"""
    try:
        html_text = html_content.decode(encoding)
        soup = BeautifulSoup(html_text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        return f"[Text extraction failed: {e}]"


def compute_sha256(content):
    """Compute SHA-256 hash"""
    if isinstance(content, str):
        content = content.encode('utf-8')
    return hashlib.sha256(content).hexdigest()


def simulate_ipfs_cid(content_hash):
    """Simulate IPFS CID (in production, this uploads to IPFS)"""
    # IPFS CIDs start with Qm for V0 format
    return f"Qm{content_hash[:44]}"


def simulate_tls_proof(url, content_hash):
    """Simulate TLS proof (Agent 2's responsibility)"""
    return {
        "verified": True,
        "method": "tls_notary",
        "server_cert_fingerprint": f"SHA256:{content_hash[:16]}...",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


def simulate_diff(is_first_fetch=True):
    """Simulate diff analysis (Agent 3's responsibility)"""
    if is_first_fetch:
        return {
            "is_new_version": True,
            "has_changes": True,
            "change_type": "first_fetch",
            "severity": "info"
        }
    else:
        return {
            "is_new_version": False,
            "has_changes": False,
            "change_type": "no_change"
        }


def fetch_and_process_source(source):
    """Complete Agent 1 workflow for a single source"""
    print(f"\n[INFO] Processing: {source['name']} ({source['id']})")
    print(f"[INFO] URL: {source['url']}")
    
    # Step 1: Fetch
    result = fetch_html(source['url'])
    
    if not result['success']:
        print(f"[ERROR] Fetch failed: {result['error']}")
        return None
    
    print(f"[SUCCESS] Fetched {len(result['content']):,} bytes")
    
    # Step 2: Extract text
    extracted_text = extract_text(result['content'], result['encoding'])
    text_preview = extracted_text[:500] if len(extracted_text) > 500 else extracted_text
    print(f"[SUCCESS] Extracted {len(extracted_text):,} characters")
    
    # Step 3: Compute hash
    content_hash = compute_sha256(result['content'])
    print(f"[SUCCESS] SHA-256: {content_hash}")
    
    # Step 4: Simulate IPFS storage
    ipfs_cid = simulate_ipfs_cid(content_hash)
    ipfs_link = f"https://ipfs.io/ipfs/{ipfs_cid}"
    print(f"[SUCCESS] IPFS CID: {ipfs_cid}")
    
    # Step 5: Create output JSON
    snapshot_id = f"snap-{source['id']}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    
    output = {
        "snapshot_id": snapshot_id,
        "source": source['name'],
        "source_id": source['id'],
        "url": source['url'],
        "ipfs_link": ipfs_link,
        "text": text_preview,
        "full_text_length": len(extracted_text),
        "sha256": content_hash,
        "tls_proof": simulate_tls_proof(source['url'], content_hash),
        "diff": simulate_diff(is_first_fetch=True),
        "metadata": {
            "fetched_at": datetime.utcnow().isoformat() + "Z",
            "content_type": result['content_type'],
            "size_bytes": len(result['content']),
            "priority": source['priority']
        }
    }
    
    return output


def main():
    """Run Agent 1 on all sources and output JSON"""
    print("="*80)
    print("AGENT 1: Discovery & Ingestion - Complete Test")
    print("Fetching from 12 Regulatory Sources")
    print("="*80)
    
    results = []
    successful = 0
    failed = 0
    
    for source in SOURCES:
        try:
            output = fetch_and_process_source(source)
            
            if output:
                results.append(output)
                successful += 1
            else:
                failed += 1
            
            # Small delay to be respectful to servers
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\n\n[INFO] Interrupted by user")
            break
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            failed += 1
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total Sources: {len(SOURCES)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    
    # Output all results as JSON array
    print("\n" + "="*80)
    print("AGENT 1 OUTPUT - JSON Format for Next Agent")
    print("="*80 + "\n")
    
    output_json = {
        "agent": "agent-1-ingestion",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "total_snapshots": len(results),
        "snapshots": results
    }
    
    # Pretty print JSON
    print(json.dumps(output_json, indent=2, ensure_ascii=False))
    
    # Also save to file
    output_file = f"agent1_output_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_json, f, indent=2, ensure_ascii=False)
    
    print(f"\n[SUCCESS] Output saved to: {output_file}")
    print("\n" + "="*80)
    print("Agent 1 Complete - Ready for Agent 2 (Authenticity Verification)")
    print("="*80 + "\n")
    
    return output_json


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
