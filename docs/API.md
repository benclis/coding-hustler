# Coding Hustler Agent - API Documentation

## Overview

Coding Hustler Agent exposes APIs for controlling and monitoring the autonomous YouTube system.

---

## Core APIs

### 1. YouTube API (`agent/youtube_api.py`)

#### Get Channel Stats
```python
from agent.youtube_api import youtube_api

stats = youtube_api.get_channel_stats()
# Returns: {
#   "title": "Coding Hustler",
#   "subscribers": "1,234",
#   "view_count": "125,000",
#   "video_count": "24"
# }
```

#### Get Video Stats
```python
stats = youtube_api.get_video_stats("dQw4w9WgXcQ")
# Returns: {
#   "title": "Video Title",
#   "views": 1500,
#   "likes": 250,
#   "comments": 45,
#   "published_at": "2026-03-26T10:00:00Z"
# }
```

#### Search Channel Videos
```python
videos = youtube_api.search_channel_videos(max_results=10)
# Returns list of videos with IDs and titles
```

---

### 2. Discord API (`agent/discord_api.py`)

#### Commands Available

**!status** - Check agent status
```
User: !status
Bot: 🤖 Agent Status: OPERATIONAL ✅
```

**!challenge** - Get current challenge
```
User: !challenge
Bot: 🏆 HAFTALIK CHALLENGE
Tema: İlk 5 kişiye LinkedIn mesajı gönder
Ödül: Special badge + mention
```

**!mentors** - List available mentors
```
User: !mentors
Bot: 👨‍🏫 Available Mentors:
- @mentor1 (Freelance)
- @mentor2 (SaaS)
- @mentor3 (YouTube)
```

---

### 3. GitHub API (`agent/github_api.py`)

#### Auto-Commit
```python
from agent.github_api import github_api

github_api.auto_commit(
    file_path="logs/build_progress.txt",
    content="Build progress update",
    message="[AUTO] Update build progress"
)
```

#### Update README
```python
github_api.update_readme(content="New README content")
```

#### Create Issue
```python
issue_num = github_api.create_issue(
    title="Bug: Video upload failed",
    body="Description of the bug"
)
```

---

### 4. Task Management (`agent/tasks.py`)

#### Create Task
```python
from agent.tasks import task_manager

task_id = task_manager.create_task(
    "Video Upload",
    "Upload new video to YouTube"
)
```

#### Task Workflow
```python
# Start task
task_manager.start_task(task_id)

# Complete task
task_manager.complete_task(task_id, "Video uploaded successfully")

# Or fail task
task_manager.fail_task(task_id, "Upload timeout")
```

#### Get Tasks
```python
# Get specific task
task = task_manager.get_task(task_id)

# Get all tasks
all_tasks = task_manager.get_all_tasks()

# Get tasks by status
pending = task_manager.get_all_tasks(status="pending")

# Get summary
summary = task_manager.get_task_summary()
# Returns: {
#   "total": 50,
#   "completed": 45,
#   "failed": 3,
#   "running": 2
# }
```

---

### 5. Monitoring (`agent/monitoring.py`)

#### Record Metric
```python
from agent.monitoring import monitoring_system

monitoring_system.record_metric("video_upload_time", 45.2)
```

#### Health Check
```python
health = monitoring_system.get_agent_health()
# Returns: {
#   "status": "HEALTHY",
#   "success_rate": 95.5,
#   "total_tasks": 50,
#   "completed": 48,
#   "failed": 2
# }
```

#### Generate Report
```python
report = monitoring_system.generate_health_report()
print(report)
```

---

### 6. API Manager (`agent/api_manager.py`)

#### Get Channel Metrics
```python
from agent.api_manager import api_manager

metrics = api_manager.get_channel_metrics()
```

#### Analyze Latest Video
```python
stats = api_manager.analyze_latest_video()
```

#### Health Check All APIs
```python
all_ok = api_manager.health_check()
# Returns: True/False
```

---

## Command Line Interface

### Status Check
```bash
python -m agent.main --status
```

Output:
```
🤖 Agent Status: READY
Database: ./data/hustler.db
Environment: development
```

### Run Agent
```bash
python -m agent.main --run
```

Executes daily schedule:
- System health check
- Content pipeline
- Video metrics analysis
- Learning update
- Daily report

### Initialize Database
```bash
python -m agent.main --init-db
```

---

## Environment Variables

Required in `.env` file:
```
YOUTUBE_API_KEY=AIzaSy...
YOUTUBE_CHANNEL_ID=UCxx...
DISCORD_BOT_TOKEN=your_token
GITHUB_TOKEN=ghp_...
ANTHROPIC_API_KEY=sk-ant-...
APP_ENV=development
LOG_LEVEL=INFO
```

---

## Error Handling

All APIs include error handling:
```python
try:
    stats = youtube_api.get_channel_stats()
except Exception as e:
    logger.error(f"Failed: {str(e)}")
```

Errors are logged to:
- Console output
- Log file: `logs/agent.log`
- Database: `errors` table

---

## Performance Metrics

Tracked metrics:
- Video upload time
- API response time
- Task completion rate
- Success/failure ratio
- Watch time percentage
- CTR (Click-through rate)

---

## Monitoring & Alerts

Agent monitors:
- Task success rate (target: 80%+)
- API health (all connected?)
- Database connectivity
- Daily task execution

Alerts triggered when:
- Success rate drops below 80%
- API connection fails
- Task execution fails
- Database error occurs

---

## Rate Limits

### YouTube API
- 1 million quota units per day
- Used by: stats requests, search queries

### Discord Bot
- Message rate: 1 per second (per channel)
- Used by: announcements, commands

### GitHub API
- 5000 requests per hour
- Used by: auto-commits, README updates

---

## Examples

### Complete Workflow
```python
from agent.api_manager import api_manager
from agent.tasks import task_manager

# Create task
task_id = task_manager.create_task("Full Workflow")
task_manager.start_task(task_id)

# Get metrics
metrics = api_manager.get_channel_metrics()
print(f"Subscribers: {metrics['subscribers']}")

# Analyze video
video_stats = api_manager.analyze_latest_video()
print(f"Views: {video_stats['views']}")

# Check health
health = api_manager.health_check()
print(f"APIs OK: {health}")

# Complete task
task_manager.complete_task(task_id, "Workflow complete")
```

---

For more info, see `/docs` folder or check source code in `/agent`.
```
