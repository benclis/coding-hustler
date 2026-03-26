"""
Coding Hustler Setup
"""

from setuptools import setup, find_packages

setup(
    name="coding-hustler",
    version="0.1.0",
    description="Autonomous YouTube automation system with AI agent",
    author="Coding Hustler",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "python-dotenv",
        "requests",
        "pyyaml",
        "anthropic",
        "google-api-python-client",
        "stripe",
        "discord.py",
        "pygithub",
        "pandas",
        "pytest",
    ],
    entry_points={
        "console_scripts": [
            "hustler=agent.main:main",
        ],
    },
)
```

Commit message:
```
[BUILD] Day 1: Add setup.py
