"""
Configuration Management
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application Configuration"""
    
    # App Settings
    APP_ENV = os.getenv("APP_ENV", "development")
    APP_DEBUG = os.getenv("APP_DEBUG", "True") == "True"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Create directories if not exist
    DATA_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/hustler.db")
    
    # API Keys
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")
    STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
    GUMROAD_API_TOKEN = os.getenv("GUMROAD_API_TOKEN")
    DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # Repo Info
    GITHUB_REPO = os.getenv("GITHUB_REPO", "benclis/coding-hustler")
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required = ["ANTHROPIC_API_KEY"]
        missing = [key for key in required if not getattr(cls, key)]
        
        if missing:
            raise ValueError(f"Missing required env vars: {missing}")
        
        return True

# Create default instance
config = Config()
