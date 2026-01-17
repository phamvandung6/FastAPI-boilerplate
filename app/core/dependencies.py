"""FastAPI dependencies.

This module re-exports common dependencies for convenience.
"""

from app.infra.database import get_db

__all__ = ["get_db"]
