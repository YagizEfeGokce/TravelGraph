# Prompts

This folder contains the AI prompts used during the development of TravelGraph.

---------------------------------------------------------------------------------------------

Sen TravelGraph projesinin backend mimarıdır.

PROJE BAĞLAMI:

- Repo: <https://github.com/YagizEfeGokce/TravelGraph>
- Stack: FastAPI 0.115, FalkorDB (falkordb==1.0.9), Pydantic v2, Python 3.11
- Graf veritabanı: FalkorDB (Redis protokolü, localhost:6379)
- Mevcut dosyalar: backend/.env.example, backend/requirements.txt

GÖREV: Aşağıdaki dosyaları oluştur.

─── backend/db/connection.py ───

- FalkorDB bağlantısı (host/port/graph adı .env'den)
- get_db() fonksiyonu → FastAPI dependency olarak kullanılacak
- check_connection() → bool döndürür (health check için)
- create_indexes() → sık sorgulanan property'lere index oluşturur
  (User.email, User.id, Destination.id, Destination.name)
- Bağlantı retry mekanizması (3 deneme, 2sn bekleme)
- Tüm hatalar logger ile loglanır

─── backend/main.py ───

- FastAPI app factory
- CORS middleware (CORS_ORIGINS .env'den, virgülle ayrılmış)
- Global exception handler: her hatada {"detail": str, "type": str} formatı
- Rate limiting: slowapi ile IP bazlı, dakikada 60 istek
- Startup event: check_connection() çağır, False ise uyar ama durma
- Startup event: create_indexes() çağır
- /health endpoint'i: FalkorDB durumu + versiyon bilgisi döner
- Tüm router'ları include_router ile bağla (henüz boş olsa bile import et)
- API prefix: /api

─── backend/core/config.py ───

- pydantic-settings ile Settings sınıfı
- Alanlar: FALKORDB_HOST, FALKORDB_PORT, FALKORDB_GRAPH,
  JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES, JWT_REFRESH_EXPIRE_DAYS,
  CORS_ORIGINS (str → list[str] validator ile)
- .env dosyasından otomatik yükle

─── backend/core/__init__.py ─── (boş)
─── backend/db/__init__.py ─── (boş)

KURALLAR:

- Pydantic v2 syntax (field_validator, model_validator, @classmethod)
- Tüm Cypher sorguları parametreli — asla f-string değil
- Type hint her fonksiyonda
- Her modülde module-level docstring

---------------------------------------------------------------------------------------------

TravelGraph backend — Auth sistemi.

MEVCUT DURUM:

- backend/db/connection.py hazır (get_db() mevcut)
- backend/core/config.py hazır (Settings mevcut)
- backend/main.py hazır

GÖREV: Aşağıdaki dosyaları oluştur.

─── backend/models/user.py ───
Pydantic v2 şemaları:

- UserBase: email (EmailStr), name (str, 2-50 karakter)
- UserCreate(UserBase): password (str, min 8, en az 1 büyük + 1 rakam — field_validator)
- UserUpdate: name, password — hepsi Optional
- UserResponse(UserBase): id, created_at — password_hash YOK

─── backend/core/security.py ───

- hash_password(plain: str) → str  (bcrypt)
- verify_password(plain: str, hashed: str) → bool
- create_access_token(data: dict) → str  (JWT, exp: JWT_EXPIRE_MINUTES)
- create_refresh_token(data: dict) → str  (JWT, exp: JWT_REFRESH_EXPIRE_DAYS gün)
- decode_token(token: str) → dict | None

─── backend/core/dependencies.py ───

- get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db)) → dict
  Token geçersizse 401 HTTP exception
- get_optional_user(...) → dict | None
  Token yoksa/geçersizse None döner (giriş gerektirmeyen endpoint'ler için)

─── backend/routers/auth.py ───
Endpoint'ler:

- POST /api/auth/register
  Body: UserCreate
  FalkorDB: User node oluştur, email unique kontrolü (409 Conflict)
  Dön: UserResponse + access_token + refresh_token
- POST /api/auth/login
  Body: email + password (OAuth2PasswordRequestForm)
  FalkorDB: email ile User bul, verify_password
  5 başarısız girişte 15 dk blok (in-memory dict yeterli)
  Dön: access_token + refresh_token + UserResponse
- POST /api/auth/refresh
  Body: refresh_token
  Dön: yeni access_token
- GET /api/auth/me
  Requires: get_current_user dependency
  Dön: UserResponse

FalkorDB Node oluşturma örneği (BUNU KULLAN):
db.query(
    "CREATE (u:User {id: $id, email: $email, name: $name, "
    "password_hash: $ph, created_at: $ca}) RETURN u",
    {"id": str(uuid4()), "email": email, "name": name,
     "ph": hash_password(password), "ca": datetime.utcnow().isoformat()}
)

KURALLAR:

- Asla f-string Cypher sorgusu
- Response'larda password_hash alanı kesinlikle olmasın
- HTTP hata kodları: 400 (hatalı istek), 401 (kimlik hatası),
  409 (email zaten kayıtlı), 429 (rate limit)

---------------------------------------------------------------------------------------------

  TravelGraph backend — Destination ve Activity CRUD + öneri endpoint'i.

MEVCUT DURUM:

- Auth sistemi hazır (get_current_user, get_optional_user mevcut)
- FalkorDB bağlantısı hazır

GÖREV:

─── backend/models/destination.py ───

- DestinationBase: name, country, description, lat (float -90/90), lng (float -180/180)
- DestinationCreate(Base): — (aynı alanlar)
- DestinationUpdate: tüm alanlar Optional
- DestinationResponse: id, name, country, description, lat, lng, avg_rating (Optional[float])

─── backend/models/activity.py ───

- ActivityBase: name, description, duration_hours (float > 0), price (float >= 0), address
- ActivityCreate(Base): destination_id
- ActivityResponse: id + Base alanları + destination_id + categories (list[str]) + tags (list[str])

─── backend/routers/destinations.py ───
GET /api/destinations
  Query params: country, category, season, min_rating (float), limit (int default 20)
  Herkese açık (get_optional_user)
  FalkorDB: MATCH (d:Destination) ile filtrele

GET /api/destinations/{id}
  Herkese açık
  FalkorDB: destination + avg_rating hesapla

GET /api/destinations/{id}/activities
  Herkese açık
  FalkorDB: MATCH (d:Destination {id:$id})-[:HAS_ACTIVITY]->(a:Activity) RETURN a

GET /api/destinations/{id}/accommodations
  Herkese açık

GET /api/destinations/{id}/restaurants
  Herkese açık

GET /api/destinations/{id}/festivals
  Herkese açık

GET /api/destinations/{id}/recommend
  Herkese açık
  FalkorDB Cypher (BUNU KULLAN):
  MATCH (d:Destination)<-[:LOCATED_IN]-(a:Activity)
        -[:IN_CATEGORY]->(c:Category)
  WHERE d.id <> $current_id
  WITH d, count(DISTINCT c) AS diversity
  MATCH (d)<-[:LOCATED_IN]-(acc:Accommodation)
  WHERE acc.price_per_night <= $max_price
  RETURN d, diversity, avg(acc.price_per_night) AS avg_price
  ORDER BY diversity DESC LIMIT 5

POST /api/destinations
  Auth gerekli
  Body: DestinationCreate
  FalkorDB: Destination node oluştur

─── backend/routers/activities.py ───
GET /api/activities  (filtreli: category, tag, destination_id)
POST /api/activities (auth gerekli)

KURALLAR:

- Tüm GET endpoint'leri herkese açık (get_optional_user)
- 404: destination bulunamadı
- Parametreli Cypher — f-string yok
- Her endpoint için response_model belirt

---------------------------------------------------------------------------------------------

TravelGraph backend — Kalan 10 entity için Pydantic v2 modelleri.

backend/models/ klasörüne şu dosyaları oluştur:

accommodation.py:
  AccommodationBase: name, type (hotel/hostel/apartment), star_rating (1-5 int),
    price_per_night (float > 0), address
  AccommodationCreate(Base): destination_id
  AccommodationResponse: id + Base + destination_id

transport.py:
  TransportBase: type (flight/train/bus/ferry), provider, duration_hours (float),
    price (float), departure_city, arrival_city
  TransportCreate(Base): —
  TransportResponse: id + Base

restaurant.py:
  RestaurantBase: name, cuisine_type, price_range (budget/mid/luxury),
    address, rating (Optional float 1-5)
  RestaurantCreate(Base): destination_id
  RestaurantResponse: id + Base + destination_id

festival.py:
  FestivalBase: name, description, start_date (date), end_date (date),
    is_recurring (bool), ticket_price (Optional float)
  model_validator: start_date < end_date kontrolü
  FestivalCreate(Base): destination_id
  FestivalResponse: id + Base + destination_id

budget.py:
  BudgetPlanCreate: total_budget (float > 0), currency (EUR/USD/TRY),
    hotel_budget, food_budget, transport_budget, activity_budget (hepsi float >= 0)
  model_validator: kalem toplamı <= total_budget
  model_validator: hiçbir kalem negatif olamaz
  BudgetPlanResponse: id + Create alanları + itinerary_id

itinerary.py:
  ItineraryBase: title (str), start_date (date), end_date (date), is_public (bool)
  model_validator: start_date < end_date
  ItineraryCreate(Base): —
  ItineraryResponse: id + Base + user_id + stops (list) + budget (Optional)

itinerary_stop.py:
  ItineraryStopCreate: destination_id, day_number (int >= 1), order (int >= 1),
    notes (Optional str max 500)
  ItineraryStopResponse: id + Create alanları + destination_name

review.py:
  ReviewCreate: target_id, target_type (activity/accommodation/restaurant),
    rating (int 1-5), comment (str max 1000)
  ReviewResponse: id + Create alanları + user_name + created_at

category.py:
  CategoryBase: name, icon (str), description (Optional)
  CategoryResponse: id + Base

tag.py:
  TagBase: name, color (str hex renk kodu — #RRGGBB validator)
  TagResponse: id + Base

season.py:
  SeasonBase: name (Spring/Summer/Autumn/Winter), months (list[int] 1-12),
    avg_temp_c (float), weather_description (str)
  SeasonResponse: id + Base

Her model için backend/models/__init__.py'ye export ekle.
Pydantic v2 syntax: field_validator @classmethod, model_validator mode='after'.

---------------------------------------------------------------------------------------------

TravelGraph backend/db/seed.py dosyasını oluştur.

Çalıştırma: python -m db.seed
FalkorDB bağlantısı: from db.connection import get_db

Oluşturulacak veri (bu sırayla, önce bağımlısız olanlar):

1. Temizlik: MATCH (n) DETACH DELETE n (idempotent)

2. Category node'ları (3):
   Museum, Nature, "Food & Drink"

3. Season node'ları (4):
   Spring (3,4,5), Summer (6,7,8), Autumn (9,10,11), Winter (12,1,2)

4. Tag node'ları (6):
   family-friendly (#4CAF50), romantic (#E91E63), budget (#FF9800),
   adventure (#9C27B0), cultural (#2196F3), foodie (#FF5722)

5. Destination node'ları (10) + BEST_IN Season kenarları:
   Istanbul/Turkey (Summer+Autumn), Paris/France (Spring+Summer),
   Barcelona/Spain (Summer), Roma/Italy (Spring+Autumn),
   Tokyo/Japan (Spring+Autumn), New York/USA (Summer),
   Bali/Indonesia (Summer), Prague/Czech Republic (Summer),
   Amsterdam/Netherlands (Spring+Summer), Lisbon/Portugal (Summer)

6. Her destinasyona 2 Activity + kategori ve tag bağlantıları
7. Her destinasyona 1-2 Restaurant (farklı cuisine_type)
8. Her destinasyona 1-2 Accommodation (farklı star_rating, price_per_night)
9. Her destinasyona 1 Festival (gerçekçi isim ve tarih)
10. 5 User (farklı isimler, bcrypt hash şifre: "Test1234!")
11. Her kullanıcıya 3-5 VISITED kenarı (User→Destination)
12. 15 Review (farklı kullanıcılar, farklı aktivite/konaklama hedefleri)

Print her adımda: "✓ 10 Destination oluşturuldu" gibi.
Hata olursa tüm script durur ve hatayı yazdırır.

---------------------------------------------------------------------------------------------

TravelGraph projesinin backend'ini test et ve çalışır hale getir.

REPO YAPISI:

- backend/main.py (FastAPI app)
- backend/core/config.py, security.py, dependencies.py
- backend/db/connection.py, seed.py
- backend/models/ (12 model dosyası)
- backend/routers/auth.py, destinations.py, activities.py, users.py
- backend/.env.example

GÖREVLER (sırayla yap):

1. ENV DOSYASI OLUŞTUR
   backend/.env.example dosyasını oku
   backend/.env dosyasını oluştur, şu değerlerle doldur:
   - FALKORDB_HOST=localhost
   - FALKORDB_PORT=6379
   - FALKORDB_GRAPH=travelgraph
   - JWT_SECRET=<python -c "import secrets; print(secrets.token_hex(32))" komutu ile üret>
   - JWT_ALGORITHM=HS256
   - JWT_EXPIRE_MINUTES=60
   - JWT_REFRESH_EXPIRE_DAYS=7
   - CORS_ORIGINS=<http://localhost:5173>

2. BAĞIMLILIKLARI KONTROL ET
   pip list ile yüklü paketleri kontrol et
   Eksik paket varsa pip install -r backend/requirements.txt çalıştır

3. DOCKER KONTROLÜ
   docker ps ile FalkorDB container'ının çalışıp çalışmadığını kontrol et
   Çalışmıyorsa docker compose up -d çalıştır
   Container ayağa kalkana kadar bekle (max 15 saniye)

4. IMPORT KONTROLÜ
   cd backend && python -c "import main" komutunu çalıştır
   Import hatası varsa:
   - Hangi modülün eksik/hatalı olduğunu tespit et
   - Hatayı düzelt (eksik import, yanlış syntax, vs.)
   - Tekrar test et, hata kalmayana kadar devam et

5. UVICORN'U BAŞLAT
   cd backend && uvicorn main:app --reload --port 8000
   Başlatırken çıkan tüm hataları yakala

6. HEALTH CHECK
   Uvicorn başarıyla başladıysa:
   curl <http://localhost:8000/health> komutu çalıştır
   {"falkordb": true} veya benzeri bir yanıt bekliyoruz

7. SEED VERİSİ
   Health check başarılıysa:
   cd backend && python -m db.seed
   Hata olursa seed.py'yi oku ve hatayı düzelt

8. SWAGGER TEST
   curl <http://localhost:8000/openapi.json> | python -m json.tool | head -50
   Tüm endpoint'lerin listelendiğini doğrula

9. AUTH TESTİ
   curl -X POST <http://localhost:8000/api/auth/register> \
     -H "Content-Type: application/json" \
     -d '{"email":"<test@test.com>","name":"Test User","password":"Test1234!"}'
   201 veya access_token içeren bir yanıt bekliyoruz

10. RAPOR
    Her adımın sonucunu özetle:
    ✅ ENV oluşturuldu
    ✅ Docker çalışıyor
    ✅ Import başarılı
    ✅ Uvicorn başladı
    ✅ Health check geçti
    ✅ Seed yüklendi
    ✅ Auth çalışıyor

    Hata olan adım varsa:
    ❌ [Adım adı]: [Hata mesajı] — [Yapılan düzeltme]

KURALLAR:

- Hata görürsen dur ve düzelt, sonraki adıma geç
- backend/.env dosyasını asla GitHub'a commit etme
- Tüm düzeltmeleri yaptıktan sonra çalışan kodu commit et:
  git add -A && git commit -m "fix: backend import hatası düzeltildi"
  (Sadece .env HARİÇ her şeyi ekle)

---------------------------------------------------------------------------------------------

  TravelGraph backend — Emirhan'ın sorumluluğundaki 6 özelliği ekle.

MEVCUT DURUM:

- backend/main.py çalışıyor (uvicorn başarıyla başlıyor)
- backend/db/connection.py → get_db() mevcut
- backend/core/dependencies.py → get_current_user, get_optional_user mevcut
- backend/models/ → tüm modeller mevcut (restaurant.py, festival.py, budget.py, review.py, tag.py, category.py, season.py)
- CORS, rate limiting, JWT auth sistemi kurulu

GÖREV: Şu 6 router dosyasını oluştur ve main.py'ye bağla.

─── backend/routers/restaurants.py ───
GET  /api/destinations/{id}/restaurants  → herkese açık
GET  /api/restaurants                    → filtreli (cuisine_type, price_range: budget/mid/luxury)
POST /api/restaurants                    → auth gerekli
Cypher örneği:
  MATCH (d:Destination {id: $id})-[:HAS_RESTAURANT]->(r:Restaurant) RETURN r
Response model: RestaurantResponse

─── backend/routers/festivals.py ───
GET /api/festivals                       → filtreli (season, start_after: date, end_before: date)
GET /api/destinations/{id}/festivals     → herkese açık
POST /api/festivals                      → auth gerekli
Cypher örneği:
  MATCH (d:Destination {id: $id})-[:HAS_FESTIVAL]->(f:Festival) RETURN f
Tarih filtresi: start_after ve end_before string olarak alınır, Cypher'da karşılaştırılır

─── backend/routers/budget.py ───
POST /api/itineraries/{id}/budget → auth gerekli, BudgetPlanCreate body
GET  /api/itineraries/{id}/budget → auth gerekli
PUT  /api/itineraries/{id}/budget → auth gerekli, BudgetPlanUpdate body
Cypher: (Itinerary)-[:HAS_BUDGET]->(BudgetPlan)
Kontrol: itinerary başka kullanıcıya aitse 403 Forbidden

─── backend/routers/reviews.py ───
POST   /api/reviews               → auth zorunlu
  Body: ReviewCreate (target_id, target_type, rating, comment)
  Aynı kullanıcı aynı hedefe 2. yorum yazarsa 409 Conflict döndür
  Duplicate kontrolü Cypher:
    MATCH (u:User {id:$uid})-[:WROTE]->(r:Review)-[:ABOUT]->(t {id:$tid}) RETURN r
  Başarılıysa: Review node + (User)-[:WROTE]->(Review) + (Review)-[:ABOUT]->(target) kenarları
GET    /api/reviews               → herkese açık (?target_id=&target_type=)
  Ortalama rating da dönsün (avg_rating field)
DELETE /api/reviews/{id}          → sadece kendi yorumu silinebilir, değilse 403

─── backend/routers/tags.py ───
GET  /api/tags                           → herkese açık, tüm tag'ler
POST /api/tags                           → auth gerekli, TagBase body
POST /api/activities/{id}/tags           → aktiviteye tag ekle (M:N)
  Cypher: MERGE (a:Activity {id:$aid})-[:TAGGED_WITH]->(t:Tag {id:$tid})
DELETE /api/activities/{id}/tags/{tag_id} → tag'i aktiviteden kaldır

─── backend/routers/categories.py ───
GET /api/categories                      → herkese açık, tüm kategoriler
GET /api/categories/{id}/activities      → kategoriye göre aktiviteler
  Cypher: MATCH (a:Activity)-[:IN_CATEGORY]->(c:Category {id:$id}) RETURN a

─── backend/routers/seasons.py ───
GET /api/seasons                         → herkese açık
GET /api/destinations/{id}/seasons       → destinasyona uygun sezonlar
  Cypher: MATCH (d:Destination {id:$id})-[:BEST_IN]->(s:Season) RETURN s

─── backend/main.py güncelle ───
Yeni router'ları import edip include_router ile ekle:
  from routers import restaurants, festivals, budget, reviews, tags, categories, seasons
Her biri prefix="/api" ile eklenmeli

GENEL KURALLAR:

- Asla f-string Cypher sorgusu — her zaman parametreli
- Her endpoint için response_model belirt
- 404: kaynak bulunamadı
- 403: yetkisiz işlem
- 409: duplicate (review için)
- get_optional_user → herkese açık endpoint'ler
- get_current_user → auth gerektiren endpoint'ler
- uuid4() ile yeni node id'leri üret
- datetime.utcnow().isoformat() ile created_at

TEST:
Her router eklendikten sonra:
  uvicorn main:app --reload ile başlat
  curl <http://localhost:8000/docs> → yeni endpoint'ler görünüyor mu kontrol et
  curl <http://localhost:8000/api/restaurants> → boş liste dönmeli (seed varsa dolu olur)
  curl <http://localhost:8000/api/festivals> → boş liste veya seed verisi dönmeli

TAMAMLAYINCA:
  git add -A
  git commit -m "feat: emirhan - restaurants, festivals, budget, reviews, tags, categories, seasons"
  git push origin main

---------------------------------------------------------------------------------------------

  TravelGraph — backend/services/recommendation.py dosyasını oluştur
ve backend/routers/destinations.py içindeki /recommend endpoint'ini güncelle.

Şu Cypher sorgularını implement et:

1. Bütçe + kategori + sezon bazlı öneri:
MATCH (u:User {id: $user_id})-[:VISITED]->(visited:Destination)
MATCH (visited)<-[:LOCATED_IN]-(a:Activity)-[:IN_CATEGORY]->(c:Category)
MATCH (d:Destination)<-[:LOCATED_IN]-(a2:Activity)-[:IN_CATEGORY]->(c)
MATCH (d)<-[:LOCATED_IN]-(acc:Accommodation)
WHERE d.id <> $current_id
  AND NOT (u)-[:VISITED]->(d)
  AND acc.price_per_night <= $max_price
WITH d, count(DISTINCT c) AS category_match, avg(acc.price_per_night) AS avg_price
RETURN d, category_match, avg_price
ORDER BY category_match DESC LIMIT 5

2. Benzer kullanıcı tercihi (collaborative filtering):
MATCH (u:User {id: $user_id})-[:VISITED]->(d:Destination)
      <-[:VISITED]-(similar:User)-[:VISITED]->(rec:Destination)
WHERE NOT (u)-[:VISITED]->(rec)
  AND rec.id <> $current_id
RETURN rec, count(similar) AS overlap
ORDER BY overlap DESC LIMIT 5

3. Kısa yol (iki destinasyon arası):
MATCH path = shortestPath(
  (a:Destination {id: $from_id})-[:CONNECTED_BY*]-(b:Destination {id: $to_id})
)
RETURN path, length(path) AS hops

GET /api/destinations/{id}/recommend endpoint'i:

- Query params: user_id (optional), max_price (optional float), season (optional str)
- user_id varsa collaborative filtering + bütçe sorgusunu birleştir
- user_id yoksa sadece bütçe/kategori bazlı öneri yap
- Sonuçları DestinationResponse listesi olarak dön

Ayrıca yeni endpoint ekle:
GET /api/destinations/route?from={id}&to={id}

- İki şehir arası bağlantı zinciri döner
- Transport node'larını geçerek shortestPath hesaplar

---------------------------------------------------------------------------------------------

TravelGraph — backend/routers/itineraries.py dosyasını oluştur.

Endpoint'ler:
POST /api/itineraries           → auth gerekli, ItineraryCreate body
  Cypher: (User)-[:CREATED]->(Itinerary) kenarı oluştur

GET  /api/itineraries           → auth gerekli, sadece kendi planları
  Cypher: MATCH (u:User {id:$uid})-[:CREATED]->(i:Itinerary) RETURN i

GET  /api/itineraries/{id}      → auth gerekli (sahip veya public ise herkes)
DELETE /api/itineraries/{id}    → sadece sahibi silebilir, 403 değilse

POST /api/itineraries/{id}/stops → auth gerekli, ItineraryStopCreate body
  Cypher: (Itinerary)-[:HAS_STOP]->(ItineraryStop)-[:AT]->(Destination)
  day_number ve order ile sıralı

GET  /api/itineraries/{id}/stops → herkese açık (public plan ise)
DELETE /api/itineraries/{id}/stops/{stop_id} → sahibi silebilir

PUT /api/itineraries/{id}/stops/{stop_id}/reorder
  Body: {new_order: int}
  Cypher: stop'un order değerini güncelle

main.py'ye ekle: from routers import itineraries
Test et, commit et.

---------------------------------------------------------------------------------------------

TravelGraph backend — Yağız'ın kalan 3 görevini tamamla.

MEVCUT DURUM:

- backend/ klasöründe tüm sistem çalışıyor
- GET /api/destinations/route her zaman {"hops": -1} dönüyor (seed'de CONNECTED_BY yok)
- responsibilities/yagiz-efe-gokce.md eski (checkbox'lar işaretlenmemiş)
- Sunum için demo dosyası yok

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GÖREV 1 — Seed'e Transport Bağlantıları Ekle
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

backend/db/seed.py dosyasına yeni bir bölüm ekle (mevcut seed'i silme, sadece ekle):

Transport node'ları ve CONNECTED_BY kenarları:

Rotalar (gerçekçi fiyat ve süre):

- Istanbul → Paris      (flight, 3.5h, 120€)
- Paris → Barcelona     (train,  6.5h, 80€)
- Barcelona → Roma      (flight, 2.0h, 95€)
- Roma → Praha          (flight, 2.0h, 110€)
- Praha → Amsterdam     (train,  8.0h, 70€)
- Amsterdam → Lizbon    (flight, 2.5h, 130€)
- Tokyo → Bali          (flight, 7.0h, 200€)
- New York → Lizbon     (flight, 7.5h, 350€)
- Istanbul → Barcelona  (flight, 3.0h, 100€)
- Paris → Roma          (train,  3.0h, 90€)

Her rota için şu adımları izle:

1. Transport node oluştur:
   CREATE (t:Transport {
     id: $id, type: $type, provider: $provider,
     duration_hours: $dur, price: $price,
     departure_city: $dep, arrival_city: $arr
   })

2. İki yönlü CONNECTED_BY kenarı oluştur:
   MATCH (a:Destination {name: $dep}), (b:Destination {name: $arr})
   MATCH (t:Transport {id: $tid})
   CREATE (a)-[:CONNECTED_BY]->(t)-[:CONNECTED_BY]->(b)

Seed bittikten sonra test et:

# Istanbul ve Paris'in id'lerini bul

  python -c "
  from db.connection import get_db
  db = get_db()
  r = db.query('MATCH (d:Destination) WHERE d.name IN [\"Istanbul\",\"Paris\"] RETURN d.id, d.name')
  print(r.result_set)
  "
  
# Route endpoint'ini test et

  curl "<http://localhost:8000/api/destinations/route?from=><istanbul_id>&to=<paris_id>"

# Beklenen: {"hops": 1, "nodes": ["Istanbul", "Paris"]} veya benzeri

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GÖREV 2 — responsibilities/yagiz-efe-gokce.md Güncelle
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

responsibilities/yagiz-efe-gokce.md dosyasını aç ve güncelle:

Tamamlanan checkbox'ları işaretle:

- [x] docker-compose.yml çalışıyor (FalkorDB ayağa kalkıyor)
- [x] uvicorn main:app --reload hatasız başlıyor
- [x] /docs Swagger UI açılıyor, tüm endpoint'ler listeli
- [x] Auth: kayıt + giriş + JWT korumalı endpoint test edildi
- [x] Destination CRUD çalışıyor
- [x] Öneri endpoint'i en az 2 Cypher traversal ile çalışıyor
- [x] GET /health FalkorDB bağlantısını doğruluyor
- [x] İtinerary CRUD + stop yönetimi tamamlandı
- [x] recommendation.py servisi tamamlandı

"Kullanılan Teknolojiler" bölümüne şunu ekle:
`slowapi` · `python-bcrypt` (passlib yerine)

"Düzeltilen Hatalar" başlığı ekle (Tamamlanan Görevler'den önce):

## Çözülen Teknik Sorunlar

1. __CORS_ORIGINS parse hatası__ — pydantic-settings 2.13 ile list[str] uyumsuzluğu → str field + property ile çözüldü
2. __bcrypt API uyumsuzluğu__ — passlib 1.7.4 + bcrypt 5.0.0 çakışması → passlib kaldırılıp bcrypt doğrudan kullanıldı
3. __Seed encoding hatası__ — Windows konsolu UTF-8 desteği → sys.stdout.reconfigure(encoding="utf-8") ile çözüldü

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GÖREV 3 — Sunum Demo Dosyası
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

backend/api_test.http dosyasını oluştur.
(VS Code REST Client formatı — her istek ### ile başlar)

İçeriği:

### 1. Health Check

GET <http://localhost:8000/health>

### 2. Register

POST <http://localhost:8000/api/auth/register>
Content-Type: application/json

{
  "email": "<demo@travelgraph.com>",
  "name": "Demo Kullanici",
  "password": "Demo1234!"
}

### 3. Login

POST <http://localhost:8000/api/auth/login>
Content-Type: application/json

{
  "username": "<demo@travelgraph.com>",
  "password": "Demo1234!"
}

### 4. Tüm Destinasyonlar

GET <http://localhost:8000/api/destinations>

### 5. Destinasyon Detay (Istanbul)

GET <http://localhost:8000/api/destinations/{{istanbul_id}}>

### 6. Aktiviteler (Istanbul)

GET <http://localhost:8000/api/destinations/{{istanbul_id}}/activities>

### 7. Restoranlar (Istanbul)

GET <http://localhost:8000/api/destinations/{{istanbul_id}}/restaurants>

### 8. Festivaller (Istanbul)

GET <http://localhost:8000/api/destinations/{{istanbul_id}}/festivals>

### 9. Graf Önerisi — Bütçe Filtreli

GET <http://localhost:8000/api/destinations/{{istanbul_id}}/recommend?max_price=150>

### 10. Graf Önerisi — Kişiselleştirilmiş

GET <http://localhost:8000/api/destinations/{{istanbul_id}}/recommend?max_price=300&user_id={{user_id}}>

### 11. Graf Route — İki Şehir Arası

GET <http://localhost:8000/api/destinations/route?from={{istanbul_id}}&to={{paris_id}}>

### 12. İtinerary Oluştur (auth gerekli)

POST <http://localhost:8000/api/itineraries>
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "title": "Avrupa Turu",
  "start_date": "2026-06-01",
  "end_date": "2026-06-15",
  "is_public": true
}

### 13. İtinerary'ye Durak Ekle

POST <http://localhost:8000/api/itineraries/{{itinerary_id}}/stops>
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "destination_id": "{{istanbul_id}}",
  "day_number": 1,
  "order": 1,
  "notes": "Galata Kulesi sabah ziyareti"
}

### 14. Yorum Yaz (auth gerekli)

POST <http://localhost:8000/api/reviews>
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "target_id": "{{activity_id}}",
  "target_type": "activity",
  "rating": 5,
  "comment": "Harika bir deneyimdi!"
}

### 15. Bütçe Planı Oluştur

POST <http://localhost:8000/api/itineraries/{{itinerary_id}}/budget>
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "total_budget": 1500,
  "currency": "EUR",
  "hotel_budget": 600,
  "food_budget": 300,
  "transport_budget": 400,
  "activity_budget": 200
}

Dosyanın başına şu yorum bloğunu ekle:

# TravelGraph API Test Dosyası

# VS Code: REST Client eklentisi ile kullan

# Her ### bloğu ayrı bir istek

# {{değişken}} → gerçek ID ile değiştir

# Token almak için önce Login isteğini çalıştır

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TAMAMLAYINCA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Seed'i tekrar çalıştır (transport eklendi):
   cd backend && python -m db.seed

2. Route testini yap:
   GET /api/destinations/route?from=<istanbul_id>&to=<paris_id>
   {"hops": 1} dönmeli

3. Her şeyi commit et:
   git add -A
   git commit -m "feat: transport seed, route fix, demo dosyasi, sorumluluk raporu guncellendi"
   git push origin main

4. Sonunda şu raporu ver:
   ✅ Transport seed eklendi — route endpoint çalışıyor
   ✅ responsibilities/yagiz-efe-gokce.md güncellendi
   ✅ api_test.http oluşturuldu (15 istek)
   ✅ Push edildi

   Route test sonucu: GET /route?from=...&to=... → <sonuç>

---------------------------------------------------------------------------------------------

   TravelGraph projesini gerçekten çalışan bir uygulamaya dönüştür.
Şu an 6 kritik sorun var — hepsini düzelt.

MEVCUT SORUNLAR (gözlemlenen):

1. Planner hardcoded demo veri gösteriyor, API'ye istek atmıyor
2. Şehirler az ve seed verisi yetersiz (sadece 10 şehir, aynı etkinlikler)
3. Register/Login çalışmıyor (API bağlantısı yok)
4. Yorum yapma fonksiyonu görünmüyor
5. Festivaller Türkiye geneli değil, şehre özel
6. "Demo" yazısı var, kaldırılmalı

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GÖREV 1 — SEED VERİSİNİ KOMPLE YENİLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

backend/db/seed.py dosyasını tamamen yeniden yaz.

TÜM TÜRKİYE ŞEHİRLERİ (81 il değil, en önemli 30 şehir):
İstanbul, Ankara, İzmir, Antalya, Bursa, Adana, Gaziantep, Konya,
Mersin, Diyarbakır, Trabzon, Kayseri, Eskişehir, Samsun, Denizli,
Bodrum (Muğla), Cappadocia (Nevşehir), Pamukkale (Denizli), Safranbolu (Karabük),
Şanlıurfa, Van, Erzurum, Mardin, Afyonkarahisar, Çanakkale,
Edirne, Balıkesir, Malatya, Kahramanmaraş, Alanya (Antalya)

Her şehir için FARKLI ve GERÇEK veriler:

Her şehre özgü aktiviteler (en az 3):

- İstanbul: Ayasofya, Topkapı Sarayı, Kapalıçarşı, Boğaz Turu, Galata Kulesi
- Ankara: Anıtkabir, Anadolu Medeniyetleri Müzesi, Ankara Kalesi, Gençlik Parkı
- İzmir: Kordon, Kemeraltı Çarşısı, Efes Antik Kenti, Şirince Köyü
- Antalya: Düden Şelalesi, Kaleiçi, Aspendos Tiyatrosu, Olympos
- Kapadokya: Balon turu, Yeraltı şehirleri, Göreme Açık Hava Müzesi, At turu
- Trabzon: Sümela Manastırı, Uzungöl, Ayasofya Müzesi, Boztepe
- Mardin: Zinciriye Medresesi, Deyrulzafaran Manastırı, Mardin Müzesi
- Şanlıurfa: Balıklıgöl, Hz. İbrahim'in Doğduğu Mağara, Göbeklitepe
- Van: Van Gölü, Akdamar Kilisesi, Van Kalesi
- Çanakkale: Truva Antik Kenti, Gelibolu Yarımadası, Çimenlik Kalesi
(Diğer şehirler için de gerçek ve farklı aktiviteler yaz)

Her şehre özgü restoranlar (en az 2, gerçek mutfak türleri):

- İstanbul: Türk, Balık, Osmanlı mutfağı, Dünya mutfağı
- Gaziantep: Baklava, kebap, Antep mutfağı (gerçekten ünlü)
- İzmir: Ege mutfağı, deniz ürünleri, zeytinyağlı yemekler
- Trabzon: Karadeniz mutfağı, hamsi, mıhlama
- Şanlıurfa: Urfa kebabı, çiğ köfte, lahmacun

Her şehre özgü konaklama (en az 2):

- Fiyatlar gerçekçi: 50-800₺/gece arası
- Tipler: hotel, boutique_hotel, hostel, resort

Her şehre özgü FESTİVALLER (kritik — hepsi farklı olsun):

- İstanbul: İstanbul Film Festivali (Nisan), İstanbul Caz Festivali (Temmuz), Lale Festivali (Nisan)
- Edirne: Kırkpınar Yağlı Güreş (Temmuz)
- Antalya: Altın Portakal Film Festivali (Ekim)
- Eskişehir: Uluslararası Eskişehir Festivali (Mayıs)
- Trabzon: Trabzon Kültür Festivali (Ağustos)
- Kapadokya: Uluslararası Balon Festivali (Temmuz)
- Şanlıurfa: Uluslararası Şanlıurfa Kültür Sanat Festivali (Eylül)
- İzmir: İzmir Enternasyonal Fuarı (Eylül)
- Gaziantep: Gastronomi Festivali (Ekim)
- Van: Van Gölü Festivali (Ağustos)
(Her şehir için 1-3 gerçek festival yaz, tarihler 2025-2026 yıllarında olsun)

5 kullanıcı + gerçekçi VISITED kenarları
20 Review (farklı şehirler, aktiviteler, konaklama için)

TRANSPORT bağlantıları (mevcut 10'a ek olarak):
İstanbul↔Ankara, İstanbul↔İzmir, İstanbul↔Antalya, Ankara↔İzmir,
İzmir↔Bodrum, Antalya↔Alanya, İstanbul↔Trabzon, Ankara↔Kapadokya,
İstanbul↔Mardin, Ankara↔Şanlıurfa

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GÖREV 2 — PLANNER SAYFASINI GERÇEK API'YE BAĞLA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

frontend/src/pages/PlannerPage.tsx dosyasını tamamen yeniden yaz.

Mevcut sorun: Hardcoded demo veri var, API çağrısı yok.

Gerçek çalışan Planner:

1. Giriş kontrolü: Kullanıcı giriş yapmamışsa /login?next=/planner'a yönlendir

2. İtinerary listesi:
   GET /api/itineraries ile kullanıcının planlarını çek
   Her plan için: başlık, tarih, durak sayısı göster
   "Yeni Plan Oluştur" butonu

3. Yeni plan formu:
   - Plan adı (text input)
   - Başlangıç/bitiş tarihi (date picker)
   - Oluştur butonu → POST /api/itineraries

4. Plan detayı (seçilince):
   - Duraklar listesi (GET /api/itineraries/{id}/stops)
   - "Durak Ekle" butonu → şehir arama dropdown'u → POST /api/itineraries/{id}/stops
   - Her durak: şehir adı, gün numarası, notlar, silme butonu
   - "Bütçe Planla" butonu → /planner/{id}/budget sayfasına git
   - Drag ile sıralama (mevcut HTML5 drag&drop kullan)

5. Bütçe sayfası (/planner/:id/budget):
   POST /api/itineraries/{id}/budget endpoint'ini çağır
   Form: toplam bütçe, otel/yemek/ulaşım/aktivite kalemleri
   Gerçek zamanlı toplam hesaplama

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GÖREV 3 — AUTH (GİRİŞ/KAYIT) DÜZELT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

frontend/src/pages/LoginPage.tsx ve RegisterPage.tsx kontrol et.
frontend/src/contexts/AuthContext.tsx kontrol et.
frontend/src/api/auth.ts kontrol et.

Sorunları bul ve düzelt:

- Login formu POST /api/auth/login çağırıyor mu?
- Register formu POST /api/auth/register çağırıyor mu?
- Token localStorage'a kaydediliyor mu?
- Axios client.ts interceptor token'ı header'a ekliyor mu?
- Başarılı girişte / adresine yönlendirme var mı?
- Hata mesajları gösteriliyor mu? (yanlış şifre, email kayıtlı vb.)

Test et:
curl -X POST <http://localhost:8000/api/auth/register> \
  -H "Content-Type: application/json" \
  -d '{"email":"<test@test.com>","name":"Test","password":"Test1234!"}'

Yanıt geliyorsa frontend form da çalışmalı. Düzelt.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GÖREV 4 — YORUM YAPMA FONKSİYONU EKLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

frontend/src/pages/DestinationDetailPage.tsx dosyasına şunları ekle:

1. Aktivite kartlarının altına "Yorum Yaz" butonu:
   - Giriş yapmamışsa /login?next=... yönlendir
   - Giriş yapmışsa yorum formu aç (modal veya inline)
   - Form: 1-5 yıldız seçimi (StarRating bileşeni var) + yorum metni
   - Submit: POST /api/reviews
     body: {target_id, target_type: "activity", rating, comment}
   - Başarılıysa yorum listesini yenile

2. Konaklama kartlarına da aynı yorum formu

3. Restoran kartlarına da aynı yorum formu

4. GET /api/reviews?target_id=&target_type= ile mevcut yorumları göster
   Her yorumda: kullanıcı adı, yıldız, yorum metni, tarih

frontend/src/components/ReviewForm.tsx zaten var — onu kullan.
frontend/src/api/reviews.ts zaten var — onu kullan.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GÖREV 5 — FESTİVALLER SAYFASI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

frontend/src/pages/FestivalsPage.tsx dosyasını güncelle.

Mevcut sorun: Festivaller şehre özgü değil veya yanlış görünüyor.

Düzeltme:

- GET /api/festivals tüm Türkiye festivallerini döndürmeli
- Şehir filtresi: dropdown ile şehir seç → o şehrin festivalleri
- Tarih filtresi: yaklaşan festivaller (start_date >= bugün)
- "Bu ay" / "Sonraki 3 ay" / "Bu yıl" filtre butonları
- Her festival kartı: festival adı, şehir, tarih aralığı, açıklama

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GÖREV 6 — "DEMO" YAZISINI KALDIR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tüm frontend dosyalarında "Demo", "Turkey Demo", "TravelGraph • Turkey Demo"
gibi placeholder metinleri bul ve kaldır.

HomePage.tsx hero bölümündeki badge: "TravelGraph • Turkey Demo" → kaldır
Başka demo/placeholder metinler varsa hepsini temizle.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TEST VE KOMİT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Seed'i yeniden çalıştır:
   cd backend && python -m db.seed

2. Backend'i başlat:
   uvicorn main:app --reload

3. Frontend'i başlat:
   cd frontend && npm run dev

4. Şunları test et:
   a) Register: yeni kullanıcı kaydı çalışıyor mu?
   b) Login: token alınıyor mu?
   c) Explore: 30 şehir görünüyor mu?
   d) Planner: plan oluşturulabiliyor mu?
   e) Festivaller: farklı şehirlerde farklı festivaller var mı?
   f) Yorum: aktiviteye yorum yazılabiliyor mu?

5. Hata varsa düzelt, tekrar test et.

6. Her şey çalışınca commit et:
   git add -A
   git commit -m "feat: gercek veri, planner API entegrasyonu, auth, yorumlar, 30 sehir"
   git push origin main

7. Rapor ver:
   ✅/❌ Register çalışıyor
   ✅/❌ Login çalışıyor
   ✅/❌ 30 şehir görünüyor
   ✅/❌ Planner API'ye bağlı
   ✅/❌ Festivaller şehre özel
   ✅/❌ Yorum yapılabiliyor
   ✅/❌ Demo yazısı kaldırıldı

---------------------------------------------------------------------------------------------

   TravelGraph — Emirhan'ın merge edilen kodunu entegre et ve test et.

GÖREV 1 — BACKEND ENTEGRASYONunu DOĞRULA
En son kodu çek:
  git pull origin main

backend/routers/ klasörüne bak — şu dosyalar var mı kontrol et:
  reviews.py, restaurants.py, festivals.py, budget.py,
  tags.py, categories.py, seasons.py

Eksik dosya varsa bildir.

GÖREV 2 — BACKEND TESTİ
Backend'i başlat:
  cd backend && uvicorn main:app --reload

<http://localhost:8000/docs> adresinde şu endpoint'lerin görünüp görünmediğini kontrol et:
  curl <http://localhost:8000/openapi.json> | python -m json.tool | grep '"path"'

Eksik endpoint varsa bildir.

GÖREV 3 — KRİTİK API TESTLERİ
Token al:
  curl -X POST <http://localhost:8000/api/auth/login> \
    -d "username=<ayse@example.com>&password=Test1234!"

Sonra şunları test et:
  a) GET /api/restaurants → liste dönmeli
  b) GET /api/festivals   → 26 festival dönmeli
  c) GET /api/categories  → 3 kategori dönmeli
  d) GET /api/tags        → tag listesi dönmeli
  e) GET /api/seasons     → 4 sezon dönmeli
  f) POST /api/reviews (token ile) → yorum oluşturulabilmeli
  g) POST /api/itineraries/{id}/budget (token ile) → bütçe oluşturulabilmeli

GÖREV 4 — FRONTEND BAĞLANTISI
Frontend'i başlat:
  cd frontend && npm run dev

Şunları test et:
  a) <http://localhost:5173/explore> → restoranlar ve festivaller görünüyor mu?
  b) <http://localhost:5173/festivals> → Emirhan'ın festival verileri geliyor mu?
  c) Bir destinasyona gir → yorum formu çalışıyor mu?
  d) Bir aktiviteye yorum yaz → POST /api/reviews çağrısı başarılı mı?

GÖREV 5 — SCREENSHOTS AL (KRİTİK!)
Her sayfa için screenshot al ve screenshots/ klasörüne kaydet:

- screenshots/home.png         → <http://localhost:5173>
- screenshots/explore.png      → <http://localhost:5173/explore>
- screenshots/destination-detail.png → herhangi bir şehir detayı
- screenshots/festivals.png    → <http://localhost:5173/festivals>
- screenshots/planner.png      → giriş yap, plan oluştur, ekranı yakala
- screenshots/api-docs.png     → <http://localhost:8000/docs>

GÖREV 6 — COMMIT
git add screenshots/
git commit -m "docs: uygulama screenshots eklendi - tum sayfalar"
git push origin main

RAPOR:
Her endpoint için ✅/❌
Her screenshot için ✅/❌
Varsa hatalar ve çözümleri

---------------------------------------------------------------------------------------------

TravelGraph frontend'ini Stitch tasarımlarına göre güncelle.

ADIM 1 — Stitch MCP Bağlantısını Kur
Stitch MCP zaten ekli:
  URL: <https://stitch.googleapis.com/mcp>
  Header: X-Goog-Api-Key: AQ.Ab8RN6IfqNeNKoPhX18T_J5xfg6vvQGuoxKM6dE1qII0BBvOig

Stitch MCP araçlarını listele — hangi araçlar mevcut?

ADIM 2 — Tasarımları Çek
Stitch MCP araçlarını kullanarak mevcut projenin tasarımlarını al:

- Tüm tasarım ekranlarını listele
- Her ekranın HTML/CSS kodunu çek
- Varsa DESIGN.md dosyasını al (renk paleti, tipografi, spacing sistemi)

ADIM 3 — Mevcut Frontend ile Karşılaştır
frontend/src/pages/ klasöründeki sayfaları oku:

- HomePage.tsx
- ExplorePage.tsx
- DestinationDetailPage.tsx
- PlannerPage.tsx
- FestivalsPage.tsx
- LoginPage.tsx / RegisterPage.tsx

Her sayfa için:

- Stitch tasarımındaki ile mevcut React kodunu karşılaştır
- Farklılıkları tespit et (renkler, layout, bileşenler)

ADIM 4 — Tasarımları Uygula
Her sayfa için Stitch tasarımını React + Tailwind CSS'e dönüştür:

Kurallar:

- Mevcut API bağlantılarını (useDestinations, useFestivals vb.) KORU
- Sadece görsel katmanı (UI) güncelle, iş mantığına dokunma
- TypeScript tiplerini koru
- Tailwind CSS kullan (başka CSS kütüphanesi ekleme)
- Responsive tasarım (mobil uyumlu)
- Bileşen yapısını koru (components/ klasöründeki bileşenleri güncelle)

ADIM 5 — Stitch'te Olmayan Sayfalar
Stitch'te tasarımı olmayan sayfalar varsa:

- Mevcut tasarım sistemini (renkler, tipografi) kullanarak kendin yap
- Stitch'teki diğer sayfalardaki UI pattern'lerini takip et

ADIM 6 — TEST
Frontend'i başlat:
  cd frontend && npm run dev

Her sayfayı kontrol et:

- Tasarım uygulandı mı?
- API çağrıları çalışıyor mu? (gerçek veri geliyor mu)
- Console'da hata var mı?
- Mobil görünüm sorunsuz mu?

ADIM 7 — SCREENSHOTS GÜNCELLE
Yeni tasarımla screenshots al ve screenshots/ klasörünü güncelle:

- screenshots/home.png
- screenshots/explore.png
- screenshots/destination-detail.png
- screenshots/festivals.png
- screenshots/planner.png
- screenshots/api-docs.png  (değişmeyecek)

ADIM 8 — COMMIT
git add -A
git commit -m "feat: stitch tasarim sistemi uygulandı - tum sayfalar guncellendi"
git push origin main

RAPOR:

- Hangi sayfalar güncellendi?
- Hangi tasarım değişiklikleri yapıldı? (renkler, layout vb.)
- Varsa karşılaşılan sorunlar

---------------------------------------------------------------------------------------------

TravelGraph'ı Railway + Vercel'e deploy için hazırla.

GÖREV 1 — backend/Procfile oluştur:
web: uvicorn main:app --host 0.0.0.0 --port $PORT

GÖREV 2 — backend/railway.json oluştur:
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}

GÖREV 3 — backend/core/config.py'yi güncelle:
FALKORDB_URL env variable desteği ekle:

- Eğer FALKORDB_URL varsa → redis://host:port formatını parse et
- host ve port'u FALKORDB_HOST ve FALKORDB_PORT olarak kullan
- Yoksa mevcut FALKORDB_HOST + FALKORDB_PORT kullan

GÖREV 4 — backend/db/connection.py'yi güncelle:
config.py'deki Settings'ten host/port al, doğrudan os.getenv yerine.

GÖREV 5 — backend/core/config.py'de CORS güncelle:
CORS_ORIGINS'e şunları ekle (production URL'leri):
  <https://travelgraph.vercel.app>
  <https://travelgraph-production.up.railway.app>

GÖREV 6 — frontend/vercel.json oluştur:
{
  "rewrites": [
    {"source": "/(.*)", "destination": "/index.html"}
  ]
}

GÖREV 7 — frontend/.env.production oluştur:
VITE_API_URL=<https://travelgraph-backend.up.railway.app>

GÖREV 8 — frontend/src/api/client.ts kontrol et:
baseURL'in import.meta.env.VITE_API_URL kullandığından emin ol.
Kullanmıyorsa güncelle.

GÖREV 9 — backend/requirements.txt'e gunicorn ekle (Railway için)

GÖREV 10 — .gitignore kontrol et:
backend/.env satırı var mı? Yoksa ekle.
frontend/.env.local satırı var mı? Yoksa ekle.

GÖREV 11 — Tüm değişiklikleri push et:
git add -A
git commit -m "feat: railway + vercel deploy konfigurasyonu"
git push origin main

RAPOR:
Oluşturulan/güncellenen dosyaların listesi
Push başarılı mı?

  ---------------------------------------------------------------------------------------------
  ---------------------------------------------------------------------------------------------

TravelGraph deploy sorunlarını düzelt. 3 görev var.

GÖREV 1 — backend/railway.json düzelt (Railpack hatası):
Dosyayı tamamen şu içerikle yeniden yaz:
{
  "$schema": "https://railway.app/railway.schema.json",
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
NOT: "build" bölümünü tamamen kaldır — Railway kendi algılasın.

GÖREV 2 — frontend/index.html title düzelt:
<title> tagini bul:
  Eski: <title>frontend</title> veya <title>Vite App</title>
  Yeni: <title>TravelGraph</title>

GÖREV 3 — backend/main.py CORS düzelt:
Mevcut CORS_ORIGINS ayarını bul.
Şu origins'in kesinlikle dahil olduğundan emin ol:

- <https://travel-graph.vercel.app>   ← Vercel URL'i bu!
- <https://travelgraph.vercel.app>    ← alternatif
- <http://localhost:5173>

NOT: Vercel URL'i "travel-graph.vercel.app" (tire ile), "travelgraph.vercel.app" değil!

Şu anda Railway Variables'taki CORS_ORIGINS değeri:
  <https://travelgraph.vercel.app,http://localhost:5173>
Bu yanlış! Doğru URL: <https://travel-graph.vercel.app>

backend/core/config.py içindeki default CORS_ORIGINS değerini de güncelle.

GÖREV 4 — Commit ve push:
git add backend/railway.json frontend/index.html backend/core/config.py backend/main.py
git commit -m "fix: railpack builder kaldirildi, cors travel-graph.vercel.app eklendi, title guncellendi"
git push origin main

RAPOR:
railway.json içeriği (build bölümü YOK mu?)
index.html title değeri
CORS origins listesi (travel-graph.vercel.app var mı?)
Push başarılı mı?
