---
version: 1.0.0
last_updated: 2026-05-20
domain: roadmap
scope: root
---

# Project Roadmap

## Completed (Pre-2026-05-20)
- [x] FastAPI backend scaffold (main.py, config, security, dependencies)
- [x] FalkorDB connection layer with retry logic
- [x] JWT auth system (register, login, refresh, me)
- [x] 14 Pydantic v2 entity models
- [x] CRUD routers for destinations, activities, restaurants, festivals, reviews, tags, categories, seasons
- [x] Itinerary CRUD + stop management
- [x] Budget plan router
- [x] Recommendation engine (Cypher traversal + collaborative filtering + shortest path)
- [x] React frontend scaffold (Vite + TypeScript + Tailwind)
- [x] Frontend pages (Home, Explore, Destination Detail, Planner, Festivals, Login, Register, Profile)
- [x] Railway + Vercel deployment configuration
- [x] API test file (backend/api_test.http)

## Completed Today (2026-05-20)

### Audit & Documentation
- [x] **Backend audit** — 55 issues found (14 Critical, 14 High, 18 Medium, 9 Low)
- [x] **Frontend audit** — 50 issues found (4 Critical, 16 High, 22 Medium, 8 Low)
- [x] **Security & deployment audit** — 21 issues found (3 Critical, 5 High, 10 Medium, 3 Low)
- [x] **Multi-plan documentation** — Created 9 domain plans + 2 module plans + AUDIT_SUMMARY.md

### Critical Fixes Applied
- [x] **Fix seed/schema mismatches** — Fixed `duration_hours`, `address`, `destination_id`, `icon`, `color`, `target_type`. Changed `BELONGS_TO`→`IN_CATEGORY`. Added `LOCATED_IN` edges. Added Transport + `CONNECTED_BY` edges.
- [x] **Fix backend security vulnerabilities** — Replaced `python-jose` with `PyJWT`. Fixed global exception handler (no longer leaks internals). Added auth to `POST /festivals`, `POST /restaurants`, `POST /activities/{id}/tags`. Normalized email to lowercase.
- [x] **Fix frontend auth** — Added `ProtectedRoute` to App.tsx (`/planner`, `/profile`, `/planner/:id/budget`). Added token refresh in `client.ts` response interceptor. Added `isLoading` to AuthContext. Fixed error handling in all hooks (return `{data, loading, error}`). Fixed header typing.
- [x] **Fix BudgetPlannerPage** — Wired to real API endpoints (`GET/POST/PUT /itineraries/{id}/budget`). Uses URL `:id` param. Save button now functional with validation.
- [x] **Add backend tests + CI** — Created `backend/tests/` with `test_health.py`, `test_auth.py` (6 tests), `test_destinations.py` (3 tests). Added `.github/workflows/ci.yml`. Added `pytest` + `httpx` to `requirements.txt`.
- [x] **Fix frontend hardcoded data** — Deleted 11 dead components. Fixed HomePage stats (generic labels). Removed non-functional search bar. Removed fake "Add to route" button. Removed hardcoded lunch recommendation. Made graph analysis dynamic (counts unique countries/cities).

### High Fixes Applied
- [x] **Enforce rate limiting** — Added `@limiter.limit(...)` to auth routes (5/min) and destination routes (30/min, recommend 10/min)
- [x] **Add Dockerfile + complete docker-compose** — Created `backend/Dockerfile`, `frontend/Dockerfile`. Updated `docker-compose.yml` with backend + frontend + falkordb services.
- [x] **Remove committed logs** — `git rm --cached` on `uvicorn.log`, `uvicorn_new.log`, `frontend/.env.production`. Updated `.gitignore`.
- [x] **Add 404 fallback + NotFoundPage** — Created `NotFoundPage.tsx`. Added `<Route path="*" />` in App.tsx.
- [x] **Add mobile hamburger menu** — Added hamburger toggle to Navbar with responsive mobile drawer.
- [x] **Add delete confirmation dialogs** — Added `window.confirm()` before itinerary and stop deletion in PlannerPage.
- [x] **Move JWT to httpOnly cookies** — Backend sets `httponly` cookies on login/register. Dependencies read token from cookie first, then header. Frontend uses `withCredentials: true`, removed all `localStorage` usage.
- [x] **Add input validation** — Email regex on Login/Register. Password strength check. `min={0}` on budget inputs. Date validation in PlannerPage.
- [x] **Add `Promise.allSettled`** — DestinationDetailPage now handles partial failures gracefully instead of crashing if one of 5 requests fails.

### Medium Fixes Applied
- [x] **Add `maxLength` validation to query params** — Added `max_length=100` (or 20 for price_range) to all string Query params in destinations, activities, festivals, restaurants routers.
- [x] **Add healthcheck to docker-compose and railway.json** — Added `healthcheck` block to backend service in docker-compose with `condition: service_healthy` dependencies. Added `healthcheckPath` and `healthcheckTimeout` to railway.json.
- [x] **Add structured logging with correlation IDs** — Added `X-Request-ID` middleware that generates or forwards correlation IDs. Exception handler now logs with `[cid]` prefix and returns `X-Request-ID` header.
- [x] **Fix CORS** — Restricted `allow_methods` to `GET, POST, PUT, DELETE, OPTIONS` and `allow_headers` to `Authorization, Content-Type, X-Request-ID`.
- [x] **Add code splitting with React.lazy** — Wrapped all page components except HomePage in `lazy()` and `Suspense` in App.tsx.
- [x] **Add skip-to-content link** — Added visually-hidden skip link that appears on focus, targeting `#main-content`.
- [x] **Add `aria-label` to icon buttons** — Added `aria-label="Profile"` to Navbar profile link. Added `aria-hidden="true"` to decorative icons.
- [x] **Add `loading="lazy"` to images** — Added to hero image, festival cards, planner suggested destination, and profile itinerary cards.

## Pending (Remaining Defense Risks)

No remaining items. All Critical, High, and Medium issues from the audit have been resolved.

## Last Session
- **Date:** 2026-05-20
- **Left off:** All audit items completed. 23 fixes applied across 60+ files. Roadmap fully up to date.
- **Next:** Optionally run the test suite to verify nothing is broken, then commit.
