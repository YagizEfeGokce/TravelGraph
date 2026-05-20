---
version: 1.0.0
last_updated: 2026-05-20
domain: api
scope: root
---

# API Plan

## Endpoint Inventory

### Auth (`/api/auth`)
| Method | Path | Auth | Status |
|--------|------|------|--------|
| POST | `/register` | Public | Working |
| POST | `/login` | Public | Working |
| POST | `/refresh` | Public | Working |
| GET | `/me` | Bearer | Working |

### Destinations (`/api/destinations`)
| Method | Path | Auth | Status |
|--------|------|------|--------|
| GET | `/` | Optional | Working |
| GET | `/{id}` | Optional | Working |
| GET | `/{id}/activities` | Optional | Working |
| GET | `/{id}/accommodations` | Optional | Working |
| GET | `/{id}/restaurants` | Optional | Working |
| GET | `/{id}/festivals` | Optional | Working |
| GET | `/{id}/recommend` | Optional | Working |
| POST | `/` | Bearer | Working |

### Activities (`/api/activities`)
| Method | Path | Auth | Status |
|--------|------|------|--------|
| GET | `/` | Optional | Working |
| POST | `/` | Bearer | Working |

### Restaurants (`/api/restaurants`)
| Method | Path | Auth | Status |
|--------|------|------|--------|
| GET | `/` | Optional | Working |
| GET | `/destinations/{id}/restaurants` | Optional | Working |
| POST | `/` | Bearer | **FIXED** |

### Festivals (`/api/festivals`)
| Method | Path | Auth | Status |
|--------|------|------|--------|
| GET | `/` | Optional | Working |
| GET | `/destinations/{id}/festivals` | Optional | Working |
| POST | `/` | Bearer | **FIXED** |

### Tags & Categories (`/api/tags`, `/api/categories`)
| Method | Path | Auth | Status |
|--------|------|------|--------|
| GET | `/tags` | Optional | Working |
| POST | `/tags` | Bearer | Working |
| POST | `/activities/{id}/tags` | Bearer | **FIXED** |
| DELETE | `/activities/{id}/tags/{tag_id}` | Bearer | Working |
| GET | `/categories` | Optional | Working |
| GET | `/categories/{id}/activities` | Optional | Working |

### Seasons (`/api/seasons`)
| Method | Path | Auth | Status |
|--------|------|------|--------|
| GET | `/` | Optional | Working |
| GET | `/destinations/{id}/seasons` | Optional | Working |

### Itineraries (`/api/itineraries`)
| Method | Path | Auth | Status |
|--------|------|------|--------|
| POST | `/` | Bearer | Working |
| GET | `/` | Bearer | Working |
| GET | `/{id}` | Bearer / Public | Working |
| DELETE | `/{id}` | Bearer | Working |
| POST | `/{id}/stops` | Bearer | Working |
| GET | `/{id}/stops` | Optional | Working |
| DELETE | `/{id}/stops/{stop_id}` | Bearer | Working |
| PUT | `/{id}/stops/{stop_id}/reorder` | Bearer | Working |

### Budget (`/api/itineraries/{id}/budget`)
| Method | Path | Auth | Status |
|--------|------|------|--------|
| POST | `/` | Bearer | Working |
| GET | `/` | Bearer | Working |
| PUT | `/` | Bearer | Working |

### Reviews (`/api/reviews`)
| Method | Path | Auth | Status |
|--------|------|------|--------|
| POST | `/` | Bearer | Working |
| GET | `/` | Optional | Working |
| DELETE | `/{id}` | Bearer | Working |

### Route
| Method | Path | Auth | Status |
|--------|------|------|--------|
| GET | `/api/destinations/route` | Optional | Working |

## Auth Contract

### Token Format
```
Authorization: Bearer <eyJhbGciOiJIUzI1NiIs...>
```

### Response Shape (Login / Register)
```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "bearer",
  "user": { "id": "uuid", "email": "...", "name": "...", "created_at": "..." }
}
```

## Rate Limiting Policy

| Route Group | Limit | Current Status |
|-------------|-------|----------------|
| Auth (register, login) | 5 / minute | **ENFORCED** |
| Auth (refresh, me) | 30 / minute | **ENFORCED** |
| Graph queries (recommend, route) | 10 / minute | **ENFORCED** |
| General read | 60 / minute | Default active |

**FIXED:** `@limiter.limit(...)` decorators applied to auth routes (5/min) and destination routes (30/min, recommend 10/min).

## Known API Issues

1. ~~**Unauthenticated POST endpoints**~~ — **FIXED** All POST endpoints now require `get_current_user`
2. **No pagination** — `GET /destinations`, `GET /activities` return unbounded lists. **PENDING**
3. **No versioning** — API URL is `/api` with no version prefix. **PENDING**
4. **No OpenAPI tags** — Swagger UI groups all endpoints under "default". **PENDING**
5. ~~**Error responses leak internals**~~ — **FIXED** Global handler returns generic `"Internal server error"`
