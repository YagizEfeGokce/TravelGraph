---
version: 1.0.0
last_updated: 2026-05-20
domain: data-model
scope: root
---

# Data Model Plan

## Database

**Engine:** FalkorDB (Redis protocol, sparse matrix adjacency representation)
**Connection:** Host/port/graph name from environment variables
**Client:** `falkordb==1.0.9` Python driver

## Node Labels

| Label | Key Properties | Optional Properties |
|-------|---------------|---------------------|
| `User` | id (uuid), email, name, password_hash | created_at |
| `Destination` | id (uuid), name, country, description | lat, lng, avg_rating |
| `Activity` | id (uuid), name, description, duration_hours, price | address |
| `Accommodation` | id (uuid), name, type, star_rating, price_per_night | address |
| `Transport` | id (uuid), type, provider, duration_hours, price | departure_city, arrival_city |
| `Restaurant` | id (uuid), name, cuisine_type, price_range | address, rating |
| `Festival` | id (uuid), name, description, start_date, end_date | is_recurring, ticket_price |
| `Itinerary` | id (uuid), title, start_date, end_date, is_public | created_at |
| `ItineraryStop` | id (uuid), day_number, order | notes |
| `BudgetPlan` | id (uuid), total_budget, currency | hotel_budget, food_budget, transport_budget, activity_budget |
| `Review` | id (uuid), target_type, rating, comment | created_at |
| `Season` | id (uuid), name, months, avg_temp_c | weather_description |
| `Category` | id (uuid), name | icon, description |
| `Tag` | id (uuid), name | color |

## Relationship Types

| Relationship | From | To | Description |
|--------------|------|----|-------------|
| `VISITED` | User | Destination | User has visited this destination |
| `CREATED` | User | Itinerary | User created this itinerary |
| `WROTE` | User | Review | User wrote this review |
| `LOCATED_IN` | Activity/Accommodation/Restaurant/Festival | Destination | Entity is in this city |
| `HAS_ACTIVITY` | Destination | Activity | Destination has this activity |
| `HAS_RESTAURANT` | Destination | Restaurant | Destination has this restaurant |
| `HAS_FESTIVAL` | Destination | Festival | Destination has this festival |
| `HAS_STOP` | Itinerary | ItineraryStop | Itinerary contains this stop |
| `AT` | ItineraryStop | Destination | Stop is at this destination |
| `HAS_BUDGET` | Itinerary | BudgetPlan | Itinerary has this budget |
| `IN_CATEGORY` | Activity/Restaurant | Category | Entity belongs to this category |
| `HAS_SEASON` | Activity/Festival/Destination | Season | Applicable season |
| `BEST_IN` | Destination | Season | Destination is best visited in this season |
| `TAGGED_WITH` | Activity/Destination | Tag | Entity has this tag |
| `ABOUT` | Review | Activity/Accommodation/Restaurant | Review targets this entity |
| `CONNECTED_BY` | Destination | Transport | Two-way connection via transport |

## Indexing Strategy

| Property | Index Type | Purpose |
|----------|-----------|---------|
| `User.email` | Exact match | Login lookup |
| `User.id` | Exact match | Auth dependency |
| `Destination.id` | Exact match | CRUD lookups |
| `Destination.name` | Exact match | Seed lookups, route queries |

**Issue:** Only 4 indexes exist. No indexes on `Activity.name`, `Festival.start_date`, `Review.target_id`, etc. Large datasets will suffer.

## Seeding Strategy

Current seed (`backend/db/seed.py`) creates:
- 3 Category nodes
- 4 Season nodes
- 6 Tag nodes
- 30 Destination nodes (Turkish cities)
- ~90 Activity nodes (3 per city, city-specific)
- ~60 Restaurant nodes (2 per city)
- ~60 Accommodation nodes (2 per city)
- 30 Festival nodes (1 per city, real festivals)
- 5 User nodes
- ~20 VISITED edges
- 15 Review nodes
- 20 Transport nodes with CONNECTED_BY edges

**Seeding order** (dependencies first):
1. Categories → Seasons → Tags
2. Destinations → BEST_IN → Seasons
3. Activities → LOCATED_IN → Destinations → IN_CATEGORY → Categories
4. Restaurants → LOCATED_IN → Destinations → IN_CATEGORY → Categories
5. Accommodations → LOCATED_IN → Destinations
6. Festivals → LOCATED_IN → Destinations → HAS_SEASON → Seasons
7. Users
8. Itineraries → CREATED → Users
9. BudgetPlans → HAS_BUDGET → Itineraries
10. Reviews → WROTE → Users, ABOUT → targets
11. Transport → CONNECTED_BY → Destinations

## Data Integrity Rules

1. **Email uniqueness:** Must be enforced at application layer; FalkorDB does not enforce unique constraints natively.
2. **One review per user per target:** Must be checked before creation.
3. **Budget line items ≤ total_budget:** Enforced by Pydantic `model_validator`.
4. **start_date < end_date:** Enforced by Pydantic `model_validator` for Itinerary and Festival.
5. **Foreign key references:** No FK constraints in graph DB; application must verify target exists before creating relationships.
