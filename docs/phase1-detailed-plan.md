# Phase 1: Detailed Implementation Plan
## Discovery & Ingestion Agent + Project Foundation

---

## 🎯 PHASE 1 OBJECTIVES

Build the **Discovery & Ingestion Agent** that:
1. Fetches regulatory content from 12 priority sources
2. Extracts text from HTML/PDF/RSS feeds
3. Computes cryptographic hashes (SHA-256)
4. Stores raw content in IPFS
5. Publishes `INGESTION_SNAPSHOT` events to Redis
6. Runs on configurable schedules (hourly/daily/weekly)
7. Detects version changes automatically

---

## 📋 PRIORITY REGULATORY SOURCES (12 Sources)

### **India (Priority for IBW Hackathon)**
1. **RBI (Reserve Bank of India)**
   - URL: https://www.rbi.org.in/Scripts/NotificationUser.aspx
   - Type: HTML table with notifications
   - Frequency: Daily (high volume)
   - Format: HTML + PDF circulars
   
2. **SEBI (Securities & Exchange Board of India)**
   - URL: https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=4&ssid=18&smid=0
   - Type: Circular listings
   - Frequency: Daily
   - Format: HTML + PDF
   
3. **Ministry of Finance (India)**
   - URL: https://dea.gov.in/press-release
   - Type: Press releases & notifications
   - Frequency: Weekly
   - Format: HTML

4. **IRDAI (Insurance Regulator)**
   - URL: https://irdai.gov.in/regulations
   - Type: Regulations & circulars
   - Frequency: Weekly
   - Format: PDF

### **International (High Impact)**
5. **GDPR Portal (EU)**
   - URL: https://gdpr.eu/category/regulatory-updates/
   - Type: RSS feed + articles
   - Frequency: Weekly
   - Format: RSS + HTML

6. **US SEC (Securities Exchange Commission)**
   - URL: https://www.sec.gov/news/pressreleases
   - Type: Press releases
   - Frequency: Daily
   - Format: HTML + RSS

7. **US Federal Register**
   - URL: https://www.federalregister.gov/documents/search?conditions%5Bagencies%5D%5B%5D=securities-and-exchange-commission
   - Type: Official regulations
   - Frequency: Daily
   - Format: HTML + API

8. **MAS Singapore**
   - URL: https://www.mas.gov.sg/news
   - Type: News & regulations
   - Frequency: Weekly
   - Format: HTML

### **Additional Fintech Sources**
9. **FCA UK**
   - URL: https://www.fca.org.uk/news
   - Type: News & policy updates
   - Frequency: Weekly
   - Format: HTML + RSS

10. **OFAC (Sanctions)**
    - URL: https://home.treasury.gov/policy-issues/financial-sanctions/recent-actions
    - Type: Sanctions updates
    - Frequency: Daily
    - Format: HTML + XML

11. **FATF (Financial Action Task Force)**
    - URL: https://www.fatf-gafi.org/en/publications.html
    - Type: Guidelines & reports
    - Frequency: Monthly
    - Format: PDF

12. **CERT-In (Cybersecurity)**
    - URL: https://www.cert-in.org.in/
    - Type: Security advisories
    - Frequency: Weekly
    - Format: HTML

---

## 🔄 FETCH FREQUENCY & SCHEDULING

### **Tiered Monitoring Strategy**:

| Priority | Sources | Frequency | Rationale |
|----------|---------|-----------|-----------|
| **Critical** | RBI, SEBI, SEC | Every 6 hours | High-volume, time-sensitive |
| **High** | GDPR, Federal Register, OFAC | Every 12 hours | Compliance deadlines |
| **Medium** | MAS, FCA, IRDAI | Daily | Regular updates |
| **Low** | FATF, CERT-In, MoF | Weekly | Lower frequency |

### **Implementation**:
- **Cron-style scheduler** using APScheduler
- **Configurable per source** via YAML config
- **Manual trigger** available via API
- **Rate limiting**: Max 1 request/minute per domain

---

## 📊 OUTPUT STRUCTURE

### **INGESTION_SNAPSHOT Event**:
```json
{
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_type": "INGESTION_SNAPSHOT",
  "trace_id": "trace-2025-11-29-001",
  "timestamp": "2025-11-29T10:30:00Z",
  "source_agent": "agent-1-ingestion",
  "payload": {
    "snapshot_id": "snap-rbi-2025-11-29-103000",
    "source": {
      "name": "RBI",
      "url": "https://www.rbi.org.in/Scripts/NotificationUser.aspx",
      "type": "html"
    },
    "fetched_at": "2025-11-29T10:30:00Z",
    "content": {
      "raw_html": "<html>...</html>",
      "extracted_text": "Circular on KYC norms...",
      "content_type": "text/html",
      "encoding": "utf-8",
      "size_bytes": 45678
    },
    "hashes": {
      "sha256": "a3c7f8e2...",
      "md5": "8f2e9a1b..."
    },
    "storage": {
      "ipfs_cid": "QmX7Y8Z...",
      "ipfs_gateway_url": "https://ipfs.io/ipfs/QmX7Y8Z..."
    },
    "metadata": {
      "dom_tree_depth": 12,
      "external_links": 5,
      "pdf_links": 3,
      "last_modified": "2025-11-28T15:00:00Z"
    },
    "version_info": {
      "is_new_version": true,
      "previous_hash": "b4d8f9e3...",
      "change_detected": true
    }
  }
}
```

### **Storage Locations**:
1. **Raw Content**: IPFS (immutable, content-addressed)
2. **Metadata**: PostgreSQL (queryable, indexed)
3. **Events**: Redis Streams (event bus)
4. **Snapshots**: Local cache (7 days retention)

---

## 🛠️ AGENT 1 TOOLS (15 Tools)

### **1. fetch_html**
```python
def fetch_html(url: str, headers: dict = None, timeout: int = 30) -> FetchResult:
    """
    Fetch HTML content with TLS metadata capture
    
    Args:
        url: Target URL
        headers: Custom headers
        timeout: Request timeout in seconds
    
    Returns:
        FetchResult with content, status, headers, TLS info
    """
```

### **2. fetch_pdf**
```python
def fetch_pdf(url: str) -> bytes:
    """Download PDF file"""
```

### **3. fetch_api**
```python
def fetch_api(endpoint: str, auth_token: str = None, params: dict = None) -> dict:
    """Fetch JSON from API endpoint"""
```

### **4. fetch_rss**
```python
def fetch_rss(feed_url: str) -> List[RSSItem]:
    """Parse RSS feed and return items"""
```

### **5. extract_text_pdf**
```python
def extract_text_pdf(pdf_bytes: bytes) -> str:
    """Extract text from PDF using PyPDF2"""
```

### **6. ocr_pdf_scanned**
```python
def ocr_pdf_scanned(pdf_bytes: bytes, lang: str = 'eng') -> str:
    """OCR scanned PDF using Tesseract"""
```

### **7. list_links**
```python
def list_links(html: str, base_url: str) -> List[str]:
    """Extract all links from HTML using BeautifulSoup"""
```

### **8. normalize_text**
```python
def normalize_text(raw_text: str) -> str:
    """Clean and normalize text (remove extra whitespace, etc.)"""
```

### **9. compute_sha256**
```python
def compute_sha256(content: Union[str, bytes]) -> str:
    """Compute SHA-256 hash"""
```

### **10. capture_dom_tree**
```python
def capture_dom_tree(html: str) -> dict:
    """Capture DOM structure for change detection"""
```

### **11. store_ipfs**
```python
def store_ipfs(content: Union[str, bytes], filename: str) -> str:
    """Upload to IPFS, return CID"""
```

### **12. detect_new_version**
```python
def detect_new_version(url: str, current_hash: str) -> bool:
    """Check if content changed since last fetch"""
```

### **13. schedule_watch**
```python
def schedule_watch(source_config: SourceConfig) -> str:
    """Schedule periodic monitoring, return job_id"""
```

### **14. validate_url**
```python
def validate_url(url: str) -> str:
    """Validate and sanitize URL"""
```

### **15. extract_metadata**
```python
def extract_metadata(html: str, content_type: str) -> dict:
    """Extract metadata (title, date, author, etc.)"""
```

---

## 🏗️ PROJECT STRUCTURE

```
/Users/priyeshsrivastava/Seraphs/
├── agents/
│   ├── __init__.py
│   ├── agent_1_ingestion/
│   │   ├── __init__.py
│   │   ├── agent.py          # Main agent logic
│   │   ├── tools.py          # 15 tools implementation
│   │   ├── config.yaml       # Source configurations
│   │   └── scheduler.py      # APScheduler setup
│   ├── agent_2_auth/
│   ├── agent_3_diff/
│   └── ... (agents 4-12)
├── orchestration/
│   ├── __init__.py
│   ├── langgraph_flow.py     # LangGraph state machine
│   ├── state.py              # State definitions
│   └── router.py             # Event routing
├── schemas/
│   ├── __init__.py
│   ├── events.py             # Event schemas (Pydantic)
│   ├── agent_io.py           # Agent I/O schemas
│   └── state.py              # State schemas
├── utils/
│   ├── __init__.py
│   ├── event_bus.py          # Redis Streams wrapper
│   ├── ipfs_client.py        # IPFS client
│   ├── logger.py             # Structured logging
│   ├── security.py           # Security utilities
│   └── config.py             # Config loader
├── tests/
│   ├── test_agent_1.py
│   ├── test_tools.py
│   └── fixtures/
│       └── mock_rbi_page.html
├── docs/
│   ├── architecture.md
│   ├── phase1-detailed-plan.md
│   └── api-docs.md
├── tasks/
│   └── todo.md
├── docker/
│   ├── Dockerfile.agent-1
│   ├── Dockerfile.orchestrator
│   └── docker-compose.yml
├── config/
│   ├── sources.yaml          # Regulatory source configs
│   ├── schedules.yaml        # Fetch schedules
│   └── dev.env.example
├── pyproject.toml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 📦 DEPENDENCIES (requirements.txt)

```txt
# Core Framework
python>=3.11
pydantic>=2.5.0
python-dotenv>=1.0.0

# LangGraph & LangChain
langgraph>=0.0.40
langchain>=0.1.0
langchain-anthropic>=0.1.0  # Claude
langchain-openai>=0.0.5     # GPT (backup)

# Event Bus
redis>=5.0.0
redis-streams>=0.2.0

# Storage
ipfs-api>=0.2.3
py-ipfs-http-client>=0.8.0
psycopg2-binary>=2.9.9      # PostgreSQL

# Web Fetching
requests>=2.31.0
httpx>=0.25.0               # Async HTTP
beautifulsoup4>=4.12.0
lxml>=4.9.3

# PDF Processing
PyPDF2>=3.0.0
pdfplumber>=0.10.0
pytesseract>=0.3.10         # OCR

# RSS Parsing
feedparser>=6.0.10

# Scheduling
APScheduler>=3.10.0

# Security
cryptography>=41.0.0
pycardano>=0.9.0           # Cardano

# API Framework
fastapi>=0.104.0
uvicorn>=0.24.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-mock>=3.12.0

# Logging & Monitoring
structlog>=23.2.0
```

---

## ⚙️ CONFIGURATION FILES

### **config/sources.yaml**
```yaml
sources:
  - id: rbi
    name: "Reserve Bank of India"
    url: "https://www.rbi.org.in/Scripts/NotificationUser.aspx"
    type: html
    schedule: "0 */6 * * *"  # Every 6 hours
    priority: critical
    parser: rbi_notifications
    
  - id: sebi
    name: "SEBI India"
    url: "https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=4&ssid=18&smid=0"
    type: html
    schedule: "0 */6 * * *"
    priority: critical
    parser: sebi_circulars
    
  - id: gdpr
    name: "GDPR Portal"
    url: "https://gdpr.eu/category/regulatory-updates/"
    type: rss
    schedule: "0 */12 * * *"  # Every 12 hours
    priority: high
    parser: generic_rss
    
  # ... (more sources)
```

---

## 🔐 SECURITY MEASURES (Phase 1)

1. **URL Validation**:
   - Whitelist-only approach (only configured domains)
   - No URL manipulation by LLM
   - SSRF prevention

2. **Rate Limiting**:
   - Max 1 request/minute per domain
   - Exponential backoff on errors
   - Respect robots.txt

3. **Content Validation**:
   - Max file size: 50MB
   - Allowed MIME types: text/html, application/pdf, application/rss+xml
   - Virus scanning for PDFs (optional)

4. **Secrets Management**:
   - No hardcoded credentials
   - Environment variables only
   - .env.example template provided

5. **IPFS Security**:
   - Private IPFS node (not public gateway)
   - Content encryption option
   - Access control on CIDs

---

## 🧪 TESTING STRATEGY

### **Unit Tests**:
- Test each of 15 tools independently
- Mock HTTP responses
- Mock IPFS client
- Mock Redis

### **Integration Tests**:
- End-to-end fetch → extract → store → event publish
- Real IPFS local node
- Real Redis local instance

### **Fixtures**:
- `mock_rbi_page.html` - Sample RBI notification page
- `mock_sebi_circular.pdf` - Sample PDF
- `mock_rss_feed.xml` - Sample RSS feed

---

## 📈 SUCCESS CRITERIA (Phase 1)

- [ ] Agent 1 successfully fetches from all 12 sources
- [ ] Text extraction works for HTML + PDF
- [ ] SHA-256 hashes computed correctly
- [ ] Content stored in IPFS (local node)
- [ ] Events published to Redis Streams
- [ ] Scheduler runs on configured intervals
- [ ] Version change detection works
- [ ] All 15 tools have unit tests (>80% coverage)
- [ ] Integration test passes end-to-end
- [ ] Docker container builds and runs

---

## ⏱️ TIMELINE

| Task | Duration | Status |
|------|----------|--------|
| Project structure setup | 30 min | Pending |
| Dependencies installation | 15 min | Pending |
| Schema definitions | 45 min | Pending |
| Event bus utility | 1 hour | Pending |
| IPFS client utility | 30 min | Pending |
| Agent 1 tool implementations | 3 hours | Pending |
| Agent 1 core logic | 2 hours | Pending |
| Scheduler setup | 1 hour | Pending |
| Unit tests | 2 hours | Pending |
| Integration tests | 1 hour | Pending |
| Docker setup | 1 hour | Pending |
| **Total** | **~12 hours** | - |

---

## 🚀 EXECUTION PLAN

### **Step 1**: Create project structure (directories, __init__.py files)
### **Step 2**: Setup configuration files (sources.yaml, .env.example)
### **Step 3**: Install dependencies (requirements.txt)
### **Step 4**: Define Pydantic schemas (events, agent I/O)
### **Step 5**: Build utilities (event_bus, ipfs_client, logger)
### **Step 6**: Implement 15 tools for Agent 1
### **Step 7**: Implement Agent 1 core orchestration
### **Step 8**: Setup APScheduler for periodic fetching
### **Step 9**: Write unit tests
### **Step 10**: Write integration test
### **Step 11**: Create Dockerfile
### **Step 12**: Test end-to-end locally

---

## 🎯 DEMO OUTPUT (After Phase 1)

You'll be able to run:
```bash
# Start Redis + IPFS locally
docker-compose up -d redis ipfs

# Run Agent 1
python -m agents.agent_1_ingestion.agent

# View events in Redis
redis-cli XREAD STREAMS seraphs:agent-1:events 0
```

**Expected Output**:
- Agent fetches from RBI, SEBI, GDPR, etc.
- Extracts text from HTML/PDF
- Computes hashes
- Stores in IPFS
- Publishes `INGESTION_SNAPSHOT` events
- Scheduler runs every 6/12/24 hours based on config

---

**Ready to execute Phase 1?** I'll start with project setup and Agent 1 implementation.

**Estimated Time**: 12 hours of coding (can be done across 2-3 sessions)

**Next Phase Preview**: Phase 2 will add Agent 2 (TLS proofs) and Agent 3 (Diff detection) to process these snapshots.
