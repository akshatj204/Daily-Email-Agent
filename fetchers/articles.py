"""
Article Fetchers
Get curated articles from: Hacker News, Dev.to, arXiv
Perfect for weekend emails with quality content.
"""

import requests
import json
import os
import feedparser
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ArticleFetcher:
    """Fetch articles from multiple sources"""
    
    def __init__(self, cache_dir: str = "data/cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
        self.hn_url = "https://hacker-news.firebaseio.com/v0"
        self.devto_url = "https://dev.to/api/articles"
        self.arxiv_url = "http://export.arxiv.org/api/query"
    
    # ======================== HACKER NEWS ========================
    
    def fetch_hn_top_stories(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Fetch top stories from Hacker News.
        
        Args:
            limit: Number of stories to return (max 30)
        
        Returns:
            List of top stories with title, URL, score, author
        """
        try:
            # Get top 30 story IDs
            response = requests.get(
                f"{self.hn_url}/topstories.json",
                timeout=5
            )
            response.raise_for_status()
            top_ids = response.json()[:30]
            
            stories = []
            for story_id in top_ids[:limit]:
                try:
                    story_response = requests.get(
                        f"{self.hn_url}/item/{story_id}.json",
                        timeout=3
                    )
                    story_response.raise_for_status()
                    story = story_response.json()
                    
                    # Only include if has URL (not self-posts)
                    if story.get("url"):
                        stories.append({
                            "title": story.get("title", "Untitled"),
                            "url": story.get("url"),
                            "score": story.get("score", 0),
                            "author": story.get("by", "Unknown"),
                            "comments": story.get("descendants", 0),
                            "source": "Hacker News"
                        })
                except Exception as e:
                    logger.warning(f"Failed to fetch HN story {story_id}: {str(e)}")
                    continue
            
            return stories[:limit]
        
        except Exception as e:
            logger.error(f"Failed to fetch HN top stories: {str(e)}")
            return []
    
    def fetch_hn_by_topic(self, topic: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Fetch HN stories by topic (search in titles).
        
        Args:
            topic: Topic to search (e.g., "AI", "Python", "Investing")
            limit: Number of results
        
        Returns:
            List of matching stories
        """
        try:
            # Get top stories
            top_stories = self.fetch_hn_top_stories(limit=30)
            
            # Filter by topic (case-insensitive)
            topic_lower = topic.lower()
            filtered = [
                s for s in top_stories
                if topic_lower in s['title'].lower()
            ]
            
            return filtered[:limit]
        
        except Exception as e:
            logger.error(f"Failed to fetch HN by topic: {str(e)}")
            return []
    
    # ======================== DEV.TO ========================
    
    def fetch_devto_articles(
        self,
        tag: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Fetch articles from Dev.to.
        
        Args:
            tag: Topic tag (e.g., 'python', 'ai', 'finance', 'healthylifestyle')
            limit: Number of articles
        
        Returns:
            List of Dev.to articles
        """
        try:
            params = {
                "per_page": min(limit, 50),
                "state": "published",
                "order": "desc"
            }
            
            if tag:
                params["tag"] = tag
            
            response = requests.get(
                self.devto_url,
                params=params,
                timeout=5
            )
            response.raise_for_status()
            
            articles = []
            for article in response.json()[:limit]:
                articles.append({
                    "title": article.get("title", "Untitled"),
                    "url": article.get("url"),
                    "description": article.get("description", "")[:150],  # Short desc
                    "author": article.get("user", {}).get("name", "Unknown"),
                    "reading_time": article.get("reading_time_minutes", 0),
                    "likes": article.get("positive_reactions_count", 0),
                    "tags": article.get("tag_list", [])[:3],  # Top 3 tags
                    "published": article.get("published_at")[:10],  # Date only
                    "source": "Dev.to"
                })
            
            return articles
        
        except Exception as e:
            logger.error(f"Failed to fetch Dev.to articles: {str(e)}")
            return []
    
    # ======================== ARXIV ========================
    
    def fetch_arxiv_papers(
        self,
        category: str = "cs.AI",
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Fetch research papers from arXiv.
        
        Args:
            category: arXiv category
                     Options: cs.AI (AI), cs.LG (ML), q-fin (Finance),
                             econ (Economics), physics.data-an (Data Analysis)
            max_results: Number of papers
        
        Returns:
            List of arXiv papers
        """
        try:
            # Build search query
            search_query = f"cat:{category}"
            
            params = {
                "search_query": search_query,
                "start": 0,
                "max_results": max_results,
                "sortBy": "submittedDate",
                "sortOrder": "descending"
            }
            
            response = requests.get(
                self.arxiv_url,
                params=params,
                timeout=5
            )
            response.raise_for_status()
            
            # Parse Atom feed
            feed = feedparser.parse(response.text)
            
            papers = []
            for entry in feed.entries[:max_results]:
                papers.append({
                    "title": entry.get("title", "Untitled"),
                    "url": entry.get("id", "").replace("http://", "https://"),
                    "authors": ", ".join([a.name for a in entry.get("authors", [])])[:100],
                    "summary": entry.get("summary", "")[:150],  # First 150 chars
                    "published": entry.get("published", "")[:10],  # Date only
                    "category": category,
                    "source": "arXiv"
                })
            
            return papers
        
        except Exception as e:
            logger.error(f"Failed to fetch arXiv papers: {str(e)}")
            return []
    
    # ======================== SUBSTACK ========================
    
    def fetch_substack_articles(
        self,
        config_path: str = "config/substack_feeds.json",
        limit_per_feed: int = 2
    ) -> List[Dict[str, Any]]:
        """
        Fetch articles from Substack RSS feeds.
        
        Args:
            config_path: Path to JSON file with Substack feed URLs
            limit_per_feed: Number of articles to fetch per feed
        
        Returns:
            List of Substack articles
        """
        try:
            # Load feed configuration
            if not os.path.exists(config_path):
                logger.warning(f"Substack config not found: {config_path}")
                return []
            
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            feeds = config.get("substack_feeds", [])
            articles = []
            
            for feed_info in feeds:
                feed_url = feed_info.get("url")
                feed_name = feed_info.get("name", "Unknown")
                
                if not feed_url:
                    continue
                
                try:
                    # Fetch RSS feed content first
                    response = requests.get(feed_url, timeout=10)
                    response.raise_for_status()
                    
                    # Parse RSS feed from content
                    feed = feedparser.parse(response.text)
                    
                    for entry in feed.entries[:limit_per_feed]:
                        articles.append({
                            "title": entry.get("title", "Untitled"),
                            "url": entry.get("link", ""),
                            "author": feed_name,
                            "summary": entry.get("summary", "")[:200],
                            "published": entry.get("published", "")[:10] if entry.get("published") else "",
                            "source": "Substack"
                        })
                    
                    logger.info(f"Fetched {len(feed.entries[:limit_per_feed])} articles from {feed_name}")
                
                except Exception as e:
                    logger.warning(f"Failed to fetch Substack feed {feed_name}: {str(e)}")
                    continue
            
            return articles
        
        except Exception as e:
            logger.error(f"Failed to fetch Substack articles: {str(e)}")
            return []
    
    # ======================== CURATED COLLECTIONS ========================
    
    def get_weekend_articles(self) -> Dict[str, Any]:
        """
        Get curated articles for weekend email.
        Returns mix of HN, Dev.to, arXiv, and Substack.
        """
        articles = {
            "hn": self.fetch_hn_top_stories(limit=3),
            "devto_ai": self.fetch_devto_articles(tag="ai", limit=2),
            "devto_python": self.fetch_devto_articles(tag="python", limit=2),
            "arxiv_ai": self.fetch_arxiv_papers(category="cs.AI", max_results=2),
            "substack": self.fetch_substack_articles(limit_per_feed=2),
            "timestamp": datetime.now().isoformat()
        }
        
        return articles
    
    def get_investing_articles(self) -> List[Dict[str, Any]]:
        """Get investing/finance focused articles"""
        articles = []
        
        # Dev.to finance articles
        devto_finance = self.fetch_devto_articles(tag="investing", limit=3)
        articles.extend(devto_finance)
        
        # HN by topic
        hn_finance = self.fetch_hn_by_topic("investing", limit=2)
        articles.extend(hn_finance)
        
        # arXiv finance papers
        arxiv_finance = self.fetch_arxiv_papers(category="q-fin", max_results=2)
        articles.extend(arxiv_finance)
        
        return articles
    
    def get_ai_articles(self) -> List[Dict[str, Any]]:
        """Get AI/ML focused articles"""
        articles = []
        
        # Dev.to AI articles
        devto_ai = self.fetch_devto_articles(tag="ai", limit=3)
        articles.extend(devto_ai)
        
        # HN AI/ML
        hn_ai = self.fetch_hn_by_topic("AI", limit=3)
        articles.extend(hn_ai)
        
        # arXiv AI papers
        arxiv_ai = self.fetch_arxiv_papers(category="cs.AI", max_results=3)
        articles.extend(arxiv_ai)
        
        return articles
    
    def get_tech_articles(self) -> List[Dict[str, Any]]:
        """Get technology articles"""
        articles = []
        
        # Top HN stories
        hn_top = self.fetch_hn_top_stories(limit=3)
        articles.extend(hn_top)
        
        # Dev.to tech
        devto_tech = self.fetch_devto_articles(tag="javascript", limit=2)
        articles.extend(devto_tech)
        
        return articles
    
    # ======================== CACHE OPERATIONS ========================
    
    def save_articles_cache(
        self,
        articles: Dict[str, Any],
        category: str = "general"
    ) -> str:
        """Save articles to cache"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        cache_path = os.path.join(self.cache_dir, f"articles_{category}_{date_str}.json")
        
        try:
            with open(cache_path, 'w') as f:
                json.dump(articles, f, indent=2, default=str)
            logger.info(f"Saved articles to {cache_path}")
            return cache_path
        except Exception as e:
            logger.error(f"Failed to save articles: {str(e)}")
            return None
    
    def load_articles_cache(
        self,
        category: str = "general",
        days_old: int = 1
    ) -> Optional[Dict[str, Any]]:
        """Load articles from cache"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        cache_path = os.path.join(self.cache_dir, f"articles_{category}_{date_str}.json")
        
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load articles cache: {str(e)}")
        
        return None
    
    def format_articles_for_email(
        self,
        articles: List[Dict[str, Any]]
    ) -> str:
        """Format articles for email display"""
        output = "📚 Curated Articles\n"
        output += "=" * 70 + "\n\n"
        
        for i, article in enumerate(articles, 1):
            source = article.get("source", "Unknown")
            title = article.get("title", "Untitled")
            url = article.get("url", "#")
            
            # Additional info based on source
            extra = ""
            if source == "Hacker News":
                score = article.get("score", 0)
                extra = f" | {score} upvotes"
            elif source == "Dev.to":
                reading_time = article.get("reading_time", 0)
                extra = f" | {reading_time}min read"
            elif source == "arXiv":
                published = article.get("published", "")
                extra = f" | {published}"
            
            output += f"{i}. [{title}]({url})\n"
            output += f"   Source: {source}{extra}\n"
            
            if "description" in article:
                desc = article.get("description", "")[:100]
                output += f"   {desc}...\n"
            
            output += "\n"
        
        return output


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    fetcher = ArticleFetcher()
    
    print("HACKER NEWS - Top Stories:")
    print("="*70)
    hn = fetcher.fetch_hn_top_stories(limit=5)
    for story in hn:
        print(f"• {story['title']}")
        print(f"  Score: {story['score']} | Author: {story['author']}\n")
    
    print("\nDEV.TO - AI Articles:")
    print("="*70)
    devto = fetcher.fetch_devto_articles(tag="ai", limit=3)
    for article in devto:
        print(f"• {article['title']}")
        print(f"  By: {article['author']} | {article['reading_time']}min read\n")
    
    print("\narXiv - AI Papers:")
    print("="*70)
    arxiv = fetcher.fetch_arxiv_papers(category="cs.AI", max_results=3)
    for paper in arxiv:
        print(f"• {paper['title']}")
        print(f"  Authors: {paper['authors'][:50]}...\n")
    
    print("\nWeekend Articles Collection:")
    print("="*70)
    weekend = fetcher.get_weekend_articles()
    print(json.dumps(weekend, indent=2, default=str))
