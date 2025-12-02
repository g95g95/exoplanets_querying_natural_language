"""Configuration module for the Exoplanet Data Analyst Agent."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Find .env file - look in project root
PROJECT_ROOT = Path(__file__).parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

print(f"[CONFIG] Looking for .env at: {ENV_FILE}")
print(f"[CONFIG] .env exists: {ENV_FILE.exists()}")

# Load .env with explicit path
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
    print("[CONFIG] .env file loaded successfully")
else:
    load_dotenv()  # Fallback to default behavior
    print("[CONFIG] WARNING: .env file not found, using default load_dotenv()")

# NASA TAP Endpoint
NASA_TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP"

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Debug: Print API key status
print(f"[CONFIG] LLM_PROVIDER: {LLM_PROVIDER}")
print(f"[CONFIG] LLM_MODEL: {LLM_MODEL}")
print(f"[CONFIG] OPENAI_API_KEY: {'SET (ends with ' + OPENAI_API_KEY[-6:] + ')' if OPENAI_API_KEY else 'NOT SET'}")
print(f"[CONFIG] ANTHROPIC_API_KEY: {'SET' if ANTHROPIC_API_KEY else 'NOT SET'}")

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Query Limits
DEFAULT_LIMIT = 1000
MAX_LIMIT = 10000
