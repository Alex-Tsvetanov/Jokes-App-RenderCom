# Hardcoded jokes - no database needed!
from typing import List, Dict

class Database:
    def __init__(self):
        # Hardcoded jokes instead of database
        self.jokes = [
            {
                'id': 1,
                'setup': "Why don't scientists trust atoms?",
                'punchline': "Because they make up everything!"
            },
            {
                'id': 2,
                'setup': "What do you call a fake noodle?",
                'punchline': "An impasta!"
            },
            {
                'id': 3,
                'setup': "Why did the scarecrow win an award?",
                'punchline': "Because he was outstanding in his field!"
            },
            {
                'id': 4,
                'setup': "What do you call a bear with no teeth?",
                'punchline': "A gummy bear!"
            }
        ]
    
    def init_db(self):
        """No-op - no database to initialize"""
        print(f"✅ Using {len(self.jokes)} hardcoded jokes (no database needed)")
    
    def get_all_jokes(self) -> List[Dict]:
        """Return hardcoded jokes"""
        return self.jokes
