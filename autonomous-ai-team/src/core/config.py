"""
Configuration management for the Autonomous AI Team system.
Uses Pydantic Settings for type-safe environment variable loading.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    # API Keys
    anthropic_api_key: str
    google_api_key: Optional[str] = None
    brave_api_key: Optional[str] = None
    serpapi_key: Optional[str] = None

    # Database
    database_url: str = "sqlite:///./ai_agents.db"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Application
    environment: str = "development"
    log_level: str = "INFO"
    max_retries: int = 3
    task_timeout_seconds: int = 300

    # Agent Settings
    default_model: str = "claude-sonnet-4-5"
    max_tokens: int = 4096
    temperature: float = 0.7

    # Cost & Rate Limiting
    max_cost_per_day: float = 50.0
    rate_limit_per_minute: int = 60

    # Human Approval Thresholds
    financial_approval_threshold: float = 1000.0
    auto_approve_content: bool = True
    auto_approve_analysis: bool = True

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment.lower() == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment.lower() == "production"


# Global settings instance
settings = Settings()
