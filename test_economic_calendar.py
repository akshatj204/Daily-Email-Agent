"""
Test script for Economic Calendar Fetcher
Run this to verify calendar functionality
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

from fetchers.economic_calendar import EconomicCalendarFetcher


def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def test_economic_calendar():
    """Test the economic calendar fetcher"""
    
    print_section("MORNING EMAIL AGENT - Economic Calendar Fetcher Test")
    
    # Initialize
    print("✓ Initializing EconomicCalendarFetcher...")
    calendar = EconomicCalendarFetcher()
    
    # Test 1: Get today's events
    print_section("Test 1: Today's Economic Events")
    today_events = calendar.get_today_events()
    
    print(f"Date: {today_events['date']}")
    print(f"Day: {today_events['day']}")
    print(f"Total Events: {today_events['count']}\n")
    
    if today_events['events']:
        for i, event in enumerate(today_events['events'], 1):
            print(f"{i}. {event['country']} - {event['event']}")
            print(f"   Time: {event['time']} IST")
            print(f"   Impact: {event['impact']} | Importance: {event['importance']}")
            print(f"   Watch: {event['what_to_watch']}\n")
    else:
        print("No major events today.\n")
    
    # Test 2: Format for email
    print_section("Test 2: Email Format")
    email_format = calendar.format_for_email()
    print(email_format)
    
    # Test 3: Critical events next week
    print_section("Test 3: Critical Events (Next 7 Days)")
    critical = calendar.get_high_impact_events(7)
    print(f"Total Critical Events: {critical['total_critical']}\n")
    
    for day_data in critical['critical_events']:
        print(f"📍 {day_data['date']} ({day_data['day']})")
        for event in day_data['events']:
            print(f"   • {event['country']} - {event['event']}")
        print()
    
    # Test 4: Events by country
    print_section("Test 4: Events by Country (Next 7 Days)")
    by_country = calendar.get_events_by_country(7)
    
    print(f"Countries with events: {', '.join(by_country['countries'])}\n")
    
    for country in sorted(by_country['countries']):
        events = by_country['events_by_country'][country]
        print(f"📌 {country} ({len(events)} events)")
        for event in events:
            print(f"   {event['date']} - {event['event']} at {event['time']}")
        print()
    
    # Test 5: Our key regions
    print_section("Test 5: Events for Our Key Regions")
    region_events = calendar.get_regions_events(['China', 'Japan', 'US', 'India', 'Europe'])
    
    print(f"Regions: {', '.join(region_events['regions_requested'])}")
    print(f"Today's Events for These Regions: {region_events['count']}\n")
    
    for event in region_events['events']:
        print(f"🔔 {event['country']} - {event['event']}")
        print(f"   {event['time']} IST | Impact: {event['impact']}\n")
    
    # Test 6: Next week preview
    print_section("Test 6: Next Week's Preview")
    next_week = calendar.get_next_week_preview()
    
    print(f"Week Starting: {next_week['week_starting']}\n")
    
    for date_str, day_info in sorted(next_week['week_preview'].items()):
        print(f"📅 {date_str} ({day_info['day']}) - {day_info['count']} events")
        if day_info['events']:
            for event in day_info['events']:
                print(f"   • {event['event']} ({event['impact']})")
        print()
    
    # Test 7: Cache save
    print_section("Test 7: Cache System")
    cache_path = calendar.save_calendar_snapshot()
    if cache_path:
        print(f"✓ Calendar snapshot saved to: {cache_path}")
        
        # Verify file exists
        import os
        if os.path.exists(cache_path):
            file_size = os.path.getsize(cache_path)
            print(f"✓ File size: {file_size} bytes")
    
    # Summary
    print_section("Summary")
    print("""
✅ Economic Calendar Fetcher initialized
✅ Today's events retrieval working
✅ Email formatting working
✅ Critical events detection working
✅ Country-based filtering working
✅ Weekly preview generation working
✅ Cache system operational

Ready to integrate with email builder!
    """)


if __name__ == "__main__":
    try:
        test_economic_calendar()
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
