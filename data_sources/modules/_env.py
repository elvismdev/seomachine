"""Shared .env loading utility for all data_sources modules."""

from pathlib import Path

_loaded = False


def ensure_env():
    """Load .env from the canonical location (data_sources/config/.env).

    Safe to call multiple times -- only loads once per process.
    """
    global _loaded
    if _loaded:
        return
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    _loaded = True
