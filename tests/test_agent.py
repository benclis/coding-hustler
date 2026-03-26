"""
Unit Tests - Agent Core Logic
"""

import unittest
from datetime import datetime
from agent.config import Config
from agent.database import Database
from agent.learning_engine import LearningEngine
from agent.tasks import TaskManager
from agent.monitoring import MonitoringSystem

class TestConfig(unittest.TestCase):
    """Test configuration"""
    
    def test_config_validation(self):
        """Test config validation"""
        self.assertTrue(Config.validate())
    
    def test_config_paths(self):
        """Test config paths exist"""
        self.assertTrue(Config.DATA_DIR.exists())
        self.assertTrue(Config.LOGS_DIR.exists())

class TestDatabase(unittest.TestCase):
    """Test database operations"""
    
    def setUp(self):
        """Setup test database"""
        self.db = Database()
    
    def test_database_init(self):
        """Test database initialization"""
        self.assertIsNotNone(self.db.db_path)
    
    def test_add_video(self):
        """Test adding video"""
        self.db.add_video(
            "test_video_123",
            "Test Video",
            {"views": 100, "ctr": 5.5}
        )
        # Should not raise exception
        self.assertTrue(True)
    
    def test_add_error(self):
        """Test adding error log"""
        self.db.add_error("test_error", "Test error message")
        self.assertTrue(True)

class TestLearningEngine(unittest.TestCase):
    """Test learning engine"""
    
    def setUp(self):
        """Setup learning engine"""
        self.engine = LearningEngine()
    
    def test_analyze_high_ctr(self):
        """Test analysis with high CTR"""
        metrics = {
            'ctr': 6.5,
            'watch_percentage': 70,
            'comments': 25,
            'affiliate_clicks': 15
        }
        
        learnings = self.engine.analyze_video_performance("test_vid", metrics)
        
        self.assertIsNotNone(learnings)
        self.assertEqual(learnings['video_id'], "test_vid")
        self.assertGreater(len(learnings['insights']), 0)
    
    def test_analyze_low_ctr(self):
        """Test analysis with low CTR"""
        metrics = {
            'ctr': 2.0,
            'watch_percentage': 40,
            'comments': 5,
            'affiliate_clicks': 2
        }
        
        learnings = self.engine.analyze_video_performance("test_vid_2", metrics)
        
        self.assertIsNotNone(learnings)
        # Should have failure insights
        failures = [i for i in learnings['insights'] if not i.get('success')]
        self.assertGreater(len(failures), 0)

class TestTaskManager(unittest.TestCase):
    """Test task management"""
    
    def setUp(self):
        """Setup task manager"""
        self.task_mgr = TaskManager()
    
    def test_create_task(self):
        """Test creating task"""
        task_id = self.task_mgr.create_task("Test Task", "Test description")
        self.assertIsNotNone(task_id)
    
    def test_task_workflow(self):
        """Test complete task workflow"""
        # Create
        task_id = self.task_mgr.create_task("Test Workflow")
        self.assertIsNotNone(task_id)
        
        # Start
        started = self.task_mgr.start_task(task_id)
        self.assertTrue(started)
        
        # Complete
        completed = self.task_mgr.complete_task(task_id, "Success")
        self.assertTrue(completed)
        
        # Verify
        task = self.task_mgr.get_task(task_id)
        self.assertEqual(task['status'], 'completed')

class TestMonitoring(unittest.TestCase):
    """Test monitoring system"""
    
    def setUp(self):
        """Setup monitoring"""
        self.monitor = MonitoringSystem()
    
    def test_record_metric(self):
        """Test recording metric"""
        result = self.monitor.record_metric("test_metric", 42.5)
        self.assertTrue(result)
    
    def test_health_report(self):
        """Test health report generation"""
        report = self.monitor.generate_health_report()
        self.assertIsNotNone(report)
        self.assertIn("AGENT HEALTH REPORT", report)

if __name__ == '__main__':
    unittest.main()
```
