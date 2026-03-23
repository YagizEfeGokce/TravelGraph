"""FalkorDB connection management: factory, dependency, health check, and index creation."""
from __future__ import annotations

import logging
import time
from collections.abc import Generator
from typing import Any

import falkordb

from core.config import settings

logger = logging.getLogger(__name__)

_MAX_RETRIES: int = 3
_RETRY_DELAY_SECONDS: int = 2


def _connect_with_retry() -> Any:
    """Create a FalkorDB graph handle, retrying up to *_MAX_RETRIES* times.

    Returns:
        A FalkorDB Graph object for the configured graph name.

    Raises:
        RuntimeError: If all connection attempts fail.
    """
    last_exc: Exception | None = None

    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            connect_kwargs: dict = {
                "host": settings.falkordb_host,
                "port": settings.falkordb_port,
            }
            if settings.falkordb_password:
                connect_kwargs["password"] = settings.falkordb_password
            client = falkordb.FalkorDB(**connect_kwargs)
            graph = client.select_graph(settings.FALKORDB_GRAPH)
            logger.info(
                "FalkorDB connected (host=%s port=%s graph=%s)",
                settings.falkordb_host,
                settings.falkordb_port,
                settings.FALKORDB_GRAPH,
            )
            return graph
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            logger.warning(
                "FalkorDB connection attempt %d/%d failed: %s",
                attempt,
                _MAX_RETRIES,
                exc,
            )
            if attempt < _MAX_RETRIES:
                time.sleep(_RETRY_DELAY_SECONDS)

    raise RuntimeError(
        f"Could not connect to FalkorDB after {_MAX_RETRIES} attempts"
    ) from last_exc


def get_db() -> Generator[Any, None, None]:
    """FastAPI dependency that yields a FalkorDB Graph instance per request.

    Usage::

        @router.get("/example")
        def example(graph = Depends(get_db)):
            result = graph.query("RETURN 1")
    """
    graph = _connect_with_retry()
    try:
        yield graph
    finally:
        # falkordb connections are stateless over Redis; nothing to close explicitly
        pass


def check_connection() -> bool:
    """Verify that FalkorDB is reachable by running a trivial query.

    Returns:
        ``True`` if the database responds correctly, ``False`` otherwise.
    """
    try:
        connect_kwargs: dict = {
            "host": settings.falkordb_host,
            "port": settings.falkordb_port,
        }
        if settings.falkordb_password:
            connect_kwargs["password"] = settings.falkordb_password
        client = falkordb.FalkorDB(**connect_kwargs)
        graph = client.select_graph(settings.FALKORDB_GRAPH)
        graph.query("RETURN 1")
        return True
    except Exception as exc:  # noqa: BLE001
        logger.error("FalkorDB health check failed: %s", exc)
        return False


def create_indexes() -> None:
    """Create indexes on frequently queried node properties.

    Indexes created:
    - ``(User)-[email]``
    - ``(User)-[id]``
    - ``(Destination)-[id]``
    - ``(Destination)-[name]``

    Each index is created independently so a single failure does not
    prevent the remaining indexes from being applied.
    """
    index_statements: list[str] = [
        "CREATE INDEX FOR (u:User) ON (u.email)",
        "CREATE INDEX FOR (u:User) ON (u.id)",
        "CREATE INDEX FOR (d:Destination) ON (d.id)",
        "CREATE INDEX FOR (d:Destination) ON (d.name)",
    ]

    try:
        connect_kwargs: dict = {
            "host": settings.falkordb_host,
            "port": settings.falkordb_port,
        }
        if settings.falkordb_password:
            connect_kwargs["password"] = settings.falkordb_password
        client = falkordb.FalkorDB(**connect_kwargs)
        graph = client.select_graph(settings.FALKORDB_GRAPH)
    except Exception as exc:  # noqa: BLE001
        logger.error("Could not connect to FalkorDB to create indexes: %s", exc)
        return

    for statement in index_statements:
        try:
            graph.query(statement)
            logger.info("Index ensured: %s", statement)
        except Exception as exc:  # noqa: BLE001
            # Index may already exist — log and continue
            logger.warning("Index statement skipped (%s): %s", statement, exc)
