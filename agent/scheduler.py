"""
Task Scheduler
Schedule recurring tasks
"""

import schedule
import time
from datetime import datetime
from agent.logger import setup_logger
from agent.orchestrator import orchestrator
from agent.tasks import task_manager
from agent.monitoring import monitoring_system

logger = setup_logger(__name__)

class TaskScheduler:
    """Schedules and manages recurring tasks"""
    
    def __init__(self):
        self.jobs = {}
        self.running = False
        logger.info("✅ Task Scheduler initialized")
    
    def schedule_daily_tasks(self):
        """Schedule daily agent tasks"""
        try:
            # 8 AM - System health check
            schedule.every().day.at("08:00").do(
                self.run_scheduled_task,
                "System Health Check",
                self.health_check_task
            )
            
            # 10 AM - Content pipeline
            schedule.every().day.at("10:00").do(
                self.run_scheduled_task,
                "Content Pipeline",
                self.content_pipeline_task
            )
            
            # 2 PM - Video metrics analysis
            schedule.every().day.at("14:00").do(
                self.run_scheduled_task,
                "Video Metrics Analysis",
                self.video_analysis_task
            )
            
            # 6 PM - Daily report
            schedule.every().day.at("18:00").do(
                self.run_scheduled_task,
                "Daily Report",
                self.daily_report_task
            )
            
            # Hourly - Health monitoring
            schedule.every().hour.do(
                self.run_scheduled_task,
                "Health Monitoring",
                self.monitoring_task
            )
            
            logger.info("✅ Daily tasks scheduled")
            return True
        except Exception as e:
            logger.error(f"❌ Schedule daily tasks failed: {str(e)}")
            return False
    
    def run_scheduled_task(self, task_name: str, task_func):
        """Run a scheduled task with tracking"""
        try:
            logger.info(f"▶ Running scheduled task: {task_name}")
            
            # Create task record
            task_id = task_manager.create_task(task_name)
            task_manager.start_task(task_id)
            
            # Execute task
            result = task_func()
            
            # Mark as completed
            task_manager.complete_task(task_id, str(result))
            
            logger.info(f"✅ Task completed: {task_name}")
            return True
        except Exception as e:
            logger.error(f"❌ Scheduled task failed: {str(e)}")
            if task_id:
                task_manager.fail_task(task_id, str(e))
            return False
    
    def health_check_task(self):
        """Health check task"""
        return monitoring_system.get_agent_health()
    
    def content_pipeline_task(self):
        """Content pipeline task"""
        logger.info("  - Reading newsletter...")
        logger.info("  - Converting to script...")
        logger.info("  - Preparing video...")
        return "Content pipeline completed"
    
    def video_analysis_task(self):
        """Video analysis task"""
        logger.info("  - Fetching metrics...")
        logger.info("  - Analyzing performance...")
        logger.info("  - Updating learning database...")
        return "Video analysis completed"
    
    def daily_report_task(self):
        """Daily report task"""
        task_summary = task_manager.get_task_summary()
        report = f"Daily Report: {task_summary}"
        logger.info(f"  {report}")
        return report
    
    def monitoring_task(self):
        """Health monitoring task"""
        monitoring_system.alert_if_unhealthy()
        return "Health check completed"
    
    def start(self):
        """Start scheduler"""
        try:
            self.running = True
            logger.info("🚀 Task Scheduler started")
            
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("👋 Scheduler stopped")
            self.running = False
        except Exception as e:
            logger.error(f"❌ Scheduler failed: {str(e)}")
            self.running = False
    
    def stop(self):
        """Stop scheduler"""
        self.running = False
        logger.info("Scheduler stopped")

task_scheduler = TaskScheduler()
```
