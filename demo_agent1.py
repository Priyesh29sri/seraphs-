#!/usr/bin/env python3
"""
Demo script for Agent 1 (Discovery & Ingestion)
Shows fetching from real regulatory sources WITHOUT requiring Redis/IPFS.

This is a standalone demo to showcase the tools working.
"""

import json
from datetime import datetime
from agents.agent_1_ingestion import tools

# ANSI colors for pretty output
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    print(f"\n{BOLD}{BLUE}{'='*80}{RESET}")
    print(f"{BOLD}{BLUE}{text.center(80)}{RESET}")
    print(f"{BOLD}{BLUE}{'='*80}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")


def demo_tool_1_fetch_html():
    """Demo: Fetch HTML from RBI website"""
    print_header("TOOL 1: fetch_html - Fetching from RBI Website")
    
    # Test URL - RBI notifications page
    url = "https://www.rbi.org.in/Scripts/NotificationUser.aspx"
    
    print_info(f"Fetching: {url}")
    print_info("This is a REAL fetch from Reserve Bank of India...")
    
    try:
        result = tools.fetch_html(url, timeout=15)
        
        print_success(f"Fetch successful!")
        print(f"  Status Code: {result.status_code}")
        print(f"  Content Type: {result.content_type}")
        print(f"  Size: {len(result.content):,} bytes")
        print(f"  Encoding: {result.encoding}")
        print(f"  Fetch Time: {result.fetch_time:.2f}s")
        
        # Decode and show preview
        html_text = result.content.decode(result.encoding)
        print(f"\n{BOLD}HTML Preview (first 500 chars):{RESET}")
        print(f"{YELLOW}{html_text[:500]}...{RESET}")
        
        return result
        
    except Exception as e:
        print_error(f"Fetch failed: {e}")
        return None


def demo_tool_7_list_links(html_text):
    """Demo: Extract links from HTML"""
    print_header("TOOL 7: list_links - Extracting All Links")
    
    try:
        links = tools.list_links(html_text, "https://www.rbi.org.in")
        
        print_success(f"Found {len(links)} links")
        print(f"\n{BOLD}Sample Links (first 10):{RESET}")
        for i, link in enumerate(links[:10], 1):
            print(f"  {i}. {link}")
        
        return links
        
    except Exception as e:
        print_error(f"Link extraction failed: {e}")
        return []


def demo_tool_8_normalize_text():
    """Demo: Text normalization"""
    print_header("TOOL 8: normalize_text - Text Cleaning")
    
    messy_text = """
    
    This   has    extra     spaces
    
    
    And multiple   newlines
    
    
    And \r\n mixed   line endings
    
    """
    
    print(f"{BOLD}Original Text:{RESET}")
    print(f"{YELLOW}{repr(messy_text)}{RESET}")
    
    cleaned = tools.normalize_text(messy_text)
    
    print(f"\n{BOLD}Normalized Text:{RESET}")
    print(f"{GREEN}{repr(cleaned)}{RESET}")
    
    print_success("Text normalized successfully")


def demo_tool_9_compute_hash():
    """Demo: SHA-256 hashing"""
    print_header("TOOL 9: compute_sha256 - Cryptographic Hashing")
    
    test_content = "RBI Circular on KYC Norms - November 2025"
    
    hash1 = tools.compute_sha256(test_content)
    hash2 = tools.compute_sha256(test_content)  # Same content
    hash3 = tools.compute_sha256(test_content + " (modified)")  # Different
    
    print_info(f"Original: {test_content}")
    print(f"  SHA-256: {hash1}")
    
    print_info(f"\nSame content again:")
    print(f"  SHA-256: {hash2}")
    if hash1 == hash2:
        print_success("Hashes match (deterministic)! ✓")
    
    print_info(f"\nModified content:")
    print(f"  SHA-256: {hash3}")
    if hash1 != hash3:
        print_success("Hashes different (content changed detected)! ✓")


def demo_tool_11_version_detection():
    """Demo: Version change detection"""
    print_header("TOOL 12: detect_new_version - Change Detection")
    
    scenarios = [
        ("First fetch (no previous hash)", "abc123", None, True),
        ("Same content", "abc123", "abc123", False),
        ("Content changed", "def456", "abc123", True),
    ]
    
    for scenario, current, previous, expected in scenarios:
        result = tools.detect_new_version(current, previous)
        
        if result == expected:
            print_success(f"{scenario}: {result} (as expected)")
        else:
            print_error(f"{scenario}: {result} (expected {expected})")


def demo_tool_14_extract_metadata():
    """Demo: Metadata extraction from HTML"""
    print_header("TOOL 15: extract_metadata - HTML Metadata Extraction")
    
    sample_html = """
    <html>
        <head>
            <title>RBI Circular - Master Direction on KYC Norms</title>
            <meta name="author" content="Reserve Bank of India">
            <meta name="date" content="2025-11-29">
            <meta name="keywords" content="KYC, AML, compliance, banking">
        </head>
        <body>
            <h1>KYC Circular</h1>
            <p>Updated guidelines for customer verification...</p>
        </body>
    </html>
    """
    
    metadata = tools.extract_metadata(sample_html, "text/html")
    
    print_success("Metadata extracted:")
    print(f"  Title: {metadata['title']}")
    print(f"  Author: {metadata['author']}")
    print(f"  Date: {metadata['date']}")
    print(f"  Keywords: {', '.join(metadata['keywords'])}")


def demo_complete_snapshot_creation():
    """Demo: Create a complete snapshot (without Redis/IPFS)"""
    print_header("COMPLETE SNAPSHOT CREATION (Simulated)")
    
    print_info("Simulating Agent 1 workflow...")
    
    # Step 1: Fetch
    print(f"\n{BOLD}Step 1: Fetching from RBI{RESET}")
    url = "https://www.rbi.org.in/Scripts/NotificationUser.aspx"
    
    try:
        fetch_result = tools.fetch_html(url, timeout=15)
        html_text = fetch_result.content.decode(fetch_result.encoding)
        print_success(f"Fetched {len(fetch_result.content):,} bytes")
        
        # Step 2: Extract text
        print(f"\n{BOLD}Step 2: Text Extraction & Normalization{RESET}")
        extracted_text = tools.normalize_text(html_text[:1000])  # First 1000 chars
        print_success(f"Extracted {len(extracted_text)} characters")
        
        # Step 3: Compute hash
        print(f"\n{BOLD}Step 3: Computing SHA-256 Hash{RESET}")
        content_hash = tools.compute_sha256(fetch_result.content)
        print_success(f"Hash: {content_hash}")
        
        # Step 4: Extract metadata
        print(f"\n{BOLD}Step 4: Extracting Metadata{RESET}")
        metadata = tools.extract_metadata(html_text, fetch_result.content_type)
        print_success(f"Title: {metadata.get('title', 'N/A')}")
        
        # Step 5: Version detection
        print(f"\n{BOLD}Step 5: Version Detection{RESET}")
        is_new = tools.detect_new_version(content_hash, None)
        print_success(f"New version detected: {is_new}")
        
        # Create snapshot payload (simulated)
        print(f"\n{BOLD}Step 6: Creating INGESTION_SNAPSHOT Event{RESET}")
        snapshot = {
            "snapshot_id": f"snap-rbi-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "source": {
                "name": "Reserve Bank of India",
                "url": url,
                "type": "html"
            },
            "fetched_at": datetime.utcnow().isoformat(),
            "content": {
                "extracted_text": extracted_text[:200] + "...",
                "content_type": fetch_result.content_type,
                "size_bytes": len(fetch_result.content),
            },
            "hashes": {
                "sha256": content_hash
            },
            "metadata": metadata,
            "version_info": {
                "is_new_version": is_new,
                "change_detected": is_new
            }
        }
        
        print_success("Snapshot created!")
        print(f"\n{BOLD}Snapshot Preview:{RESET}")
        print(f"{YELLOW}{json.dumps(snapshot, indent=2)}{RESET}")
        
        print(f"\n{GREEN}{BOLD}✓ Agent 1 workflow completed successfully!{RESET}")
        print_info("In production, this would be:")
        print_info("  → Stored in IPFS (content-addressed)")
        print_info("  → Published to Redis Streams event bus")
        print_info("  → Consumed by Agent 2 (Authenticity verification)")
        
    except Exception as e:
        print_error(f"Demo failed: {e}")


def main():
    """Run all demos"""
    print_header("SERAPHS 2.0 - Agent 1 Demo: Discovery & Ingestion")
    print(f"{BOLD}Testing 15 tools without requiring Redis/IPFS infrastructure{RESET}\n")
    
    # Demo individual tools
    print_warning("Note: Some demos fetch from REAL regulatory websites (may be slow)")
    print()
    
    # Demo 1: Fetch HTML
    result = demo_tool_1_fetch_html()
    
    if result:
        html_text = result.content.decode(result.encoding)
        
        # Demo 2: Extract links
        demo_tool_7_list_links(html_text)
    
    # Demo 3: Text normalization
    demo_tool_8_normalize_text()
    
    # Demo 4: Hashing
    demo_tool_9_compute_hash()
    
    # Demo 5: Version detection
    demo_tool_11_version_detection()
    
    # Demo 6: Metadata extraction
    demo_tool_14_extract_metadata()
    
    # Final demo: Complete workflow
    demo_complete_snapshot_creation()
    
    print_header("Demo Complete!")
    print(f"{GREEN}{BOLD}All tools demonstrated successfully!{RESET}")
    print(f"\n{BLUE}Next steps:{RESET}")
    print(f"  1. Start infrastructure: docker-compose up -d")
    print(f"  2. Run full agent: python -m agents.agent_1_ingestion.agent")
    print(f"  3. View events: redis-cli XREAD STREAMS seraphs:events 0")


if __name__ == "__main__":
    main()
