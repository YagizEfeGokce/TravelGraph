# TravelGraph — Project Report

## 1. Business Problem

Turkey receives over 50 million tourists annually, yet travelers face significant challenges
discovering authentic local experiences beyond major hotspots. Existing platforms rely on
simple keyword search and flat relational data, failing to surface meaningful connections
between destinations, activities, seasons, and user preferences.

TravelGraph solves this with a graph-based travel intelligence platform that models
relationships between 14 entity types — enabling multi-hop traversal queries that
relational databases cannot express efficiently. A traveler's visited destinations,
preferred categories, and budget constraints are all first-class graph edges, enabling
a recommendation engine that understands context, not just keywords.

---

## 2. Technologies & Concepts Applied

### Graph Database — FalkorDB

- Stored all 14 entities as labeled nodes with typed properties
- Modeled relationships as directed edges: LOCATED_IN, IN_CATEGORY, HAS_SEASON, VISITED, REVIEWED
- Used Cypher for multi-hop traversal queries
- Applied sparse matrix representation (FalkorDB's core advantage) for fast neighbor lookup
- Created node indexes on User.email, User.id, Destination.id, Destination.name

### Recommendation Engine (services/recommendation.py)

- Cypher traversal: User → VISITED → Destination ← LOCATED_IN ← Activity → IN_CATEGORY → Category
- Matches candidate destinations sharing categories with already-visited ones
- Filters by accommodation price_per_night ≤ user budget
- Excludes already-visited destinations with NOT (u)-[:VISITED]->(d)
- Equivalent SQL would require 9 JOINs + NOT EXISTS subquery — FalkorDB expresses it in one traversal

### Shortest Path

- Implemented shortestPath() between any two destinations via shared activity categories
- Used for "how connected are these two cities?" feature in itinerary planning

### Backend — FastAPI + Python 3.11

- 14 Pydantic v2 models with full validation
- JWT authentication (bcrypt hashing, access + refresh tokens)
- Modular router structure: auth, destinations, activities, itineraries, users, restaurants, festivals, budgets, reviews, tags_categories
- CORS middleware configured for production and local origins

### Frontend — React 18 + Vite 5 + TypeScript + Tailwind CSS

- 9 pages: Home, Explore, Destinations, Festivals, Planner, Login, Register, Profile, NotFound
- 16 reusable components following Google Stitch design system
- Plus Jakarta Sans typography, #003d9b primary palette
- Axios API layer with JWT interceptors for token refresh

### Deployment

- Frontend: Vercel (auto-deploy from main branch)
- Backend + FalkorDB: Railway (internal network via railway.internal)
- Environment-based configuration via Railway Variables

---

## 3. Entity Model (14 Entities)

| Entity | Type | Key Relationships |
|---|---|---|
| User | Node | VISITED, REVIEWED, HAS_BUDGET |
| Destination | Node | LOCATED_IN (activities, restaurants, festivals) |
| Itinerary | Node | CREATED_BY (user), HAS_STOP |
| ItineraryStop | Node (M:N junction) | connects Itinerary ↔ Destination |
| Activity | Node | LOCATED_IN, IN_CATEGORY, HAS_SEASON |
| Accommodation | Node | LOCATED_IN, HAS_SEASON |
| Transport | Node | FROM / TO (destinations) |
| Restaurant | Node | LOCATED_IN, IN_CATEGORY |
| Festival | Node | LOCATED_IN, HAS_SEASON |
| BudgetPlan | Node | CREATED_BY (user) |
| Review | Node | WRITTEN_BY (user), ABOUT (destination) |
| Season | Node | HAS_SEASON (activities, festivals) |
| Category | Node | IN_CATEGORY (activities, restaurants) |
| Tag | Node | TAGGED (destinations, activities) |

---

## 4. Key Cypher Query — Recommendation Engine

```cypher
MATCH (u:User {id: $uid})-[:VISITED]->(v:Destination)
      <-[:LOCATED_IN]-(a:Activity)-[:IN_CATEGORY]->(c:Category)
MATCH (d:Destination)<-[:LOCATED_IN]-(a2:Activity)-[:IN_CATEGORY]->(c)
MATCH (d)<-[:LOCATED_IN]-(acc:Accommodation)
WHERE acc.price_per_night <= $budget AND NOT (u)-[:VISITED]->(d)
RETURN d, count(c) AS match ORDER BY match DESC LIMIT 5
```

SQL equivalent: 9 JOINs + NOT EXISTS subquery across 5 tables.

---

## 5. Team

| Name | Student No | Role |
|---|---|---|
| Yağız Efe Gökçe | 2309111075 | Architect & Backend Lead |
| Berfin Aksoy | 220911801 | Frontend |
| Emirhan Polat | 220911799 | Features & Documentation |

---

## 6. Live URLs

- Frontend: https://travel-graph.vercel.app
- Backend API: https://travelgraph-production-069c.up.railway.app
- GitHub: https://github.com/YagizEfeGokce/TravelGraph
