# Quick Start Guide - Running Agent 1

## Prerequisites

Install all required dependencies:

```bash
cd /Users/priyeshsrivastava/Seraphs

# Install Python dependencies
pip install requests beautifulsoup4 lxml pydantic python-dotenv pyyaml feedparser PyPDF2

# For full system (Redis, IPFS)
pip install redis ipfshttpclient structlog
```

## Option 1: Quick Demo (No Infrastructure Required)

Test individual tools without Redis/IPFS:

```bash
python -c "
from agents.agent_1_ingestion.tools import fetch_html, compute_sha256, normalize_text

# Fetch from RBI  
result = fetch_html('https://www.rbi.org.in', timeout=20)
print(f'✓ Fetched {len(result.content):,} bytes from RBI')

# Compute hash
hash_val = compute_sha256(result.content)
print(f'✓ SHA-256: {hash_val}')

print('✓ Agent 1 tools working!')
"
```

## Option 2: Full Agent with Infrastructure

### Step 1: Start Infrastructure

```bash
# Start Redis + IPFS + PostgreSQL
docker-compose up -d

# Verify services are running
docker ps
# Should see: seraphs-redis, seraphs-ipfs, seraphs-postgres
```

### Step 2: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Verify Redis is accessible
redis-cli ping
# Should return: PONG

# Verify IPFS is accessible
curl http://localhost:5001/api/v0/version
# Should return JSON with IPFS version
```

### Step 3: Run Agent 1

```bash
# Fetch from all 12 regulatory sources
python -m agents.agent_1_ingestion.agent

# Expected output:
# [INFO] agent_initialized: sources=12
# [INFO] fetching_source: source_id=rbi
# [INFO] fetch_success: size=156234
# [INFO] ipfs_stored: cid=QmX7Y8Z...
# [INFO] event_published: event_id=550e8400...
# ...
# [INFO] fetch_complete: successful=12/12
```

### Step 4: View Published Events

```bash
# Read events from Redis Streams
redis-cli XREAD COUNT 10 STREAMS seraphs:events 0

# Or use Redis GUI
redis-cli
> XLEN seraphs:events
> XRANGE seraphs:events - + COUNT 5
```

### Step 5: View IPFS Storage

```bash
# List pinned content
ipfs pin ls --type=recursive

# View a snapshot (replace with actual CID)
ipfs cat QmX7Y8Z9a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
```

## Option 3: Run Specific Source Only

Edit `config/sources.yaml` and disable sources:

```yaml
sources:
  - id: rbi
    enabled: true  # Only fetch RBI
    
  - id: sebi
    enabled: false  # Skip SEBI
    
  # ... disable others
```

Then run:
```bash
python -m agents.agent_1_ingestion.agent
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'X'"
```bash
# Install missing module
pip install X

# Or install all at once
pip install -r requirements.txt  # (if you create one)
```

### Issue: "ConnectionError: Redis server not available"
```bash
# Start Redis
docker-compose up -d redis

# Or use local Redis
redis-server
```

### Issue: "IPFS connection failed"
```bash
# Start IPFS
docker-compose up -d ipfs

# Or use local IPFS daemon
ipfs daemon
```

### Issue: "Timeout fetching from regulatory website"
```bash
# Increase timeout in sources.yaml
settings:
  request_timeout_seconds: 60  # Increase from 30
```

## Testing Output

See [agent1-output-examples.md](agent1-output-examples.md) for detailed output examples showing:
- Exact JSON event structures
- Redis stream output
- IPFS storage format
- Sample data from RBI, SEBI, GDPR, etc.

## Next Steps

Once Agent 1 is running:

1. **Verify events in Redis**: Check that `INGESTION_SNAPSHOT` events are being published
2. **Verify IPFS storage**: Confirm content is stored with correct CIDs
3. **Move to Phase 2**: Implement Agents 2 & 3 to process these events

---

**Need help?** Check the full [README.md](../README.md) or [architecture.md](architecture.md)
