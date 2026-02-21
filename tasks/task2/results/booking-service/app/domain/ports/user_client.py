"""User service client port."""
from abc import ABC, abstractmethod
from typing import Optional


class UserClient(ABC):
    """Client interface for user service."""

    @abstractmethod
    async def is_user_active(self, user_id: str) -> bool:
        """Check if user is active."""
        pass

    @abstractmethod
    async def is_user_blacklisted(self, user_id: str) -> bool:
        """Check if user is blacklisted."""
        pass

    @abstractmethod
    async def get_user_status(self, user_id: str) -> Optional[str]:
        """Get user status (VIP/ACTIVE/etc)."""
        pass
