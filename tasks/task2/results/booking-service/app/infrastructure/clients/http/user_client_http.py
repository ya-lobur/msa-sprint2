"""HTTP implementation of user client."""
from typing import Optional

import structlog

from app.domain.ports import UserClient
from .base import BaseHTTPClient

logger = structlog.get_logger()


class UserClientHTTP(UserClient):
    """HTTP client for user service."""

    def __init__(self, base_url: str):
        self.client = BaseHTTPClient(base_url)

    async def close(self):
        """Close HTTP client."""
        await self.client.close()

    async def is_user_active(self, user_id: str) -> bool:
        """Check if user is active."""
        try:
            result = await self.client.get(f"/api/users/{user_id}/active")
            return bool(result) if isinstance(result, bool) else result == "true"
        except Exception as e:
            logger.error("user_active_check_failed", user_id=user_id, error=str(e))
            return False

    async def is_user_blacklisted(self, user_id: str) -> bool:
        """Check if user is blacklisted."""
        try:
            result = await self.client.get(f"/api/users/{user_id}/blacklisted")
            return bool(result) if isinstance(result, bool) else result == "true"
        except Exception as e:
            logger.error("user_blacklist_check_failed", user_id=user_id, error=str(e))
            return False

    async def get_user_status(self, user_id: str) -> Optional[str]:
        """Get user status."""
        try:
            result = await self.client.get(f"/api/users/{user_id}/status")
            return str(result) if result else None
        except Exception as e:
            logger.error("user_status_get_failed", user_id=user_id, error=str(e))
            return None
