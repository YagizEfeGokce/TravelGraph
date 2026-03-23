# TravelGraph 🌍

> A graph-based intelligent travel route planning and destination discovery platform.

![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react)
![FalkorDB](https://img.shields.io/badge/FalkorDB-Graph%20DB-FF4B4B?style=flat)
![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=flat&logo=vite)

## 📸 Screenshots

| Home | Route Planner | Destination Detail |
|------|---------------|--------------------|
| ![Home](screenshots/home.png) | ![Planner](screenshots/planner.png) | ![Detail](screenshots/destination-detail.png) |

| Budget Planner | Festival Calendar | API Docs |
|----------------|-------------------|----------|
| ![Budget](screenshots/budget.png) | ![Festival](screenshots/festivals.png) | ![API](screenshots/api-docs.png) |

## ✨ Features

- 🗺️ **Destination Discovery** — City info, points of interest, no login required
- 🏨 **Accommodation Suggestions** — Hotel/hostel filtering by budget
- 🍽️ **Restaurant Recommendations** — Restaurant + cuisine type discovery
- 🎯 **Activity Planning** — Tourist attractions and custom activities
- 🎉 **Festival Calendar** — Event discovery by date
- 💶 **Budget Planner** — Hotel / food / transport / activity line items
- 🔗 **Graph-Based Recommendations** — Personalized suggestions via FalkorDB Cypher traversal
- 💬 **User Reviews** — Optional reviews for logged-in users

## 🚀 Quick Start

### Requirements
- Python 3.11+
- Node.js 20+
- Docker Desktop

### 1. Start FalkorDB
```bash
docker compose up -d
```
FalkorDB UI: http://localhost:3000

### 2. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```
API: http://localhost:8000
Swagger Docs: http://localhost:8000/docs

### 3. Load Seed Data
```bash
cd backend
python -m db.seed
```

### 4. Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
App: http://localhost:5173

## 🏗️ Architecture

```
TravelGraph
├── backend/                  # FastAPI + FalkorDB
│   ├── routers/              # API endpoints
│   ├── models/               # Pydantic schemas (14 entities)
│   ├── db/                   # FalkorDB connection & seed
│   └── services/             # Recommendation engine & Cypher queries
└── frontend/                 # React + Vite
    └── src/
        ├── pages/            # 9 pages
        ├── components/       # UI components
        ├── hooks/            # Custom React hooks
        ├── api/              # Axios request layer
        └── contexts/         # Auth state
```

## 🗂️ Entities (14 Entity Types)

| Entity | Description | Relationship |
|--------|-------------|--------------|
| User | Traveler / member | — |
| Destination | City & country | — |
| Itinerary | Travel plan | Owned by User |
| ItineraryStop | Plan ↔ Stop bridge | M:N |
| Activity | Tourist attractions & custom activities | Located in Destination |
| Accommodation | Hotel / hostel | Located in Destination |
| Transport | Flight / train / bus | Connects Destinations |
| Restaurant | Restaurant + cuisine type | Located in Destination |
| Festival | Event + date range | Located in Destination |
| BudgetPlan | User budget + line items | Belongs to Itinerary |
| Review | Comment & rating (optional) | Written by User |
| Season | Weather & season info | For Destination |
| Category | Museum, Nature, Food... | M:N with Activity |
| Tag | Label & filter | M:N with Activity |

## 🔗 FalkorDB Graph Query Example

```cypher
// Recommendation for a user with €500 budget, loves museums, travelling in April
MATCH (u:User {id: $user_id})-[:VISITED]->(visited:Destination)
MATCH (d:Destination)<-[:LOCATED_IN]-(a:Activity)-[:IN_CATEGORY]->(c:Category {name: "Museum"})
MATCH (d)<-[:HELD_IN]-(f:Festival)-[:IN_SEASON]->(s:Season {name: "Spring"})
MATCH (d)<-[:LOCATED_IN]-(acc:Accommodation)
WHERE acc.price_per_night * 5 <= $budget * 0.4
  AND NOT (u)-[:VISITED]->(d)
RETURN d.name, count(a) AS museum_count, f.name AS spring_festival
ORDER BY museum_count DESC
LIMIT 5
```

## 👥 Team

| Name | Role |
|------|------|
| Yağız Efe Gökçe | Architect & Backend Lead |
| Berfin Aksoy | Frontend |
| Emirhan Polat | Features & Documentation |

## 🌐 Live URLs

- **Frontend:** https://travel-graph.vercel.app
- **Backend API:** https://travelgraph-production-069c.up.railway.app

## 📄 License

MIT
