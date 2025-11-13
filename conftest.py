"""
Root conftest.py for pytest configuration.
This ensures Django settings are properly loaded for all tests.
"""

import os
from pathlib import Path

# Load environment variables from .env file
import environ

env = environ.Env()

# Build paths
BASE_DIR = Path(__file__).resolve().parent

# Read .env file
env_file = BASE_DIR / ".env"
if env_file.exists():
    env.read_env(str(env_file))

# Set default environment variables for testing if not set
if "DATABASE_URL" not in os.environ:
    os.environ["DATABASE_URL"] = "sqlite:///test.db"

if "REDIS_URL" not in os.environ:
    os.environ["REDIS_URL"] = "redis://localhost:6379/0"

if "SECRET_KEY" not in os.environ:
    os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"


def pytest_configure(config):
    """Configure pytest with Django settings."""
    from django.conf import settings

    if not settings.configured:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.test")
        import django

        django.setup()
