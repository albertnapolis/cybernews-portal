from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.models import NewsArticle, Category
from app.models.database import get_db
from app.models.news import SeverityLevel
from app.schemas import NewsArticle as NewsArticleSchema, NewsArticleList
from app.core.config import settings

router = APIRouter()

@router.get("/", response_model=NewsArticleList)
def get_news_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    severity: Optional[SeverityLevel] = None,
    category: Optional[str] = None,
    source_id: Optional[int] = None,
    search: Optional[str] = None,
    days: Optional[int] = Query(None, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get paginated list of news articles with optional filters"""
    query = db.query(NewsArticle)

    # Apply filters
    if severity:
        query = query.filter(NewsArticle.severity == severity)

    if category:
        query = query.join(NewsArticle.categories).filter(Category.slug == category)

    if source_id:
        query = query.filter(NewsArticle.source_id == source_id)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (NewsArticle.title.ilike(search_term)) |
            (NewsArticle.description.ilike(search_term))
        )

    if days:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        query = query.filter(NewsArticle.published_date >= cutoff_date)

    # Get total count
    total = query.count()

    # Apply pagination
    offset = (page - 1) * page_size
    articles = query.order_by(NewsArticle.published_date.desc()).offset(offset).limit(page_size).all()

    return NewsArticleList(
        total=total,
        page=page,
        page_size=page_size,
        articles=articles
    )

@router.get("/{article_id}", response_model=NewsArticleSchema)
def get_news_article(article_id: int, db: Session = Depends(get_db)):
    """Get a specific news article by ID"""
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.get("/latest/critical", response_model=List[NewsArticleSchema])
def get_critical_news(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get latest critical severity news"""
    articles = db.query(NewsArticle).filter(
        NewsArticle.severity == SeverityLevel.CRITICAL
    ).order_by(NewsArticle.published_date.desc()).limit(limit).all()
    return articles

@router.get("/trending/", response_model=List[NewsArticleSchema])
def get_trending_news(
    hours: int = Query(24, ge=1, le=168),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get trending news from the last N hours"""
    cutoff_date = datetime.utcnow() - timedelta(hours=hours)
    articles = db.query(NewsArticle).filter(
        NewsArticle.published_date >= cutoff_date
    ).order_by(NewsArticle.published_date.desc()).limit(limit).all()
    return articles

@router.post("/refresh")
def refresh_news_feeds(db: Session = Depends(get_db)):
    """Manually trigger news feed refresh"""
    from app.services.news_aggregator import NewsAggregator
    aggregator = NewsAggregator(db)
    count = aggregator.fetch_all_feeds()
    return {"message": f"Fetched {count} new articles"}