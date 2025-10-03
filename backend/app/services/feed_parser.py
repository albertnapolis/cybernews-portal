import feedparser
import httpx
from datetime import datetime
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import re
import logging

logger = logging.getLogger(__name__)

class FeedParser:
    """Parse RSS feeds and extract cybersecurity news articles"""

    def __init__(self):
        self.client = httpx.Client(timeout=30.0)

    def parse_feed(self, feed_url: str) -> List[Dict]:
        """Parse an RSS feed and return list of articles"""
        try:
            feed = feedparser.parse(feed_url)
            articles = []

            for entry in feed.entries:
                article = self._extract_article_data(entry)
                if article:
                    articles.append(article)

            return articles
        except Exception as e:
            logger.error(f"Error parsing feed {feed_url}: {str(e)}")
            return []

    def _extract_article_data(self, entry) -> Optional[Dict]:
        """Extract article data from feed entry"""
        try:
            # Extract basic fields
            title = entry.get('title', '')
            url = entry.get('link', '')

            if not title or not url:
                return None

            # Extract description/summary
            description = entry.get('summary', '') or entry.get('description', '')
            description = self._clean_html(description)

            # Extract content if available
            content = ''
            if hasattr(entry, 'content'):
                content = entry.content[0].value if entry.content else ''
                content = self._clean_html(content)

            # Extract published date
            published_date = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                import time
                published_date = datetime.fromtimestamp(
                    time.mktime(entry.published_parsed)
                )
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                import time
                published_date = datetime.fromtimestamp(
                    time.mktime(entry.updated_parsed)
                )

            # Extract image URL if available
            image_url = self._extract_image_url(entry)

            # Determine severity based on keywords
            severity = self._determine_severity(title + ' ' + description)

            return {
                'title': title[:500],  # Limit title length
                'url': url,
                'description': description[:2000],  # Limit description length
                'content': content[:5000],  # Limit content length
                'published_date': published_date or datetime.utcnow(),
                'image_url': image_url,
                'severity': severity
            }
        except Exception as e:
            logger.error(f"Error extracting article data: {str(e)}")
            return None

    def _clean_html(self, text: str) -> str:
        """Remove HTML tags and clean text"""
        if not text:
            return ''

        # Parse HTML
        soup = BeautifulSoup(text, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text and clean whitespace
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text

    def _extract_image_url(self, entry) -> Optional[str]:
        """Extract image URL from feed entry"""
        # Check for media content
        if hasattr(entry, 'media_content'):
            for media in entry.media_content:
                if 'image' in media.get('type', ''):
                    return media.get('url')

        # Check for media thumbnail
        if hasattr(entry, 'media_thumbnail'):
            if entry.media_thumbnail:
                return entry.media_thumbnail[0].get('url')

        # Check for enclosures
        if hasattr(entry, 'enclosures'):
            for enclosure in entry.enclosures:
                if 'image' in enclosure.get('type', ''):
                    return enclosure.get('href')

        # Try to extract from content
        if hasattr(entry, 'content'):
            content = entry.content[0].value if entry.content else ''
            soup = BeautifulSoup(content, 'html.parser')
            img = soup.find('img')
            if img and img.get('src'):
                return img['src']

        return None

    def _determine_severity(self, text: str) -> str:
        """Determine severity level based on keywords"""
        text_lower = text.lower()

        critical_keywords = ['critical', 'emergency', 'zero-day', 'ransomware', 'major breach']
        high_keywords = ['high severity', 'vulnerability', 'exploit', 'breach', 'attack']
        medium_keywords = ['medium severity', 'update', 'patch', 'security issue']
        low_keywords = ['low severity', 'minor', 'informational']

        if any(keyword in text_lower for keyword in critical_keywords):
            return 'critical'
        elif any(keyword in text_lower for keyword in high_keywords):
            return 'high'
        elif any(keyword in text_lower for keyword in medium_keywords):
            return 'medium'
        elif any(keyword in text_lower for keyword in low_keywords):
            return 'low'

        return 'info'

    def __del__(self):
        """Clean up HTTP client"""
        if hasattr(self, 'client'):
            self.client.close()