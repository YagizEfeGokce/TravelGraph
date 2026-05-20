---
version: 1.0.0
last_updated: 2026-05-20
domain: deployment
scope: root
---

# Deployment Plan

## Current Infrastructure

| Component | Platform | URL |
|-----------|----------|-----|
| Frontend | Vercel | https://travel-graph.vercel.app |
| Backend API | Railway | https://travelgraph-production-069c.up.railway.app |
| Graph Database | Railway (internal) | railway.internal |

## Deployment Configurations

### Railway (Backend)
- **Procfile:** `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
- **railway.json:** Start command override with `ON_FAILURE` restart policy
- **Environment:** Railway Variables for DB host, JWT secret, CORS origins

### Vercel (Frontend)
- **vercel.json:** SPA rewrite (`/(.+)`) to `index.html`
- **Environment:** `VITE_API_URL` pointing to Railway backend
- **Build:** `npm run build` → static output

### Docker (Local Development)
- **docker-compose.yml:** Defines `falkordb`, `backend`, and `frontend` services with health checks
- **backend/Dockerfile:** Python 3.11-slim, requirements copied, uvicorn on port 8000
- **frontend/Dockerfile:** Node 20-alpine, dev server on port 5173

## Deployment Issues — ALL RESOLVED

### Critical — RESOLVED
1. ~~**No backend Dockerfile**~~ — Created `backend/Dockerfile` and `frontend/Dockerfile`
2. ~~**Procfile path assumption**~~ — Railway uses `startCommand` in `railway.json`; working directory is repo root

### High — RESOLVED
3. ~~**No CI/CD pipeline**~~ — `.github/workflows/ci.yml` added with pytest on PR/push
4. ~~**No health checks**~~ — Docker `healthcheck` block added; Railway `healthcheckPath` added
5. ~~**Production logs committed**~~ — `git rm --cached` applied; `*.log` in `.gitignore`

### Medium — RESOLVED
6. ~~**`.env.production` committed**~~ — Removed from git; added to `.gitignore`
7. **No security headers** — Still open — Vercel config lacks CSP, HSTS, X-Frame-Options
8. ~~**Restart policy too weak**~~ — `ON_FAILURE` with 3 retries is acceptable for Railway free tier

## Required Fixes — Status

| Fix | Priority | Status | Commit |
|-----|----------|--------|--------|
| Add backend Dockerfile | **Critical** | **DONE** | `1e1feba` |
| Complete docker-compose.yml | **Critical** | **DONE** | `1e1feba` |
| Fix Procfile/railway.json path | **Critical** | **DONE** | `1e1feba` |
| Add GitHub Actions CI/CD | **High** | **DONE** | `1e1feba` |
| Add health checks | **High** | **DONE** | `275f90d` |
| Purge committed logs | **High** | **DONE** | `1e1feba` |
| Remove `.env.production` from git | **High** | **DONE** | `1e1feba` |
| Add security headers | **Medium** | **PENDING** | — |
| Fix restart policy | **Medium** | **N/A** | `1e1feba` |

## Environment Variables

### Backend (.env)
```
FALKORDB_HOST=localhost
FALKORDB_PORT=6379
FALKORDB_GRAPH=travelgraph
JWT_SECRET=<64-char hex random>
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
JWT_REFRESH_EXPIRE_DAYS=7
CORS_ORIGINS=http://localhost:5173,https://travel-graph.vercel.app
```

### Frontend (.env)
```
VITE_API_URL=https://travelgraph-production-069c.up.railway.app
```

**Note:** `backend/.env` and `frontend/.env.local` must be in `.gitignore`.
