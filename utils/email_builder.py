"""
Email Builder
Constructs beautiful HTML emails from all fetched data.
"""

import os
from datetime import datetime
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class EmailBuilder:
    """Build formatted HTML emails from fetcher data"""
    
    def __init__(self):
        self.email_date = datetime.now()
        self.day_of_week = self.email_date.strftime("%A")
    
    def build_email(self, data: Dict[str, Any]) -> str:
        """
        Build complete email HTML.
        
        Args:
            data: Dict with keys: market, calendar, fitness, learning, 
                  python_function, articles (optional), singapore_jobs (optional)
        
        Returns:
            HTML string ready to send
        """
        html = self._get_html_header()
        
        # Add sections based on data availability
        if data.get("market"):
            html += self._build_market_section(data["market"])
        
        if data.get("calendar"):
            html += self._build_calendar_section(data["calendar"])
        
        if data.get("fitness"):
            html += self._build_fitness_section(data["fitness"])
        
        if data.get("learning"):
            html += self._build_learning_section(data["learning"])
        
        if data.get("python_function"):
            html += self._build_python_function_section(data["python_function"])
        
        if data.get("articles"):
            html += self._build_articles_section(data["articles"])
        
        if data.get("singapore_jobs"):
            html += self._build_singapore_jobs_section(data["singapore_jobs"])
        
        html += self._get_html_footer()
        
        return html
    
    def _get_html_header(self) -> str:
        """Get HTML header with styles"""
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Morning Email - {self.day_of_week}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 600px;
            margin: 20px auto;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 28px;
            margin-bottom: 5px;
        }}
        
        .header p {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 20px;
        }}
        
        .section {{
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }}
        
        .section:last-child {{
            border-bottom: none;
        }}
        
        .section-title {{
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #667eea;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .section-title .emoji {{
            font-size: 24px;
        }}
        
        .metric {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 15px;
        }}
        
        .metric-item {{
            background: #f8f9fa;
            padding: 12px;
            border-radius: 6px;
            border-left: 4px solid #667eea;
        }}
        
        .metric-name {{
            font-size: 12px;
            color: #888;
            text-transform: uppercase;
            margin-bottom: 5px;
        }}
        
        .metric-value {{
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }}
        
        .metric-change {{
            font-size: 14px;
            margin-top: 5px;
        }}
        
        .positive {{
            color: #27ae60;
        }}
        
        .negative {{
            color: #e74c3c;
        }}
        
        .event {{
            background: #f8f9fa;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 12px;
            border-left: 4px solid #667eea;
        }}
        
        .event-header {{
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}
        
        .event-details {{
            font-size: 13px;
            color: #666;
        }}
        
        .impact-badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: bold;
            margin-right: 8px;
        }}
        
        .impact-critical {{
            background-color: #ffe5e5;
            color: #c41e3a;
        }}
        
        .impact-high {{
            background-color: #fff3cd;
            color: #856404;
        }}
        
        .impact-medium {{
            background-color: #d1ecf1;
            color: #0c5460;
        }}
        
        .article {{
            background: #f8f9fa;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 12px;
            border-left: 4px solid #667eea;
        }}
        
        .article-title {{
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}
        
        .article-source {{
            font-size: 12px;
            color: #888;
        }}
        
        .task-box {{
            background: #f0f7ff;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #667eea;
            margin-bottom: 15px;
        }}
        
        .task-title {{
            font-weight: bold;
            color: #333;
            margin-bottom: 8px;
        }}
        
        .task-meta {{
            display: flex;
            gap: 15px;
            font-size: 13px;
            color: #666;
            margin-bottom: 10px;
        }}
        
        .task-description {{
            color: #555;
            font-size: 14px;
        }}
        
        .code-box {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 12px;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            overflow-x: auto;
            margin: 10px 0;
        }}
        
        .footer {{
            background-color: #f8f9fa;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #888;
            border-top: 1px solid #eee;
        }}
        
        .footer a {{
            color: #667eea;
            text-decoration: none;
        }}
        
        .button {{
            display: inline-block;
            padding: 10px 20px;
            background-color: #667eea;
            color: white;
            border-radius: 6px;
            text-decoration: none;
            font-size: 14px;
            margin-top: 10px;
        }}
        
        .button:hover {{
            background-color: #764ba2;
        }}
        
        .alert {{
            background-color: #fffbea;
            border-left: 4px solid #ffc107;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 15px;
            font-size: 13px;
            color: #856404;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📧 Morning Update</h1>
            <p>{self.day_of_week}, {self.email_date.strftime('%B %d, %Y')}</p>
        </div>
        <div class="content">
"""
    
    def _build_market_section(self, market_data: Dict[str, Any]) -> str:
        """Build market data section"""
        html = """
            <div class="section">
                <div class="section-title">
                    <span class="emoji">📊</span>
                    <span>Market Data</span>
                </div>
"""
        
        region = market_data.get("region", "Unknown")
        data = market_data.get("data", {})
        
        html += f'                <p style="color: #666; font-size: 13px; margin-bottom: 15px;">Region: <strong>{region.title().replace("_", " ")}</strong></p>\n'
        
        html += '                <div class="metric">\n'
        
        count = 0
        for name, values in sorted(data.items()):
            if values.get("status") == "success":
                price = values.get("price", "N/A")
                change = values.get("change_pct", 0)
                
                change_class = "positive" if change >= 0 else "negative"
                change_symbol = "▲" if change >= 0 else "▼"
                
                html += f"""                    <div class="metric-item">
                        <div class="metric-name">{name}</div>
                        <div class="metric-value">{price}</div>
                        <div class="metric-change {change_class}">{change_symbol} {abs(change):.2f}%</div>
                    </div>
"""
                count += 1
                if count % 2 == 0:
                    html += '                </div>\n                <div class="metric">\n'
        
        html += """                </div>
            </div>
"""
        return html
    
    def _build_calendar_section(self, calendar_data: Dict[str, Any]) -> str:
        """Build economic calendar section"""
        html = """
            <div class="section">
                <div class="section-title">
                    <span class="emoji">📅</span>
                    <span>Economic Calendar</span>
                </div>
"""
        
        events = calendar_data.get("events", [])
        
        if not events:
            html += '                <p style="color: #888;">No major economic events scheduled.</p>\n'
        else:
            for event in events:
                country = event.get("country", "Unknown")
                event_name = event.get("event", "Unknown")
                time = event.get("time", "N/A")
                impact = event.get("impact", "MEDIUM")
                what_to_watch = event.get("what_to_watch", "")
                
                impact_class = f"impact-{impact.lower()}"
                
                html += f"""                <div class="event">
                    <div class="event-header">
                        <span class="impact-badge {impact_class}">{impact}</span>
                        {country} - {event_name}
                    </div>
                    <div class="event-details">
                        <strong>Time:</strong> {time} IST<br>
                        <strong>Watch for:</strong> {what_to_watch}
                    </div>
                </div>
"""
        
        html += """            </div>
"""
        return html
    
    def _build_fitness_section(self, fitness_data: Dict[str, Any]) -> str:
        """Build fitness section"""
        html = """
            <div class="section">
                <div class="section-title">
                    <span class="emoji">💪</span>
                    <span>Fitness Insight</span>
                </div>
"""
        
        topic = fitness_data.get("topic", "General")
        title = fitness_data.get("title", "Unknown")
        duration = fitness_data.get("duration", "N/A")
        focus = fitness_data.get("focus", "")
        key_points = fitness_data.get("key_points", [])
        
        html += f"""                <div class="task-box" style="background: #ffe5f0;">
                    <div class="task-title">{title}</div>
                    <div class="task-meta">
                        <span><strong>Topic:</strong> {topic}</span>
                        <span><strong>Duration:</strong> {duration}</span>
                    </div>
                    <div class="task-description">
                        <strong>Focus:</strong> {focus}<br><br>
                        <strong>Key Points:</strong>
"""
        
        for point in key_points:
            html += f"                        <br>• {point}"
        
        html += """
                    </div>
                </div>
            </div>
"""
        return html
    
    def _build_learning_section(self, learning_data: Dict[str, Any]) -> str:
        """Build learning task section"""
        html = """
            <div class="section">
                <div class="section-title">
                    <span class="emoji">📚</span>
                    <span>Today's Learning Task</span>
                </div>
"""
        
        title = learning_data.get("title", "Learning Task")
        difficulty = learning_data.get("difficulty", "Intermediate")
        time = learning_data.get("time", "30 min")
        task = learning_data.get("task", "")
        resources = learning_data.get("resources", [])
        
        html += f"""                <div class="task-box">
                    <div class="task-title">{title}</div>
                    <div class="task-meta">
                        <span><strong>Difficulty:</strong> {difficulty}</span>
                        <span><strong>Time:</strong> {time}</span>
                    </div>
                    <div class="task-description">
                        {task}<br><br>
                        <strong>Resources:</strong> {', '.join(resources)}
                    </div>
                </div>
            </div>
"""
        return html
    
    def _build_python_function_section(self, func_data: Dict[str, Any]) -> str:
        """Build Python function section"""
        html = """
            <div class="section">
                <div class="section-title">
                    <span class="emoji">🐍</span>
                    <span>Python Function of the Day</span>
                </div>
"""
        
        name = func_data.get("name", "Unknown")
        difficulty = func_data.get("difficulty", "Intermediate")
        description = func_data.get("description", "")
        use_case = func_data.get("use_case", "")
        example = func_data.get("example", "")
        
        html += f"""                <div class="task-box" style="background: #f0f5ff;">
                    <div class="task-title"><code>{name}</code></div>
                    <div class="task-meta">
                        <span><strong>Difficulty:</strong> {difficulty}</span>
                    </div>
                    <div class="task-description">
                        <strong>What it does:</strong> {description}<br><br>
                        <strong>Use case:</strong> {use_case}<br><br>
                        <strong>Example:</strong>
                        <div class="code-box">{example}</div>
                    </div>
                </div>
            </div>
"""
        return html
    
    def _build_articles_section(self, articles: List[Dict[str, Any]]) -> str:
        """Build curated articles section"""
        html = """
            <div class="section">
                <div class="section-title">
                    <span class="emoji">📰</span>
                    <span>Curated Articles</span>
                </div>
"""
        
        for article in articles[:5]:  # Limit to 5 articles
            title = article.get("title", "Untitled")
            url = article.get("url", "#")
            source = article.get("source", "Unknown")
            
            # Add source-specific info
            extra = ""
            if source == "Hacker News":
                score = article.get("score", 0)
                extra = f" • {score} upvotes"
            elif source == "Dev.to":
                reading_time = article.get("reading_time", 0)
                extra = f" • {reading_time}min read"
            
            html += f"""                <div class="article">
                    <div class="article-title"><a href="{url}" style="color: #667eea; text-decoration: none;">{title}</a></div>
                    <div class="article-source">{source}{extra}</div>
                </div>
"""
        
        html += """            </div>
"""
        return html
    
    def _build_singapore_jobs_section(self, jobs: List[Dict[str, Any]]) -> str:
        """Build Singapore jobs section"""
        html = """
            <div class="section">
                <div class="section-title">
                    <span class="emoji">💼</span>
                    <span>Singapore Job Opportunities</span>
                </div>
"""
        
        for job in jobs[:3]:  # Limit to 3 jobs
            title = job.get("title", "Job Title")
            company = job.get("company", "Company")
            salary = job.get("salary", "Competitive")
            url = job.get("url", "#")
            
            html += f"""                <div class="article">
                    <div class="article-title"><a href="{url}" style="color: #667eea; text-decoration: none;">{title}</a></div>
                    <div class="article-source"><strong>{company}</strong> • {salary}</div>
                </div>
"""
        
        html += """            </div>
"""
        return html
    
    def _get_html_footer(self) -> str:
        """Get HTML footer"""
        return """        </div>
        <div class="footer">
            <p>
                Morning Email Agent | Next update: Tomorrow at 6:00 AM IST
            </p>
            <p style="margin-top: 10px; color: #aaa;">
                <a href="#">View in Browser</a> • 
                <a href="#">Unsubscribe</a> • 
                <a href="#">Settings</a>
            </p>
        </div>
    </div>
</body>
</html>
"""
    
    def save_email_html(self, html: str, output_dir: str = "data/emails") -> str:
        """Save HTML email to file"""
        os.makedirs(output_dir, exist_ok=True)
        
        date_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filepath = os.path.join(output_dir, f"email_{date_str}.html")
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            logger.info(f"Email saved to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save email: {str(e)}")
            return None


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Sample data
    sample_data = {
        "market": {
            "region": "us_markets",
            "data": {
                "S&P 500": {"price": 5234.45, "change_pct": 1.23, "status": "success"},
                "Nasdaq": {"price": 16543.21, "change_pct": 2.15, "status": "success"},
            }
        },
        "calendar": {
            "events": [
                {
                    "country": "US",
                    "event": "Fed Decision",
                    "time": "2:00 PM",
                    "impact": "CRITICAL",
                    "what_to_watch": "Rate decision expected"
                }
            ]
        },
        "fitness": {
            "topic": "Running",
            "title": "5K Training Program",
            "duration": "8 weeks",
            "focus": "Building endurance",
            "key_points": ["Consistent training", "Proper form", "Recovery"]
        },
        "learning": {
            "title": "Python Risk Calculation",
            "difficulty": "Intermediate",
            "time": "30 min",
            "task": "Write a Python function to calculate volatility",
            "resources": ["NumPy docs", "Pandas docs"]
        },
        "python_function": {
            "name": "numpy.linalg.matrix_power",
            "difficulty": "Intermediate",
            "description": "Compute matrix power",
            "use_case": "Portfolio calculations",
            "example": "result = np.linalg.matrix_power(matrix, 2)"
        }
    }
    
    builder = EmailBuilder()
    html = builder.build_email(sample_data)
    
    # Save and print summary
    filepath = builder.save_email_html(html)
    print(f"✓ Email generated: {filepath}")
    print(f"✓ HTML size: {len(html)} bytes")
    
    # Show preview
    print("\nPreview (first 500 chars):")
    print(html[:500] + "...")
