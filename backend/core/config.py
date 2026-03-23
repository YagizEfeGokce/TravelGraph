"""Application configuration loaded from environment variables via pydantic-settings."""
from __future__ import annotations

from urllib.parse import urlparse

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All runtime settings for the TravelGraph backend.

    Values are read from the environment or a `.env` file in the working directory.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # FalkorDB — individual host/port (local dev default)
    FALKORDB_HOST: str = "localhost"
    FALKORDB_PORT: int = 6379
    FALKORDB_GRAPH: str = "travelgraph"

    # FalkorDB — Railway / cloud URL (takes priority when set)
    # Format: redis://host:port  or  redis://:password@host:port
    FALKORDB_URL: str = ""

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_EXPIRE_DAYS: int = 7

    # CORS — stored as comma-separated string in .env
    CORS_ORIGINS: str = (
        "http://localhost:5173,"
        "https://travel-graph.vercel.app,"
        "https://travelgraph.vercel.app"
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Return CORS_ORIGINS as a list, split on commas."""
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    @property
    def falkordb_host(self) -> str:
        """Return the resolved FalkorDB host.

        If FALKORDB_URL is set it takes priority over FALKORDB_HOST.
        """
        if self.FALKORDB_URL:
            return urlparse(self.FALKORDB_URL).hostname or self.FALKORDB_HOST
        return self.FALKORDB_HOST

    @property
    def falkordb_port(self) -> int:
        """Return the resolved FalkorDB port.

        If FALKORDB_URL is set it takes priority over FALKORDB_PORT.
        """
        if self.FALKORDB_URL:
            return urlparse(self.FALKORDB_URL).port or self.FALKORDB_PORT
        return self.FALKORDB_PORT

    @property
    def falkordb_password(self) -> str | None:
        """Return the FalkorDB password from FALKORDB_URL, or None."""
        if self.FALKORDB_URL:
            return urlparse(self.FALKORDB_URL).password or None
        return None


settings = Settings()
