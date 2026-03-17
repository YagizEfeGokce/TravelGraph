# Yağız Efe Gökçe — Sorumluluk Raporu

## Rol: Mimar & Backend Geliştirici

---

## Üstlenilen Görevler

### 1. Proje Mimarisi ve Repo Kurulumu
- GitHub repo oluşturma, branch stratejisi (`main`, `dev`, `feature/*`)
- Klasör yapısının kurulumu, `docker-compose.yml`
- `.env.example` şablonları, `requirements.txt`
- Ekip üyelerine branch ve PR kurallarının aktarılması

### 2. FalkorDB Entegrasyonu
- `backend/db/connection.py`: Bağlantı havuzu, retry mekanizması, graph adı config'den
- FalkorDB'de tüm node ve edge tiplerinin indeks tanımları
- Bağlantı sağlık kontrolü (`/health` endpoint'i)

### 3. FastAPI Uygulama Çatısı (`main.py`)
- CORS middleware (yalnızca frontend origin)
- Global exception handler (tutarlı hata formatı)
- Rate limiting middleware (`slowapi`)
- Tüm router'ların `include_router` ile bağlanması
- Startup event: FalkorDB bağlantı testi

### 4. Auth Sistemi (`routers/auth.py`)
- Kullanıcı kaydı — bcrypt şifre hashleme
- Giriş — JWT access token + refresh token (HS256)
- Token yenileme endpoint'i
- `get_current_user` dependency (zorunlu)
- `get_optional_user` dependency (opsiyonel — giriş gerektirmeyen sayfalarda)

### 5. Temel Router'lar
- `routers/destinations.py`: CRUD + bütçe/kategori/sezon filtreli listeleme
- `routers/itineraries.py`: Plan oluşturma, durak ekleme/sıralama
- `routers/users.py`: Profil görüntüleme, ziyaret geçmişi
- `routers/activities.py`: Aktivite listeleme, tag/category filtresi

### 6. Pydantic Modelleri (Core)
- `models/user.py`, `models/destination.py`, `models/itinerary.py`
- `models/itinerary_stop.py`, `models/activity.py`, `models/accommodation.py`
- `models/transport.py`
- Her model için `Base / Create / Update / Response` şema katmanları

### 7. Graf Öneri Servisi
- `services/recommendation.py`: Bütçe + kategori + sezon bazlı destinasyon önerisi
- `services/graph_queries.py`: Tüm Cypher sorguları merkezi dosyada, parametreli
- En kısa ulaşım yolu (`shortestPath`)
- Collaborative filtering: Benzer ziyaret geçmişi olan kullanıcıların tercihleri

---

## Teslim Edilen Çıktılar

- [ ] `docker-compose.yml` çalışıyor (FalkorDB ayağa kalkıyor)
- [ ] `uvicorn main:app --reload` hatasız başlıyor
- [ ] `/docs` Swagger UI açılıyor, tüm endpoint'ler listeli
- [ ] Auth: kayıt + giriş + JWT korumalı endpoint test edildi
- [ ] Destination CRUD çalışıyor
- [ ] Öneri endpoint'i en az 2 Cypher traversal ile çalışıyor
- [ ] `GET /health` FalkorDB bağlantısını doğruluyor

---

## Kullanılan Teknolojiler

`FastAPI 0.115` · `FalkorDB` · `Pydantic v2` · `python-jose` · `bcrypt` · `slowapi` · `Docker`
