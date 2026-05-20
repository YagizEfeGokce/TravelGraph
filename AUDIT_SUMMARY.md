# TravelGraph Audit Summary

**Date:** 2026-05-20
**Audited by:** 3 parallel subagents (Backend, Frontend, Security/Deployment)

---

## Executive Summary

The project has a polished visual layer but **severe engineering deficiencies** underneath. Multiple core "graph-powered" features are **completely non-functional** due to seed data / query mismatches. Several features are **fake UI** with no backend integration. Security and deployment configs have critical gaps. **Zero automated tests exist.**

A professor will immediately attack:
1. Seed data contradicts API schemas → runtime crashes on basic reads
2. Graph queries reference relationships that don't exist → "graph intelligence" is an illusion
3. Zero tests → no evidence anything works
4. Unauthenticated POST endpoints → anyone can mutate the database
5. Vulnerable JWT library → known CVEs

---

## Issue Count by Severity

| Severity | Backend | Frontend | Security/Deployment | Total |
|----------|---------|----------|---------------------|-------|
| **Critical** | 14 | 4 | 3 | **21** |
| **High** | 14 | 16 | 5 | **35** |
| **Medium** | 18 | 22 | 10 | **50** |
| **Low** | 9 | 8 | 3 | **20** |
| **Total** | 55 | 50 | 21 | **126** |

---

## Top 10 Critical Issues

| # | Issue | Location | Impact |
|---|-------|----------|--------|
| 1 | **Seed/schema property mismatch** — `duration_minutes` vs `duration_hours`, missing `address`, missing `destination_id` | `backend/db/seed.py` + `backend/models/activity.py` | `GET /api/activities` crashes with `KeyError` |
| 2 | **Cypher relationship mismatch** — Seed creates `BELONGS_TO`, queries search `IN_CATEGORY` | `backend/db/seed.py` + routers | Category filtering completely broken |
| 3 | **Cypher relationship mismatch** — Seed creates `HAS_ACTIVITY`, queries search `LOCATED_IN` (reverse direction) | `backend/db/seed.py` + `services/recommendation.py` | Recommendations completely broken |
| 4 | **Average rating queries non-existent `:Rating` nodes** | `backend/routers/destinations.py` | `avg_rating` always `None` |
| 5 | **Shortest-path routing has zero edges** — No `CONNECTED_BY` seeded | `backend/db/seed.py` + `services/recommendation.py` | Route finding always returns empty |
| 6 | **python-jose has known CVEs** | `backend/requirements.txt` + `core/security.py` | Algorithm confusion attack possible |
| 7 | **Unauthenticated POST endpoints** | `festivals.py`, `restaurants.py`, `tags_categories.py` | Anyone can create festivals, restaurants, tags |
| 8 | **Budget Planner page is 100% fake** | `frontend/src/pages/BudgetPlannerPage.tsx` | No API calls; Save button is a no-op |
| 9 | **ProtectedRoute exists but is never used** | `frontend/src/components/ProtectedRoute.tsx` + `App.tsx` | All routes accessible without auth |
| 10 | **Zero automated tests** | Entire repo | No evidence the code works |

---

## Completely Broken Features

### Backend
- Activity category filtering (`BELONGS_TO` vs `IN_CATEGORY`)
- Activity tag filtering (`a.tags` property vs `HAS_TAG` relationship)
- Destination average rating (`:Rating` node doesn't exist)
- Destination `min_rating` filter (undefined property)
- Collaborative filtering recommendations (`LOCATED_IN` mismatch)
- Budget-aware recommendations (`LOCATED_IN` mismatch)
- Route finding (`CONNECTED_BY` edges never seeded)
- `users.py` router is completely empty
- Transport model exists but no router/seed

### Frontend
- Budget Planner (no API integration)
- Token refresh (refresh_token received but never used)
- Search in Planner (decorative input)
- "Add to route" on Festivals (decorative button)
- Recommendations UI (`useRecommendations` hook never imported)
- Lunch Recommendation (hardcoded text)
- Currency Preference (local state only)
- AI Insight Slider (placebo)

---

## Security Quick Wins

| Fix | Effort |
|-----|--------|
| Replace `python-jose` with `PyJWT` | 15 min |
| Add `@limiter.limit(...)` to auth routes | 15 min |
| Add `Depends(get_current_user)` to POST /festivals, POST /restaurants | 15 min |
| Fix global exception handler (return generic message) | 10 min |
| Normalize email to lowercase | 10 min |

---

## Plans Created

All findings are documented in the [`plans/`](plans/) directory:

- `plans/roadmap.md` — Prioritized fix list
- `plans/architecture.md` — System overview + architectural issues
- `plans/api.md` — Endpoint inventory + rate limiting gaps
- `plans/business-logic.md` — Domain rules + broken workflows
- `plans/data-model.md` — FalkorDB schema + indexing
- `plans/security.md` — Vulnerabilities + threat model
- `plans/ui-ux.md` — Design system + accessibility gaps
- `plans/deployment.md` — Infrastructure + missing CI/CD
- `plans/testing.md` — Test strategy + CI pipeline

Module-specific plans:
- `plans/modules/backend/api.md` — Backend Cypher alignment + missing endpoints
- `plans/modules/frontend/ui-ux.md` — Frontend broken features + dead components
