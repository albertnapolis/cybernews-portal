from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime
from enum import Enum

class SeverityLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

# Category schemas
class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    color: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

# Source schemas
class SourceBase(BaseModel):
    name: str
    url: str
    feed_url: str
    description: Optional[str] = None
    is_active: bool = True

class SourceCreate(SourceBase):
    pass

class Source(SourceBase):
    id: int
    last_fetched: Optional[datetime] = None

    class Config:
        from_attributes = True

# NewsArticle schemas
class NewsArticleBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    url: str
    image_url: Optional[str] = None
    severity: SeverityLevel = SeverityLevel.INFO

class NewsArticleCreate(NewsArticleBase):
    source_id: int
    category_ids: List[int] = []

class NewsArticleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    severity: Optional[SeverityLevel] = None

class NewsArticle(NewsArticleBase):
    id: int
    published_date: datetime
    fetched_date: datetime
    source: Source
    categories: List[Category] = []

    class Config:
        from_attributes = True

class NewsArticleList(BaseModel):
    total: int
    page: int
    page_size: int
    articles: List[NewsArticle]