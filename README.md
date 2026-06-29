# Morning Email Agent 🌅

A Python-based intelligent agent that sends you a curated morning email at 6 AM IST with:
- Market data (rotating daily: Asia-Pacific, Emerging Markets, US, Europe, Commodities)
- Economic calendar (key events from China, Japan, US, India, Europe)
- Fitness insights (rotating articles on running, swimming, strength training, etc.)
- Career & Learning (daily learning task + Python function of the day)
- Friday: Singapore job market opportunities
- Weekend: Curated articles on investing, AI, tech, travel

---

## Features

### Market Data (Daily Rotation)
- **Monday**: Asia-Pacific (Nifty, Sensex, Shanghai, Nikkei, Singapore, Australia)
- **Tuesday**: Emerging Markets (MSCI EM, Mexico, Brazil, Turkey, South Korea)
- **Wednesday**: US Markets (S&P 500, Nasdaq, Dow, Treasury yields, VIX)
- **Thursday**: Europe & Fixed Income (DAX, FTSE, CAC, STOXX, German yields)
- **Friday**: Weekly summary + Singapore job market article

### Economic Calendar
- Daily: 2-3 important economic events from China, Japan, US, India, Europe
- Weekly: Every Sunday, get next week's full economic calendar

### Fitness & Career
- Daily fitness article (rotating topics)
- Daily learning task (small, doable)
- Daily Python function of the day (with explanation)

### Smart Features
- **Caching**: Fallback to cached data if API fails
- **Error Handling**: Graceful degradation if data unavailable
- **Tracking**: Implicit tracking of engagement for future personalization
- **Scheduled**: Runs daily at 6 AM IST via cloud scheduler

---

## Project Structure

```
morning-email-agent/
├── fetchers/                   # Data fetching modules
│   ├── market_data.py         # Market indices, prices
│   ├── economic_calendar.py   # Economic events
│   ├── articles.py            # HN, Dev.to, arXiv
│   ├── fitness.py             # Fitness articles
│   ├── learning.py            # Learning tasks & Python functions
│   └── singapore_jobs.py      # Singapore job market
├── utils/
│   ├── storage.py             # JSON read/write
│   ├── email_builder.py       # HTML email template
│   └── logger.py              # Logging utilities
├── data/
│   ├── emails/                # Sent emails archive
│   ├── cache/                 # Cached API responses
│   ├── tasks/                 # Learning tasks & functions
│   └── logs/                  # Agent logs
├── main.py                    # Main orchestrator
├── test_market_data.py        # Test script
├── requirements.txt           # Dependencies
├── .gitignore                 # Git ignore
└── README.md                  # This file
```

---

## Setup & Installation

### 1. Clone & Setup
```bash
git clone https://github.com/yourusername/morning-email-agent.git
cd morning-email-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Test Market Data Fetcher
```bash
python test_market_data.py
```

Expected output:
- Market data for today's designated region
- Cache files created
- All systems operational ✓

### 3. (Later) Set Up Gmail API
- Create Google Cloud project
- Enable Gmail API
- Create OAuth 2.0 credentials
- Save `credentials.json` to project root

### 4. (Later) Deploy to Cloud
- Create Google Cloud Function
- Set up Cloud Scheduler (6 AM IST daily)
- Configure environment variables

---

## Data Sources

| Component | Source | Type | Notes |
|-----------|--------|------|-------|
| Market Data | yfinance | API | Free, reliable |
| Economic Calendar | FRED, Trading Economics | API + Manual | Free tier |
| Articles | HN, Dev.to, arXiv | API | Free |
| Fitness | Dev.to, Reddit, arXiv | API + Scrape | Free |
| Singapore Jobs | LinkedIn, JobStreet | Scrape | Free |
| Email | Gmail API | API | Free for personal use |

---

## Usage

### Run Locally
```bash
python main.py
```

### Create Test Email
```bash
python -c "from main import agent; agent.run()"
```

### View Logs
```bash
cat data/logs/agent_2026-06-27.log
```

---

## Configuration

Edit `data/config.json` to customize:
- Send time (default: 6:00 AM IST)
- Email recipients
- Data sources
- Topics of interest

---

## Future Enhancements

- [ ] Personalization engine (learns your interests)
- [ ] Firestore integration (scalable database)
- [ ] Advanced NLP (summarize articles)
- [ ] Portfolio tracking (your holdings)
- [ ] Mobile app notifications
- [ ] Slack/Teams integration

---

## Cost Breakdown

- **Cloud Scheduler**: Free (1st 3 invocations/month free)
- **Cloud Functions**: Free (2M calls/month)
- **Data APIs**: Free (yfinance, FRED, HN, etc.)
- **Gmail API**: Free (for personal use)
- **Storage**: Free (JSON files)

**Total Monthly Cost**: $0

*Optional upgrades later:*
- Trading Economics Pro: $99/year
- LinkedIn Premium: $240/year
- Medium membership: $5/month

---

## Contributing

Feel free to:
- Add new data sources
- Improve existing fetchers
- Optimize performance
- Add more regions/markets

---

## License

MIT - Feel free to use for personal or commercial use.

---

## Author

Created by Akshat Jain
- Location: Gurgaon, India
- Focus: Portfolio management, AI, quantitative finance

---

## Support

For issues or questions:
1. Check test output: `python test_market_data.py`
2. View logs: `data/logs/`
3. Verify API keys are set
4. Check network connectivity

---

## Next Steps

1. ✓ **Market Data Fetcher** (Just built!)
2. → **Economic Calendar** (Next)
3. → **Article Fetchers** (Articles, Fitness, Learning)
4. → **Email Builder** (HTML template)
5. → **Gmail Integration** (Send emails)
6. → **Cloud Deployment** (Schedule & run in cloud)

Ready to start building the economic calendar fetcher?
