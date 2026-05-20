"""TravelGraph FastAPI application factory."""
from __future__ import annotations

import logging
import uuid
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from core.config import settings
from core.limiter import limiter
from db.connection import check_connection, create_indexes
from routers import activities, auth, destinations, festivals, itineraries, reviews, users, restaurants, budgets, tags_categories

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Run startup tasks before the application begins serving requests."""
    if not check_connection():
        logger.warning(
            "FalkorDB is unreachable at startup — continuing without database"
        )
    else:
        create_indexes()

    yield


def create_app() -> FastAPI:
    """Construct and configure the FastAPI application instance."""
    app = FastAPI(
        title="TravelGraph API",
        version="0.1.0",
        lifespan=lifespan,
    )

    # ── Correlation ID middleware ──────────────────────────────────────────────
    @app.middleware("http")
    async def correlation_id_middleware(request: Request, call_next):
        cid = request.headers.get("X-Request-ID") or str(uuid.uuid4())[:12]
        request.state.correlation_id = cid
        response = await call_next(request)
        response.headers["X-Request-ID"] = cid
        return response

    # ── Rate limiting ──────────────────────────────────────────────────────────
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # ── CORS ───────────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    )

    # ── Exception handlers ─────────────────────────────────────────────────────
    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail, "type": "HTTPException"},
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        cid = getattr(request.state, "correlation_id", "unknown")
        logger.error(
            "[%s] Unhandled exception for %s %s: %s",
            cid,
            request.method,
            request.url,
            exc,
            exc_info=True,
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
            headers={"X-Request-ID": cid},
        )

    # ── Routers ────────────────────────────────────────────────────────────────
    app.include_router(auth.router, prefix="/api")
    app.include_router(users.router, prefix="/api")
    app.include_router(destinations.router, prefix="/api")
    app.include_router(activities.router, prefix="/api")
    app.include_router(itineraries.router, prefix="/api")
    app.include_router(reviews.router, prefix="/api")
    app.include_router(festivals.router, prefix="/api")
    app.include_router(restaurants.router, prefix="/api")
    app.include_router(budgets.router, prefix="/api")
    app.include_router(tags_categories.router, prefix="/api")

    # ── Health endpoint ────────────────────────────────────────────────────────
    @app.get("/api/health", tags=["health"])
    @limiter.exempt
    async def health(request: Request) -> dict:
        """Return database reachability status and API version."""
        db_ok = check_connection()
        return {
            "status": "ok",
            "db": db_ok,
            "version": app.version,
        }

    return app


app = create_app()
