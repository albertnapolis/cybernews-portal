from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Cybersecurity News Portal"
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./cybernews.db")

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Redis (for caching)
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL", None)

    # RSS Feed Sources
    RSS_FEEDS: List[dict] = [
        {"name": "The Hacker News", "url": "https://feeds.feedburner.com/TheHackersNews", "category": "general"},
        {"name": "SecurityWeek", "url": "https://feeds.feedburner.com/Securityweek", "category": "general"},
        {"name": "Krebs on Security", "url": "https://krebsonsecurity.com/feed/", "category": "general"},
        {"name": "ThreatPost", "url": "https://threatpost.com/feed/", "category": "threats"},
        {"name": "Dark Reading", "url": "https://www.darkreading.com/rss.xml", "category": "general"},
        {"name": "BleepingComputer", "url": "https://www.bleepingcomputer.com/feed/", "category": "general"},
        {"name": "CISA Alerts", "url": "https://www.cisa.gov/uscert/ncas/alerts.xml", "category": "vulnerability"},
        {"name": "Zero Day Initiative", "url": "https://www.zerodayinitiative.com/rss/published/", "category": "vulnerability"},
    ]

    # Scheduler settings
    FEED_UPDATE_INTERVAL_MINUTES: int = 30

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()