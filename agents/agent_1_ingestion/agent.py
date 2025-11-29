"""
Agent 1: Discovery & Ingestion
Main agent logic for fetching regulatory content.

This agent:
1. Loads source configurations
2. Fetches content from regulatory websites
3. Extracts text
4. Computes hashes
5. Stores in IPFS  
6. Publishes INGESTION_SNAPSHOT events
7. Schedules periodic monitoring
"""

import uuid
from datetime import datetime
from typing import Dict, Optional

from agents.agent_1_ingestion import tools
from schemas.events import (
    EventEnvelope,
    EventType,
    IngestionSnapshotPayload,
    SourceInfo,
    ContentData,
    HashData,
    StorageInfo,
    VersionInfo,
)
from utils.config import load_sources_config
from utils.event_bus import EventBus
from utils.ipfs_client import IPFSClient
from utils.logger import get_logger, bind_trace_id

logger = get_logger(__name__)


class IngestionAgent:
    """
    Agent 1: Discovery & Ingestion
    
    Autonomously monitors regulatory websites and publishes snapshots.
    """
    
    def __init__(
        self,
        event_bus: EventBus,
        ipfs_client: IPFSClient,
        sources_config_path: str = "config/sources.yaml",
    ):
        self.event_bus = event_bus
        self.ipfs_client = ipfs_client
        
        # Load source configurations
        config = load_sources_config(sources_config_path)
        self.sources = config['sources']
        self.settings = config['settings']
        
        # Track last hashes for version detection
        self.last_hashes: Dict[str, str] = {}
        
        logger.info("agent_initialized", agent="agent-1-ingestion", sources=len(self.sources))
    
    def fetch_source(self, source_config: Dict) -> Optional[EventEnvelope]:
        """
        Fetch content from a single regulatory source.
        
        Args:
            source_config: Source configuration dict
            
        Returns:
            EventEnvelope with INGESTION_SNAPSHOT, or None if failed
        """
        source_id = source_config['id']
        source_url = source_config['url']
        source_type = source_config['type']
        
        # Create trace ID for this fetch
        trace_id = f"trace-{source_id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        bind_trace_id(trace_id)
        
        logger.info(
            "fetching_source",
            source_id=source_id,
            url=source_url,
            type=source_type,
        )
        
        try:
            # Validate URL
            validated_url = tools.validate_url(source_url)
            
            # Fetch based on type
            if source_type == 'html':
                result = self._fetch_html_source(source_config, validated_url)
            elif source_type == 'pdf':
                result = self._fetch_pdf_source(source_config, validated_url)
            elif source_type == 'rss':
                result = self._fetch_rss_source(source_config, validated_url)
            else:
                raise ValueError(f"Unknown source type: {source_type}")
            
            if result:
                logger.info("fetch_complete", source_id=source_id, snapshot_id=result.event_id)
            
            return result
        
        except Exception as e:
            logger.error("fetch_failed", source_id=source_id, error=str(e), exc_info=True)
            return None
    
    def _fetch_html_source(self, source_config: Dict, url: str) -> EventEnvelope:
        """Fetch HTML source and create snapshot"""
        source_id = source_config['id']
        
        # Fetch HTML
        fetch_result = tools.fetch_html(url)
        
        # Extract text
        html_text = fetch_result.content.decode(fetch_result.encoding)
        extracted_text = tools.normalize_text(html_text)
        
        # Extract metadata
        metadata = tools.extract_metadata(html_text, fetch_result.content_type)
        metadata['dom_tree'] = tools.capture_dom_tree(html_text)
        metadata['external_links'] = len(tools.list_links(html_text, url))
        
        # Compute hash
        content_hash = tools.compute_sha256(fetch_result.content)
        
        # Detect version change
        is_new_version = tools.detect_new_version(
            content_hash,
            self.last_hashes.get(source_id)
        )
        self.last_hashes[source_id] = content_hash
        
        # Store in IPFS
        ipfs_cid = self.ipfs_client.add(fetch_result.content)
        ipfs_gateway_url = self.ipfs_client.get_gateway_url(ipfs_cid)
        
        # Create snapshot
        snapshot_id = f"snap-{source_id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        payload = IngestionSnapshotPayload(
            snapshot_id=snapshot_id,
            source=SourceInfo(
                name=source_config['name'],
                url=url,
                type='html',
            ),
            fetched_at=datetime.utcnow(),
            content=ContentData(
                raw_html=html_text[:10000],  # First 10k chars for storage
                extracted_text=extracted_text,
                content_type=fetch_result.content_type,
                encoding=fetch_result.encoding,
                size_bytes=len(fetch_result.content),
            ),
            hashes=HashData(
                sha256=content_hash,
            ),
            storage=StorageInfo(
                ipfs_cid=ipfs_cid,
                ipfs_gateway_url=ipfs_gateway_url,
            ),
            metadata=metadata,
            version_info=VersionInfo(
                is_new_version=is_new_version,
                previous_hash=self.last_hashes.get(source_id),
                change_detected=is_new_version,
            ),
        )
        
        # Create event
        event = EventEnvelope(
            event_id=str(uuid.uuid4()),
            event_type=EventType.INGESTION_SNAPSHOT,
            payload=payload.model_dump(),
            source_agent="agent-1-ingestion",
            trace_id=f"trace-{source_id}-{datetime.utcnow().isoformat()}",
        )
        
        # Publish to event bus
        self.event_bus.publish(event)
        
        return event
    
    def _fetch_pdf_source(self, source_config: Dict, url: str) -> EventEnvelope:
        """Fetch PDF source and create snapshot"""
        source_id = source_config['id']
        
        # Fetch PDF
        pdf_bytes = tools.fetch_pdf(url)
        
        # Extract text
        extracted_text = tools.extract_text_pdf(pdf_bytes)
        normalized_text = tools.normalize_text(extracted_text)
        
        # Compute hash
        content_hash = tools.compute_sha256(pdf_bytes)
        
        # Detect version change
        is_new_version = tools.detect_new_version(
            content_hash,
            self.last_hashes.get(source_id)
        )
        self.last_hashes[source_id] = content_hash
        
        # Store in IPFS
        ipfs_cid = self.ipfs_client.add(pdf_bytes)
        ipfs_gateway_url = self.ipfs_client.get_gateway_url(ipfs_cid)
        
        # Create snapshot
        snapshot_id = f"snap-{source_id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        payload = IngestionSnapshotPayload(
            snapshot_id=snapshot_id,
            source=SourceInfo(
                name=source_config['name'],
                url=url,
                type='pdf',
            ),
            fetched_at=datetime.utcnow(),
            content=ContentData(
                extracted_text=normalized_text,
                content_type='application/pdf',
                size_bytes=len(pdf_bytes),
            ),
            hashes=HashData(
                sha256=content_hash,
            ),
            storage=StorageInfo(
                ipfs_cid=ipfs_cid,
                ipfs_gateway_url=ipfs_gateway_url,
            ),
            metadata={'format': 'PDF'},
            version_info=VersionInfo(
                is_new_version=is_new_version,
                previous_hash=self.last_hashes.get(source_id),
                change_detected=is_new_version,
            ),
        )
        
        # Create and publish event
        event = EventEnvelope(
            event_id=str(uuid.uuid4()),
            event_type=EventType.INGESTION_SNAPSHOT,
            payload=payload.model_dump(),
            source_agent="agent-1-ingestion",
            trace_id=f"trace-{source_id}-{datetime.utcnow().isoformat()}",
        )
        
        self.event_bus.publish(event)
        return event
    
    def _fetch_rss_source(self, source_config: Dict, url: str) -> EventEnvelope:
        """Fetch RSS feed and create snapshot"""
        source_id = source_config['id']
        
        # Fetch RSS
        items = tools.fetch_rss(url)
        
        # Convert to text
        rss_text = '\n\n'.join([
            f"Title: {item['title']}\nLink: {item['link']}\nPublished: {item['published']}\nSummary: {item['summary']}"
            for item in items
        ])
        
        # Compute hash
        content_hash = tools.compute_sha256(rss_text)
        
        # Detect version change
        is_new_version = tools.detect_new_version(
            content_hash,
            self.last_hashes.get(source_id)
        )
        self.last_hashes[source_id] = content_hash
        
        # Store in IPFS
        ipfs_cid = self.ipfs_client.add(rss_text)
        ipfs_gateway_url = self.ipfs_client.get_gateway_url(ipfs_cid)
        
        # Create snapshot
        snapshot_id = f"snap-{source_id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        payload = IngestionSnapshotPayload(
            snapshot_id=snapshot_id,
            source=SourceInfo(
                name=source_config['name'],
                url=url,
                type='rss',
            ),
            fetched_at=datetime.utcnow(),
            content=ContentData(
                extracted_text=rss_text,
                content_type='application/rss+xml',
                size_bytes=len(rss_text),
            ),
            hashes=HashData(
                sha256=content_hash,
            ),
            storage=StorageInfo(
                ipfs_cid=ipfs_cid,
                ipfs_gateway_url=ipfs_gateway_url,
            ),
            metadata={'items_count': len(items)},
            version_info=VersionInfo(
                is_new_version=is_new_version,
                previous_hash=self.last_hashes.get(source_id),
                change_detected=is_new_version,
            ),
        )
        
        # Create and publish event
        event = EventEnvelope(
            event_id=str(uuid.uuid4()),
            event_type=EventType.INGESTION_SNAPSHOT,
            payload=payload.model_dump(),
            source_agent="agent-1-ingestion",
            trace_id=f"trace-{source_id}-{datetime.utcnow().isoformat()}",
        )
        
        self.event_bus.publish(event)
        return event
    
    def fetch_all_sources(self) -> int:
        """
        Fetch all enabled sources.
        
        Returns:
            Number of successful fetches
        """
        logger.info("fetching_all_sources", total_sources=len(self.sources))
        
        successful = 0
        for source in self.sources:
            if not source.get('enabled', True):
                logger.debug("source_disabled", source_id=source['id'])
                continue
            
            result = self.fetch_source(source)
            if result:
                successful += 1
        
        logger.info("fetch_complete", successful=successful, total=len(self.sources))
        return successful


def main():
    """Main entry point for Agent 1"""
    from utils.config import config
    
    # Initialize clients
    event_bus = EventBus(
        redis_host=config.redis.host,
        redis_port=config.redis.port,
        stream_name=config.redis.stream_name,
    )
    
    ipfs_client = IPFSClient(
        api_host=config.ipfs.api_host,
        api_port=config.ipfs.api_port,
        gateway_url=config.ipfs.gateway_url,
    )
    
    # Create agent
    agent = IngestionAgent(event_bus, ipfs_client)
    
    # Fetch all sources
    agent.fetch_all_sources()


if __name__ == "__main__":
    main()
