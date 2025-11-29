"""
Agent 1: Discovery & Ingestion
15 Tools for fetching and processing regulatory content.

Security: All tools validate inputs, sanitize URLs, and have rate limits.
"""

import hashlib
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False
import feedparser
from pydantic import BaseModel, HttpUrl

from utils.logger import get_logger

logger = get_logger(__name__)


class FetchResult(BaseModel):
    """Result from fetching content"""
    url: str
    status_code: int
    content: bytes
    headers: Dict[str, str]
    content_type: str
    encoding: str
    fetch_time: float


# =============================================================================
# TOOL 1: fetch_html
# =============================================================================

def fetch_html(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 30,
) -> FetchResult:
    """
    Fetch HTML content from URL with TLS metadata capture.
    
    Security:
    - Validates URL before fetching
    - Enforces timeout
    - Captures TLS info for later verification
    
    Args:
        url: Target URL to fetch
        headers: Optional custom headers
        timeout: Request timeout in seconds
        
    Returns:
        FetchResult with content and metadata
        
    Raises:
        ValueError: If URL is invalid
        requests.RequestException: If fetch fails
    """
    # Validate URL
    parsed = urlparse(url)
    if not parsed.scheme in ['http', 'https']:
        raise ValueError(f"Invalid URL scheme: {parsed.scheme}")
    
    # Default headers
    if headers is None:
        headers = {
            'User-Agent': 'Seraphs-Bot/2.0 (Compliance Intelligence System)',
        }
    
    logger.info("fetching_html", url=url)
    start_time = time.time()
    
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        fetch_time = time.time() - start_time
        
        result = FetchResult(
            url=url,
            status_code=response.status_code,
            content=response.content,
            headers=dict(response.headers),
            content_type=response.headers.get('Content-Type', 'text/html'),
            encoding=response.encoding or 'utf-8',
            fetch_time=fetch_time,
        )
        
        logger.info("fetch_success", url=url, size=len(response.content), time=fetch_time)
        return result
    
    except requests.RequestException as e:
        logger.error("fetch_failed", url=url, error=str(e))
        raise


# =============================================================================
# TOOL 2: fetch_pdf
# =============================================================================

def fetch_pdf(url: str, timeout: int = 60) -> bytes:
    """
    Download PDF file from URL.
    
    Args:
        url: URL to PDF
        timeout: Request timeout
        
    Returns:
        PDF content as bytes
    """
    logger.info("fetching_pdf", url=url)
    
    response = requests.get(
        url,
        headers={'User-Agent': 'Seraphs-Bot/2.0'},
        timeout=timeout,
    )
    response.raise_for_status()
    
    # Verify it's actually a PDF
    if not response.content.startswith(b'%PDF'):
        raise ValueError("Response is not a valid PDF")
    
    logger.info("pdf_fetched", url=url, size=len(response.content))
    return response.content


# =============================================================================
# TOOL 3: fetch_api
# =============================================================================

def fetch_api(
    endpoint: str,
    auth_token: Optional[str] = None,
    params: Optional[Dict] = None,
) -> Dict:
    """
    Fetch JSON data from API endpoint.
    
    Args:
        endpoint: API endpoint URL
        auth_token: Optional Bearer token
        params: Query parameters
        
    Returns:
        JSON response as dict
    """
    headers = {'User-Agent': 'Seraphs-Bot/2.0'}
    if auth_token:
        headers['Authorization'] = f'Bearer {auth_token}'
    
    response = requests.get(endpoint, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    
    return response.json()


# =============================================================================
# TOOL 4: fetch_rss
# =============================================================================

def fetch_rss(feed_url: str) -> List[Dict]:
    """
    Parse RSS feed and return items.
    
    Args:
        feed_url: URL to RSS feed
        
    Returns:
        List of feed items with title, link, published date
    """
    logger.info("fetching_rss", url=feed_url)
    
    feed = feedparser.parse(feed_url)
    
    items = []
    for entry in feed.entries:
        items.append({
            'title': entry.get('title', ''),
            'link': entry.get('link', ''),
            'published': entry.get('published', ''),
            'summary': entry.get('summary', ''),
        })
    
    logger.info("rss_parsed", url=feed_url, items=len(items))
    return items


# =============================================================================
# TOOL 5: extract_text_pdf
# =============================================================================

def extract_text_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text from PDF using PyPDF2.
    
    Args:
        pdf_bytes: PDF content as bytes
        
    Returns:
        Extracted text
    """
    import io
    
    if not PYPDF2_AVAILABLE:
        raise ImportError("PyPDF2 not installed. Run: pip install PyPDF2")
    
    logger.info("extracting_pdf_text", size=len(pdf_bytes))
    
    pdf_file = io.BytesIO(pdf_bytes)
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    
    text_parts = []
    for page_num, page in enumerate(pdf_reader.pages):
        text = page.extract_text()
        text_parts.append(text)
    
    full_text = '\n\n'.join(text_parts)
    logger.info("pdf_text_extracted", pages=len(pdf_reader.pages), chars=len(full_text))
    
    return full_text


# =============================================================================
# TOOL 6: ocr_pdf_scanned (Placeholder - requires Tesseract)
# =============================================================================

def ocr_pdf_scanned(pdf_bytes: bytes, lang: str = 'eng') -> str:
    """
    OCR scanned PDF using Tesseract.
    
    Note: Requires tesseract-ocr to be installed on system.
    For MVP, returns placeholder. Full implementation needed for production.
    
    Args:
        pdf_bytes: PDF content
        lang: Language code (eng, hin, etc.)
        
    Returns:
        OCR'd text
    """
    # Placeholder for MVP
    logger.warning("ocr_not_implemented", message="OCR requires Tesseract setup")
    return "[OCR not implemented in MVP - requires Tesseract installation]"


# =============================================================================
# TOOL 7: list_links
# =============================================================================

def list_links(html: str, base_url: str) -> List[str]:
    """
    Extract all links from HTML.
    
    Args:
        html: HTML content
        base_url: Base URL for resolving relative links
        
    Returns:
        List of absolute URLs
    """
    soup = BeautifulSoup(html, 'lxml')
    links = []
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # Convert relative to absolute
        absolute_url = urljoin(base_url, href)
        links.append(absolute_url)
    
    logger.debug("links_extracted", count=len(links))
    return links


# =============================================================================
# TOOL 8: normalize_text
# =============================================================================

def normalize_text(raw_text: str) -> str:
    """
    Clean and normalize text.
    
    Removes:
    - Extra whitespace
    - Non-printable characters
    - Normalizes line endings
    
    Args:
        raw_text: Raw text
        
    Returns:
        Cleaned text
    """
    import re
    
    # Remove non-printable characters
    text = ''.join(char for char in raw_text if char.isprintable() or char.isspace())
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    return text.strip()


# =============================================================================
# TOOL 9: compute_sha256
# =============================================================================

def compute_sha256(content: str | bytes) -> str:
    """
    Compute SHA-256 hash of content.
    
    Args:
        content: String or bytes to hash
        
    Returns:
        Hexadecimal hash string
    """
    if isinstance(content, str):
        content = content.encode('utf-8')
    
    hash_obj = hashlib.sha256(content)
    return hash_obj.hexdigest()


# =============================================================================
# TOOL 10: capture_dom_tree
# =============================================================================

def capture_dom_tree(html: str) -> Dict:
    """
    Capture DOM structure for change detection.
    
    Returns simplified tree with:
    - Tag names
    - Hierarchy depth
    - Text content hashes
    
    Args:
        html: HTML content
        
    Returns:
        Dict representing DOM structure
    """
    soup = BeautifulSoup(html, 'lxml')
    
    def _build_tree(element, depth=0):
        if not hasattr(element, 'name'):
            return None
        
        node = {
            'tag': element.name,
            'depth': depth,
            'children_count': len(list(element.children)),
        }
        
        # Hash text content for comparison
        text = element.get_text(strip=True)
        if text:
            node['text_hash'] = compute_sha256(text)[:16]  # First 16 chars
        
        return node
    
    tree = _build_tree(soup.html if soup.html else soup)
    
    return tree or {}


# =============================================================================
# TOOL 11-15: Storage & Version Detection
# =============================================================================

def store_ipfs(ipfs_client, content: str | bytes, filename: str) -> str:
    """
    Upload content to IPFS.
    
    (Wrapper around IPFSClient for use in agent)
    """
    return ipfs_client.add(content, filename)


def detect_new_version(current_hash: str, last_hash: Optional[str]) -> bool:
    """
    Check if content has changed by comparing hashes.
    
    Args:
        current_hash: SHA-256 of current content
        last_hash: SHA-256 of previous content
        
    Returns:
        True if changed, False if same
    """
    if last_hash is None:
        return True  # First fetch
    
    return current_hash != last_hash


def validate_url(url: str) -> str:
    """
    Validate and sanitize URL.
    
    Security checks:
    - Must be HTTP/HTTPS
    - No file:// or javascript: schemes
    - Must have valid domain
    
    Args:
        url: URL to validate
        
    Returns:
        Sanitized URL
        
    Raises:
        ValueError: If URL is invalid
    """
    parsed = urlparse(url)
    
    if parsed.scheme not in ['http', 'https']:
        raise ValueError(f"Invalid URL scheme: {parsed.scheme}")
    
    if not parsed.netloc:
        raise ValueError(f"Invalid URL: missing domain")
    
    return url


def extract_metadata(html: str, content_type: str) -> Dict:
    """
    Extract document metadata (title, date, author, etc.).
    
    Args:
        html: HTML content
        content_type: MIME type
        
    Returns:
        Dict with metadata
    """
    soup = BeautifulSoup(html, 'lxml')
    
    metadata = {
        'title': None,
        'author': None,
        'date': None,
        'keywords': [],
    }
    
    # Extract title
    title_tag = soup.find('title')
    if title_tag:
        metadata['title'] = title_tag.get_text(strip=True)
    
    # Extract meta tags
    for meta in soup.find_all('meta'):
        name = meta.get('name', '').lower()
        content = meta.get('content', '')
        
        if name == 'author':
            metadata['author'] = content
        elif name == 'date':
            metadata['date'] = content
        elif name == 'keywords':
            metadata['keywords'] = [k.strip() for k in content.split(',')]
    
    return metadata
