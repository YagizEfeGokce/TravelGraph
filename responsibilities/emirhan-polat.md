# Emirhan Polat — Sorumluluk Raporu

## Rol: Feature Geliştirici & Dokümantasyon

---

## Üstlenilen Görevler

### 1. Restaurant Sistemi
- `models/restaurant.py`: `RestaurantBase/Create/Update/Response` şemaları
  - Alanlar: name, cuisine_type, price_range (budget/mid/luxury), address, rating, opening_hours
- `routers/restaurants.py`:
  - `GET /api/destinations/{id}/restaurants` — destinasyona göre listele
  - `GET /api/restaurants` — filtreli (mutfak türü, fiyat aralığı)
  - `POST /api/restaurants` — yeni restoran ekle
- FalkorDB: `(Destination)-[:HAS_RESTAURANT]->(Restaurant)` kenarı

### 2. Festival Sistemi
- `models/festival.py`: `FestivalBase/Create/Update/Response` şemaları
  - Alanlar: name, description, start_date, end_date, is_recurring, ticket_price
- `routers/festivals.py`:
  - `GET /api/festivals` — tarih aralığı filtresi (start_after, end_before)
  - `GET /api/destinations/{id}/festivals` — destinasyona göre
  - `POST /api/festivals` — yeni festival ekle
- FalkorDB: `(Destination)-[:HELD_IN]->(Festival)-[:IN_SEASON]->(Season)` kenarları

### 3. BudgetPlan Sistemi
- `models/budget.py`: `BudgetPlanBase/Create/Response` şemaları
  - Alanlar: total_budget, currency (EUR/USD/TRY), hotel_budget, food_budget, transport_budget, activity_budget
  - Validator: kalem toplamı ≤ total_budget
- `routers/budget.py`:
  - `POST /api/itineraries/{id}/budget` — bütçe planı oluştur (auth gerekli)
  - `GET /api/itineraries/{id}/budget` — mevcut bütçeyi getir
  - `PUT /api/itineraries/{id}/budget` — bütçe güncelle
- FalkorDB: `(Itinerary)-[:HAS_BUDGET]->(BudgetPlan)` kenarı

### 4. Review Sistemi
- `models/review.py`: şema (rating 1-5, comment max 1000 karakter)
- `routers/reviews.py`:
  - `POST /api/reviews` — yorum yaz (auth zorunlu)
  - `GET /api/reviews?target_id=&target_type=` — yorumları getir (herkese açık)
  - `DELETE /api/reviews/{id}` — kendi yorumunu sil
  - Aynı kullanıcı aynı yere 2 kez yorum yazamaz (409 Conflict)
- FalkorDB: `(Review)-[:ABOUT]->(Activity | Accommodation | Restaurant)` kenarları

### 5. Tag & Category Sistemi
- `models/tag.py`, `models/category.py`
- `routers/tags.py`, `routers/categories.py`
- `POST /api/activities/{id}/tags` — aktiviteye tag ekle (M:N)
- `GET /api/categories/{id}/activities` — kategoriye göre aktiviteler

### 6. Seed Verisi (`db/seed.py`)
- 5 User (farklı ziyaret geçmişleri)
- 10 Destination: İstanbul, Paris, Barcelona, Roma, Tokyo, New York, Bali, Prag, Amsterdam, Lizbon
- 3 Category: Museum, Nature, Food & Drink
- 4 Season: Spring, Summer, Autumn, Winter
- 20 Activity (her destinasyona 2, kategori bağlı)
- 15 Restaurant (her destinasyona 1-2, farklı mutfak türleri)
- 10 Festival (mevsimle ilişkili)
- 10 Accommodation (farklı yıldız ve fiyat)
- 15 Review (farklı kullanıcılar, farklı hedefler)
- Tüm M:N kenarları (Activity↔Category, Activity↔Tag)
- Seed idempotent: iki kez çalıştırılınca hata vermiyor

### 7. Dokümantasyon ve Screenshots
- `REPORT.md` teknik bölümlerini doldurma (Yağız ile koordineli)
- `README.md` kurulum adımlarını test etme ve güncelleme
- `screenshots/` klasörüne eklenmesi gereken görseller:
  - `home.png`, `planner.png`, `destination-detail.png`
  - `budget.png`, `festivals.png`, `api-docs.png`

---

## Teslim Edilen Çıktılar

- [ ] Restaurant CRUD endpoint'leri (`/docs`'tan test edildi)
- [ ] Festival listesi tarih filtresi çalışıyor
- [ ] BudgetPlan oluşturma + kalem validasyonu çalışıyor
- [ ] Review endpoint'leri çalışıyor (duplicate engeli test edildi)
- [ ] Tag/Category endpoint'leri çalışıyor
- [ ] Seed çalıştırıldı, FalkorDB UI'da veri görünüyor (`localhost:3000`)
- [ ] `screenshots/` klasöründe 6 görüntü mevcut
- [ ] `REPORT.md` tamamlandı

---

## Kullanılan Teknolojiler

`FastAPI` · `FalkorDB` · `Pydantic v2` · `Python 3.11`
