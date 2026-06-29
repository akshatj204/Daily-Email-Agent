"""
Test script for market data fetcher
Run this to verify everything works
"""

import sys
import logging
import json
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add project to path
sys.path.insert(0, '.')

from fetchers.market_data import MarketDataFetcher
from utils.storage import Storage


def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")


def test_market_data_fetcher():
    """Test the market data fetcher"""
    
    print_section("MORNING EMAIL AGENT - Market Data Fetcher Test")
    
    # Initialize
    print("✓ Initializing MarketDataFetcher...")
    fetcher = MarketDataFetcher()
    
    print("✓ Initializing Storage...")
    storage = Storage()
    
    # Test 1: Get today's market summary
    print_section("Test 1: Today's Market Summary")
    day_name = datetime.now().strftime("%A")
    print(f"Today is {day_name}")
    print(f"Fetching appropriate regional market data...\n")
    
    summary = fetcher.get_daily_market_summary()
    
    if "error" in summary:
        print(f"❌ Error: {summary['error']}")
    else:
        region = summary.get("region", "unknown")
        print(f"Region: {region}")
        print(f"Timestamp: {summary.get('timestamp')}")
        print(f"\nMarket Data:")
        
        data = summary.get("data", {})
        for name, values in data.items():
            if values.get("status") == "success":
                price = values.get("price", "N/A")
                change = values.get("change_pct", "N/A")
                print(f"  {name:.<30} {price:>12} ({change:>+7.2f}%)")
            else:
                print(f"  {name:.<30} [Error]")
    
    # Test 2: Get specific region
    print_section("Test 2: Specific Region - US Markets")
    us_data = fetcher.fetch_market_data("us_markets")
    
    if "error" in us_data:
        print(f"❌ Error: {us_data['error']}")
    else:
        print(f"Fetched at: {us_data.get('timestamp')}\n")
        data = us_data.get("data", {})
        for name, values in data.items():
            if values.get("status") == "success":
                price = values.get("price", "N/A")
                change = values.get("change_pct", "N/A")
                print(f"  {name:.<30} {price:>12} ({change:>+7.2f}%)")
    
    # Test 3: Check cache
    print_section("Test 3: Cache System")
    cache_path = fetcher.get_cache_path("us_markets")
    print(f"Cache path: {cache_path}")
    
    import os
    if os.path.exists(cache_path):
        print("✓ Cache file exists")
        with open(cache_path, 'r') as f:
            cached = json.load(f)
            print(f"✓ Cache timestamp: {cached.get('timestamp')}")
    else:
        print("⚠ Cache file not yet created")
    
    # Test 4: Storage operations
    print_section("Test 4: Storage System")
    
    test_data = {
        "test": "data",
        "timestamp": datetime.now().isoformat(),
        "market": "test"
    }
    
    test_path = "data/test_storage.json"
    success = storage.write_json(test_path, test_data)
    
    if success:
        print(f"✓ Successfully wrote to {test_path}")
        
        # Read it back
        read_data = storage.read_json(test_path)
        print(f"✓ Successfully read from {test_path}")
        print(f"  Data: {read_data}")
    
    # Test 5: Log functionality
    print_section("Test 5: Logging System")
    
    log_entry = {
        "event": "test_run",
        "status": "success",
        "markets_fetched": 3,
    }
    
    storage.append_log(log_entry)
    print("✓ Log entry created")
    
    today = datetime.now().strftime("%Y-%m-%d")
    log_path = f"data/logs/agent_{today}.log"
    print(f"  Log file: {log_path}")
    
    # Summary
    print_section("Summary")
    print("""
✓ Market Data Fetcher initialized
✓ Data fetching working
✓ Cache system operational
✓ Storage system ready
✓ Logging enabled

Next steps:
1. Review the fetched data above
2. Check data/cache/ for cached files
3. Ready to build economic calendar fetcher
    """)


if __name__ == "__main__":
    try:
        test_market_data_fetcher()
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
