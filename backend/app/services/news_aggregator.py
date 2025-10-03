from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import logging
from app.models import NewsArticle, Source, Category
from app.models.news import SeverityLevel
from app.services.feed_parser import FeedParser
from app.core.config import settings

logger = logging.getLogger(__name__)

class NewsAggregator:
    """Aggregate news from multiple RSS feeds"""

    def __init__(self, db: Session):
        self.db = db
        self.parser = FeedParser()

    def initialize_sources(self):
        """Initialize default RSS feed sources"""
        for feed_data in settings.RSS_FEEDS:
            existing = self.db.query(Source).filter_by(feed_url=feed_data['url']).first()
            if not existing:
                source = Source(
                    name=feed_data['name'],
                    url=feed_data['url'],
                    feed_url=feed_data['url'],
                    description=f"RSS feed from {feed_data['name']}"
                )
                self.db.add(source)

        # Initialize default categories
        default_categories = [
            {"name": "Vulnerabilities", "slug": "vulnerabilities", "color": "#FF6B6B"},
            {"name": "Data Breaches", "slug": "data-breaches", "color": "#FFA500"},
            {"name": "Malware", "slug": "malware", "color": "#9B59B6"},
            {"name": "Security Tools", "slug": "security-tools", "color": "#3498DB"},
            {"name": "Best Practices", "slug": "best-practices", "color": "#2ECC71"},
            {"name": "Threats", "slug": "threats", "color": "#E74C3C"},
            {"name": "General", "slug": "general", "color": "#95A5A6"},
        ]

        for cat_data in default_categories:
            existing = self.db.query(Category).filter_by(slug=cat_data['slug']).first()
            if not existing:
                category = Category(**cat_data)
                self.db.add(category)

        self.db.commit()

    def fetch_all_feeds(self):
        """Fetch news from all active sources"""
        sources = self.db.query(Source).filter_by(is_active=1).all()
        total_articles = 0

        for source in sources:
            try:
                articles_count = self._fetch_source_feed(source)
                total_articles += articles_count
                logger.info(f"Fetched {articles_count} articles from {source.name}")
            except Exception as e:
                logger.error(f"Error fetching feed from {source.name}: {str(e)}")

        return total_articles

    def _fetch_source_feed(self, source: Source) -> int:
        """Fetch and store articles from a single source"""
        articles_data = self.parser.parse_feed(source.feed_url)
        new_articles = 0

        for article_data in articles_data:
            # Check if article already exists
            existing = self.db.query(NewsArticle).filter_by(url=article_data['url']).first()
            if existing:
                continue

            # Create new article
            article = NewsArticle(
                title=article_data['title'],
                description=article_data.get('description'),
                content=article_data.get('content'),
                url=article_data['url'],
                image_url=article_data.get('image_url'),
                published_date=article_data.get('published_date', datetime.utcnow()),
                severity=self._map_severity(article_data.get('severity', 'info')),
                source_id=source.id
            )

            # Assign categories based on content
            categories = self._determine_categories(article_data)
            for category in categories:
                article.categories.append(category)

            self.db.add(article)
            new_articles += 1

        # Update source last_fetched timestamp
        source.last_fetched = datetime.utcnow()
        self.db.commit()

        return new_articles

    def _map_severity(self, severity_str: str) -> SeverityLevel:
        """Map severity string to enum"""
        severity_map = {
            'critical': SeverityLevel.CRITICAL,
            'high': SeverityLevel.HIGH,
            'medium': SeverityLevel.MEDIUM,
            'low': SeverityLevel.LOW,
            'info': SeverityLevel.INFO
        }
        return severity_map.get(severity_str, SeverityLevel.INFO)

    def _determine_categories(self, article_data: dict) -> List[Category]:
        """Determine article categories based on content"""
        categories = []
        text = (article_data.get('title', '') + ' ' +
                article_data.get('description', '')).lower()

        # Category keyword mapping
        category_keywords = {
            'vulnerabilities': ['vulnerability', 'cve', 'exploit', 'zero-day', 'patch'],
            'data-breaches': ['breach', 'leak', 'exposed', 'stolen', 'compromised'],
            'malware': ['malware', 'ransomware', 'trojan', 'virus', 'botnet'],
            'security-tools': ['tool', 'software', 'solution', 'platform', 'scanner'],
            'best-practices': ['best practice', 'guideline', 'recommendation', 'tips', 'how to'],
            'threats': ['threat', 'attack', 'campaign', 'actor', 'apt']
        }

        for slug, keywords in category_keywords.items():
            if any(keyword in text for keyword in keywords):
                category = self.db.query(Category).filter_by(slug=slug).first()
                if category:
                    categories.append(category)

        # If no categories found, add to general
        if not categories:
            general = self.db.query(Category).filter_by(slug='general').first()
            if general:
                categories.append(general)

        return categories

    def clean_old_articles(self, days: int = 30):
        """Remove articles older than specified days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        deleted = self.db.query(NewsArticle).filter(
            NewsArticle.fetched_date < cutoff_date
        ).delete()
        self.db.commit()
        logger.info(f"Deleted {deleted} articles older than {days} days")
        return deleted