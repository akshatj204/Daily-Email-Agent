"""
Market Data Fetcher
Fetches market data for different regions based on day of week.
Handles caching and fallback logic.
"""

import yfinance as yf
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class MarketDataFetcher:
    """Fetch and cache market data for different regions"""
    
    def __init__(self, cache_dir: str = "data/cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
        # Define indices for different regions
        self.indices = {
            "asia_pacific": {
                "Nifty 50": "^NSEI",
                "Sensex": "^BSESN",
                "Shanghai Composite": "000001.SS",
                "Nikkei 225": "^N225",
                "STI (Singapore)": "^STI",
                "ASX 200": "^AXJO",
            },
            "emerging_markets": {
                "MSCI EM": "IEMG",
                "Mexico IPC": "^MXX",
                "Brazil Ibovespa": "^BVSP",
                "Turkey": "XU100.IS",
                "South Korea KOSPI": "^KS11",
            },
            "us_markets": {
                "S&P 500": "^GSPC",
                "Nasdaq 100": "^NDX",
                "Dow Jones": "^DJI",
                "US 10Y Yield": "^TNX",
                "VIX": "^VIX",
            },
            "europe_fixed_income": {
                "DAX": "^GDAXI",
                "FTSE 100": "^FTSE",
                "CAC 40": "^FCHI",
                "STOXX 600": "^STOXX",
                "German 10Y Yield": "^TRICE",
            },
            "commodities": {
                "WTI Crude": "CL=F",
                "Gold": "GC=F",
                "Natural Gas": "NG=F",
                "Copper": "HG=F",
            },
            "currencies": {
                "INR/USD": "INRUSD=X",
                "EUR/USD": "EURUSD=X",
                "USD/JPY": "USDJPY=X",
                "USD/CNY": "USDCNY=X",
            }
        }
    
    def fetch_indices(self, tickers_dict: Dict[str, str]) -> Dict[str, Any]:
        """
        Fetch current price and change for multiple indices.
        
        Args:
            tickers_dict: Dict of {name: ticker_symbol}
        
        Returns:
            Dict with price, change %, and status
        """
        results = {}
        
        for name, ticker in tickers_dict.items():
            try:
                # Fetch 1 day history
                data = yf.Ticker(ticker).history(period="1d")
                
                if len(data) > 0:
                    close_price = data['Close'].iloc[-1]
                    
                    # Try to get previous close for change calculation
                    data_2d = yf.Ticker(ticker).history(period="2d")
                    if len(data_2d) > 1:
                        prev_close = data_2d['Close'].iloc[-2]
                        change_pct = ((close_price - prev_close) / prev_close) * 100
                    else:
                        change_pct = 0.0
                    
                    results[name] = {
                        "price": round(float(close_price), 2),
                        "change_pct": round(change_pct, 2),
                        "status": "success"
                    }
                else:
                    results[name] = {"status": "error", "error": "No data returned"}
                    
            except Exception as e:
                logger.warning(f"Failed to fetch {name} ({ticker}): {str(e)}")
                results[name] = {"status": "error", "error": str(e)}
        
        return results
    
    def get_cache_path(self, region: str, date: datetime = None) -> str:
        """Get cache file path for a region and date"""
        if date is None:
            date = datetime.now()
        
        date_str = date.strftime("%Y-%m-%d")
        return os.path.join(self.cache_dir, f"market_{region}_{date_str}.json")
    
    def load_from_cache(self, region: str) -> Dict[str, Any]:
        """Load market data from cache (today's file)"""
        cache_path = self.get_cache_path(region)
        
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load cache for {region}: {str(e)}")
        
        return None
    
    def save_to_cache(self, region: str, data: Dict[str, Any]) -> None:
        """Save market data to cache"""
        cache_path = self.get_cache_path(region)
        
        try:
            with open(cache_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save cache for {region}: {str(e)}")
    
    def fetch_market_data(self, region: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Fetch market data for a region with fallback to cache.
        
        Args:
            region: 'asia_pacific', 'emerging_markets', 'us_markets', etc.
            use_cache: If True, use cache on API failure
        
        Returns:
            Dict with indices data
        """
        # Try cache first
        if use_cache:
            cached_data = self.load_from_cache(region)
            if cached_data and cached_data.get("fetched_today") == True:
                logger.info(f"Using cached data for {region}")
                return cached_data
        
        # Fetch fresh data
        if region not in self.indices:
            return {"error": f"Unknown region: {region}"}
        
        logger.info(f"Fetching fresh data for {region}")
        tickers = self.indices[region]
        market_data = self.fetch_indices(tickers)
        
        # Add metadata
        result = {
            "region": region,
            "timestamp": datetime.now().isoformat(),
            "fetched_today": True,
            "data": market_data
        }
        
        # Save to cache
        self.save_to_cache(region, result)
        
        return result
    
    def get_daily_market_summary(self) -> Dict[str, Any]:
        """
        Get market summary based on day of week.
        Returns appropriate region's data.
        """
        day_of_week = datetime.now().weekday()  # 0=Monday, 6=Sunday
        
        # Map day to region
        day_mapping = {
            0: "asia_pacific",      # Monday
            1: "emerging_markets",  # Tuesday
            2: "us_markets",        # Wednesday
            3: "europe_fixed_income",  # Thursday
            4: "us_markets",        # Friday (weekly summary)
            5: "commodities",       # Saturday
            6: "currencies",        # Sunday
        }
        
        region = day_mapping.get(day_of_week, "asia_pacific")
        
        return self.fetch_market_data(region)
    
    def get_all_markets(self) -> Dict[str, Any]:
        """Get all market data (for comprehensive view)"""
        all_markets = {}
        
        for region in self.indices.keys():
            all_markets[region] = self.fetch_market_data(region)
        
        return all_markets


# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Test fetcher
    fetcher = MarketDataFetcher()
    
    # Get today's summary
    print("Today's Market Summary:")
    summary = fetcher.get_daily_market_summary()
    print(json.dumps(summary, indent=2))
    
    # Test with specific region
    print("\n\nUS Markets:")
    us_data = fetcher.fetch_market_data("us_markets")
    print(json.dumps(us_data, indent=2))
