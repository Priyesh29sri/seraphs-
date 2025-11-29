"""
Structured logging configuration for Seraphs 2.0.

All logs include trace_id for distributed tracing across agents.
"""

import logging
import sys
from typing import Any, Dict

try:
    import structlog
    STRUCT_LOG_AVAILABLE = True
except ImportError:
    STRUCT_LOG_AVAILABLE = False


def configure_logging(log_level: str = "INFO", json_logs: bool = False) -> None:
    """
    Configure structured logging for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_logs: If True, output JSON format (for production)
    """
    
    # Configure stdlib logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper()),
    )
    
    # Processors for structlog
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    
    # Add JSON renderer for production, console for development
    if json_logs:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str):
    """
    Get a logger instance.
    
    Usage:
        logger = get_logger(__name__)
        logger.info("event_occurred", event_id="123", agent="agent-1")
    """
    if STRUCT_LOG_AVAILABLE:
        return structlog.get_logger(name)
    else:
        return logging.getLogger(name)


def bind_trace_id(trace_id: str) -> None:
    """
    Bind trace_id to all subsequent log entries in this context.
    
    This enables distributed tracing across agents.
    """
    structlog.contextvars.bind_contextvars(trace_id=trace_id)


def clear_trace_id() -> None:
    """Clear trace_id binding"""
    structlog.contextvars.clear_contextvars()
