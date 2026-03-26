"""
Thumbnail Generator - AI-powered YouTube thumbnails
Generates optimized thumbnails for maximum CTR
"""

from datetime import datetime
from agent.logger import setup_logger

logger = setup_logger(__name__)

class ThumbnailGenerator:
    """Generates YouTube thumbnails with AI optimization"""
    
    def __init__(self):
        logger.info("✅ Thumbnail Generator initialized")
    
    def generate_thumbnail_design(self, video_title: str, hook_text: str = None, analytics_data: dict = None):
        """Generate optimized thumbnail design specification"""
        try:
            logger.info(f"🖼️ Generating thumbnail for: {video_title}")
            
            # Analyze title for key elements
            keywords = self.extract_keywords(video_title)
            emotion = self.detect_emotion(video_title)
            
            thumbnail = {
                "title": video_title,
                "created_at": datetime.now().isoformat(),
                "specifications": {
                    "dimensions": "1280x720px",
                    "format": "PNG/JPG",
                    "file_size_max": "2MB"
                },
                "design_elements": {
                    "background": self.generate_background(emotion),
                    "main_text": self.generate_text(video_title),
                    "visuals": self.generate_visuals(keywords),
                    "accent_colors": self.generate_colors(emotion),
                    "branding": self.generate_branding()
                },
                "ctr_optimization": {
                    "contrast_level": "HIGH",
                    "text_readability": "MOBILE_OPTIMIZED",
                    "emotion_trigger": emotion,
                    "pattern": self.get_successful_pattern(analytics_data)
                },
                "canva_instructions": self.generate_canva_instructions(video_title, keywords),
                "estimated_ctr": self.estimate_ctr(keywords, emotion)
            }
            
            logger.info(f"✅ Thumbnail design generated")
            return thumbnail
        
        except Exception as e:
            logger.error(f"❌ Thumbnail generation failed: {str(e)}")
            return None
    
    def extract_keywords(self, title: str) -> list:
        """Extract key words from video title"""
        try:
            # Remove common words
            stop_words = ["nasıl", "ne", "kaç", "hangi", "kim", "neden"]
            words = title.lower().split()
            keywords = [w for w in words if w not in stop_words and len(w) > 3]
            return keywords[:3]  # Top 3 keywords
        except:
            return ["Title"]
    
    def detect_emotion(self, title: str) -> str:
        """Detect dominant emotion to convey"""
        try:
            emotions = {
                "exciting": ["nasıl", "yöntemi", "sırrı", "hile"],
                "urgent": ["acil", "son", "sınırlı", "bitmiş"],
                "curious": ["şaşıracaksın", "biliyor musun", "hiç"],
                "educational": ["rehber", "dersi", "öğren", "başla"]
            }
            
            title_lower = title.lower()
            
            for emotion, keywords in emotions.items():
                if any(kw in title_lower for kw in keywords):
                    return emotion
            
            return "educational"
        except:
            return "neutral"
    
    def generate_background(self, emotion: str) -> dict:
        """Generate background design"""
        try:
            backgrounds = {
                "exciting": {
                    "color_primary": "#FF6B6B",  # Red
                    "color_secondary": "#FFD93D",  # Yellow
                    "pattern": "Bold gradient with movement",
                    "style": "High energy, dynamic"
                },
                "urgent": {
                    "color_primary": "#FF3333",  # Bright red
                    "color_secondary": "#000000",  # Black
                    "pattern": "Diagonal stripes or shapes",
                    "style": "Alert-like, attention-grabbing"
                },
                "curious": {
                    "color_primary": "#6C63FF",  # Purple
                    "color_secondary": "#00D9FF",  # Cyan
                    "pattern": "Question marks or mystery elements",
                    "style": "Intriguing, mysterious"
                },
                "educational": {
                    "color_primary": "#1E90FF",  # Blue
                    "color_secondary": "#32CD32",  # Green
                    "pattern": "Clean, professional gradient",
                    "style": "Clear, organized, trustworthy"
                }
            }
            
            return backgrounds.get(emotion, backgrounds["educational"])
        except:
            return {"color_primary": "#1E90FF", "color_secondary": "#32CD32"}
    
    def generate_text(self, title: str) -> dict:
        """Generate text specifications"""
        try:
            # Shorten title for thumbnail readability
            words = title.split()
            if len(words) > 5:
                display_text = " ".join(words[:3])
                emoji = self.get_emoji_for_title(title)
            else:
                display_text = title
                emoji = self.get_emoji_for_title(title)
            
            return {
                "main_text": display_text.upper(),
                "emoji": emoji,
                "font": "Bold sans-serif (Arial, Montserrat Bold)",
                "font_size": "PRIMARY_TEXT: 80-100px, SECONDARY: 40-50px",
                "color": "#FFFFFF",
                "stroke": "2px black outline for readability",
                "placement": "Top-center and bottom-center",
                "shadow": "Drop shadow for depth"
            }
        except Exception as e:
            logger.error(f"❌ Text generation failed: {str(e)}")
            return {}
    
    def get_emoji_for_title(self, title: str) -> str:
        """Get relevant emoji for title"""
        try:
            emojis = {
                "para": "💰",
                "serbest": "🚀",
                "code": "💻",
                "yazılımcı": "👨‍💻",
                "nasıl": "❓",
                "rehber": "📚",
                "eğitim": "🎓",
                "başla": "⚡",
                "hile": "🔥",
                "yöntemi": "📋"
            }
            
            title_lower = title.lower()
            for word, emoji in emojis.items():
                if word in title_lower:
                    return emoji
            
            return "✨"
        except:
            return "✨"
    
    def generate_visuals(self, keywords: list) -> dict:
        """Generate visual elements"""
        try:
            visuals = {
                "primary_image": f"Icon/graphic representing: {keywords[0] if keywords else 'topic'}",
                "secondary_elements": [
                    "Arrow or pointer (showing growth/direction)",
                    "Number or statistics (if applicable)",
                    "Face or character (optional)"
                ],
                "effects": [
                    "Bold outlines around key elements",
                    "Highlight/glow on main visual",
                    "Motion blur lines (optional)"
                ]
            }
            return visuals
        except:
            return {}
    
    def generate_colors(self, emotion: str) -> list:
        """Generate optimized color palette"""
        try:
            palettes = {
                "exciting": ["#FF6B6B", "#FFD93D", "#FFFFFF", "#000000"],
                "urgent": ["#FF3333", "#000000", "#FFFFFF", "#FFD700"],
                "curious": ["#6C63FF", "#00D9FF", "#FFFFFF", "#000000"],
                "educational": ["#1E90FF", "#32CD32", "#FFFFFF", "#000000"]
            }
            
            return palettes.get(emotion, palettes["educational"])
        except:
            return ["#1E90FF", "#32CD32", "#FFFFFF", "#000000"]
    
    def generate_branding(self) -> dict:
        """Generate branding elements"""
        try:
            return {
                "channel_logo": {
                    "position": "Top-left corner",
                    "size": "80x80px",
                    "opacity": 0.9,
                    "design": "CH logo (white with outline)"
                },
                "watermark": {
                    "text": "Coding Hustler",
                    "position": "Bottom-right",
                    "size": "Small, subtle",
                    "opacity": 0.6,
                    "font": "Syne, bold"
                },
                "consistency": "Same style across all thumbnails for brand recognition"
            }
        except:
            return {}
    
    def generate_canva_instructions(self, title: str, keywords: list) -> str:
        """Generate step-by-step Canva instructions"""
        try:
            instructions = f"""
CANVA THUMBNAIL CREATION - {title}

STEP 1: Setup
- New design → YouTube Thumbnail (1280x720)
- Background: Use gradient (see colors above)

STEP 2: Main Text
- Add text: "{title.upper()}"
- Font: Montserrat Bold, 80-100px
- Color: White with 2px black stroke
- Position: Top/Center

STEP 3: Visuals
- Add emoji: {self.get_emoji_for_title(title)}
- Size: 150-200px
- Position: Center or corner

STEP 4: Branding
- Add "Coding Hustler" logo (top-left, 80x80)
- Add watermark "CH" (bottom-right, subtle)

STEP 5: Final touches
- Check mobile preview (small screens)
- High contrast test
- Ensure text is readable
- Download as PNG (2MB max)

CANVA TEMPLATE: (To be created)
- Save as brand template
- Reuse for consistency
"""
            return instructions
        except:
            return ""
    
    def estimate_ctr(self, keywords: list, emotion: str) -> dict:
        """Estimate expected CTR based on design"""
        try:
            base_ctr = 4.0  # 4% baseline
            
            # Adjust based on emotion
            emotion_boost = {
                "exciting": 1.5,
                "urgent": 1.8,
                "curious": 1.6,
                "educational": 1.2
            }
            
            estimated = base_ctr * emotion_boost.get(emotion, 1.0)
            
            return {
                "estimated_ctr_percent": estimated,
                "reasoning": f"{emotion.upper()} emotion + {len(keywords)} strong keywords",
                "target_ctr": "5%+ (top 10% performer)",
                "confidence": "MEDIUM (before real testing)"
            }
        except:
            return {"estimated_ctr_percent": 4.0}
    
    def get_successful_pattern(self, analytics_data: dict = None) -> str:
        """Get pattern from successful videos"""
        try:
            if analytics_data and analytics_data.get("ctr", 0) > 5:
                return "Bold text + emoji + high contrast (PROVEN)"
            
            return "Bold text + bright colors + emoji (STANDARD)"
        except:
            return "Standard high-contrast design"

thumbnail_generator = ThumbnailGenerator()
```
