"""
B-Roll Manager
Stock footage, images, transitions
"""

import os
import requests
from typing import List
from agent.logger import setup_logger

logger = setup_logger(__name__)

class BRollManager:
    """Manages B-roll and stock footage"""
    
    def __init__(self):
        self.output_dir = "videos/broll"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # API Keys for free stock footage
        self.pixabay_key = os.getenv("PIXABAY_API_KEY", "demo")
        self.pexels_key = os.getenv("PEXELS_API_KEY", "demo")
        
        logger.info("✅ B-Roll Manager initialized")
    
    def search_pixabay_videos(self, query: str, count: int = 5) -> List[dict]:
        """Search Pixabay for free stock videos"""
        try:
            logger.info(f"🎬 Searching Pixabay: {query}")
            
            url = "https://pixabay.com/api/videos/"
            params = {
                "key": self.pixabay_key,
                "q": query,
                "per_page": count,
                "order": "popular"
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            videos = []
            if data.get("hits"):
                for video in data["hits"][:count]:
                    videos.append({
                        "id": video["id"],
                        "title": video["tags"],
                        "url": video["videos"]["large"]["url"],
                        "duration": video["duration"],
                        "source": "pixabay"
                    })
            
            logger.info(f"✅ Found {len(videos)} videos on Pixabay")
            return videos
        
        except Exception as e:
            logger.error(f"❌ Pixabay search failed: {str(e)}")
            return self.get_mock_broll(query)
    
    def search_pexels_videos(self, query: str, count: int = 5) -> List[dict]:
        """Search Pexels for free stock videos"""
        try:
            logger.info(f"🎬 Searching Pexels: {query}")
            
            url = "https://api.pexels.com/videos/search"
            headers = {"Authorization": self.pexels_key}
            params = {
                "query": query,
                "per_page": count
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            data = response.json()
            
            videos = []
            if data.get("videos"):
                for video in data["videos"][:count]:
                    videos.append({
                        "id": video["id"],
                        "title": query,
                        "url": video["video_files"][0]["link"],
                        "duration": video["duration"],
                        "source": "pexels"
                    })
            
            logger.info(f"✅ Found {len(videos)} videos on Pexels")
            return videos
        
        except Exception as e:
            logger.error(f"❌ Pexels search failed: {str(e)}")
            return self.get_mock_broll(query)
    
    def download_video(self, url: str, filename: str) -> str:
        """Download video from URL"""
        try:
            logger.info(f"📥 Downloading: {filename}")
            
            filepath = f"{self.output_dir}/{filename}"
            
            response = requests.get(url, stream=True, timeout=30)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            logger.info(f"✅ Downloaded: {filepath}")
            return filepath
        
        except Exception as e:
            logger.error(f"❌ Download failed: {str(e)}")
            return None
    
    def search_unsplash_images(self, query: str, count: int = 10) -> List[dict]:
        """Search Unsplash for free stock images"""
        try:
            logger.info(f"🖼️ Searching Unsplash: {query}")
            
            url = "https://api.unsplash.com/search/photos"
            params = {
                "query": query,
                "per_page": count,
                "order_by": "relevant"
            }
            
            # Using demo client ID (replace with your own)
            headers = {"Authorization": "Client-ID demo"}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            data = response.json()
            
            images = []
            if data.get("results"):
                for img in data["results"][:count]:
                    images.append({
                        "id": img["id"],
                        "title": img["description"] or query,
                        "url": img["urls"]["regular"],
                        "source": "unsplash"
                    })
            
            logger.info(f"✅ Found {len(images)} images on Unsplash")
            return images
        
        except Exception as e:
            logger.error(f"❌ Unsplash search failed: {str(e)}")
            return self.get_mock_images(query)
    
    def get_mock_broll(self, query: str) -> List[dict]:
        """Return mock B-roll for testing (no API key needed)"""
        logger.warning(f"⚠️ Using mock B-roll for: {query}")
        
        mock_videos = {
            "serbest": [
                {"id": 1, "title": "Laptop workspace", "url": "mock://video1.mp4", "duration": 10, "source": "mock"},
                {"id": 2, "title": "Typing", "url": "mock://video2.mp4", "duration": 5, "source": "mock"}
            ],
            "para": [
                {"id": 3, "title": "Money", "url": "mock://video3.mp4", "duration": 8, "source": "mock"},
                {"id": 4, "title": "Success", "url": "mock://video4.mp4", "duration": 6, "source": "mock"}
            ],
            "default": [
                {"id": 5, "title": "Office", "url": "mock://video5.mp4", "duration": 10, "source": "mock"},
                {"id": 6, "title": "Tech", "url": "mock://video6.mp4", "duration": 8, "source": "mock"}
            ]
        }
        
        return mock_videos.get(query, mock_videos["default"])
    
    def get_mock_images(self, query: str) -> List[dict]:
        """Return mock images for testing"""
        logger.warning(f"⚠️ Using mock images for: {query}")
        
        mock_images = {
            "serbest": [
                {"id": 1, "title": "Freelancer", "url": "mock://image1.jpg", "source": "mock"},
                {"id": 2, "title": "Working", "url": "mock://image2.jpg", "source": "mock"}
            ],
            "default": [
                {"id": 3, "title": "Business", "url": "mock://image3.jpg", "source": "mock"},
                {"id": 4, "title": "Success", "url": "mock://image4.jpg", "source": "mock"}
            ]
        }
        
        return mock_images.get(query, mock_images["default"])
    
    def get_transition_effects(self) -> List[str]:
        """Get available FFmpeg transition effects"""
        return [
            "fade",           # Fade to black
            "wiperight",      # Wipe right
            "wipeleft",       # Wipe left
            "slideright",     # Slide right
            "slideleft",      # Slide left
            "slideup",        # Slide up
            "slidedown",      # Slide down
            "circleopen",     # Circle open
            "circleclose",    # Circle close
            "dissolve"        # Cross dissolve
        ]
    
    def apply_transition(self, video1: str, video2: str, transition: str = "fade", duration: float = 1.0) -> str:
        """Apply transition between two videos"""
        try:
            import subprocess
            
            logger.info(f"✨ Applying {transition} transition")
            
            output_file = f"{self.output_dir}/transition_{transition}.mp4"
            
            # FFmpeg transition filter
            filter_complex = f"xfade=transition={transition}:duration={duration}"
            
            cmd = [
                "ffmpeg",
                "-i", video1,
                "-i", video2,
                "-filter_complex", filter_complex,
                "-c:a", "aac",
                "-y",
                output_file
            ]
            
            subprocess.run(cmd, capture_output=True)
            
            logger.info(f"✅ Transition applied: {output_file}")
            return output_file
        
        except Exception as e:
            logger.error(f"❌ Transition failed: {str(e)}")
            return None
    
    def create_slideshow(self, images: List[str], duration_per_image: float = 3.0, 
                        transition: str = "fade") -> str:
        """Create slideshow from images"""
        try:
            import subprocess
            
            logger.info("🖼️ Creating slideshow...")
            
            # Create concat demuxer file
            concat_file = f"{self.output_dir}/concat_images.txt"
            
            with open(concat_file, 'w') as f:
                for img in images:
                    f.write(f"file '{img}'\n")
                    f.write(f"duration {duration_per_image}\n")
            
            output_file = f"{self.output_dir}/slideshow.mp4"
            
            cmd = [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", concat_file,
                "-vf", f"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-y",
                output_file
            ]
            
            subprocess.run(cmd, capture_output=True)
            
            logger.info(f"✅ Slideshow created: {output_file}")
            return output_file
        
        except Exception as e:
            logger.error(f"❌ Slideshow creation failed: {str(e)}")
            return None
    
    def get_royalty_free_music(self, mood: str = "energetic") -> dict:
        """Get royalty-free music metadata"""
        
        music_library = {
            "energetic": {
                "name": "Upbeat Energy",
                "url": "https://www.bensound.com/bensound-music/bensound-ukulele.mp3",
                "artist": "Bensound",
                "license": "CC-BY-3.0"
            },
            "calm": {
                "name": "Calm Music",
                "url": "https://www.bensound.com/bensound-music/bensound-sunny.mp3",
                "artist": "Bensound",
                "license": "CC-BY-3.0"
            },
            "cinematic": {
                "name": "Cinematic",
                "url": "https://www.bensound.com/bensound-music/bensound-epic.mp3",
                "artist": "Bensound",
                "license": "CC-BY-3.0"
            },
            "corporate": {
                "name": "Corporate",
                "url": "https://www.bensound.com/bensound-music/bensound-actioncinematic.mp3",
                "artist": "Bensound",
                "license": "CC-BY-3.0"
            }
        }
        
        return music_library.get(mood, music_library["energetic"])

broll_manager = BRollManager()
