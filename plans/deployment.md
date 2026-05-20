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
- **docker-compose.yml:** Only defines `falkordb` service
- **Missing:** Backend Dockerfile, frontend service, health checks

## Known Deployment Issues

### Critical
1. **No backend Dockerfile** — `docker-compose.yml` only runs FalkorDB. Application is not containerized.
2. **Procfile path assumption** — `uvicorn main:app` assumes `main.py` is in cwd, but it lives in `backend/`. Deployment may fail.

### High
3. **No CI/CD pipeline** — Zero `.github/workflows/`. Every deploy is manual.
4. **No health checks** — Docker and Railway have no healthcheck endpoints configured.
5. **Production logs committed** — `uvicorn.log`, `uvicorn_new.log` in git history.

### Medium
6. **`.env.production` committed** — Production URL exposed in repository.
7. **No security headers** — Vercel config lacks CSP, HSTS, X-Frame-Options.
8. **Restart policy too weak** — `ON_FAILURE` with max 3 retries gives up permanently.

## Required Fixes

| Fix | Priority | Details |
|-----|----------|---------|
| Add backend Dockerfile | **Critical** | Python 3.11-slim, copy requirements, run uvicorn |
| Complete docker-compose.yml | **Critical** | Add backend service, frontend service, health checks |
| Fix Procfile/railway.json path | **Critical** | Ensure `main.py` resolves correctly at runtime |
| Add GitHub Actions CI/CD | **High** | pytest, ruff, ESLint, build on PR |
| Add health checks | **High** | Docker `HEALTHCHECK`, Railway `healthcheckPath` |
| Purge committed logs | **High** | `git rm --cached`, add `*.log` to `.gitignore` |
| Remove `.env.production` from git | **High** | Inject via Vercel dashboard |
| Add security headers | **Medium** | CSP, HSTS, X-Frame-Options in vercel.json |
| Fix restart policy | **Medium** | Use `ALWAYS` or `UNLESS_STOPPED` |

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
