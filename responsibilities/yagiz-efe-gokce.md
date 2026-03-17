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
- Brute-force koruması: 5 başarısız girişte 15 dk blok (in-memory dict)

### 5. Temel Router'lar
- `routers/destinations.py`: CRUD + bütçe/kategori/sezon filtreli listeleme
- `routers/itineraries.py`: Plan oluşturma, durak ekleme/sıralama/silme
- `routers/users.py`: Profil görüntüleme, ziyaret geçmişi
- `routers/activities.py`: Aktivite listeleme, tag/category filtresi

### 6. Pydantic Modelleri (Core)
- `models/user.py`, `models/destination.py`, `models/itinerary.py`
- `models/itinerary_stop.py`, `models/activity.py`, `models/accommodation.py`
- `models/transport.py`
- Her model için `Base / Create / Update / Response` şema katmanları

### 7. Graf Öneri Servisi
- `services/recommendation.py`: Bütçe + kategori + sezon bazlı destinasyon önerisi
- En kısa ulaşım yolu (`shortestPath`) — `GET /api/destinations/route`
- Collaborative filtering: Benzer ziyaret geçmişi olan kullanıcıların tercihleri
- Üç strateji birleşik skor sistemiyle sıralanır (category_match + overlap × 2)

### 8. Seed Verisi
- `backend/db/seed.py`: 10 destinasyon, 3 kategori, 4 sezon, 6 etiket
- 20 aktivite (IN_CATEGORY + HAS_TAG kenarları), 18 restoran, 20 konaklama
- 10 festival, 5 kullanıcı (şifre: `Test1234!`), 19 VISITED kenarı, 15 yorum
- 10 Transport node + çift yönlü CONNECTED_BY kenarları (rota grafiği)

---

## Çözülen Teknik Sorunlar

1. **CORS_ORIGINS parse hatası** — pydantic-settings 2.13 ile `list[str]` uyumsuzluğu → `str` field + `@property` ile çözüldü
2. **bcrypt API uyumsuzluğu** — passlib 1.7.4 + bcrypt 5.0.0 çakışması → passlib kaldırılıp bcrypt doğrudan kullanıldı
3. **Seed encoding hatası** — Windows konsolu UTF-8 desteği → `sys.stdout.reconfigure(encoding="utf-8")` ile çözüldü
4. **FalkorDB shortestPath yönlendirme** — undirected traversal desteklenmiyor → `(a)-[:CONNECTED_BY*]->(b)` directed pattern kullanıldı
5. **shortestPath MATCH/RETURN konumu** — FalkorDB yalnızca RETURN/WITH içinde kabul ediyor → `RETURN shortestPath(...)` formatına geçildi

---

## Teslim Edilen Çıktılar

- [x] `docker-compose.yml` çalışıyor (FalkorDB ayağa kalkıyor)
- [x] `uvicorn main:app --reload` hatasız başlıyor
- [x] `/docs` Swagger UI açılıyor, tüm endpoint'ler listeli
- [x] Auth: kayıt + giriş + JWT korumalı endpoint test edildi
- [x] Destination CRUD çalışıyor
- [x] Öneri endpoint'i en az 2 Cypher traversal ile çalışıyor
- [x] `GET /health` FalkorDB bağlantısını doğruluyor
- [x] İtinerary CRUD + stop yönetimi tamamlandı
- [x] `recommendation.py` servisi tamamlandı (3 strateji)
- [x] Transport seed eklendi — `GET /api/destinations/route` çalışıyor

---

## Kullanılan Teknolojiler

`FastAPI 0.115` · `FalkorDB` · `Pydantic v2` · `python-jose` · `python-bcrypt` (passlib yerine) · `slowapi` · `Docker`
