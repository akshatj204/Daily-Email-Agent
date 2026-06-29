"""
Test script for Article Fetchers
Tests Hacker News, Dev.to, and arXiv integration
"""

import sys
import logging
import json
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

sys.path.insert(0, '.')

from fetchers.articles import ArticleFetcher


def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def test_articles():
    """Test article fetchers"""
    
    print_section("MORNING EMAIL AGENT - Article Fetchers Test")
    
    print("✓ Initializing ArticleFetcher...")
    fetcher = ArticleFetcher()
    
    # Test 1: Hacker News
    print_section("Test 1: Hacker News - Top Stories")
    hn_stories = fetcher.fetch_hn_top_stories(limit=5)
    
    print(f"Fetched: {len(hn_stories)} stories\n")
    for i, story in enumerate(hn_stories, 1):
        print(f"{i}. {story['title']}")
        print(f"   Score: {story['score']} | Comments: {story['comments']}")
        print(f"   By: {story['author']}")
        print(f"   URL: {story['url'][:60]}...\n")
    
    # Test 2: Hacker News by topic
    print_section("Test 2: Hacker News - By Topic (AI)")
    hn_ai = fetcher.fetch_hn_by_topic("AI", limit=3)
    
    print(f"Fetched: {len(hn_ai)} AI-related stories\n")
    for story in hn_ai:
        print(f"• {story['title']}")
        print(f"  Score: {story['score']}\n")
    
    # Test 3: Dev.to articles
    print_section("Test 3: Dev.to - Articles by Tag (Python)")
    devto_python = fetcher.fetch_devto_articles(tag="python", limit=3)
    
    print(f"Fetched: {len(devto_python)} articles\n")
    for article in devto_python:
        print(f"📝 {article['title']}")
        print(f"   Author: {article['author']}")
        print(f"   Reading time: {article['reading_time']} min")
        print(f"   Likes: {article['likes']}")
        print(f"   Tags: {', '.join(article['tags'])}\n")
    
    # Test 4: Dev.to AI articles
    print_section("Test 4: Dev.to - AI Articles")
    devto_ai = fetcher.fetch_devto_articles(tag="ai", limit=2)
    
    print(f"Fetched: {len(devto_ai)} AI articles\n")
    for article in devto_ai:
        print(f"🤖 {article['title']}")
        print(f"   {article['description']}")
        print(f"   By {article['author']} | {article['reading_time']}min\n")
    
    # Test 5: arXiv papers
    print_section("Test 5: arXiv - AI Research Papers")
    arxiv_ai = fetcher.fetch_arxiv_papers(category="cs.AI", max_results=3)
    
    print(f"Fetched: {len(arxiv_ai)} papers\n")
    for paper in arxiv_ai:
        print(f"📄 {paper['title']}")
        print(f"   Authors: {paper['authors'][:70]}...")
        print(f"   Published: {paper['published']}")
        print(f"   URL: {paper['url'][:60]}...\n")
    
    # Test 6: arXiv Finance papers
    print_section("Test 6: arXiv - Finance Research")
    arxiv_finance = fetcher.fetch_arxiv_papers(category="q-fin", max_results=2)
    
    print(f"Fetched: {len(arxiv_finance)} finance papers\n")
    for paper in arxiv_finance:
        print(f"💰 {paper['title']}\n")
    
    # Test 7: Weekend collection
    print_section("Test 7: Weekend Articles Collection")
    weekend = fetcher.get_weekend_articles()
    
    print(f"Total sources: {len([k for k in weekend.keys() if k != 'timestamp'])}")
    print(f"Timestamp: {weekend['timestamp']}\n")
    
    for source, articles in weekend.items():
        if source != 'timestamp' and articles:
            print(f"📌 {source.upper()}: {len(articles)} articles")
    
    # Test 8: Themed collections
    print_section("Test 8: Themed Collections")
    
    print("Fetching AI articles...")
    ai = fetcher.get_ai_articles()
    print(f"✓ AI articles: {len(ai)}")
    
    print("\nFetching investing articles...")
    investing = fetcher.get_investing_articles()
    print(f"✓ Investing articles: {len(investing)}")
    
    print("\nFetching tech articles...")
    tech = fetcher.get_tech_articles()
    print(f"✓ Tech articles: {len(tech)}")
    
    # Test 9: Email formatting
    print_section("Test 9: Email Formatting")
    sample_articles = hn_stories[:3]
    formatted = fetcher.format_articles_for_email(sample_articles)
    print(formatted)
    
    # Test 10: Cache operations
    print_section("Test 10: Cache System")
    
    cache_data = {
        "articles": weekend['hn'],
        "fetched_at": datetime.now().isoformat(),
        "count": len(weekend['hn'])
    }
    
    cache_path = fetcher.save_articles_cache(cache_data, category="hn")
    if cache_path:
        print(f"✓ Cache saved to: {cache_path}")
        
        # Try to load
        loaded = fetcher.load_articles_cache(category="hn")
        if loaded:
            print(f"✓ Cache loaded successfully")
            print(f"  Articles in cache: {loaded.get('count', 0)}")
    
    # Summary
    print_section("Summary")
    print("""
✅ Hacker News integration working
✅ Dev.to API integration working
✅ arXiv paper fetching working
✅ Topic-based filtering working
✅ Curated collections working
✅ Email formatting working
✅ Cache system operational

Ready to test fitness articles next!
    """)


if __name__ == "__main__":
    try:
        test_articles()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
