# Getting Started - Coding Hustler Agent

Quick start guide to run the autonomous YouTube agent.

---

## Prerequisites

- Python 3.11+
- Git
- YouTube Channel (created)
- Google Cloud Project with YouTube Data API enabled
- Discord Server (optional, for community)
- GitHub Account

---

## 1. Installation

### Clone Repository
```bash
git clone https://github.com/benclis/coding-hustler.git
cd coding-hustler
```

### Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 2. Configuration

### Get API Keys

#### YouTube API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable "YouTube Data API v3"
4. Create API Key in Credentials
5. Copy the key

#### YouTube Channel ID
1. Go to your YouTube channel
2. Click Settings → Advanced Settings
3. Copy Channel ID

#### Discord Bot Token (Optional)
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create New Application
3. Create Bot
4. Copy Token

#### GitHub Token (Optional)
1. Go to [GitHub Settings](https://github.com/settings/tokens)
2. Create Personal Access Token
3. Give repo access
4. Copy token

### Setup .env File
```bash
# Copy template
cp .env.example .env

# Edit with your keys
notepad .env  # Windows
nano .env     # Mac/Linux
```

Fill in:
```
YOUTUBE_API_KEY=AIzaSy...
YOUTUBE_CHANNEL_ID=UC...
DISCORD_BOT_TOKEN=your_token
GITHUB_TOKEN=ghp_...
ANTHROPIC_API_KEY=sk-ant-...
APP_ENV=development
LOG_LEVEL=INFO
```

---

## 3. Initialize Database
```bash
python -m agent.main --init-db
```

Creates SQLite database with tables:
- `videos` - Video records
- `learning_patterns` - Success patterns
- `errors` - Error logs
- `tasks` - Task tracking

---

## 4. Check Status
```bash
python -m agent.main --status
```

Expected output:
```
🤖 Agent Status: READY
Database: ./data/hustler.db
Environment: development
```

---

## 5. Run Agent

### One-Time Execution
```bash
python -m agent.main --run
```

Executes:
1. ✅ System health check
2. ✅ Content pipeline
3. ✅ Video metrics analysis
4. ✅ Learning update
5. ✅ Daily report

### Scheduled Execution (Coming Soon)
```bash
python -m agent.main --schedule
```

Runs on schedule:
- 8 AM: System health
- 10 AM: Content pipeline
- 2 PM: Video analysis
- 6 PM: Daily report
- Hourly: Health monitoring

---

## 6. View Results

### Logs
```bash
# View real-time logs
tail -f logs/agent.log

# Windows
type logs\agent.log
```

### Database
```bash
# Query SQLite
sqlite3 data/hustler.db

# In SQLite shell:
SELECT * FROM videos;
SELECT * FROM tasks;
SELECT * FROM errors;
```

### GitHub
```bash
# Check auto-commits
git log --oneline
```

---

## 7. Common Commands

### Agent Commands
```bash
# Initialize database
python -m agent.main --init-db

# Check status
python -m agent.main --status

# Run full workflow
python -m agent.main --run

# Run tests
pytest tests/ -v
```

### Git Commands
```bash
# Pull latest code
git pull origin main

# Check status
git status

# View commits
git log --oneline
```

### Database Commands
```bash
# Query videos
sqlite3 data/hustler.db "SELECT * FROM videos LIMIT 5;"

# Query tasks
sqlite3 data/hustler.db "SELECT * FROM tasks WHERE status='completed';"

# Query errors
sqlite3 data/hustler.db "SELECT * FROM errors ORDER BY timestamp DESC LIMIT 10;"
```

---

## 8. Troubleshooting

### "ModuleNotFoundError: No module named 'agent'"

**Fix:**
```bash
# Ensure virtual env is activated
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### "YOUTUBE_API_KEY not found"

**Fix:**
```bash
# Check .env file exists
cat .env

# Ensure variables are set
echo %YOUTUBE_API_KEY%  # Windows
echo $YOUTUBE_API_KEY   # Mac/Linux
```

### "Database locked" error

**Fix:**
```bash
# Close any open connections
# Delete lock file if exists
rm data/hustler.db-journal

# Reinitialize
python -m agent.main --init-db
```

### Agent not running scheduled tasks

**Fix:**
```bash
# Check logs for errors
tail -f logs/agent.log

# Verify cron job (if using Linux)
crontab -l
```

---

## 9. Next Steps

### Set Up Discord (Optional)
1. Create Discord server
2. Add bot to server
3. Enable commands channel
4. Test with `!status` command

### Enable GitHub Auto-Commits
1. Add GitHub token to .env
2. Agent will auto-commit on milestones

### Configure YouTube
1. Verify channel is set as default
2. Check upload permissions
3. Monitor video analytics

### Monitor Agent
1. Check logs daily
2. Review task success rate
3. Monitor API health
4. Check database size

---

## 10. Production Setup

### Run on VPS
```bash
# Install Python
sudo apt-get install python3.11

# Clone and setup
git clone https://github.com/benclis/coding-hustler.git
cd coding-hustler
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with systemd
# Create /etc/systemd/system/coding-hustler.service
```

### Systemd Service File
```ini
[Unit]
Description=Coding Hustler Agent
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/coding-hustler
ExecStart=/home/ubuntu/coding-hustler/venv/bin/python -m agent.main --run
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

## 11. Support

- 📖 [API Documentation](./API.md)
- 🐛 [GitHub Issues](https://github.com/benclis/coding-hustler/issues)
- 💬 [Discord Community](#)
- 📧 Email: support@codinghustler.com

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python -m agent.main --status` | Check agent status |
| `python -m agent.main --run` | Run full workflow |
| `python -m agent.main --init-db` | Initialize database |
| `pytest tests/` | Run tests |
| `git pull origin main` | Get latest code |
| `tail -f logs/agent.log` | View live logs |

---

**Ready to go!** Start with `python -m agent.main --run` 🚀
```
```
╚═══════════════════════════════════════════════════════╝
