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
3. **Token Usage** — Access token in `Authorization: Bearer <token>` header (60 min expiry)
4. **Token Refresh** — `/api/auth/refresh` with refresh_token → new access_token issued (no DB verification)
5. **Storage** — Both tokens stored in `localStorage` (frontend) — **CRITICAL VULNERABILITY**

## Current Threat Model

### What We Protect
- User accounts (email, password_hash, itineraries, reviews)
- Destination/activity data (public read, restricted write)
- Graph integrity (relationships between entities)

### Attack Vectors

| Vector | Risk | Status |
|--------|------|--------|
| JWT secret brute-force | Medium | Secret is env-based but example is weak |
| XSS stealing tokens from localStorage | **High** | Tokens in localStorage = trivial XSS exploit |
| CSRF via permissive CORS | **Medium** | `allow_methods=["*"]`, `allow_headers=["*"]` |
| Brute-force login | **High** | Rate limiting configured but NOT enforced |
| Unauthenticated writes | **High** | POST /festivals, POST /restaurants, POST /tags have no auth |
| Algorithm confusion (CVE) | **Critical** | python-jose has known CVEs for key confusion |
| Exception detail leakage | **Medium** | Global handler returns `str(exc)` to clients |
| SQL/Cypher injection | Low | All Cypher queries are parameterized (no f-strings) |
| Session fixation | Medium | No session binding to IP or device fingerprint |
| Token revocation | Medium | No logout endpoint; tokens live until expiry |

## Known Vulnerabilities (Prioritized)

### Critical
1. **python-jose CVEs** — `python-jose==3.3.0` is unmaintained with published CVEs for algorithm confusion and key confusion attacks.
2. **Unauthenticated data mutation** — `POST /festivals`, `POST /restaurants`, `POST /activities/{id}/tags` allow anonymous graph writes.
3. **No rate limiting enforcement** — slowapi instantiated but zero routes use `@limiter.limit(...)`.

### High
4. **localStorage token storage** — Access and refresh tokens in `localStorage` are vulnerable to XSS extraction.
5. **Exception detail leakage** — `main.py` global handler returns `{"detail": str(exc), "type": type(exc).__name__}` exposing internal implementation.
6. **Refresh token does not verify user existence** — Deleted/banned users can refresh forever.
7. **Race condition: duplicate email** — Read-then-write pattern allows concurrent duplicate registrations.
8. **CORS overly permissive** — `allow_methods=["*"]` and `allow_headers=["*"]` with `allow_credentials=True`.

### Medium
9. **No input sanitization** — Strings not stripped; whitespace-only names accepted.
10. **No maximum lengths** — Description fields, query params unbounded.
11. **No role-based access control** — Any authenticated user can create global content.
12. **Email not normalized** — `User@Example.com` and `user@example.com` are separate accounts.
13. **Weak example JWT secret** — `.env.example` has placeholder inviting copy-paste deployment.

## Fix Roadmap

| Priority | Fix | Effort |
|----------|-----|--------|
| P0 | Replace `python-jose` with `PyJWT>=2.8.0` | Small |
| P0 | Add `@limiter.limit(...)` to auth and graph routes | Small |
| P0 | Add `Depends(get_current_user)` to POST /festivals, POST /restaurants, POST /tags | Small |
| P1 | Move tokens from localStorage to httpOnly cookies | Medium |
| P1 | Fix global exception handler to return generic messages | Small |
| P1 | Verify user exists in refresh endpoint | Small |
| P1 | Normalize email to lowercase before storage/lookup | Small |
| P2 | Restrict CORS to exact origins and methods | Small |
| P2 | Add `max_length` validators to all text fields | Small |
| P2 | Add `role` field to User and admin checks | Medium |
