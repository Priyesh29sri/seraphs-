"""
IPFS client wrapper for content-addressed storage.

All regulatory snapshots and proofs are stored in IPFS for immutability.
"""

import hashlib
import logging
from typing import Optional, Union

import ipfshttpclient

logger = logging.getLogger(__name__)


class IPFSClient:
    """
    Wrapper around IPFS HTTP API client with helper methods.
    
    Security Notes:
    - Use private IPFS node (not public gateway) for sensitive data
    - Consider encryption for sensitive content before upload
    - Store CIDs in database for retrieval
    """
    
    def __init__(
        self,
        api_host: str = "localhost",
        api_port: int = 5001,
        gateway_url: str = "http://localhost:8080",
    ):
        self.api_addr = f"/ip4/{api_host}/tcp/{api_port}/http"
        self.gateway_url = gateway_url
        
        try:
            self.client = ipfshttpclient.connect(self.api_addr)
            logger.info(f"Connected to IPFS node: {self.api_addr}")
        except Exception as e:
            logger.error(f"Failed to connect to IPFS: {e}")
            raise
    
    def add(self, content: Union[str, bytes], filename: Optional[str] = None) -> str:
        """
        Add content to IPFS.
        
        Args:
            content: String or bytes to upload
            filename: Optional filename for the content
            
        Returns:
            IPFS CID (Content Identifier)
        """
        try:
            # Convert string to bytes if needed
            if isinstance(content, str):
                content = content.encode('utf-8')
            
            # Add to IPFS
            res = self.client.add_bytes(content)
            cid = res
            
            logger.info(f"Added to IPFS: CID={cid}, size={len(content)} bytes")
            
            return cid
        
        except Exception as e:
            logger.error(f"Failed to add to IPFS: {e}", exc_info=True)
            raise
    
    def add_json(self, data: dict) -> str:
        """
        Add JSON object to IPFS.
        
        Args:
            data: Dictionary to serialize and upload
            
        Returns:
            IPFS CID
        """
        import json
        json_str = json.dumps(data, indent=2, default=str)
        return self.add(json_str)
    
    def get(self, cid: str) -> bytes:
        """
        Retrieve content from IPFS by CID.
        
        Args:
            cid: IPFS Content Identifier
            
        Returns:
            Content as bytes
        """
        try:
            content = self.client.cat(cid)
            logger.debug(f"Retrieved from IPFS: CID={cid}")
            return content
        except Exception as e:
            logger.error(f"Failed to retrieve from IPFS: {e}")
            raise
    
    def get_text(self, cid: str, encoding: str = 'utf-8') -> str:
        """Retrieve text content from IPFS"""
        content_bytes = self.get(cid)
        return content_bytes.decode(encoding)
    
    def get_json(self, cid: str) -> dict:
        """Retrieve and parse JSON from IPFS"""
        import json
        content_str = self.get_text(cid)
        return json.loads(content_str)
    
    def pin(self, cid: str) -> None:
        """
        Pin content to ensure it's not garbage collected.
        
        Args:
            cid: Content ID to pin
        """
        try:
            self.client.pin.add(cid)
            logger.info(f"Pinned: {cid}")
        except Exception as e:
            logger.error(f"Failed to pin {cid}: {e}")
            raise
    
    def unpin(self, cid: str) -> None:
        """Unpin content (allows garbage collection)"""
        try:
            self.client.pin.rm(cid)
            logger.info(f"Unpinned: {cid}")
        except Exception as e:
            logger.warning(f"Failed to unpin {cid}: {e}")
    
    def get_gateway_url(self, cid: str) -> str:
        """
        Get HTTP gateway URL for a CID.
        
        Useful for sharing links to stored content.
        """
        return f"{self.gateway_url}/ipfs/{cid}"
    
    def verify_hash(self, content: Union[str, bytes], expected_cid: str) -> bool:
        """
        Verify that content matches expected CID.
        
        This proves content integrity.
        """
        actual_cid = self.add(content)
        return actual_cid == expected_cid
    
    def health_check(self) -> bool:
        """Check if IPFS node is responsive"""
        try:
            self.client.id()
            return True
        except Exception as e:
            logger.error(f"IPFS health check failed: {e}")
            return False
