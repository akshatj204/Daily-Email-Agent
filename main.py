"""
Morning Email Agent - Main Orchestrator
Coordinates all fetchers, builds email, and prepares for sending.
"""

import sys
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import all fetchers and utilities
from fetchers import (
    MarketDataFetcher,
    EconomicCalendarFetcher,
    ArticleFetcher,
    FitnessAndLearningFetcher
)
from utils import Storage, EmailBuilder


class MorningEmailAgent:
    """
    Main agent that orchestrates the entire morning email pipeline.
    Fetches data, builds email, and prepares for sending.
    """
    
    def __init__(self):
        """Initialize all components"""
        self.timestamp = datetime.now()
        self.day_of_week = self.timestamp.strftime("%A")
        
        # Initialize fetchers
        self.market_fetcher = MarketDataFetcher()
        self.calendar_fetcher = EconomicCalendarFetcher()
        self.article_fetcher = ArticleFetcher()
        self.learning_fetcher = FitnessAndLearningFetcher()
        
        # Initialize utilities
        self.storage = Storage()
        self.email_builder = EmailBuilder()
        
        logger.info(f"Agent initialized for {self.day_of_week}")
    
    def fetch_all_data(self) -> Dict[str, Any]:
        """
        Fetch all data from all sources.
        Includes error handling with graceful degradation.
        """
        logger.info("Starting data fetch from all sources...")
        
        data = {
            "timestamp": self.timestamp.isoformat(),
            "day": self.day_of_week,
            "errors": []
        }
        
        # 1. Fetch market data
        try:
            logger.info("Fetching market data...")
            market_data = self.market_fetcher.get_daily_market_summary()
            data["market"] = market_data
            logger.info(f"✓ Market data: {market_data.get('region')}")
        except Exception as e:
            logger.error(f"Failed to fetch market data: {str(e)}")
            data["errors"].append(f"Market data: {str(e)}")
        
        # 2. Fetch economic calendar
        try:
            logger.info("Fetching economic calendar...")
            calendar_data = self.calendar_fetcher.get_today_events()
            data["calendar"] = calendar_data
            logger.info(f"✓ Economic calendar: {calendar_data['count']} events")
        except Exception as e:
            logger.error(f"Failed to fetch calendar: {str(e)}")
            data["errors"].append(f"Calendar: {str(e)}")
        
        # 3. Fetch fitness article
        try:
            logger.info("Fetching fitness article...")
            fitness_data = self.learning_fetcher.get_fitness_article_of_day()
            data["fitness"] = fitness_data
            logger.info(f"✓ Fitness: {fitness_data.get('title')}")
        except Exception as e:
            logger.error(f"Failed to fetch fitness: {str(e)}")
            data["errors"].append(f"Fitness: {str(e)}")
        
        # 4. Fetch learning task
        try:
            logger.info("Fetching learning task...")
            learning_data = self.learning_fetcher.get_today_learning_task()
            data["learning"] = learning_data
            logger.info(f"✓ Learning task: {learning_data.get('title')}")
        except Exception as e:
            logger.error(f"Failed to fetch learning task: {str(e)}")
            data["errors"].append(f"Learning task: {str(e)}")
        
        # 5. Fetch Python function
        try:
            logger.info("Fetching Python function...")
            func_data = self.learning_fetcher.get_python_function_of_day()
            data["python_function"] = func_data
            logger.info(f"✓ Python function: {func_data.get('name')}")
        except Exception as e:
            logger.error(f"Failed to fetch Python function: {str(e)}")
            data["errors"].append(f"Python function: {str(e)}")
        
        # 6. Fetch articles (weekend only)
        if self.day_of_week in ["Saturday", "Sunday"]:
            try:
                logger.info("Fetching curated articles...")
                articles = self.article_fetcher.get_weekend_articles()
                # Flatten the articles for email
                all_articles = []
                for key, articles_list in articles.items():
                    if key != "timestamp" and isinstance(articles_list, list):
                        all_articles.extend(articles_list)
                
                if all_articles:
                    data["articles"] = all_articles
                    logger.info(f"✓ Articles: {len(all_articles)} articles collected")
            except Exception as e:
                logger.warning(f"Failed to fetch articles: {str(e)}")
                data["errors"].append(f"Articles: {str(e)}")
        
        # 7. Fetch Singapore jobs (Friday only)
        if self.day_of_week == "Friday":
            try:
                logger.info("Fetching Singapore job opportunities...")
                jobs = self.article_fetcher.fetch_singapore_jobs() if hasattr(
                    self.article_fetcher, 'fetch_singapore_jobs') else []
                
                if jobs:
                    data["singapore_jobs"] = jobs
                    logger.info(f"✓ Singapore jobs: {len(jobs)} opportunities")
            except Exception as e:
                logger.warning(f"Failed to fetch Singapore jobs: {str(e)}")
                data["errors"].append(f"Singapore jobs: {str(e)}")
        
        logger.info(f"Data fetch complete. Errors: {len(data['errors'])}")
        return data
    
    def build_email(self, data: Dict[str, Any]) -> str:
        """
        Build HTML email from fetched data.
        """
        logger.info("Building email...")
        
        try:
            # Remove metadata before passing to email builder
            email_data = {k: v for k, v in data.items() 
                         if k not in ["timestamp", "day", "errors"]}
            
            html = self.email_builder.build_email(email_data)
            logger.info(f"✓ Email built successfully ({len(html)} bytes)")
            return html
        
        except Exception as e:
            logger.error(f"Failed to build email: {str(e)}")
            raise
    
    def save_email(self, html: str) -> Optional[str]:
        """
        Save email HTML to file for archival.
        """
        try:
            filepath = self.email_builder.save_email_html(html)
            logger.info(f"✓ Email saved to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save email: {str(e)}")
            return None
    
    def log_execution(self, data: Dict[str, Any]) -> None:
        """
        Log execution details for tracking.
        """
        log_entry = {
            "event": "morning_email_generated",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "day": self.day_of_week,
            "data_sources_fetched": len([k for k in data.keys() 
                                        if k not in ["timestamp", "day", "errors"]]),
            "errors": len(data.get("errors", [])),
            "status": "success" if len(data.get("errors", [])) == 0 else "partial"
        }
        
        self.storage.append_log(log_entry)
        logger.info(f"✓ Execution logged")
    
    def run(self) -> Dict[str, Any]:
        """
        Execute the complete morning email pipeline.
        
        Returns:
            Dict with keys: data, html, filepath, status
        """
        logger.info("="*70)
        logger.info(f"MORNING EMAIL AGENT - {self.day_of_week}, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("="*70)
        
        result = {
            "status": "success",
            "data": None,
            "html": None,
            "filepath": None,
            "errors": []
        }
        
        try:
            # Step 1: Fetch all data
            logger.info("\n[Step 1/4] Fetching data from all sources...")
            data = self.fetch_all_data()
            result["data"] = data
            
            if data.get("errors"):
                result["status"] = "partial"
                logger.warning(f"Encountered {len(data['errors'])} errors during data fetch")
            
            # Step 2: Build email
            logger.info("\n[Step 2/4] Building email...")
            html = self.build_email(data)
            result["html"] = html
            
            # Step 3: Save email
            logger.info("\n[Step 3/4] Saving email...")
            filepath = self.save_email(html)
            result["filepath"] = filepath
            
            # Step 4: Log execution
            logger.info("\n[Step 4/4] Logging execution...")
            self.log_execution(data)
            
            logger.info("\n" + "="*70)
            logger.info("✅ MORNING EMAIL AGENT - EXECUTION SUCCESSFUL")
            logger.info("="*70)
            logger.info(f"Email ready for sending")
            logger.info(f"Saved to: {filepath}")
            logger.info(f"Status: {result['status']}")
            logger.info("="*70)
            
            return result
        
        except Exception as e:
            result["status"] = "failed"
            result["errors"].append(str(e))
            logger.error(f"\n❌ FATAL ERROR: {str(e)}")
            logger.error("="*70)
            return result
    
    def get_summary(self, result: Dict[str, Any]) -> str:
        """
        Get readable summary of execution.
        """
        data = result.get("data", {})
        
        summary = f"""
{'='*70}
MORNING EMAIL AGENT - EXECUTION SUMMARY
{'='*70}

Status: {result['status'].upper()}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Day: {data.get('day', 'Unknown')}

Data Sources:
✓ Market Data: {bool(data.get('market'))}
✓ Economic Calendar: {bool(data.get('calendar'))}
✓ Fitness Article: {bool(data.get('fitness'))}
✓ Learning Task: {bool(data.get('learning'))}
✓ Python Function: {bool(data.get('python_function'))}
✓ Articles: {bool(data.get('articles'))}
✓ Singapore Jobs: {bool(data.get('singapore_jobs'))}

Email Stats:
- HTML Size: {len(result.get('html', '')) if result.get('html') else 0:,} bytes
- Saved to: {result.get('filepath', 'N/A')}

Errors: {len(data.get('errors', []))}
{chr(10).join(f"  - {e}" for e in data.get('errors', []))}

Next Step: Email ready for sending via Gmail API
{'='*70}
"""
        return summary


# Example usage and testing
if __name__ == "__main__":
    print("\n" + "="*70)
    print("  MORNING EMAIL AGENT - ORCHESTRATOR TEST")
    print("="*70 + "\n")
    
    # Create and run agent
    agent = MorningEmailAgent()
    
    print("Running morning email pipeline...")
    result = agent.run()
    
    # Print summary
    print(agent.get_summary(result))
    
    # Show email preview if successful
    if result["status"] in ["success", "partial"] and result.get("html"):
        print("\nEmail Preview (first 1500 characters):")
        print("-" * 70)
        print(result["html"][:1500])
        print("\n... [email continues] ...")

        # Send email via Gmail
        from utils.gmail_sender import GmailSender
        sender = GmailSender()
        sender.send_morning_email(
            to='akshat.jain204@gmail.com',
            html_body=result['html'],
            day_of_week=agent.day_of_week
        )
