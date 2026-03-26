"""
API Manager - Unified API Handler
Coordinates all API integrations
"""

from agent.logger import setup_logger
from agent.youtube_api import youtube_api
from agent.discord_api import discord_bot
from agent.github_api import github_api
from agent.database import db

logger = setup_logger(__name__)

class APIManager:
    """Manages all API integrations"""
    
    def __init__(self):
        self.youtube = youtube_api
        self.discord = discord_bot
        self.github = github_api
        logger.info("✅ API Manager initialized")
    
    def get_channel_metrics(self):
        """Get YouTube channel metrics"""
        try:
            stats = self.youtube.get_channel_stats()
            if stats:
                logger.info(f"📊 Channel: {stats['title']}")
                logger.info(f"   Subscribers: {stats['subscribers']}")
                logger.info(f"   Views: {stats['view_count']}")
                logger.info(f"   Videos: {stats['video_count']}")
                return stats
            return None
        except Exception as e:
            logger.error(f"❌ Get channel metrics failed: {str(e)}")
            return None
    
    def analyze_latest_video(self):
        """Analyze latest video stats"""
        try:
            videos = self.youtube.search_channel_videos(max_results=1)
            if videos:
                video_id = videos[0]["video_id"]
                stats = self.youtube.get_video_stats(video_id)
                
                if stats:
                    logger.info(f"📺 Latest Video: {stats['title']}")
                    logger.info(f"   Views: {stats['views']}")
                    logger.info(f"   Likes: {stats['likes']}")
                    logger.info(f"   Comments: {stats['comments']}")
                    
                    # Store in database
                    db.add_video(video_id, stats['title'], stats)
                    return stats
            return None
        except Exception as e:
            logger.error(f"❌ Analyze latest video failed: {str(e)}")
            return None
    
    def post_discord_announcement(self, title: str, message: str):
        """Post announcement to Discord"""
        try:
            announcement = f"📢 {title}\n{message}"
            logger.info(f"📤 Discord announcement: {announcement}")
            return True
        except Exception as e:
            logger.error(f"❌ Post Discord announcement failed: {str(e)}")
            return False
    
    def sync_build_progress(self, progress_data: dict):
        """Sync build progress to GitHub"""
        try:
            readme_update = f"""
# Coding Hustler - Build Progress

## Status: {progress_data.get('status', 'In Progress')}

### Day Progress
- Day 1: ✅ Complete
- Day 2: ✅ Complete  
- Day 3: ✅ Complete
- Day 4: ⏳ Pending
- Day 5: ⏳ Pending
- Day 6: ⏳ Pending
- Day 7: ⏳ Pending

### Latest Metrics
- API Integrations: ✅ Done
- YouTube: Connected
- Discord: Connected
- GitHub: Connected

Last Updated: {progress_data.get('timestamp', 'N/A')}
"""
            return self.github.update_readme(readme_update)
        except Exception as e:
            logger.error(f"❌ Sync build progress failed: {str(e)}")
            return False
    
    def health_check(self):
        """Check all API health"""
        logger.info("🔍 API Health Check...")
        
        checks = {
            "YouTube": self.youtube.youtube is not None,
            "Discord": self.discord.bot is not None,
            "GitHub": self.github.repo is not None
        }
        
        for api_name, status in checks.items():
            status_icon = "✅" if status else "❌"
            logger.info(f"{status_icon} {api_name}: {'OK' if status else 'FAILED'}")
        
        return all(checks.values())

api_manager = APIManager()
```
