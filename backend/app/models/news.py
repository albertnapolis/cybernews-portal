from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

# Association table for many-to-many relationship between articles and categories
article_categories = Table(
    'article_categories',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('news_articles.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

class SeverityLevel(enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    content = Column(Text)
    url = Column(String(1000), unique=True, nullable=False)
    image_url = Column(String(1000))
    published_date = Column(DateTime, default=datetime.utcnow)
    fetched_date = Column(DateTime, default=datetime.utcnow)
    severity = Column(SQLEnum(SeverityLevel), default=SeverityLevel.INFO)

    # Foreign keys
    source_id = Column(Integer, ForeignKey('sources.id'))

    # Relationships
    source = relationship("Source", back_populates="articles")
    categories = relationship("Category", secondary=article_categories, back_populates="articles")

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    url = Column(String(500), nullable=False)
    feed_url = Column(String(500), unique=True, nullable=False)
    description = Column(Text)
    last_fetched = Column(DateTime)
    is_active = Column(Integer, default=1)  # SQLite doesn't have Boolean

    # Relationships
    articles = relationship("NewsArticle", back_populates="source")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    color = Column(String(7))  # Hex color code

    # Relationships
    articles = relationship("NewsArticle", secondary=article_categories, back_populates="categories")