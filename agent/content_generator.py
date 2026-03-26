"""
Content Generator - Blog to Video Pipeline
Converts blog posts into video scripts and content
"""

from datetime import datetime
from agent.logger import setup_logger
from agent.database import db

logger = setup_logger(__name__)

class ContentGenerator:
    """Generates video scripts from blog content"""
    
    def __init__(self):
        logger.info("✅ Content Generator initialized")
    
    def blog_to_script(self, blog_title: str, blog_content: str, video_length_minutes: int = 12):
        """Convert blog post to video script"""
        try:
            logger.info(f"📝 Converting blog to script: {blog_title}")
            
            # Parse blog structure
            sections = blog_content.split("\n\n")
            
            script = {
                "title": blog_title,
                "duration_minutes": video_length_minutes,
                "sections": [],
                "hook": None,
                "cta": None,
                "timestamps": []
            }
            
            # Generate hook (first 10 seconds)
            hook = self.generate_hook(blog_title)
            script["hook"] = hook
            
            # Generate body sections
            current_time = 0.5  # After hook
            
            for i, section in enumerate(sections[:5]):  # Max 5 sections
                if section.strip():
                    section_data = {
                        "number": i + 1,
                        "content": section[:500],  # Max 500 chars per section
                        "start_time": current_time,
                        "duration": 2.0,  # 2 min per section
                        "visual": self.suggest_visual(section)
                    }
                    script["sections"].append(section_data)
                    script["timestamps"].append({
                        "time": current_time,
                        "label": f"Section {i+1}"
                    })
                    current_time += 2.0
            
            # Generate CTA (last 30 seconds)
            cta = self.generate_cta(blog_title)
            script["cta"] = cta
            script["timestamps"].append({
                "time": video_length_minutes - 0.5,
                "label": "CTA"
            })
            
            logger.info(f"✅ Script generated: {video_length_minutes} minutes")
            return script
        
        except Exception as e:
            logger.error(f"❌ Blog to script conversion failed: {str(e)}")
            return None
    
    def generate_hook(self, title: str) -> dict:
        """Generate attention-grabbing hook (first 10 seconds)"""
        try:
            hooks = [
                f"Serbest çalışmaya başlamak istiyorsun ama nereden? Bu videoda göstereceğim.",
                f"{title} hakkında bilmen gereken 1 şey var: konu için 10 dakikan var.",
                f"İlk 1000 dolar kazanmak istiyorsan, bu 3 adımı izle.",
                f"Yazılımcılar bu yöntemi kullanarak ayda 5000 dolar kazanıyor. Nasıl mı?"
            ]
            
            hook_text = hooks[hash(title) % len(hooks)]
            
            return {
                "text": hook_text,
                "duration_seconds": 10,
                "visual": "Title card + transition",
                "emotion": "curiosity"
            }
        except Exception as e:
            logger.error(f"❌ Hook generation failed: {str(e)}")
            return None
    
    def generate_cta(self, title: str) -> dict:
        """Generate call-to-action (last 30 seconds)"""
        try:
            cta_text = f"""
Eğer {title} hakkında daha derinlemesine öğrenmek istersen:

1. Discord'a katıl (link açıklamada)
2. Newsletter'a abone ol
3. First 1K programına göz at

Sonraki videoda görüşürüz!
"""
            
            return {
                "text": cta_text,
                "duration_seconds": 30,
                "links": [
                    {"text": "Discord", "url": "discord.gg/codinghustler"},
                    {"text": "Newsletter", "url": "substack.com/codinghustler"},
                    {"text": "First 1K", "url": "codinghustler.com/first1k"}
                ],
                "visual": "End screen + subscribe button"
            }
        except Exception as e:
            logger.error(f"❌ CTA generation failed: {str(e)}")
            return None
    
    def suggest_visual(self, section_content: str) -> dict:
        """Suggest B-roll and visual elements for section"""
        try:
            keywords = ["serbest", "para", "code", "laptop", "developer"]
            
            visuals = []
            
            if any(kw in section_content.lower() for kw in keywords[:3]):
                visuals.append("Screen recording of code/dashboard")
            if "masaüstü" in section_content.lower() or "workspace" in section_content.lower():
                visuals.append("Desk setup B-roll")
            if any(kw in section_content.lower() for kw in ["grafik", "chart", "data"]):
                visuals.append("Chart/graph animation")
            
            return {
                "primary": visuals[0] if visuals else "Generic B-roll",
                "secondary": visuals[1] if len(visuals) > 1 else "Transition effect",
                "music": "Background royalty-free music",
                "text_overlay": "Key points highlighted"
            }
        except Exception as e:
            logger.error(f"❌ Visual suggestion failed: {str(e)}")
            return None
    
    def add_seo_metadata(self, script: dict, keywords: list = None) -> dict:
        """Add SEO metadata for YouTube"""
        try:
            if not keywords:
                keywords = ["serbest çalışma", "para kazanma", "freelance"]
            
            script["seo"] = {
                "title": script.get("title", ""),
                "description": f"Bu videoda {script.get('title', '')} hakkında tam rehber. {', '.join(keywords[:3])}",
                "tags": keywords + ["Coding Hustler", "yazılımcı", "para"],
                "category": "Education",
                "language": "Turkish",
                "keywords": keywords
            }
            
            logger.info(f"✅ SEO metadata added")
            return script
        except Exception as e:
            logger.error(f"❌ SEO metadata failed: {str(e)}")
            return None
    
    def save_script(self, script: dict, filename: str = None):
        """Save script to file"""
        try:
            if not filename:
                filename = f"scripts/{script['title'].replace(' ', '_')}.json"
            
            import json
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(script, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ Script saved: {filename}")
            return filename
        except Exception as e:
            logger.error(f"❌ Save script failed: {str(e)}")
            return None

content_generator = ContentGenerator()
```
