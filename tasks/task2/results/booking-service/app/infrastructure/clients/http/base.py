"""Base HTTP client with retries and timeouts."""
import structlog
from httpx import AsyncClient, HTTPError, Timeout
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = structlog.get_logger()


class BaseHTTPClient:
    """Base HTTP client with retry logic."""

    def __init__(self, base_url: str, timeout: float = 5.0, max_retries: int = 3):
        self.base_url = base_url.rstrip("/")
        self.timeout = Timeout(timeout)
        self.max_retries = max_retries
        self.client = AsyncClient(timeout=self.timeout, follow_redirects=True)

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=2),
        retry=retry_if_exception_type(HTTPError),
        reraise=True,
    )
    async def get(self, path: str) -> dict | str | bool:
        """Execute GET request with retries."""
        url = f"{self.base_url}{path}"
        logger.debug("http_get", url=url)

        try:
            response = await self.client.get(url)
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                return response.json()
            else:
                text = response.text.strip()
                # Handle boolean responses
                if text.lower() in ("true", "false"):
                    return text.lower() == "true"
                return text

        except HTTPError as e:
            logger.error("http_get_error", url=url, error=str(e))
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=2),
        retry=retry_if_exception_type(HTTPError),
        reraise=True,
    )
    async def post(self, path: str, json: dict | None = None) -> dict | str:
        """Execute POST request with retries."""
        url = f"{self.base_url}{path}"
        logger.debug("http_post", url=url, json=json)

        try:
            response = await self.client.post(url, json=json)
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                return response.json()
            else:
                return response.text

        except HTTPError as e:
            logger.error("http_post_error", url=url, error=str(e))
            raise
