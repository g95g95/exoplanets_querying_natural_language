"""Query cache for TAP results."""

import hashlib
import json
import time
from typing import Dict, Any, Optional
from pathlib import Path

# In-memory cache with TTL
_cache: Dict[str, Dict[str, Any]] = {}

# Default TTL: 15 minutes
DEFAULT_TTL = 900

# Cache directory for persistent storage
CACHE_DIR = Path(__file__).parent.parent.parent / ".cache"


def _get_cache_key(query: str) -> str:
    """Generate cache key from query.

    Args:
        query: SQL query string

    Returns:
        MD5 hash of normalized query
    """
    normalized = " ".join(query.lower().split())
    return hashlib.md5(normalized.encode()).hexdigest()


def get_cached(query: str) -> Optional[Dict[str, Any]]:
    """Get cached result for a query.

    Args:
        query: SQL query string

    Returns:
        Cached result or None if not found/expired
    """
    key = _get_cache_key(query)

    # Check memory cache first
    if key in _cache:
        entry = _cache[key]
        if time.time() < entry["expires"]:
            return entry["data"]
        else:
            del _cache[key]

    # Check file cache
    cache_file = CACHE_DIR / f"{key}.json"
    if cache_file.exists():
        try:
            with open(cache_file, "r") as f:
                entry = json.load(f)
            if time.time() < entry["expires"]:
                # Restore to memory cache
                _cache[key] = entry
                return entry["data"]
            else:
                cache_file.unlink()
        except (json.JSONDecodeError, KeyError):
            cache_file.unlink()

    return None


def set_cached(query: str, data: Dict[str, Any], ttl: int = DEFAULT_TTL):
    """Cache a query result.

    Args:
        query: SQL query string
        data: Result data to cache
        ttl: Time to live in seconds
    """
    key = _get_cache_key(query)
    expires = time.time() + ttl

    entry = {
        "data": data,
        "expires": expires,
        "query": query
    }

    # Store in memory
    _cache[key] = entry

    # Store to file for persistence
    CACHE_DIR.mkdir(exist_ok=True)
    cache_file = CACHE_DIR / f"{key}.json"
    try:
        with open(cache_file, "w") as f:
            json.dump(entry, f)
    except IOError:
        pass  # File cache is optional


def clear_cache():
    """Clear all cached entries."""
    global _cache
    _cache = {}

    if CACHE_DIR.exists():
        for f in CACHE_DIR.glob("*.json"):
            f.unlink()


def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics.

    Returns:
        Dict with cache stats
    """
    memory_count = len(_cache)
    file_count = len(list(CACHE_DIR.glob("*.json"))) if CACHE_DIR.exists() else 0

    return {
        "memory_entries": memory_count,
        "file_entries": file_count,
        "cache_dir": str(CACHE_DIR)
    }
