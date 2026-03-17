# Emirhan için Antigravity Talimatları

> **Antigravity'ye ekle:** `Settings → Knowledge → Add File` — bu dosyayı seç.

---

## Sen Kimsin?

**TravelGraph** projesinin Feature Geliştirici ve Dokümantasyon sorumlususun.  
Sorumluluğun: Restaurant, Festival, BudgetPlan, Review, Tag, Category sistemleri + Seed verisi + Dokümantasyon.

**Dokunma:**
- `backend/routers/auth.py` → Yağız
- `backend/routers/destinations.py` → Yağız
- `backend/routers/itineraries.py` → Yağız
- `backend/db/connection.py` → Yağız
- `frontend/` → Berfin (sadece Berfin'in senden istediği şeyi söyle, sende dokunma)

---

## Proje Özeti

| Alan | Değer |
|------|-------|
| Proje | TravelGraph — Graf tabanlı seyahat platformu |
| Veritabanı | FalkorDB (graf DB, Redis uyumlu) |
| Bağlantı | `backend/db/connection.py` içindeki `get_db()` fonksiyonu |
| FalkorDB UI | `http://localhost:3000` (çalışıp çalışmadığını buradan doğrula) |
| API Docs | `http://localhost:8000/docs` |

---

## FalkorDB Kullanım Kuralları

```python
# DOĞRU — her zaman parametreli sorgu
from db.connection import get_db

db = get_db()
result = db.query(
    "MATCH (r:Restaurant {id: $id}) RETURN r",
    {"id": restaurant_id}
)

# YANLIŞ — asla f-string veya format ile sorgu oluşturma (injection açığı!)
db.query(f"MATCH (r:Restaurant {{name: '{name}'}}) RETURN r")  # ❌
```

---

## Senin Endpoint'lerin

### Restaurant
```
GET  /api/destinations/{id}/restaurants   ← destinasyona göre listele
GET  /api/restaurants                     ← filtreli (cuisine_type, price_range)
POST /api/restaurants                     ← yeni restoran ekle
```

### Festival
```
GET  /api/festivals                       ← tarih filtreli (start_after, end_before, season)
GET  /api/destinations/{id}/festivals     ← destinasyona göre listele
POST /api/festivals                       ← yeni festival ekle
```

### BudgetPlan
```
POST /api/itineraries/{id}/budget         ← oluştur (auth zorunlu)
GET  /api/itineraries/{id}/budget         ← görüntüle (auth zorunlu)
PUT  /api/itineraries/{id}/budget         ← güncelle (auth zorunlu)
```

### Review
```
POST   /api/reviews                       ← yorum yaz (auth zorunlu)
GET    /api/reviews                       ← listele (?target_id=&target_type=)
DELETE /api/reviews/{id}                  ← sil (sadece kendi yorumu)
```

### Tag & Category
```
GET  /api/tags                            ← tüm tag'ler
GET  /api/categories                      ← tüm kategoriler
POST /api/activities/{id}/tags            ← aktiviteye tag ekle (M:N)
GET  /api/categories/{id}/activities      ← kategoriye göre aktiviteler
```

---

## Pydantic v2 Şema Şablonları

### Restaurant şeması örneği
```python
# backend/models/restaurant.py
from pydantic import BaseModel, field_validator
from typing import Optional, Literal
from datetime import datetime

class RestaurantBase(BaseModel):
    name: str
    cuisine_type: str
    price_range: Literal['budget', 'mid', 'luxury']
    address: str
    rating: Optional[float] = None

    @field_validator('rating')
    @classmethod
    def validate_rating(cls, v):
        if v is not None and not (1.0 <= v <= 5.0):
            raise ValueError('Puan 1.0 ile 5.0 arasında olmalı')
        return v

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Restoran adı en az 2 karakter olmalı')
        return v.strip()

class RestaurantCreate(RestaurantBase):
    destination_id: str

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    cuisine_type: Optional[str] = None
    price_range: Optional[Literal['budget', 'mid', 'luxury']] = None
    rating: Optional[float] = None

class RestaurantResponse(RestaurantBase):
    id: str
    destination_id: str
```

### BudgetPlan şeması — validator ile
```python
# backend/models/budget.py
from pydantic import BaseModel, model_validator
from typing import Literal

class BudgetPlanCreate(BaseModel):
    total_budget: float
    currency: Literal['EUR', 'USD', 'TRY'] = 'EUR'
    hotel_budget: float
    food_budget: float
    transport_budget: float
    activity_budget: float

    @model_validator(mode='after')
    def validate_budget_sum(self):
        total_items = (
            self.hotel_budget + self.food_budget +
            self.transport_budget + self.activity_budget
        )
        if total_items > self.total_budget:
            raise ValueError(
                f'Kalem toplamı ({total_items}) toplam bütçeyi ({self.total_budget}) aşamaz'
            )
        if any(v < 0 for v in [self.hotel_budget, self.food_budget,
                                self.transport_budget, self.activity_budget]):
            raise ValueError('Bütçe kalemleri negatif olamaz')
        return self
```

---

## Antigravity'ye Verilecek Prompt Örnekleri

### Örnek 1 — Festival endpoint'i
```
TravelGraph projesinin backend geliştiricisiyim.
Stack: FastAPI 0.115, FalkorDB, Pydantic v2, Python 3.11.
FalkorDB bağlantısı backend/db/connection.py içindeki get_db() ile yapılıyor.

Festival endpoint'lerini yaz:
- GET /api/festivals: Tüm festivalleri getir.
  Query params: start_after (date), end_before (date), season (str)
  FalkorDB Cypher: MATCH (f:Festival) ile filtrele
- GET /api/destinations/{id}/festivals: Destinasyona ait festivaller
  Cypher: MATCH (d:Destination {id: $id})-[:HAS_FESTIVAL]->(f:Festival) RETURN f
- POST /api/festivals: Yeni festival ekle (auth gerekmiyor, test amaçlı)

Pydantic v2 syntax kullan (field_validator, model_validator).
Tüm Cypher sorguları parametreli olsun — f-string yok.
HTTP hataları: 404 (destination bulunamadı), 422 (validasyon hatası).

Dosyalar:
- backend/models/festival.py
- backend/routers/festivals.py
```

### Örnek 2 — Review sistemi (duplicate kontrolü ile)
```
TravelGraph için Review endpoint'lerini yaz.
FastAPI + FalkorDB + Pydantic v2.

POST /api/reviews:
- Auth zorunlu (get_current_user dependency'si Yağız'ın auth.py'sinde)
- Body: {target_id, target_type ("activity"|"accommodation"|"restaurant"), rating (1-5), comment (max 1000 karakter)}
- Kontrol: aynı kullanıcı aynı yere zaten yorum yazdıysa 409 Conflict döndür
  Cypher: MATCH (u:User {id:$uid})-[:WROTE]->(r:Review)-[:ABOUT]->(t {id:$tid}) RETURN r
- Yorum yoksa: Review node oluştur, iki kenar ekle:
  (User)-[:WROTE]->(Review) ve (Review)-[:ABOUT]->(target)

GET /api/reviews?target_id=&target_type=:
- Herkese açık (auth gerekmez)
- Ortalama puanı da döndür

DELETE /api/reviews/{id}:
- Sadece yorumu yazan kullanıcı silebilir (403 Forbidden değilse)

Dosyalar: backend/models/review.py, backend/routers/reviews.py
```

### Örnek 3 — Seed verisi
```
TravelGraph için FalkorDB seed scripti yaz.
Dosya: backend/db/seed.py
Çalıştırma: python -m db.seed

Oluşturulacak veri:
- 5 User node
- 10 Destination: Istanbul, Paris, Barcelona, Roma, Tokyo, New York, Bali, Prag, Amsterdam, Lizbon
- 3 Category: Museum, Nature, Food & Drink
- 4 Season: Spring, Summer, Autumn, Winter
- 20 Activity (her destinasyona 2, en az bir kategori bağlı)
- 15 Restaurant (farklı cuisine_type: Turkish, French, Japanese, Italian, Fusion)
- 10 Festival (başlangıç/bitiş tarihi gerçekçi, sezona bağlı)
- 10 Accommodation (farklı star_rating ve price_per_night)
- 15 Review (farklı kullanıcılar, farklı hedefler, rating 3-5)
- M:N kenarları: Activity↔Category, Activity↔Tag
- (User)-[:VISITED]->(Destination) kenarları (her kullanıcı 3-5 şehir)

Script idempotent olsun: önce mevcut tüm node'ları temizle, sonra yeniden oluştur.
FalkorDB bağlantısı: from db.connection import get_db
```

---

## Berfin ile Koordinasyon

Berfin frontend'ini geliştirirken senden bazı bilgiler bekleyecek. Endpoint hazır olunca şunu söyle:

**Restaurant hazır olunca:**
> "GET /api/destinations/{id}/restaurants hazır. Dönen format: [{id, name, cuisine_type, price_range: 'budget'|'mid'|'luxury', address, rating}]"

**Festival hazır olunca:**
> "GET /api/festivals?start_after=2024-04-01&end_before=2024-05-31 hazır. Dönen format: [{id, name, start_date, end_date, is_recurring, destination_name}]"

**BudgetPlan hazır olunca:**
> "POST /api/itineraries/{id}/budget hazır. Body: {total_budget, currency, hotel_budget, food_budget, transport_budget, activity_budget}. Auth header gerekli."

---

## Screenshot Alma Rehberi

`screenshots/` klasörüne eklenecekler:

| Dosya adı | Ne göstermeli |
|-----------|--------------|
| `home.png` | Ana sayfa, destinasyon listesi |
| `planner.png` | Rota planlayıcı, en az 2 durak |
| `destination-detail.png` | Aktivite + restoran + festival görünür |
| `budget.png` | Bütçe planlayıcı formu dolu |
| `festivals.png` | Festival takvimi, tarih filtresi açık |
| `api-docs.png` | `localhost:8000/docs` tüm endpoint'ler görünür |

Antigravity Browser görünümünde `Ctrl+Shift+S` ile yakala.

---

## Teslim Kontrol Listesi

- [ ] Restaurant endpoint'leri `/docs`'tan test edildi
- [ ] Festival tarih filtresi çalışıyor
- [ ] BudgetPlan kalem validasyonu çalışıyor (toplam aşma hatası test edildi)
- [ ] Review duplicate engeli test edildi (aynı kullanıcı 2. yorumda 409 alıyor)
- [ ] Seed çalıştırıldı, `localhost:3000` FalkorDB UI'da veri görünüyor
- [ ] `screenshots/` klasöründe 6 görüntü mevcut
- [ ] `REPORT.md` teknik bölümleri dolduruldu
