import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "FinAI Nexus"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEMO_MODE: bool = True
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "finai-nexus-super-secret-key-change-in-production-min-32-chars"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    ALGORITHM: str = "HS256"

    # Database
    DATABASE_URL: str = "sqlite:///./finai_nexus.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # LLM & Embeddings
    LLM_PROVIDER: str = "mock"  # "mock", "openai", "gemini"
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o"
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-1.5-pro"

    EMBEDDING_PROVIDER: str = "mock"  # "mock", "openai", "gemini", "huggingface"
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    VECTOR_SEARCH_TOP_K: int = 5
    SIMILARITY_THRESHOLD: float = 0.70

    # Responsible AI
    STRICT_CITATION_CHECK: bool = True
    MAX_HALLUCINATION_SCORE: float = 0.25
    PROMPT_INJECTION_PROTECTION: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
