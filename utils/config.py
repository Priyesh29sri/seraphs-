"""
Configuration loader with validation.

Loads settings from environment variables and YAML files.

"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel, Field
from dotenv import load_dotenv


# Load .env file
load_dotenv()


class RedisConfig(BaseModel):
    """Redis configuration"""
    host: str = Field(default="localhost")
    port: int = Field(default=6379)
    password: Optional[str] = None
    db: int = Field(default=0)
    stream_name: str = Field(default="seraphs:events")


class IPFSConfig(BaseModel):
    """IPFS configuration"""
    api_host: str = Field(default="localhost")
    api_port: int = Field(default=5001)
    gateway_url: str = Field(default="http://localhost:8080")


class DatabaseConfig(BaseModel):
    """PostgreSQL configuration"""
    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    name: str = Field(default="seraphs")
    user: str = Field(default="seraphs_user")
    password: str = Field(default="changeme")
    pool_size: int = Field(default=10)


class LLMConfig(BaseModel):
    """LLM API configuration"""
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    default_model: str = Field(default="claude-sonnet-3-5")


class Config(BaseModel):
    """Main application configuration"""
    environment: str = Field(default="development")
    log_level: str = Field(default="INFO")
    debug: bool = Field(default=False)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    ipfs: IPFSConfig = Field(default_factory=IPFSConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)


def load_config() -> Config:
    """
    Load configuration from environment variables.
    
    Returns:
        Config object with all settings
    """
    return Config(
        environment=os.getenv("ENVIRONMENT", "development"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        debug=os.getenv("DEBUG", "false").lower() == "true",
        redis=RedisConfig(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            password=os.getenv("REDIS_PASSWORD"),
            db=int(os.getenv("REDIS_DB", "0")),
            stream_name=os.getenv("REDIS_STREAM_NAME", "seraphs:events"),
        ),
        ipfs=IPFSConfig(
            api_host=os.getenv("IPFS_API_HOST", "localhost"),
            api_port=int(os.getenv("IPFS_API_PORT", "5001")),
            gateway_url=os.getenv("IPFS_GATEWAY_URL", "http://localhost:8080"),
        ),
        database=DatabaseConfig(
            host=os.getenv("DATABASE_HOST", "localhost"),
            port=int(os.getenv("DATABASE_PORT", "5432")),
            name=os.getenv("DATABASE_NAME", "seraphs"),
            user=os.getenv("DATABASE_USER", "seraphs_user"),
            password=os.getenv("DATABASE_PASSWORD", "changeme"),
            pool_size=int(os.getenv("DATABASE_POOL_SIZE", "10")),
        ),
        llm=LLMConfig(
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        ),
    )


def load_sources_config(config_path: str = "config/sources.yaml") -> Dict[str, Any]:
    """
    Load regulatory sources configuration from YAML.
    
    Args:
        config_path: Path to sources.yaml file
        
    Returns:
        Dictionary with sources and settings
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Sources config not found: {config_path}")
    
    with open(path, 'r') as f:
        return yaml.safe_load(f)


# Global config instance
config = load_config()
