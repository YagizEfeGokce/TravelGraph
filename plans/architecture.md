---
version: 1.0.0
last_updated: 2026-05-20
domain: architecture
scope: root
---

# Architecture Plan

## Overview

TravelGraph is a graph-based travel intelligence platform with a FastAPI backend and React frontend, backed by FalkorDB (a graph database).

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Backend framework | FastAPI | 0.115 |
| Database | FalkorDB | 1.0.9 |
| Language | Python | 3.11+ |
| Frontend framework | React | 18 |
| Build tool | Vite | 5 |
| Styling | Tailwind CSS | 3.x |
| Language | TypeScript | 5.x |
| Deployment (backend) | Railway | — |
| Deployment (frontend) | Vercel | — |

## System Components

```
┌─────────────────┐      HTTP/REST       ┌─────────────────┐
│   React SPA     │ ◄───────────────────► │   FastAPI       │
│   (Vercel)      │   JWT Bearer Token    │   (Railway)     │
└─────────────────┘                       └─────────────────┘
                                                │
                                                │ Redis protocol
                                                ▼
                                         ┌─────────────────┐
                                         │   FalkorDB      │
                                         │   (Graph DB)    │
                                         └─────────────────┘
```

## Component Boundaries

### Backend (`backend/`)
- `main.py` — FastAPI app factory, lifespan events, exception handlers, CORS, rate limiter setup
- `core/` — Configuration (pydantic-settings), security (bcrypt/JWT), dependencies (auth injection)
- `db/` — FalkorDB connection singleton, seed script
- `models/` — 14 Pydantic v2 schemas (validation + serialization)
- `routers/` — API endpoint modules (auth, destinations, activities, etc.)
- `services/` — Recommendation engine (Cypher traversal queries)

### Frontend (`frontend/src/`)
- `api/` — Axios client + per-domain API wrappers
- `contexts/` — React context for auth state
- `hooks/` — Custom data-fetching hooks (useDestinations, useItinerary, etc.)
- `pages/` — Route-level page components (9 pages)
- `components/` — Reusable UI components (16 components, many unused)

## Data Flow

### Request Flow
1. React SPA makes HTTP request to FastAPI backend (via Axios)
2. FastAPI routes validate request with Pydantic models
3. Auth dependency extracts JWT from `access_token` httpOnly cookie first, then `Authorization: Bearer <token>` header
4. Router executes parameterized Cypher query via FalkorDB
5. Response serialized through Pydantic `response_model`
6. Frontend receives JSON, updates React state

### Auth Flow
1. User registers → `POST /api/auth/register` → bcrypt hash → create User node → set httpOnly cookies
2. User logs in → `POST /api/auth/login` → verify password → set httpOnly cookies
3. Frontend uses `withCredentials: true`; no localStorage usage (**FIXED**)
4. Axios response interceptor handles 401 → calls `/auth/refresh` → retry original request
5. User logs out → `POST /auth/logout` → cookies cleared

## Known Architectural Issues

1. **No connection pooling** — `get_db()` creates a new FalkorDB connection per HTTP request.
2. **No API gateway / reverse proxy** — Frontend talks directly to backend; no rate limiting at edge.
3. ~~**Monolithic frontend bundle**~~ — **FIXED** — `React.lazy` + `Suspense` code splitting implemented
4. **No caching layer** — Every request hits FalkorDB directly.
5. **No event-driven architecture** — Reviews, itinerary updates are synchronous only.
6. **Single graph for everything** — No separation of concerns (auth graph vs content graph).
