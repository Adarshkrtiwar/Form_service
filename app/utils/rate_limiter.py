from datetime import datetime, timedelta
from collections import defaultdict

class RateLimiter:
    def __init__(self, requests_limit: int = 5, time_window: int = 60):
        self.requests_limit = requests_limit
        self.time_window = time_window
        self.access_records = defaultdict(list)
    
    def check_limit(self, key: str) -> bool:
        now = datetime.now()
        window_start = now - timedelta(seconds=self.time_window)
        
        # Remove old records
        self.access_records[key] = [
            t for t in self.access_records[key] if t > window_start
        ]
        
        if len(self.access_records[key]) >= self.requests_limit:
            return False
        
        self.access_records[key].append(now)
        return True