"""
Storage Utilities
Handle reading/writing JSON data for the agent.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List


class Storage:
    """Handle JSON file operations"""
    
    def __init__(self, base_dir: str = "data"):
        self.base_dir = base_dir
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create necessary directories"""
        dirs = [
            "data",
            "data/emails",
            "data/cache",
            "data/tasks",
            "data/logs"
        ]
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
    
    def read_json(self, filepath: str) -> Dict[str, Any]:
        """Read JSON file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}
    
    def write_json(self, filepath: str, data: Dict[str, Any]) -> bool:
        """Write JSON file"""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Error writing to {filepath}: {e}")
            return False
    
    def append_log(self, log_entry: Dict[str, Any]) -> None:
        """Append to log file"""
        today = datetime.now().strftime("%Y-%m-%d")
        log_path = f"{self.base_dir}/logs/agent_{today}.log"
        
        try:
            # Add timestamp
            log_entry["timestamp"] = datetime.now().isoformat()
            
            # Append to file (store as newline-delimited JSON)
            with open(log_path, 'a') as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"Error writing log: {e}")
    
    def save_email(self, email_data: Dict[str, Any]) -> str:
        """Save sent email for records"""
        date = datetime.now().strftime("%Y-%m-%d")
        email_path = f"{self.base_dir}/emails/{date}.json"
        
        if self.write_json(email_path, email_data):
            return email_path
        return None
    
    def load_learning_tasks(self) -> List[Dict[str, Any]]:
        """Load learning tasks"""
        tasks_path = f"{self.base_dir}/tasks/learning_tasks.json"
        return self.read_json(tasks_path).get("tasks", [])
    
    def load_python_functions(self) -> List[Dict[str, Any]]:
        """Load Python functions"""
        functions_path = f"{self.base_dir}/tasks/python_functions.json"
        return self.read_json(functions_path).get("functions", [])
