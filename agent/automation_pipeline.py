"""
Automation Pipeline - Full Content to Upload Workflow
Orchestrates: Newsletter → Blog → Script → Thumbnail → Upload
"""

from datetime import datetime
from agent.logger import setup_logger
from agent.content_generator import content_generator
from agent.thumbnail_generator import thumbnail_generator
from agent.youtube_uploader import youtube_uploader
from agent.database import db
from agent.api_manager import api_manager

logger = setup_logger(__name__)

class AutomationPipeline:
    """Full automation pipeline from content to YouTube upload"""
    
    def __init__(self):
        self.pipeline_id = None
        self.status = "IDLE"
        self.current_stage = None
        logger.info("✅ Automation Pipeline initialized")
    
    def start_pipeline(self, newsletter_content: str, topic: str):
        """Start the full automation pipeline"""
        try:
            logger.info("🚀 STARTING AUTOMATION PIPELINE")
            logger.info("=" * 50)
            
            self.pipeline_id = f"PIPELINE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.status = "RUNNING"
            
            pipeline_log = {
                "pipeline_id": self.pipeline_id,
                "topic": topic,
                "started_at": datetime.now().isoformat(),
                "stages": []
            }
            
            # STAGE 1: Newsletter to Blog
            logger.info("\n📝 STAGE 1: Newsletter → Blog Conversion")
            blog_result = self.stage_newsletter_to_blog(newsletter_content, topic)
            pipeline_log["stages"].append(blog_result)
            
            if not blog_result["success"]:
                return self.pipeline_failed(pipeline_log, "Newsletter conversion failed")
            
            # STAGE 2: Blog to Script
            logger.info("\n🎬 STAGE 2: Blog → Video Script")
            script_result = self.stage_blog_to_script(
                blog_result["blog_title"],
                blog_result["blog_content"],
                topic
            )
            pipeline_log["stages"].append(script_result)
            
            if not script_result["success"]:
                return self.pipeline_failed(pipeline_log, "Script generation failed")
            
            # STAGE 3: Script to Thumbnail
            logger.info("\n🖼️ STAGE 3: Script → Thumbnail Design")
            thumbnail_result = self.stage_script_to_thumbnail(
                script_result["script"]
            )
            pipeline_log["stages"].append(thumbnail_result)
            
            if not thumbnail_result["success"]:
                return self.pipeline_failed(pipeline_log, "Thumbnail generation failed")
            
            # STAGE 4: Prepare Upload
            logger.info("\n📤 STAGE 4: Prepare for YouTube Upload")
            upload_result = self.stage_prepare_upload(
                script_result["script"],
                thumbnail_result["thumbnail"]
            )
            pipeline_log["stages"].append(upload_result)
            
            if not upload_result["success"]:
                return self.pipeline_failed(pipeline_log, "Upload preparation failed")
            
            # STAGE 5: SEO Optimization
            logger.info("\n🔍 STAGE 5: SEO Optimization")
            seo_result = self.stage_seo_optimization(script_result["script"])
            pipeline_log["stages"].append(seo_result)
            
            # STAGE 6: Schedule & Monitor
            logger.info("\n📅 STAGE 6: Schedule & Monitoring Setup")
            scheduling_result = self.stage_schedule_monitoring(
                upload_result["upload_package"]
            )
            pipeline_log["stages"].append(scheduling_result)
            
            # COMPLETION
            logger.info("\n" + "=" * 50)
            logger.info("✅ AUTOMATION PIPELINE COMPLETE")
            logger.info("=" * 50)
            
            self.status = "COMPLETED"
            pipeline_log["completed_at"] = datetime.now().isoformat()
            pipeline_log["status"] = "SUCCESS"
            
            self.save_pipeline_log(pipeline_log)
            
            return {
                "status": "SUCCESS",
                "pipeline_id": self.pipeline_id,
                "pipeline_log": pipeline_log,
                "ready_for_upload": True,
                "next_action": "Upload video file to YouTube"
            }
        
        except Exception as e:
            logger.error(f"❌ Pipeline failed: {str(e)}")
            return self.pipeline_failed(pipeline_log, str(e))
    
    def stage_newsletter_to_blog(self, newsletter_content: str, topic: str):
        """Stage 1: Convert newsletter to blog post"""
        try:
            logger.info("  Converting newsletter to blog format...")
            
            blog_title = f"Serbest Çalışma Rehberi: {topic}"
            blog_content = f"""
# {blog_title}

## Giriş
{newsletter_content[:200]}...

## Ana Bölümler
1. Başlangıç adımları
2. İlk projeyi bulma
3. Fiyatlandırma stratejisi
4. Müşteri bulma yöntemleri
5. Başarı hikayeleri

## Sonuç
{newsletter_content[-200:]}...
"""
            
            logger.info(f"  ✅ Blog created: {blog_title}")
            
            return {
                "stage": "newsletter_to_blog",
                "success": True,
                "blog_title": blog_title,
                "blog_content": blog_content,
                "word_count": len(blog_content.split()),
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"  ❌ Failed: {str(e)}")
            return {"stage": "newsletter_to_blog", "success": False, "error": str(e)}
    
    def stage_blog_to_script(self, blog_title: str, blog_content: str, topic: str):
        """Stage 2: Convert blog to video script"""
        try:
            logger.info("  Generating video script...")
            
            script = content_generator.blog_to_script(
                blog_title,
                blog_content,
                video_length_minutes=12
            )
            
            if not script:
                return {"stage": "blog_to_script", "success": False, "error": "Script generation failed"}
            
            # Add SEO
            script = content_generator.add_seo_metadata(
                script,
                keywords=["serbest çalışma", topic, "para kazanma", "freelance"]
            )
            
            logger.info(f"  ✅ Script generated: {len(script.get('sections', []))} sections")
            
            return {
                "stage": "blog_to_script",
                "success": True,
                "script": script,
                "sections": len(script.get("sections", [])),
                "duration": script.get("duration_minutes"),
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"  ❌ Failed: {str(e)}")
            return {"stage": "blog_to_script", "success": False, "error": str(e)}
    
    def stage_script_to_thumbnail(self, script: dict):
        """Stage 3: Generate thumbnail from script"""
        try:
            logger.info("  Generating thumbnail design...")
            
            thumbnail = thumbnail_generator.generate_thumbnail_design(
                script.get("title", ""),
                script.get("hook", {}).get("text", "")
            )
            
            if not thumbnail:
                return {"stage": "script_to_thumbnail", "success": False}
            
            logger.info(f"  ✅ Thumbnail designed: Estimated CTR {thumbnail.get('estimated_ctr', {}).get('estimated_ctr_percent', 4)}%")
            
            return {
                "stage": "script_to_thumbnail",
                "success": True,
                "thumbnail": thumbnail,
                "ctr_estimate": thumbnail.get("estimated_ctr", {}).get("estimated_ctr_percent"),
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"  ❌ Failed: {str(e)}")
            return {"stage": "script_to_thumbnail", "success": False, "error": str(e)}
    
    def stage_prepare_upload(self, script: dict, thumbnail: dict):
        """Stage 4: Prepare for YouTube upload"""
        try:
            logger.info("  Preparing upload package...")
            
            upload_package = youtube_uploader.prepare_upload(
                video_file="./video.mp4",  # Placeholder
                script=script,
                thumbnail=thumbnail
            )
            
            if not upload_package:
                return {"stage": "prepare_upload", "success": False}
            
            logger.info(f"  ✅ Upload ready: {upload_package.get('status')}")
            
            return {
                "stage": "prepare_upload",
                "success": True,
                "upload_package": upload_package,
                "publish_time": upload_package.get("scheduling", {}).get("publish_time"),
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"  ❌ Failed: {str(e)}")
            return {"stage": "prepare_upload", "success": False, "error": str(e)}
    
    def stage_seo_optimization(self, script: dict):
        """Stage 5: SEO optimization"""
        try:
            logger.info("  Optimizing SEO...")
            
            seo_data = script.get("seo", {})
            
            optimization = {
                "title": seo_data.get("title"),
                "keywords": seo_data.get("keywords", []),
                "tags": seo_data.get("tags", []),
                "description_length": len(seo_data.get("description", "")),
                "optimization_score": self.calculate_seo_score(seo_data)
            }
            
            logger.info(f"  ✅ SEO Score: {optimization['optimization_score']}/100")
            
            return {
                "stage": "seo_optimization",
                "success": True,
                "optimization": optimization,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"  ❌ Failed: {str(e)}")
            return {"stage": "seo_optimization", "success": False, "error": str(e)}
    
    def stage_schedule_monitoring(self, upload_package: dict):
        """Stage 6: Schedule and setup monitoring"""
        try:
            logger.info("  Setting up monitoring...")
            
            scheduling = {
                "publish_time": upload_package.get("scheduling", {}).get("publish_time"),
                "monitoring_enabled": True,
                "alerts_enabled": True,
                "metrics_to_track": [
                    "views", "ctr", "watch_time", "engagement", "affiliate_clicks"
                ],
                "check_interval": "hourly"
            }
            
            logger.info(f"  ✅ Monitoring configured: {scheduling['check_interval']} checks")
            
            return {
                "stage": "schedule_monitoring",
                "success": True,
                "scheduling": scheduling,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"  ❌ Failed: {str(e)}")
            return {"stage": "schedule_monitoring", "success": False, "error": str(e)}
    
    def calculate_seo_score(self, seo_data: dict) -> int:
        """Calculate SEO optimization score"""
        try:
            score = 0
            
            # Title (max 20 points)
            if seo_data.get("title") and len(seo_data.get("title", "")) > 30:
                score += 20
            
            # Description (max 20 points)
            if seo_data.get("description") and len(seo_data.get("description", "")) > 100:
                score += 20
            
            # Keywords (max 20 points)
            if seo_data.get("keywords") and len(seo_data.get("keywords", [])) >= 3:
                score += 20
            
            # Tags (max 20 points)
            if seo_data.get("tags") and len(seo_data.get("tags", [])) >= 5:
                score += 20
            
            # Language (max 10 points)
            if seo_data.get("language"):
                score += 10
            
            # Category (max 10 points)
            if seo_data.get("category"):
                score += 10
            
            return min(score, 100)
        except:
            return 0
    
    def pipeline_failed(self, pipeline_log: dict, error: str):
        """Handle pipeline failure"""
        try:
            logger.error(f"❌ PIPELINE FAILED: {error}")
            
            self.status = "FAILED"
            pipeline_log["status"] = "FAILED"
            pipeline_log["error"] = error
            pipeline_log["failed_at"] = datetime.now().isoformat()
            
            self.save_pipeline_log(pipeline_log)
            db.add_error("automation_pipeline", error)
            
            return {
                "status": "FAILED",
                "error": error,
                "pipeline_log": pipeline_log
            }
        except Exception as e:
            logger.error(f"❌ Error handling failure: {str(e)}")
            return {"status": "FAILED", "error": str(e)}
    
    def save_pipeline_log(self, pipeline_log: dict):
        """Save pipeline log to file"""
        try:
            import json
            
            log_file = f"logs/pipeline_{pipeline_log['pipeline_id']}.json"
            
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(pipeline_log, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ Pipeline log saved: {log_file}")
        except Exception as e:
            logger.error(f"❌ Save log failed: {str(e)}")

automation_pipeline = AutomationPipeline()
```
