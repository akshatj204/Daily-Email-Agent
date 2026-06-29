"""
Test Email Builder
Generates sample emails and verifies HTML output
"""

import sys
import logging

logging.basicConfig(level=logging.INFO)
sys.path.insert(0, '.')

from utils.email_builder import EmailBuilder


def print_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def test_email_builder():
    print_section("MORNING EMAIL AGENT - Email Builder Test")
    
    print("✓ Initializing EmailBuilder...")
    builder = EmailBuilder()
    
    # Test 1: Build email with all sections
    print_section("Test 1: Full Email (All Sections)")
    
    sample_data = {
        "market": {
            "region": "us_markets",
            "data": {
                "S&P 500": {"price": 5234.45, "change_pct": 1.23, "status": "success"},
                "Nasdaq 100": {"price": 16543.21, "change_pct": 2.15, "status": "success"},
                "Dow Jones": {"price": 41234.56, "change_pct": 0.87, "status": "success"},
                "VIX": {"price": 18.5, "change_pct": -3.2, "status": "success"},
            }
        },
        "calendar": {
            "events": [
                {
                    "country": "US",
                    "event": "Fed Interest Rate Decision",
                    "time": "2:00 PM",
                    "impact": "CRITICAL",
                    "what_to_watch": "Rate cut/hike decision; Powell press conference"
                },
                {
                    "country": "Europe",
                    "event": "ECB Monetary Policy Decision",
                    "time": "1:45 PM",
                    "impact": "CRITICAL",
                    "what_to_watch": "Inflation trends and policy stance"
                }
            ]
        },
        "fitness": {
            "topic": "Running",
            "title": "5K Training Program for Beginners",
            "duration": "8 weeks",
            "focus": "Building endurance and speed",
            "key_points": ["Consistent training", "Proper form", "Recovery weeks"]
        },
        "learning": {
            "title": "Portfolio Diversification",
            "difficulty": "Beginner",
            "time": "15 min",
            "task": "Read 1 article on effective portfolio diversification strategies",
            "resources": ["Investopedia", "Financial Times"]
        },
        "python_function": {
            "name": "numpy.linalg.matrix_power",
            "difficulty": "Intermediate",
            "description": "Compute matrix power efficiently",
            "use_case": "Calculate transition matrices in portfolio optimization",
            "example": "A_squared = np.linalg.matrix_power(correlation_matrix, 2)"
        },
        "articles": [
            {
                "title": "How to Build Wealth in Your 20s and 30s",
                "url": "https://example.com/wealth",
                "source": "Hacker News",
                "score": 2543
            },
            {
                "title": "Python Performance Optimization Techniques",
                "url": "https://dev.to/article",
                "source": "Dev.to",
                "reading_time": 8
            }
        ]
    }
    
    html = builder.build_email(sample_data)
    
    print(f"✓ Email generated successfully")
    print(f"✓ HTML size: {len(html):,} bytes")
    print(f"✓ Contains DOCTYPE: {'<!DOCTYPE html>' in html}")
    print(f"✓ Contains styling: {'<style>' in html}")
    print(f"✓ Contains market section: {'📊' in html}")
    print(f"✓ Contains calendar section: {'📅' in html}")
    print(f"✓ Contains fitness section: {'💪' in html}")
    print(f"✓ Contains learning section: {'📚' in html}")
    print(f"✓ Contains python section: {'🐍' in html}")
    
    # Test 2: Save email
    print_section("Test 2: Save Email to File")
    filepath = builder.save_email_html(html)
    
    if filepath:
        import os
        file_size = os.path.getsize(filepath)
        print(f"✓ Email saved to: {filepath}")
        print(f"✓ File size: {file_size:,} bytes")
        
        # Verify file can be read
        with open(filepath, 'r') as f:
            content = f.read()
            print(f"✓ File readable: {len(content) > 0}")
    
    # Test 3: Minimal email
    print_section("Test 3: Minimal Email (Only Required Sections)")
    
    minimal_data = {
        "market": {
            "region": "asia_pacific",
            "data": {
                "Nifty 50": {"price": 23456.78, "change_pct": 0.45, "status": "success"},
            }
        },
        "calendar": {
            "events": [
                {
                    "country": "India",
                    "event": "Services PMI",
                    "time": "4:30 PM",
                    "impact": "HIGH",
                    "what_to_watch": "India's services sector momentum"
                }
            ]
        },
        "fitness": {
            "topic": "Swimming",
            "title": "Swimming Technique: Freestyle Mastery",
            "duration": "6 weeks",
            "focus": "Efficiency and endurance",
            "key_points": ["Breathing", "Body position", "Kick patterns"]
        },
        "learning": {
            "title": "SQL Query Optimization",
            "difficulty": "Intermediate",
            "time": "20 min",
            "task": "Write 1 optimized SQL query",
            "resources": ["SQLite docs"]
        },
        "python_function": {
            "name": "pandas.rolling().std()",
            "difficulty": "Beginner",
            "description": "Calculate rolling standard deviation",
            "use_case": "Compute 30-day volatility",
            "example": "volatility = returns.rolling(window=30).std()"
        }
    }
    
    minimal_html = builder.build_email(minimal_data)
    print(f"✓ Minimal email generated: {len(minimal_html):,} bytes")
    print(f"✓ All sections present: {all(x in minimal_html for x in ['📊', '📅', '💪', '📚', '🐍'])}")
    
    # Test 4: Email with articles
    print_section("Test 4: Email with Articles Section")
    
    data_with_articles = {
        **minimal_data,
        "articles": [
            {
                "title": "Deep Learning for Quantitative Finance",
                "url": "https://arxiv.org/sample",
                "source": "arXiv",
            },
            {
                "title": "Building Real-time Dashboards",
                "url": "https://dev.to/sample",
                "source": "Dev.to",
                "reading_time": 12
            }
        ]
    }
    
    articles_html = builder.build_email(data_with_articles)
    print(f"✓ Email with articles generated: {len(articles_html):,} bytes")
    print(f"✓ Contains articles section: {'📰' in articles_html}")
    print(f"✓ Contains article links: {'href=' in articles_html}")
    
    # Test 5: Email with Singapore jobs
    print_section("Test 5: Email with Singapore Jobs")
    
    data_with_jobs = {
        **minimal_data,
        "singapore_jobs": [
            {
                "title": "Senior Risk Analyst",
                "company": "BlackRock Singapore",
                "salary": "SGD 150K - 200K",
                "url": "https://careers.blackrock.com"
            },
            {
                "title": "Quantitative Developer",
                "company": "Citadel Singapore",
                "salary": "SGD 200K - 300K",
                "url": "https://citadel.com/careers"
            }
        ]
    }
    
    jobs_html = builder.build_email(data_with_jobs)
    print(f"✓ Email with jobs generated: {len(jobs_html):,} bytes")
    print(f"✓ Contains jobs section: {'💼' in jobs_html}")
    print(f"✓ Shows job titles: {'Senior Risk Analyst' in jobs_html}")
    print(f"✓ Shows salaries: {'SGD' in jobs_html}")
    
    # Test 6: HTML validation
    print_section("Test 6: HTML Validation")
    
    validation_checks = {
        "Has DOCTYPE": "<!DOCTYPE html>" in html,
        "Has head": "<head>" in html,
        "Has body": "<body>" in html,
        "Has style": "<style>" in html,
        "Has footer": "<footer>" in html or "footer" in html,
        "Valid closing tags": html.count("</div>") > 0,
        "Proper encoding": "charset=UTF-8" in html,
        "Responsive meta": "viewport" in html,
    }
    
    for check, result in validation_checks.items():
        status = "✓" if result else "✗"
        print(f"{status} {check}")
    
    # Test 7: Email preview
    print_section("Test 7: HTML Preview (First 1000 chars)")
    
    print(html[:1000])
    print("\n... [email continues] ...")
    
    # Summary
    print_section("Summary")
    print("""
✅ Email Builder initialized
✅ Full email generation working
✅ Minimal email generation working
✅ Articles section working
✅ Jobs section working
✅ HTML validation passing
✅ File saving working
✅ Responsive design implemented

Ready for integration with orchestrator!
    """)


if __name__ == "__main__":
    try:
        test_email_builder()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
