---
version: 1.0.0
last_updated: 2026-05-20
domain: business-logic
scope: root
---

# Business Logic Plan

## Domain Entities (14 Types)

| Entity | Description | Key Rules |
|--------|-------------|-----------|
| User | Traveler / member | Email unique, password min 8 chars with 1 uppercase + 1 digit |
| Destination | City & country | lat ∈ [-90, 90], lng ∈ [-180, 180] |
| Itinerary | Travel plan | start_date < end_date, owned by User |
| ItineraryStop | Plan ↔ Stop bridge | day_number ≥ 1, order ≥ 1, notes max 500 chars |
| Activity | Tourist attractions | duration_hours > 0, price ≥ 0 |
| Accommodation | Hotel / hostel / apartment | star_rating 1-5, price_per_night > 0 |
| Transport | Flight / train / bus / ferry | Connects two destinations via CONNECTED_BY edges |
| Restaurant | Restaurant + cuisine | rating optional 1-5, price_range ∈ {budget, mid, luxury} |
| Festival | Event + date range | start_date < end_date, is_recurring flag |
| BudgetPlan | User budget + line items | Hotel + food + transport + activity ≤ total_budget, all ≥ 0 |
| Review | Comment & rating | rating 1-5, comment max 1000 chars, one review per user per target |
| Season | Weather & season info | name ∈ {Spring, Summer, Autumn, Winter}, months 1-12 |
| Category | Museum, Nature, Food... | M:N with Activity |
| Tag | Label & color | hex color code validated |

## Workflows

### User Registration
1. Validate `UserCreate` (email format, name length 2-50, password complexity)
2. Check email uniqueness via Cypher `MATCH (u:User {email: $email})`
3. Hash password with bcrypt
4. Create User node with `uuid4()` id and ISO timestamp
5. Issue access_token (60 min) and refresh_token (7 days)
6. Return `UserResponse` + tokens

### Destination Discovery
1. Optional auth injection (`get_optional_user`)
2. Parse query params: country, category, season, min_rating, limit
3. Build parameterized Cypher MATCH with optional filters
4. Calculate avg_rating from linked Review nodes
5. Return paginated list (currently unbounded — missing pagination)

### Recommendation Engine
**Input:** user_id (optional), current destination_id, max_price (optional), season (optional)

**Logic:**
1. If user_id provided:
   - Run collaborative filtering: find users who visited same destinations → recommend their other visits
   - Run budget-aware category matching: find destinations with overlapping categories, within budget
2. If no user_id:
   - Run diversity-based recommendation: destinations with most diverse activity categories
3. Exclude already-visited destinations with `NOT (u)-[:VISITED]->(d)`
4. Order by match score DESC, limit 5

**Current Issue:** The frontend `useRecommendations` hook exists but is **never used** in any page. The "Best Next Stop" in Planner is just `.find()` on the destination list.

### Itinerary Planning
1. Authenticated user creates Itinerary with title, dates, visibility
2. User adds ItineraryStops with destination, day, order, notes
3. Stops ordered by (day_number, order)
4. User can delete or reorder stops
5. Public itineraries viewable without auth

**Current Issue:** PlannerPage "Graph Analysis" shows hardcoded stats (`"Countries", 1`) regardless of actual data.

### Budget Planning
**Intended Flow:**
1. User creates BudgetPlan linked to an Itinerary
2. BudgetPlan has total_budget + 4 line items (hotel, food, transport, activity)
3. Sum of line items must not exceed total_budget
4. BudgetPlan is fetched and updated via API

**Current Issue:** BudgetPlannerPage is a **complete mockup**. It ignores the `:id` URL param, never calls `getBudget` or `createBudget`, and the "Save Budget" button has zero `onClick` handler.

### Review System
1. Authenticated user submits Review with target_id, target_type, rating, comment
2. Duplicate check: one review per user per target (409 Conflict)
3. Review linked to User via WROTE edge and to target via ABOUT edge
4. Reviews displayed on destination detail page

**Current Issue:** ReviewCard component exists but is never imported. Reviews are rendered inline in DestinationDetailPage.

## Known Broken Features

| Feature | Status | Evidence |
|---------|--------|----------|
| Budget Planner | **100% fake** | No API calls, no `onClick` on Save |
| Search in Planner | **Decorative only** | Input exists but no state/filter logic |
| "Add to route" on Festivals | **Decorative only** | Button with no `onClick` |
| Recommendations (UI) | **Not connected** | `useRecommendations` hook never imported |
| Lunch Recommendation | **Hardcoded** | "Local cuisine · Highly rated" is static text |
| Currency Preference | **Local state only** | Not persisted to API or localStorage |
| AI Insight Slider | **Placebo** | Changes no behavior anywhere |
