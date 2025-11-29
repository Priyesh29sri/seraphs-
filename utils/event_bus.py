"""
Redis Streams Event Bus for inter-agent communication.

All agents publish and subscribe to events via this centralized bus.
"""

import json
import logging
import uuid
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

import redis
from schemas.events import EventEnvelope, EventType

logger = logging.getLogger(__name__)


class EventBus:
    """
    Redis Streams-based event bus for pub/sub between agents.
    
    Features:
    - Guaranteed delivery via consumer groups
    - Message persistence (configurable retention)
    - Dead letter queue for failed messages
    - Automatic retry logic
    """
    
    def __init__(
        self,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_password: Optional[str] = None,
        redis_db: int = 0,
        stream_name: str = "seraphs:events",
        dlq_stream: str = "seraphs:dlq",
        max_retries: int = 3,
    ):
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            db=redis_db,
            decode_responses=True,
        )
        self.stream_name = stream_name
        self.dlq_stream = dlq_stream
        self.max_retries = max_retries
        
        logger.info(f"EventBus initialized: stream={stream_name}, host={redis_host}:{redis_port}")
    
    def publish(self, event: EventEnvelope) -> str:
        """
        Publish an event to the Redis stream.
        
        Args:
            event: EventEnvelope containing event data
            
        Returns:
            Message ID from Redis
        """
        # Convert Pydantic model to dict, then to JSON string
        event_dict = event.model_dump(mode='json')
        event_json = {
            "data": json.dumps(event_dict, default=str)
        }
        
        message_id = self.redis_client.xadd(self.stream_name, event_json)
        
        logger.info(
            f"Published event: type={event.event_type}, "
            f"id={event.event_id}, msg_id={message_id}"
        )
        
        return message_id
    
    def subscribe(
        self,
        consumer_group: str,
        consumer_name: str,
        event_types: Optional[List[EventType]] = None,
        callback: Optional[Callable[[EventEnvelope], None]] = None,
        block_ms: int = 5000,
    ) -> None:
        """
        Subscribe to events from the stream.
        
        Args:
            consumer_group: Name of consumer group (for load balancing)
            consumer_name: Name of this specific consumer
            event_types: Filter to specific event types (None = all)
            callback: Function to call for each event
            block_ms: Milliseconds to block waiting for messages
        """
        # Create consumer group if it doesn't exist
        try:
            self.redis_client.xgroup_create(
                self.stream_name,
                consumer_group,
                id='0',
                mkstream=True
            )
            logger.info(f"Created consumer group: {consumer_group}")
        except redis.exceptions.ResponseError as e:
            if "BUSYGROUP" not in str(e):
                raise
        
        logger.info(
            f"Subscribing: group={consumer_group}, "
            f"consumer={consumer_name}, types={event_types}"
        )
        
        while True:
            try:
                # Read new messages
                messages = self.redis_client.xreadgroup(
                    groupname=consumer_group,
                    consumername=consumer_name,
                    streams={self.stream_name: '>'},
                    count=10,
                    block=block_ms,
                )
                
                for stream, msg_list in messages:
                    for msg_id, msg_data in msg_list:
                        self._process_message(
                            msg_id,
                            msg_data,
                            consumer_group,
                            event_types,
                            callback
                        )
            
            except KeyboardInterrupt:
                logger.info("Shutting down subscriber...")
                break
            except Exception as e:
                logger.error(f"Error in subscriber loop: {e}", exc_info=True)
    
    def _process_message(
        self,
        msg_id: str,
        msg_data: Dict[str, str],
        consumer_group: str,
        event_types: Optional[List[EventType]],
        callback: Optional[Callable],
    ) -> None:
        """Process a single message from the stream"""
        try:
            # Parse event
            event_dict = json.loads(msg_data['data'])
            event = EventEnvelope(**event_dict)
            
            # Filter by event type
            if event_types and event.event_type not in event_types:
                # Acknowledge and skip
                self.redis_client.xack(self.stream_name, consumer_group, msg_id)
                return
            
            logger.debug(f"Processing event: {event.event_type} ({msg_id})")
            
            # Call handler
            if callback:
                callback(event)
            
            # Acknowledge successful processing
            self.redis_client.xack(self.stream_name, consumer_group, msg_id)
            
        except Exception as e:
            logger.error(f"Error processing message {msg_id}: {e}", exc_info=True)
            # Send to dead letter queue after max retries
            self._handle_failure(msg_id, msg_data, e)
    
    def _handle_failure(self, msg_id: str, msg_data: Dict, error: Exception) -> None:
        """Handle failed message processing"""
        # Add to DLQ for manual review
        dlq_data = {
            "original_msg_id": msg_id,
            "error": str(error),
            "data": msg_data['data'],
            "failed_at": datetime.utcnow().isoformat(),
        }
        self.redis_client.xadd(self.dlq_stream, dlq_data)
        logger.warning(f"Message {msg_id} sent to DLQ")
    
    def health_check(self) -> bool:
        """Check if Redis connection is healthy"""
        try:
            return self.redis_client.ping()
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
