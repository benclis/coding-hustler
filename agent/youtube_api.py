"""
YouTube API Integration
"""

import os
from google.auth.oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_httplib2 import AuthorizedHttp
from googleapiclient.discovery import build
from agent.logger import setup_logger

logger = setup_logger(__name__)

class YouTubeAPI:
    """YouTube Data API v3 Handler"""
    
    def __init__(self, api_key: str = None, channel_id: str = None):
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY")
        self.channel_id = channel_id or os.getenv("YOUTUBE_CHANNEL_ID")
        self.youtube = None
        self.init_client()
    
    def init_client(self):
        """Initialize YouTube API client"""
        try:
            self.youtube = build(
                "youtube", 
                "v3", 
                developerKey=self.api_key
            )
            logger.info("✅ YouTube API initialized")
        except Exception as e:
            logger.error(f"❌ YouTube API init failed: {str(e)}")
    
    def get_channel_stats(self):
        """Get channel statistics"""
        try:
            request = self.youtube.channels().list(
                part="statistics,snippet",
                id=self.channel_id
            )
            response = request.execute()
            
            if response.get("items"):
                stats = response["items"][0]["statistics"]
                snippet = response["items"][0]["snippet"]
                
                return {
                    "title": snippet["title"],
                    "subscribers": stats.get("subscriberCount", "Hidden"),
                    "view_count": stats.get("viewCount", 0),
                    "video_count": stats.get("videoCount", 0)
                }
        except Exception as e:
            logger.error(f"❌ Get channel stats failed: {str(e)}")
            return None
    
    def get_video_stats(self, video_id: str):
        """Get video statistics"""
        try:
            request = self.youtube.videos().list(
                part="statistics,snippet,contentDetails",
                id=video_id
            )
            response = request.execute()
            
            if response.get("items"):
                stats = response["items"][0]["statistics"]
                snippet = response["items"][0]["snippet"]
                
                return {
                    "title": snippet["title"],
                    "views": int(stats.get("viewCount", 0)),
                    "likes": int(stats.get("likeCount", 0)),
                    "comments": int(stats.get("commentCount", 0)),
                    "published_at": snippet["publishedAt"]
                }
        except Exception as e:
            logger.error(f"❌ Get video stats failed: {str(e)}")
            return None
    
    def search_channel_videos(self, max_results: int = 10):
        """Search videos on channel"""
        try:
            request = self.youtube.search().list(
                part="snippet",
                channelId=self.channel_id,
                maxResults=max_results,
                order="date",
                type="video"
            )
            response = request.execute()
            
            videos = []
            for item in response.get("items", []):
                videos.append({
                    "video_id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "published_at": item["snippet"]["publishedAt"]
                })
            
            return videos
        except Exception as e:
            logger.error(f"❌ Search videos failed: {str(e)}")
            return []

youtube_api = YouTubeAPI()
```
