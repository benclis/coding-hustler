"""
Monitoring & Alerting System
Track agent health and performance
"""

from datetime import datetime
from agent.database import db
from agent.logger import setup_logger
from agent.tasks import task_manager

logger = setup_logger(__name__)

class MonitoringSystem:
    """Monitors agent health and performance"""
    
    def __init__(self):
        self.metrics = {}
        logger.info("✅ Monitoring system initialized")
    
    def record_metric(self, metric_name: str, value: float):
        """Record performance metric"""
        try:
            self.metrics[metric_name] = {
                "value": value,
                "timestamp": datetime.now()
            }
            logger.info(f"📊 Metric: {metric_name} = {value}")
            return True
        except Exception as e:
            logger.error(f"❌ Record metric failed: {str(e)}")
            return False
    
    def get_agent_health(self):
        """Get overall agent health"""
        try:
            task_summary = task_manager.get_task_summary()
            
            if task_summary:
                total = task_summary.get("total", 0)
                completed = task_summary.get("completed", 0)
                failed = task_summary.get("failed", 0)
                
                if total > 0:
                    success_rate = (completed / total) * 100
                else:
                    success_rate = 0
                
                health_status = "HEALTHY" if success_rate >= 80 else "WARNING" if success_rate >= 60 else "CRITICAL"
                
                return {
                    "status": health_status,
                    "success_rate": success_rate,
                    "total_tasks": total,
                    "completed": completed,
                    "failed": failed
                }
            return None
        except Exception as e:
            logger.error(f"❌ Get agent health failed: {str(e)}")
            return None
    
    def check_api_health(self, api_manager):
        """Check all API connections"""
        try:
            return api_manager.health_check()
        except Exception as e:
            logger.error(f"❌ Check API health failed: {str(e)}")
            return False
    
    def generate_health_report(self, api_manager=None):
        """Generate comprehensive health report"""
        try:
            report = f"""
╔════════════════════════════════════════╗
║     AGENT HEALTH REPORT                ║
╚════════════════════════════════════════╝

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

AGENT STATUS:
"""
            
            # Task health
            health = self.get_agent_health()
            if health:
                report += f"""
  Status: {health['status']}
  Success Rate: {health['success_rate']:.1f}%
  Tasks Completed: {health['completed']}/{health['total_tasks']}
  Failed Tasks: {health['failed']}
"""
            
            # API health
            if api_manager:
                report += "\nAPI CONNECTIONS:\n"
                api_ok = api_manager.health_check()
                report += f"  Overall: {'✅ OK' if api_ok else '❌ FAILED'}\n"
            
            # Metrics
            if self.metrics:
                report += "\nPERFORMANCE METRICS:\n"
                for metric_name, metric_data in self.metrics.items():
                    report += f"  {metric_name}: {metric_data['value']}\n"
            
            report += "\n════════════════════════════════════════"
            
            logger.info(report)
            return report
        except Exception as e:
            logger.error(f"❌ Generate health report failed: {str(e)}")
            return None
    
    def alert_if_unhealthy(self):
        """Send alert if health is degraded"""
        try:
            health = self.get_agent_health()
            
            if health and health["success_rate"] < 80:
                alert_msg = f"""
⚠️ AGENT HEALTH ALERT
Success Rate: {health['success_rate']:.1f}%
Failed Tasks: {health['failed']}
Status: {health['status']}

Action: Review failed tasks and API connections
"""
                logger.warning(alert_msg)
                db.add_error("health_alert", alert_msg)
                return True
            
            return False
        except Exception as e:
            logger.error(f"❌ Alert check failed: {str(e)}")
            return False

monitoring_system = MonitoringSystem()
```
