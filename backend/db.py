import psycopg2
import os
from typing import List, Dict

class Database:
    def __init__(self):
        # Get database URL from environment variable (Render.com sets this automatically)
        self.database_url = os.getenv('DATABASE_URL')
        
        if not self.database_url:
            # Fallback for local development
            self.database_url = "postgresql://localhost/jokes_db"
        
        # Render.com uses postgres:// but psycopg2 needs postgresql://
        if self.database_url.startswith('postgres://'):
            self.database_url = self.database_url.replace('postgres://', 'postgresql://', 1)
    
    def get_connection(self):
        return psycopg2.connect(self.database_url)
    
    def init_db(self):
        """Initialize database with schema and sample data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Create jokes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jokes (
                    id SERIAL PRIMARY KEY,
                    setup TEXT NOT NULL,
                    punchline TEXT NOT NULL
                )
            """)
            
            # Check if we already have jokes
            cursor.execute("SELECT COUNT(*) FROM jokes")
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Insert sample jokes
                jokes = [
                    ("Why don't scientists trust atoms?", "Because they make up everything!"),
                    ("What do you call a fake noodle?", "An impasta!"),
                    ("Why did the scarecrow win an award?", "Because he was outstanding in his field!"),
                    ("What do you call a bear with no teeth?", "A gummy bear!")
                ]
                
                for setup, punchline in jokes:
                    cursor.execute(
                        "INSERT INTO jokes (setup, punchline) VALUES (%s, %s)",
                        (setup, punchline)
                    )
                
                print("✅ Database initialized with sample jokes")
            else:
                print(f"✅ Database already contains {count} jokes")
            
            conn.commit()
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
    
    def get_all_jokes(self) -> List[Dict]:
        """Fetch all jokes from database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT id, setup, punchline FROM jokes ORDER BY id")
            jokes = []
            for row in cursor.fetchall():
                jokes.append({
                    'id': row[0],
                    'setup': row[1],
                    'punchline': row[2]
                })
            return jokes
        finally:
            cursor.close()
            conn.close()
