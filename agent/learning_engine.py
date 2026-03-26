"""
Database Management (SQLite)
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from agent.config import Config
from agent.logger import setup_logger

logger = setup_logger(__name__)

class Database:
    """SQLite Database Handler"""
    
    def __init__(self):
        self.db_path = Config.DATA_DIR / "hustler.db"
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize database schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Videos table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                youtube_id TEXT UNIQUE,
                title TEXT,
                published_at TIMESTAMP,
                metrics TEXT,
                learning_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Learning database
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_name TEXT UNIQUE,
                success_rate REAL DEFAULT 0.0,
                sample_size INTEGER DEFAULT 0,
                notes TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Errors log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_type TEXT,
                description TEXT,
                resolved BOOLEAN DEFAULT 0,
                fix_applied TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Agent tasks
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT,
                status TEXT DEFAULT 'pending',
                result TEXT,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info("Database initialized")
    
    def add_video(self, youtube_id, title, metrics):
        """Add video record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO videos (youtube_id, title, metrics)
            VALUES (?, ?, ?)
        """, (youtube_id, title, json.dumps(metrics)))
        
        conn.commit()
        conn.close()
        logger.info(f"Video added: {title}")
    
    def add_error(self, error_type, description):
        """Log error"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO errors (error_type, description)
            VALUES (?, ?)
        """, (error_type, description))
        
        conn.commit()
        conn.close()
        logger.warning(f"Error logged: {error_type} - {description}")
    
    def update_learning_pattern(self, pattern_name, success_rate, sample_size):
        """Update learning database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO learning_patterns 
            (pattern_name, success_rate, sample_size, updated_at)
            VALUES (?, ?, ?, ?)
        """, (pattern_name, success_rate, sample_size, datetime.now()))
        
        conn.commit()
        conn.close()
        logger.info(f"Pattern updated: {pattern_name} ({success_rate:.1f}%)")

# Create global instance
db = Database()
```
