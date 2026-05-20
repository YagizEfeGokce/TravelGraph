---
version: 1.0.0
last_updated: 2026-05-20
domain: api
scope: module
module: backend
---

# Backend API Module Plan

## Backend-Specific Endpoint Issues

### Seed/Schema Mismatches (CRITICAL)

| Seed Property | Model Expectation | Status |
|---------------|-------------------|--------|
| `duration_minutes` | `duration_hours` | **Crash on GET /activities** |
| Missing `address` | `address: str` | **Crash on ActivityResponse** |
| Missing `destination_id` | `destination_id: str` | **Crash on ActivityResponse** |
| Missing `icon` | `icon: str` | **Crash on CategoryResponse** |
| Missing `color` | `color: str` | **Crash on TagResponse** |
| `target_type: 'mixed'` | `Literal["activity","accommodation","restaurant"]` | **Validation fails** |

### Cypher Relationship Mismatches (CRITICAL)

| Seed Creates | Queries Search | Feature Affected |
|--------------|----------------|------------------|
| `BELONGS_TO` | `IN_CATEGORY` | Activity category filter |
| `HAS_ACTIVITY` | `LOCATED_IN` (Activity→Destination) | Recommendations, route finding |
| `HAS_TAG` (relationship) | `a.tags` (property) | Tag filtering |
| `WROTE`/`ABOUT` (Review) | `RATES` (Rating node) | Average rating calculation |
| `CONNECTED_BY` (Transport) | Nothing seeded | Route finding always empty |

**Fix:** Unify all relationship names. The canonical set should be:
- `IN_CATEGORY` (not `BELONGS_TO`)
- `LOCATED_IN` (Activity→Destination)
- `HAS_TAG` (relationship, not property)
- `ABOUT` (Review→target) with `avg(r.rating)`
- `CONNECTED_BY` (seed Transport nodes)

### Missing CRUD Endpoints

| Entity | Missing Operation | Impact |
|--------|-------------------|--------|
| User | PUT /users/{id}, DELETE /users/{id} | Cannot update profile or delete account |
| Transport | All CRUD | Model exists but no router |
| Itinerary | PUT /itineraries/{id} | Cannot edit title/dates/visibility |
| ItineraryStop | PUT notes | Cannot edit stop notes |
| Destination | PUT /destinations/{id} | Cannot update destination info |
| Activity | PUT /activities/{id} | Cannot update activity info |
| Restaurant | PUT /restaurants/{id} | Cannot update restaurant info |
| Festival | PUT /festivals/{id} | Cannot update festival info |

### Duplicate Route Registration

`festivals.py` and `restaurants.py` both register `GET /destinations/{id}/festivals` and `GET /destinations/{id}/restaurants`, shadowing the routes in `destinations.py`.

**Fix:** Remove duplicate sub-resource routes from `festivals.py` and `restaurants.py`.

### Backend-Specific Auth Gaps

- `users.py` router registered but **completely empty** — no endpoints at all.
- No admin role check on any write endpoint.
- No password change endpoint.
- No email verification.
- No logout/token revocation.
