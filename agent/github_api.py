"""
GitHub API Integration
Auto-commits for build progress
"""

import os
from github import Github
from agent.logger import setup_logger

logger = setup_logger(__name__)

class GitHubAPI:
    """GitHub Handler"""
    
    def __init__(self, token: str = None, repo: str = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.repo_name = repo or os.getenv("GITHUB_REPO")
        self.g = Github(self.token)
        self.repo = None
        self.init_repo()
    
    def init_repo(self):
        """Initialize repo connection"""
        try:
            self.repo = self.g.get_repo(self.repo_name)
            logger.info(f"✅ GitHub repo initialized: {self.repo_name}")
        except Exception as e:
            logger.error(f"❌ GitHub repo init failed: {str(e)}")
    
    def auto_commit(self, file_path: str, content: str, message: str):
        """Auto-commit file to GitHub"""
        try:
            # Check if file exists
            try:
                file = self.repo.get_contents(file_path)
                # Update existing file
                self.repo.update_file(
                    file_path,
                    message,
                    content,
                    file.sha
                )
            except:
                # Create new file
                self.repo.create_file(
                    file_path,
                    message,
                    content
                )
            
            logger.info(f"✅ Auto-committed: {file_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Auto-commit failed: {str(e)}")
            return False
    
    def get_build_progress(self):
        """Get build progress from README"""
        try:
            readme = self.repo.get_contents("README.md")
            return readme.decoded_content.decode()
        except Exception as e:
            logger.error(f"❌ Get README failed: {str(e)}")
            return None
    
    def update_readme(self, content: str):
        """Update README with build progress"""
        try:
            readme = self.repo.get_contents("README.md")
            self.repo.update_file(
                "README.md",
                "[AUTO] Update build progress",
                content,
                readme.sha
            )
            logger.info("✅ README updated")
            return True
        except Exception as e:
            logger.error(f"❌ Update README failed: {str(e)}")
            return False
    
    def create_issue(self, title: str, body: str):
        """Create GitHub issue (bug report, etc)"""
        try:
            issue = self.repo.create_issue(
                title=title,
                body=body
            )
            logger.info(f"✅ Issue created: {title}")
            return issue.number
        except Exception as e:
            logger.error(f"❌ Create issue failed: {str(e)}")
            return None

github_api = GitHubAPI()
```
