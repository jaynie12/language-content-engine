from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from .env"""
    
    # Anthropic
    anthropic_api_key: str
    
    # Database
    database_url: str = "postgresql://localhost/french_app_db"
    sqlalchemy_echo: bool = False
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"
    
    # YouTube
    youtube_api_key: Optional[str] = None
    
    # App
    debug: bool = False
    environment: str = "development"
    log_level: str = "INFO"
    
    # CORS
    frontend_url: str = "http://localhost:5173"
    
    # Cost tracking
    track_tokens: bool = True
    log_cost_per_request: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
