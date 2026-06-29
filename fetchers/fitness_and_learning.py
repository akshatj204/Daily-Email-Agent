"""
Fitness & Learning Fetcher
Provides daily fitness articles and learning tasks.
"""

import json
import os
import random
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class FitnessAndLearningFetcher:
    """Fetch fitness articles and learning tasks"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.tasks_dir = os.path.join(data_dir, "tasks")
        os.makedirs(self.tasks_dir, exist_ok=True)
        
        # Daily learning tasks (map to day of week)
        self.learning_tasks = {
            "Monday": {
                "title": "Portfolio Diversification",
                "task": "Read 1 article on effective portfolio diversification strategies",
                "difficulty": "Beginner",
                "time": "15 min",
                "resources": ["Investopedia", "Financial Times"]
            },
            "Tuesday": {
                "title": "Python Risk Calculation",
                "task": "Write 1 Python function to calculate portfolio volatility (standard deviation)",
                "difficulty": "Intermediate",
                "time": "30 min",
                "resources": ["NumPy docs", "Pandas docs"]
            },
            "Wednesday": {
                "title": "SQL Query Optimization",
                "task": "Write 1 optimized SQL query for calculating weighted portfolio returns",
                "difficulty": "Intermediate",
                "time": "20 min",
                "resources": ["SQLite docs", "Your notes"]
            },
            "Thursday": {
                "title": "Asset Allocation Models",
                "task": "Study 1 asset allocation model (e.g., 60/40, All-Weather)",
                "difficulty": "Intermediate",
                "time": "25 min",
                "resources": ["Harry Markowitz papers", "Ray Dalio"]
            },
            "Friday": {
                "title": "AI in Finance",
                "task": "Read 1 research paper on AI applications in portfolio management",
                "difficulty": "Advanced",
                "time": "40 min",
                "resources": ["arXiv", "Research Gate"]
            },
            "Saturday": {
                "title": "Streamlit Dashboard",
                "task": "Build 1 simple Streamlit dashboard with portfolio metrics",
                "difficulty": "Intermediate",
                "time": "45 min",
                "resources": ["Streamlit docs", "Your previous code"]
            },
            "Sunday": {
                "title": "Weekly Review",
                "task": "Review this week's learning + plan next week's topics",
                "difficulty": "Beginner",
                "time": "20 min",
                "resources": ["Your notes", "Progress log"]
            }
        }
        
        # Python functions of the day
        self.python_functions = [
            {
                "name": "numpy.linalg.matrix_power",
                "description": "Compute matrix power efficiently",
                "use_case": "Calculate transition matrices in portfolio optimization",
                "example": "A_squared = np.linalg.matrix_power(correlation_matrix, 2)",
                "difficulty": "Intermediate"
            },
            {
                "name": "pandas.rolling().std()",
                "description": "Calculate rolling standard deviation",
                "use_case": "Compute 30-day volatility for trend analysis",
                "example": "volatility = returns.rolling(window=30).std()",
                "difficulty": "Beginner"
            },
            {
                "name": "scipy.optimize.minimize",
                "description": "Minimize an objective function (portfolio risk)",
                "use_case": "Find optimal portfolio weights for given constraints",
                "example": "result = minimize(portfolio_variance, x0, constraints=constraints)",
                "difficulty": "Advanced"
            },
            {
                "name": "pandas.corr()",
                "description": "Calculate correlation matrix",
                "use_case": "Understand relationships between assets",
                "example": "corr_matrix = returns.corr()",
                "difficulty": "Beginner"
            },
            {
                "name": "numpy.dot()",
                "description": "Compute dot product (matrix multiplication)",
                "use_case": "Calculate portfolio returns and weights",
                "example": "port_return = np.dot(weights, returns)",
                "difficulty": "Intermediate"
            },
            {
                "name": "pandas.concat()",
                "description": "Concatenate multiple DataFrames",
                "use_case": "Combine multiple assets' time series",
                "example": "combined = pd.concat([asset1, asset2, asset3], axis=1)",
                "difficulty": "Beginner"
            },
            {
                "name": "numpy.percentile()",
                "description": "Calculate Value at Risk (VaR)",
                "use_case": "Find portfolio loss at given confidence level",
                "example": "var_95 = np.percentile(returns, 5)",
                "difficulty": "Intermediate"
            },
            {
                "name": "scipy.stats.zscore()",
                "description": "Standardize data",
                "use_case": "Normalize features for machine learning models",
                "example": "z_scores = scipy.stats.zscore(returns)",
                "difficulty": "Intermediate"
            },
            {
                "name": "sklearn.decomposition.PCA",
                "description": "Principal Component Analysis",
                "use_case": "Reduce dimensionality in large portfolios",
                "example": "pca = PCA(n_components=3).fit(returns)",
                "difficulty": "Advanced"
            },
            {
                "name": "plotly.graph_objects.Scatter",
                "description": "Interactive scatter plot",
                "use_case": "Visualize risk-return tradeoff",
                "example": "fig = go.Figure(data=go.Scatter(x=risk, y=return))",
                "difficulty": "Intermediate"
            },
        ]
        
        # Fitness topics (rotating)
        self.fitness_articles = [
            {
                "topic": "Running",
                "title": "5K Training Program for Beginners",
                "focus": "Building endurance and speed",
                "duration": "8 weeks",
                "key_points": ["Consistent training", "Proper form", "Recovery"],
                "source": "Running communities"
            },
            {
                "topic": "Swimming",
                "title": "Swimming Technique: Freestyle Mastery",
                "focus": "Efficiency and endurance in water",
                "duration": "6 weeks",
                "key_points": ["Breathing technique", "Body position", "Kick patterns"],
                "source": "Swimming coaching resources"
            },
            {
                "topic": "Strength Training",
                "title": "Progressive Overload: Building Muscle",
                "focus": "Systematic strength increase",
                "duration": "12 weeks",
                "key_points": ["Progressive weights", "Volume management", "Recovery time"],
                "source": "Strength training science"
            },
            {
                "topic": "Nutrition Science",
                "title": "Protein Timing for Muscle Recovery",
                "focus": "Optimal nutrient timing post-workout",
                "duration": "Ongoing",
                "key_points": ["Post-workout window", "Protein synthesis", "Amino acids"],
                "source": "Sports nutrition research"
            },
            {
                "topic": "HIIT",
                "title": "High Intensity Interval Training Benefits",
                "focus": "Efficient cardio workouts",
                "duration": "4-6 weeks",
                "key_points": ["Intensity variation", "Recovery periods", "Metabolic impact"],
                "source": "Exercise physiology"
            },
            {
                "topic": "Yoga",
                "title": "Yoga for Flexibility and Mobility",
                "focus": "Injury prevention and recovery",
                "duration": "12 weeks",
                "key_points": ["Flexibility", "Body awareness", "Stress reduction"],
                "source": "Yoga science"
            },
            {
                "topic": "Cycling",
                "title": "Cycling Performance: VO2 Max Training",
                "focus": "Aerobic capacity building",
                "duration": "8-10 weeks",
                "key_points": ["Zone training", "Cadence", "Endurance builds"],
                "source": "Cycling coaching"
            },
            {
                "topic": "Recovery",
                "title": "Active Recovery and Deloading",
                "focus": "Prevent overtraining syndrome",
                "duration": "Ongoing",
                "key_points": ["Rest days", "Sleep quality", "Light activity"],
                "source": "Sports science"
            },
        ]
    
    def get_today_learning_task(self) -> Dict[str, Any]:
        """Get today's learning task"""
        day_name = datetime.now().strftime("%A")
        
        task = self.learning_tasks.get(day_name, self.learning_tasks["Monday"])
        
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "day": day_name,
            **task,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_python_function_of_day(self) -> Dict[str, Any]:
        """Get Python function for today"""
        # Use day of year as seed for consistent rotation
        day_of_year = datetime.now().timetuple().tm_yday
        index = day_of_year % len(self.python_functions)
        
        func = self.python_functions[index]
        
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            **func,
            "position": f"{index + 1}/{len(self.python_functions)}",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_fitness_article_of_day(self) -> Dict[str, Any]:
        """Get fitness article for today"""
        # Rotate daily
        day_of_year = datetime.now().timetuple().tm_yday
        index = day_of_year % len(self.fitness_articles)
        
        article = self.fitness_articles[index]
        
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "day": datetime.now().strftime("%A"),
            **article,
            "position": f"{index + 1}/{len(self.fitness_articles)}",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_random_fitness_article(self) -> Dict[str, Any]:
        """Get random fitness article (for variation)"""
        article = random.choice(self.fitness_articles)
        
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "day": datetime.now().strftime("%A"),
            **article,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_fitness_article_by_topic(self, topic: str) -> Optional[Dict[str, Any]]:
        """Get fitness article by specific topic"""
        for article in self.fitness_articles:
            if article["topic"].lower() == topic.lower():
                return {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    **article,
                    "timestamp": datetime.now().isoformat()
                }
        return None
    
    def get_all_learning_tasks(self) -> Dict[str, Any]:
        """Get all learning tasks"""
        return {
            "total_tasks": len(self.learning_tasks),
            "tasks": self.learning_tasks,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_all_python_functions(self) -> Dict[str, Any]:
        """Get all Python functions"""
        return {
            "total_functions": len(self.python_functions),
            "functions": self.python_functions,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_all_fitness_topics(self) -> Dict[str, Any]:
        """Get all fitness topics available"""
        topics = [a["topic"] for a in self.fitness_articles]
        
        return {
            "total_topics": len(self.fitness_articles),
            "topics": sorted(set(topics)),
            "articles": self.fitness_articles,
            "timestamp": datetime.now().isoformat()
        }
    
    def format_task_for_email(self, task: Dict[str, Any]) -> str:
        """Format learning task for email"""
        output = "📚 Today's Learning Task\n"
        output += "=" * 60 + "\n\n"
        output += f"Topic: {task.get('title', 'N/A')}\n"
        output += f"Difficulty: {task.get('difficulty', 'N/A')}\n"
        output += f"Time: {task.get('time', 'N/A')}\n\n"
        output += f"Task:\n{task.get('task', 'N/A')}\n\n"
        output += f"Resources: {', '.join(task.get('resources', []))}\n"
        
        return output
    
    def format_python_function_for_email(self, func: Dict[str, Any]) -> str:
        """Format Python function for email"""
        output = "🐍 Python Function of the Day\n"
        output += "=" * 60 + "\n\n"
        output += f"Function: {func.get('name', 'N/A')}\n"
        output += f"Difficulty: {func.get('difficulty', 'N/A')}\n\n"
        output += f"Description:\n{func.get('description', 'N/A')}\n\n"
        output += f"Use Case:\n{func.get('use_case', 'N/A')}\n\n"
        output += f"Example:\n```python\n{func.get('example', 'N/A')}\n```\n"
        
        return output
    
    def format_fitness_article_for_email(self, article: Dict[str, Any]) -> str:
        """Format fitness article for email"""
        output = "💪 Fitness Insight\n"
        output += "=" * 60 + "\n\n"
        output += f"Topic: {article.get('topic', 'N/A')}\n"
        output += f"Title: {article.get('title', 'N/A')}\n"
        output += f"Duration: {article.get('duration', 'N/A')}\n\n"
        output += f"Focus:\n{article.get('focus', 'N/A')}\n\n"
        output += f"Key Points:\n"
        for point in article.get('key_points', []):
            output += f"• {point}\n"
        output += f"\nSource: {article.get('source', 'N/A')}\n"
        
        return output


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    fetcher = FitnessAndLearningFetcher()
    
    print("TODAY'S LEARNING TASK:")
    print("="*70)
    task = fetcher.get_today_learning_task()
    print(json.dumps(task, indent=2))
    
    print("\n\nPYTHON FUNCTION OF THE DAY:")
    print("="*70)
    func = fetcher.get_python_function_of_day()
    print(json.dumps(func, indent=2))
    
    print("\n\nFITNESS ARTICLE OF THE DAY:")
    print("="*70)
    fitness = fetcher.get_fitness_article_of_day()
    print(json.dumps(fitness, indent=2))
    
    print("\n\nALL FITNESS TOPICS:")
    print("="*70)
    topics = fetcher.get_all_fitness_topics()
    for topic in topics['topics']:
        print(f"• {topic}")
