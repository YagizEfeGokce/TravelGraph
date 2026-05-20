---
version: 1.0.0
last_updated: 2026-05-20
domain: testing
scope: root
---

# Testing Plan

## Current State

**Zero automated tests exist.**

- No backend unit tests (pytest)
- No backend integration tests (httpx / TestClient)
- No frontend unit tests (Vitest / Jest)
- No frontend component tests
- No end-to-end tests (Playwright / Cypress)
- Only manual testing file: `backend/api_test.http`

## Why This Matters for Defense

A professor will ask: "How do you know your code works?" The only answer currently is "I manually tested it." That is insufficient for any software engineering project.

## Test Pyramid Strategy

### Layer 1: Unit Tests (Fast, Isolated)

**Backend:**
- `pytest` + `pytest-asyncio`
- Test every Pydantic model validator
- Test `core/security.py` (hash, verify, encode, decode)
- Test `core/dependencies.py` (token extraction, user lookup)
- Test Cypher query builders (if extracted from routers)

**Frontend:**
- `vitest` (already in Vite ecosystem)
- Test auth context (login, logout, token refresh)
- Test hooks (loading states, error states, data transformation)
- Test utility functions (formatting, validation)

### Layer 2: Integration Tests (API Contract Validation)

**Backend:**
- `httpx` or FastAPI `TestClient`
- Test every endpoint:
  - Auth: register, login, refresh, me
  - Destinations: CRUD, filters, recommendations
  - Itineraries: CRUD, stops, reorder
  - Reviews: create, duplicate check, delete
  - Budget: create, get, update
- Test auth requirements (public vs protected)
- Test error responses (404, 409, 403, 422)

**Target:** 30+ integration tests covering all routers.

### Layer 3: E2E Tests (User Journey Validation)

**Tool:** Playwright

**Scenarios:**
1. User registers → logs in → views destinations → creates itinerary → adds stop
2. User searches festivals → filters by season → views festival details
3. User views destination → sees activities → writes review
4. Unauthenticated user tries to access protected route → redirected to login
5. Budget planner: create budget → verify total matches line items

**Target:** 5-10 critical user journeys.

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
name: CI
on: [push, pull_request]
jobs:
  backend-tests:
    runs-on: ubuntu-latest
    services:
      falkordb:
        image: falkordb/falkordb:latest
        ports: [6379:6379]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r backend/requirements.txt pytest pytest-asyncio httpx
      - run: pytest backend/tests/ -v
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: cd frontend && npm ci
      - run: cd frontend && npm run test
      - run: cd frontend && npm run build
```

## Linting and Type Checking

| Tool | Scope | Config File |
|------|-------|-------------|
| ruff | Python formatting + linting | `pyproject.toml` |
| mypy | Python type checking | `pyproject.toml` |
| ESLint | TypeScript/React linting | `eslint.config.js` |
| TypeScript compiler | Frontend type checking | `tsconfig.json` |

## Fixtures and Test Data

**Backend:**
- Reuse `backend/db/seed.py` data or create a minimal `conftest.py` fixture
- Use `TestClient` with overridden `get_db()` dependency pointing to test graph
- Clear graph before each test with `MATCH (n) DETACH DELETE n`

**Frontend:**
- Mock API responses with `msw` (Mock Service Worker)
- Test with known user/token states

## Testing Roadmap

| Phase | Deliverable | Effort |
|-------|-------------|--------|
| 1 | Add pytest + TestClient, test auth endpoints | 2 hours |
| 2 | Add tests for all routers | 4 hours |
| 3 | Add GitHub Actions CI | 1 hour |
| 4 | Add Vitest + test auth context | 2 hours |
| 5 | Add Playwright E2E for 3 critical journeys | 3 hours |
| 6 | Add linting configs (ruff, mypy, ESLint) | 1 hour |
