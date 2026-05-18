import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from repository root .env file
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_FILE)

# Authentication
USERNAME = os.getenv("IG_USERNAME", "")
PASSWORD = os.getenv("IG_PASSWORD", "")

# Data source account (followers from this account will be added)
TARGET = os.getenv("IG_TARGET", "")  # Ex: "my_profile"

# Session persistence
SESSION_FILE = os.getenv("SESSION_FILE", "SRC/session_settings.json")

# Logging configuration
LOG_DIR = os.getenv("LOG_DIR", "SRC/log")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Execution tuning
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "200"))
REQUEST_DELAY_SECONDS = float(os.getenv("REQUEST_DELAY_SECONDS", "2"))
