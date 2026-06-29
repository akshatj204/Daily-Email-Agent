"""
Economic Calendar Fetcher
Provides daily economic events and weekly preview.
Hardcoded for reliability (no API dependency).
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class EconomicCalendarFetcher:
    """Fetch important economic events by day and region"""
    
    def __init__(self, cache_dir: str = "data/cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
        # Define important daily events
        # Format: {day_number: [{country, event, time_ist, impact, importance}]}
        # Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday, 5=Saturday, 6=Sunday
        self.daily_events = {
            0: [  # Monday
                {
                    "country": "China",
                    "event": "Manufacturing PMI",
                    "time": "09:30 AM",
                    "impact": "HIGH",
                    "importance": "CRITICAL",
                    "type": "Manufacturing",
                    "what_to_watch": "Expansion above 50, contraction below 50"
                },
                {
                    "country": "China",
                    "event": "Non-Manufacturing PMI",
                    "time": "09:45 AM",
                    "impact": "MEDIUM",
                    "importance": "HIGH",
                    "type": "Services",
                    "what_to_watch": "Services sector health indicator"
                },
                {
                    "country": "India",
                    "event": "Services PMI",
                    "time": "04:30 PM",
                    "impact": "MEDIUM",
                    "importance": "HIGH",
                    "type": "Services",
                    "what_to_watch": "India's services sector momentum"
                },
            ],
            1: [  # Tuesday
                {
                    "country": "Japan",
                    "event": "Manufacturing PMI",
                    "time": "08:30 AM",
                    "impact": "MEDIUM",
                    "importance": "HIGH",
                    "type": "Manufacturing",
                    "what_to_watch": "Japanese manufacturing health"
                },
                {
                    "country": "US",
                    "event": "ADP Employment Report",
                    "time": "01:15 PM",
                    "impact": "MEDIUM",
                    "importance": "HIGH",
                    "type": "Employment",
                    "what_to_watch": "Preview of official jobs report; look for 200k+ additions"
                },
                {
                    "country": "Europe",
                    "event": "Eurozone Services PMI",
                    "time": "10:00 AM",
                    "impact": "MEDIUM",
                    "importance": "HIGH",
                    "type": "Services",
                    "what_to_watch": "European services momentum"
                },
            ],
            2: [  # Wednesday
                {
                    "country": "China",
                    "event": "China GDP (Quarterly)",
                    "time": "10:00 AM",
                    "impact": "CRITICAL",
                    "importance": "CRITICAL",
                    "type": "GDP",
                    "what_to_watch": "Quarterly GDP growth rate; expected ~5% YoY"
                },
                {
                    "country": "US",
                    "event": "Fed Interest Rate Decision",
                    "time": "02:00 PM",
                    "impact": "CRITICAL",
                    "importance": "CRITICAL",
                    "type": "Monetary Policy",
                    "what_to_watch": "Rate cut/hike decision; Powell press conference follows"
                },
                {
                    "country": "Europe",
                    "event": "ECB Monetary Policy Decision",
                    "time": "01:45 PM",
                    "impact": "CRITICAL",
                    "importance": "CRITICAL",
                    "type": "Monetary Policy",
                    "what_to_watch": "Potential rate decision; inflation trends"
                },
            ],
            3: [  # Thursday
                {
                    "country": "UK",
                    "event": "UK CPI (Inflation)",
                    "time": "08:00 AM",
                    "impact": "HIGH",
                    "importance": "CRITICAL",
                    "type": "Inflation",
                    "what_to_watch": "Latest inflation reading; affects BoE policy"
                },
                {
                    "country": "Japan",
                    "event": "BOJ Policy Decision",
                    "time": "02:00 PM",
                    "impact": "CRITICAL",
                    "importance": "CRITICAL",
                    "type": "Monetary Policy",
                    "what_to_watch": "Potential rate hike; policy shifts expected"
                },
                {
                    "country": "US",
                    "event": "Initial Jobless Claims",
                    "time": "01:30 PM",
                    "impact": "MEDIUM",
                    "importance": "HIGH",
                    "type": "Employment",
                    "what_to_watch": "Weekly claims; look for <300k for healthy labor market"
                },
            ],
            4: [  # Friday
                {
                    "country": "US",
                    "event": "Non-Farm Payrolls (Jobs Report)",
                    "time": "01:30 PM",
                    "impact": "CRITICAL",
                    "importance": "CRITICAL",
                    "type": "Employment",
                    "what_to_watch": "Expected +200k jobs; unemployment rate, wage growth"
                },
                {
                    "country": "US",
                    "event": "Consumer Sentiment Index",
                    "time": "03:00 PM",
                    "impact": "MEDIUM",
                    "importance": "HIGH",
                    "type": "Consumer",
                    "what_to_watch": "Consumer confidence; spending indicator"
                },
                {
                    "country": "US",
                    "event": "University of Michigan Inflation",
                    "time": "03:00 PM",
                    "impact": "MEDIUM",
                    "importance": "MEDIUM",
                    "type": "Inflation",
                    "what_to_watch": "Consumer inflation expectations"
                },
            ],
            5: [  # Saturday
                {
                    "country": "India",
                    "event": "Weekend Markets Closed",
                    "time": "-",
                    "impact": "NONE",
                    "importance": "NONE",
                    "type": "Information",
                    "what_to_watch": "No trading; review week's market moves"
                },
            ],
            6: [  # Sunday
                {
                    "country": "Multi-Region",
                    "event": "Week Ahead Preview",
                    "time": "Check times below",
                    "impact": "VARIES",
                    "importance": "HIGH",
                    "type": "Preview",
                    "what_to_watch": "See detailed weekly calendar below"
                },
            ]
        }
    
    def get_today_events(self) -> Dict[str, Any]:
        """Get today's economic events"""
        today = datetime.now().weekday()
        
        events = self.daily_events.get(today, [])
        
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "day": datetime.now().strftime("%A"),
            "events": events,
            "count": len(events),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_next_week_preview(self) -> Dict[str, Any]:
        """Get full next week's economic calendar"""
        today = datetime.now()
        next_monday = today + timedelta(days=(7 - today.weekday()))
        
        week_preview = {}
        
        for day_offset in range(7):
            current_date = next_monday + timedelta(days=day_offset)
            day_num = current_date.weekday()
            day_name = current_date.strftime("%A")
            date_str = current_date.strftime("%Y-%m-%d")
            
            events = self.daily_events.get(day_num, [])
            
            week_preview[date_str] = {
                "day": day_name,
                "events": events,
                "count": len(events)
            }
        
        return {
            "week_starting": next_monday.strftime("%Y-%m-%d"),
            "week_preview": week_preview,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_high_impact_events(self, min_days: int = 7) -> Dict[str, Any]:
        """Get high-impact events in next N days"""
        today = datetime.now()
        high_impact_events = []
        
        for day_offset in range(min_days):
            current_date = today + timedelta(days=day_offset)
            day_num = current_date.weekday()
            date_str = current_date.strftime("%Y-%m-%d")
            day_name = current_date.strftime("%A")
            
            events = self.daily_events.get(day_num, [])
            
            # Filter for CRITICAL impact
            critical_events = [e for e in events if e.get("impact") == "CRITICAL"]
            
            if critical_events:
                high_impact_events.append({
                    "date": date_str,
                    "day": day_name,
                    "events": critical_events,
                    "count": len(critical_events)
                })
        
        return {
            "period_days": min_days,
            "critical_events": high_impact_events,
            "total_critical": sum(e["count"] for e in high_impact_events),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_events_by_country(self, days: int = 7) -> Dict[str, Any]:
        """Get events organized by country for next N days"""
        today = datetime.now()
        country_events = {}
        
        for day_offset in range(days):
            current_date = today + timedelta(days=day_offset)
            day_num = current_date.weekday()
            
            events = self.daily_events.get(day_num, [])
            
            for event in events:
                country = event.get("country")
                if country not in country_events:
                    country_events[country] = []
                
                country_events[country].append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "day": current_date.strftime("%A"),
                    **event
                })
        
        return {
            "period_days": days,
            "countries": sorted(country_events.keys()),
            "events_by_country": country_events,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_regions_events(self, regions: List[str] = None) -> Dict[str, Any]:
        """
        Get events for specific regions.
        
        Args:
            regions: List of regions to include
                    Options: ['China', 'Japan', 'US', 'India', 'Europe', 'UK']
        """
        if regions is None:
            regions = ['China', 'Japan', 'US', 'India', 'Europe', 'UK']
        
        today = self.get_today_events()
        
        # Filter today's events by region
        filtered_events = [
            e for e in today['events'] 
            if e.get('country') in regions
        ]
        
        return {
            "date": today['date'],
            "day": today['day'],
            "regions_requested": regions,
            "events": filtered_events,
            "count": len(filtered_events),
            "timestamp": today['timestamp']
        }
    
    def format_for_email(self) -> str:
        """Format today's events for email"""
        today_data = self.get_today_events()
        
        output = f"📅 Economic Calendar - {today_data['day']}\n"
        output += "=" * 60 + "\n\n"
        
        if not today_data['events']:
            output += "No major economic events scheduled today.\n"
            return output
        
        for event in today_data['events']:
            output += f"🔔 {event['country']} - {event['event']}\n"
            output += f"   Time: {event['time']} IST\n"
            output += f"   Impact: {event['impact']} | Importance: {event['importance']}\n"
            output += f"   Watch for: {event['what_to_watch']}\n\n"
        
        return output
    
    def save_calendar_snapshot(self) -> str:
        """Save today's calendar to cache"""
        today_data = self.get_today_events()
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        cache_path = os.path.join(self.cache_dir, f"econ_calendar_{date_str}.json")
        
        try:
            with open(cache_path, 'w') as f:
                json.dump(today_data, f, indent=2)
            logger.info(f"Saved calendar snapshot to {cache_path}")
            return cache_path
        except Exception as e:
            logger.error(f"Failed to save calendar: {str(e)}")
            return None


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    calendar = EconomicCalendarFetcher()
    
    # Today's events
    print("TODAY'S EVENTS:")
    print(calendar.format_for_email())
    
    # High impact events
    print("\n" + "="*60)
    print("CRITICAL EVENTS (Next 7 Days):")
    print("="*60 + "\n")
    critical = calendar.get_high_impact_events(7)
    print(json.dumps(critical, indent=2))
    
    # Events by region (for email)
    print("\n" + "="*60)
    print("EVENTS FOR OUR REGIONS:")
    print("="*60 + "\n")
    region_events = calendar.get_regions_events(['China', 'Japan', 'US', 'India', 'Europe'])
    print(json.dumps(region_events, indent=2))
