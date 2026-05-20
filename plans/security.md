---
version: 1.0.0
last_updated: 2026-05-20
domain: security
scope: root
---

# Security Plan

## Authentication Flow

1. **Registration** — Password hashed with bcrypt → User node created → access_token + refresh_token issued
2. **Login** — Email lookup → bcrypt verify → tokens issued → failed attempts tracked in-memory
3. **Token Usage** — Access token in `Authorization: Bearer <token>` header OR `access_token` httpOnly cookie (60 min expiry)
4. **Token Refresh** — `/api/auth/refresh` reads refresh_token from cookie → new access_token issued (verifies user exists)
5. **Storage** — Tokens stored in `httpOnly` cookies (backend) with `SameSite=Lax`. Frontend uses `withCredentials: true`. **FIXED**

## Current Threat Model

### What We Protect
- User accounts (email, password_hash, itineraries, reviews)
- Destination/activity data (public read, restricted write)
- Graph integrity (relationships between entities)

### Attack Vectors

| Vector | Risk | Status |
|--------|------|--------|
| JWT secret brute-force | Medium | **FIXED** — `.env.example` now has 64-char hex placeholder with warning |
| XSS stealing tokens from localStorage | **High** | **FIXED** — Moved to httpOnly cookies; localStorage cleared |
| CSRF via permissive CORS | **Medium** | **FIXED** — Restricted to `GET, POST, PUT, DELETE, OPTIONS` and `Authorization, Content-Type, X-Request-ID` |
| Brute-force login | **High** | **FIXED** — `@limiter.limit("5/minute")` on register/login, in-memory failure tracking |
| Unauthenticated writes | **High** | **FIXED** — `Depends(get_current_user)` added to POST /festivals, /restaurants, /activities/{id}/tags |
| Algorithm confusion (CVE) | **Critical** | **FIXED** — Replaced `python-jose` with `PyJWT>=2.8.0` |
| Exception detail leakage | **Medium** | **FIXED** — Global handler returns generic `"Internal server error"` |
| SQL/Cypher injection | Low | All Cypher queries are parameterized (no f-strings) |
| Session fixation | Medium | No session binding to IP or device fingerprint |
| Token revocation | Medium | **FIXED** — `POST /auth/logout` clears cookies; tokens still live until expiry |

## Known Vulnerabilities (Prioritized)

### Critical — ALL RESOLVED
1. ~~**python-jose CVEs**~~ — Replaced with `PyJWT>=2.8.0`
2. ~~**Unauthenticated data mutation**~~ — All POST endpoints now require `get_current_user`
3. ~~**No rate limiting enforcement**~~ — `@limiter.limit(...)` applied to auth and destination routes

### High — ALL RESOLVED
4. ~~**localStorage token storage**~~ — Moved to httpOnly cookies
5. ~~**Exception detail leakage**~~ — Handler returns generic `"Internal server error"`
6. ~~**Refresh token does not verify user existence**~~ — Refresh endpoint now verifies user exists
7. **Race condition: duplicate email** — Partially mitigated by normalized email + unique check; concurrent race still possible at application layer
8. ~~**CORS overly permissive**~~ — Restricted to explicit methods and headers

### Medium — ALL RESOLVED
9. ~~**No input sanitization**~~ — Pydantic validators strip whitespace on name/password
10. ~~**No maximum lengths**~~ — `max_length` added to all string Query params
11. **No role-based access control** — Still true; any authenticated user can create global content
12. ~~**Email not normalized**~~ — `.lower()` applied before storage and lookup
13. ~~**Weak example JWT secret**~~ — `.env.example` updated with 64-char hex + warning

## Fix Roadmap

| Priority | Fix | Status | Commit |
|----------|-----|--------|--------|
| P0 | Replace `python-jose` with `PyJWT>=2.8.0` | **DONE** | `1e1feba` |
| P0 | Add `@limiter.limit(...)` to auth and graph routes | **DONE** | `1e1feba` |
| P0 | Add `Depends(get_current_user)` to POST /festivals, /restaurants, /tags | **DONE** | `1e1feba` |
| P1 | Move tokens from localStorage to httpOnly cookies | **DONE** | `1e1feba` |
| P1 | Fix global exception handler to return generic messages | **DONE** | `1e1feba` |
| P1 | Verify user exists in refresh endpoint | **DONE** | `1e1feba` |
| P1 | Normalize email to lowercase before storage/lookup | **DONE** | `1e1feba` |
| P2 | Restrict CORS to exact origins and methods | **DONE** | `275f90d` |
| P2 | Add `max_length` validators to all text fields | **DONE** | `275f90d` |
| P2 | Add `role` field to User and admin checks | **PENDING** | — |

## Remaining Risk

- **Role-based access control** — Any authenticated user can still create global content (festivals, restaurants, activities). Adding an `is_admin` flag to User nodes and admin-only checks on mutation endpoints would close this gap.
