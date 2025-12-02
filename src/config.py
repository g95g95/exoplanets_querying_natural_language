"""Configuration module for the Exoplanet Data Analyst Agent."""

import os
from dotenv import load_dotenv

load_dotenv()

# NASA TAP Endpoint
NASA_TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP"

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Query Limits
DEFAULT_LIMIT = 1000
MAX_LIMIT = 10000
