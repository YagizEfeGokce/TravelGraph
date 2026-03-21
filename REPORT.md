# REPORT.md — TravelGraph

## 1. İş Problemi ve Motivasyon

Seyahat planlamak dağınık ve zaman alıcı bir süreçtir: gezginler destinasyon araştırması, konaklama seçimi, restoran keşfi, aktivite planlaması, festival takibi ve bütçe yönetimini birden fazla platform üzerinden yürütmek zorunda kalır.

**TravelGraph**, bu süreci tek bir platformda birleştiren, kullanıcı davranışlarını graf yapısında modelleyerek **kişiselleştirilmiş, bütçeye uygun rota önerileri** sunan bir SaaS web uygulamasıdır.

### Çözülen Problem

| Problem | TravelGraph Çözümü |
|---------|-------------------|
| Dağınık planlama araçları | Tek platformda destinasyon + otel + yemek + aktivite + festival |
| Kişisel olmayan öneriler | FalkorDB graf traversal ile kullanıcı davranış analizi |
| Bütçe takibinin zorluğu | Kalem kalem harcama planı (otel/yemek/ulaşım/aktivite) |
| İçerik için zorunlu kayıt | Giriş gerektirmeden gezme; yalnızca yorum için kayıt |

### Neden Graf Veritabanı?

Seyahat verisinde ilişkiler birinci sınıf vatandaştır:
- Bir kullanıcı birden fazla destinasyonu ziyaret eder
- Bir destinasyon onlarca aktivite, restoran, festival barındırır
- Bir aktivite birden fazla kategoriye ve etikete aittir
- Bütçe planı otel, yemek, ulaşım ve aktivite kalemleriyle ilişkilidir

Bu çok katmanlı ilişki ağı üzerinde **"Bütçesi 500€, müze seven, Nisan'da seyahat edecek kullanıcıya hangi destinasyonu önerelim?"** gibi sorgular ilişkisel veritabanlarında onlarca JOIN gerektirir. FalkorDB'de tek bir Cypher traversal ile milisaniyeler içinde yanıtlanır.

---

## 2. Teknik Mimari

### 2.1 Teknoloji Yığını

| Katman | Teknoloji | Versiyon | Gerekçe |
|--------|-----------|----------|---------|
| Backend API | FastAPI | 0.115 | Async, otomatik OpenAPI/Swagger, Pydantic entegrasyonu |
| Veritabanı | FalkorDB | Latest | Graf modeli, Cypher sorgu dili, Redis uyumlu |
| Frontend | React + Vite | 18 / 5 | Hızlı geliştirme, component tabanlı, HMR |
| Validasyon | Pydantic v2 | 2.x | Tip güvenliği, otomatik şema üretimi |
| HTTP İstemci | Axios | 1.x | Interceptor desteği, token yönetimi |
| Sunucu Durumu | React Query | 5.x | Cache, background refetch, loading state |
| Stil | Tailwind CSS | 3.x | Utility-first, responsive tasarım |
| Konteyner | Docker | — | FalkorDB kolay kurulum ve izolasyon |

### 2.2 Sistem Mimarisi

```
[Tarayıcı — React + Vite]
        │ HTTP/JSON
        ▼
[FastAPI Backend]
   ├── CORS Middleware
   ├── JWT Auth Middleware (opsiyonel endpoint'ler açık)
   ├── Rate Limiting (slowapi)
   ├── Global Exception Handler
   ├── Routers (14 entity için REST endpoint'ler)
   ├── Pydantic v2 Validasyon
   └── Services (öneri motoru, bütçe hesaplama)
        │ Cypher Query (parametreli)
        ▼
[FalkorDB Graf Veritabanı]
   ├── 14 Node tipi
   ├── 15+ Edge (ilişki) tipi
   └── Graf indeksleri (performans)
```

### 2.3 Veri Modeli

**Node'lar (14 Entity):**

```
User          {id, name, email, password_hash, created_at}
Destination   {id, name, country, lat, lng, description, population}
Itinerary     {id, title, start_date, end_date, is_public, created_at}
ItineraryStop {id, day_number, order, notes}
Activity      {id, name, description, duration_hours, price, address}
Accommodation {id, name, type, star_rating, price_per_night, address}
Transport     {id, type, provider, duration_hours, price, departure, arrival}
Restaurant    {id, name, cuisine_type, price_range, address, rating}
Festival      {id, name, description, start_date, end_date, is_recurring}
BudgetPlan    {id, total_budget, currency, hotel_budget, food_budget,
               transport_budget, activity_budget, created_at}
Review        {id, rating, comment, created_at}
Season        {id, name, months, avg_temp_c, weather_description}
Category      {id, name, icon, description}
Tag           {id, name, color}
```

**Edge'ler (İlişkiler):**

```
(User)-[:VISITED]->(Destination)              M:N
(User)-[:CREATED]->(Itinerary)
(User)-[:WROTE]->(Review)
(Itinerary)-[:HAS_STOP]->(ItineraryStop)
(Itinerary)-[:HAS_BUDGET]->(BudgetPlan)
(ItineraryStop)-[:AT]->(Destination)
(Destination)-[:HAS_ACTIVITY]->(Activity)
(Destination)-[:HAS_ACCOMMODATION]->(Accommodation)
(Destination)-[:HAS_RESTAURANT]->(Restaurant)
(Destination)-[:HAS_FESTIVAL]->(Festival)
(Destination)-[:CONNECTED_BY]->(Transport)
(Destination)-[:BEST_IN]->(Season)
(Activity)-[:IN_CATEGORY]->(Category)         M:N
(Activity)-[:TAGGED_WITH]->(Tag)              M:N
(Restaurant)-[:IN_CATEGORY]->(Category)       M:N
(Festival)-[:IN_SEASON]->(Season)
(Review)-[:ABOUT]->(Activity | Accommodation | Restaurant)
```

---

## 3. Uygulanan Kavramlar ve Teknolojiler

### 3.1 FastAPI

- **Router yapısı**: Her entity için ayrı router modülü (`/api/destinations`, `/api/restaurants`, `/api/festivals`...)
- **Dependency Injection**: `get_db()` ile veritabanı bağlantısı, `get_current_user()` ile auth — isteğe bağlı dependency ile opsiyonel auth
- **Opsiyonel auth**: İçerik endpoint'leri herkese açık; yorum endpoint'leri JWT zorunlu
- **Background Tasks**: Öneri skoru güncelleme asenkron
- **Global Exception Handler**: Tutarlı hata yanıtı formatı
- **Rate Limiting**: `slowapi` ile IP bazlı istek sınırı

### 3.2 Pydantic v2 Validasyon

Her entity için dört şema katmanı:
- `Base`: Ortak alanlar
- `Create`: Yeni kayıt için kullanıcı girdisi (kısıtlamalar burada)
- `Update`: Kısmi güncelleme (tüm alanlar `Optional`)
- `Response`: API yanıtı (parola hash'i gibi hassas alanlar hariç)

Özel validasyonlar:
```python
# Koordinat aralığı
@field_validator('lat')
def validate_lat(cls, v):
    if not -90 <= v <= 90:
        raise ValueError('Enlem -90 ile 90 arasında olmalı')
    return v

# Tarih mantığı
@model_validator(mode='after')
def validate_dates(self):
    if self.start_date >= self.end_date:
        raise ValueError('Başlangıç tarihi bitiş tarihinden önce olmalı')
    return self

# Bütçe toplamı kontrolü
@model_validator(mode='after')
def validate_budget_sum(self):
    total = self.hotel_budget + self.food_budget + self.transport_budget + self.activity_budget
    if total > self.total_budget:
        raise ValueError('Kalem toplamı toplam bütçeyi aşamaz')
    return self
```

### 3.3 FalkorDB — Graf Veritabanının Katkısı

**Neden graf?** İlişkisel veritabanlarında "kullanıcının ziyaret ettiği şehirlerdeki müzelere benzer müzeleri olan, Nisan'da festival olan ve bütçeye uygun otel bulunan şehirleri bul" sorgusu birden fazla tablo join'i gerektirir. FalkorDB'de:

```cypher
MATCH (u:User {id: $uid})-[:VISITED]->(v:Destination)
      <-[:LOCATED_IN]-(a:Activity)-[:IN_CATEGORY]->(c:Category {name:"Museum"})
MATCH (d:Destination)<-[:LOCATED_IN]-(a2:Activity)-[:IN_CATEGORY]->(c)
MATCH (d)<-[:HELD_IN]-(f:Festival)-[:IN_SEASON]->(s:Season {name:"Spring"})
MATCH (d)<-[:LOCATED_IN]-(acc:Accommodation)
WHERE acc.price_per_night <= $hotel_budget / $nights
  AND NOT (u)-[:VISITED]->(d)
RETURN d.name, count(DISTINCT a2) AS museum_count, collect(f.name) AS festivals
ORDER BY museum_count DESC LIMIT 5
```

Bu tek sorgu; User, Destination, Activity, Category, Festival, Season ve Accommodation node'larını geçer.

**M:N ilişkilerin doğal modellenmesi**: Activity↔Category ve Activity↔Tag ilişkileri ara tablo gerektirmeden graf kenarlarıyla temsil edilir.

**Graf algoritmaları**: İki destinasyon arasındaki en kısa ulaşım rotası için Cypher `shortestPath()` fonksiyonu kullanılır.

### 3.3.1 FalkorDB Graf Sorgusu Örnekleri

Aşağıdaki üç sorgu `backend/services/recommendation.py` dosyasında canlı olarak çalışmakta ve seed verisiyle test edilmiştir. Her sorguda ilişkisel veritabanı karşılığının kaç JOIN gerektireceği hesaplanmıştır.

---

#### Sorgu 1 — Bütçe + Kategori Eşleşmesi (Budget & Category Match)

```cypher
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
```

**Ne yapar?** Kullanıcının daha önce ziyaret ettiği destinasyonlardaki aktivitelerin kategorilerini belirler; aynı kategorilerde aktivitesi olan ve bütçeye uygun konaklaması bulunan henüz ziyaret edilmemiş destinasyonları sıralar.

**SQL karşılığı:**

| # | JOIN |
|---|------|
| 1 | `users` → `user_visited_destinations` (VISITED M:N ara tablo) |
| 2 | `user_visited_destinations` → `destinations` (visited) |
| 3 | `destinations` → `activities` a (LOCATED_IN — ziyaret edilen dest. aktiviteleri) |
| 4 | `activities` → `activity_categories` (IN_CATEGORY M:N ara tablo) |
| 5 | `activity_categories` → `categories` c |
| 6 | `activity_categories` ac2 → `categories` c (aynı kategori, aday aktiviteler) |
| 7 | `activity_categories` ac2 → `activities` a2 |
| 8 | `activities` a2 → `destinations` d (LOCATED_IN — aday destinasyon) |
| 9 | `destinations` d → `accommodations` (LOCATED_IN — fiyat filtresi) |
| + | `NOT EXISTS` alt sorgusu: `user_visited_destinations` (NOT VISITED kontrolü) |

> **Bu sorgu ilişkisel veritabanında 9 adet JOIN gerektirir** (+ 1 NOT EXISTS alt sorgusu).
> FalkorDB'de tek bir Cypher traversal ile milisaniyeler içinde yanıtlanır.

---

#### Sorgu 2 — İşbirlikçi Filtreleme (Collaborative Filtering)

```cypher
MATCH (u:User {id: $user_id})-[:VISITED]->(d:Destination)
      <-[:VISITED]-(similar:User)-[:VISITED]->(rec:Destination)
WHERE NOT (u)-[:VISITED]->(rec)
  AND rec.id <> $current_id
RETURN rec, count(similar) AS overlap
ORDER BY overlap DESC LIMIT 5
```

**Ne yapar?** Kullanıcıyla en az bir ortak ziyaret destinasyonu paylaşan "benzer" kullanıcıları bulur; bu kullanıcıların gittiği, asıl kullanıcının henüz görmediği destinasyonları ortak kullanıcı sayısına göre sıralar.

**SQL karşılığı:**

| # | JOIN |
|---|------|
| 1 | `users` u → `user_visited_destinations` uvd1 (u'nun ziyaretleri) |
| 2 | `user_visited_destinations` uvd1 → `destinations` d (ortak destinasyon) |
| 3 | `user_visited_destinations` uvd2 → `destinations` d (aynı destinasyonu ziyaret eden diğerleri) |
| 4 | `user_visited_destinations` uvd2 → `users` similar (benzer kullanıcılar) |
| 5 | `users` similar → `user_visited_destinations` uvd3 (similar'ın ziyaretleri) |
| 6 | `user_visited_destinations` uvd3 → `destinations` rec (önerilecek destinasyon) |
| + | `NOT EXISTS` alt sorgusu: `user_visited_destinations` (NOT VISITED kontrolü) |

> **Bu sorgu ilişkisel veritabanında 6 adet JOIN gerektirir** (+ 1 NOT EXISTS alt sorgusu).
> Graf modelinde ise üç `VISITED` kenarı tek bir MATCH satırında zincirlenir.

---

#### Sorgu 3 — En Kısa Rota (ShortestPath)

```cypher
MATCH (a:Destination {id: $from_id}), (b:Destination {id: $to_id})
RETURN shortestPath((a)-[:CONNECTED_BY*]->(b)) AS path
```

**Ne yapar?** İki destinasyon arasındaki `CONNECTED_BY` (Transport) kenarları üzerinden minimum aktarmalı rotayı bulur. `shortestPath()` BFS (Breadth-First Search) algoritmasını dahili olarak çalıştırır; sonuç tam node ve edge listesini içeren bir Path nesnesidir.

**SQL karşılığı:**

Sabit derinlikte bir yol biliniyorsa N JOIN yeterlidir; ancak `CONNECTED_BY*` ifadesi **bilinmeyen derinlikte** yinelemeli traversal demektir. SQL'de bu zorunlu olarak Recursive CTE gerektirir:

```sql
WITH RECURSIVE route AS (
  SELECT from_destination_id, to_destination_id, 1 AS hops,
         ARRAY[from_destination_id] AS path
  FROM transports WHERE from_destination_id = :from_id
  UNION ALL
  SELECT t.from_destination_id, t.to_destination_id, r.hops + 1,
         r.path || t.from_destination_id
  FROM transports t
  JOIN route r ON t.from_destination_id = r.to_destination_id   -- her hop'ta 1 JOIN
  WHERE NOT t.from_destination_id = ANY(r.path) AND r.hops < 20
)
SELECT r.*, d1.name, d2.name
FROM route r
JOIN destinations d1 ON r.from_destination_id = d1.id           -- JOIN (başlangıç adı)
JOIN destinations d2 ON r.to_destination_id   = d2.id           -- JOIN (bitiş adı)
WHERE r.to_destination_id = :to_id
ORDER BY r.hops ASC LIMIT 1;
```

| Hop Sayısı | Toplam JOIN Eşdeğeri |
|------------|----------------------|
| 1 hop | 3 JOIN |
| 2 hop | 4 JOIN |
| 3 hop | 5 JOIN |
| N hop | N + 2 JOIN |

> **Bu sorgu ilişkisel veritabanında hop başına 1 JOIN + 2 sabit JOIN gerektirir; derinlik bilinmediğinden recursive CTE zorunludur (10+ hop'ta 12+ JOIN eşdeğeri).**
> FalkorDB'de `shortestPath()` tek satır Cypher ile native BFS olarak çalışır; ek JOIN ya da recursive yapı gerekmez.

### 3.4 React + Vite Frontend

- **React Query**: Sunucu durumu yönetimi, otomatik cache geçersizleştirme
- **React Router v6**: Nested route desteği ile `ProtectedRoute` bileşeni
- **Axios Interceptor**: Her isteğe JWT ekleme; 401'de token yenileme
- **AuthContext**: Global kimlik doğrulama durumu
- **Opsiyonel auth UI**: Giriş yapmadan içerik görünür; yorum formu giriş butonuna yönlendirir

### 3.5 Güvenlik ve Sağlamlık

| Tehdit | Önlem |
|--------|-------|
| Şifre sızıntısı | bcrypt ile hashleme, Response şemada parola alanı yok |
| Token sahteciliği | JWT HS256, kısa ömürlü access token + refresh token |
| Cypher injection | Tüm sorgular parametreli — f-string kullanımı yok |
| Kaba kuvvet | Rate limiting (slowapi), 5 başarısız girişte 15 dk blok |
| XSS | Axios ile JSON iletişim, HTML render edilmez |
| CORS | Yalnızca frontend origin'e izin |
| Yetkisiz erişim | Dependency injection ile endpoint bazlı auth kontrolü |

---

## 4. API Endpoint Özeti

| Method | Endpoint | Auth | Açıklama |
|--------|----------|------|---------|
| POST | /api/auth/register | — | Kayıt |
| POST | /api/auth/login | — | Giriş, JWT döner |
| GET | /api/destinations | — | Destinasyon listesi |
| GET | /api/destinations/{id} | — | Destinasyon detay |
| GET | /api/destinations/{id}/recommend | — | Graf tabanlı öneri |
| GET | /api/destinations/{id}/activities | — | Aktiviteler |
| GET | /api/destinations/{id}/restaurants | — | Restoranlar |
| POST | /api/restaurants | — | Yeni restoran ekle |
| GET | /api/destinations/{id}/festivals | — | Festival takvimi |
| GET | /api/destinations/{id}/accommodations | — | Konaklamalar |
| POST | /api/itineraries | ✓ | Seyahat planı oluştur |
| POST | /api/itineraries/{id}/stops | ✓ | Durak ekle |
| POST | /api/itineraries/{id}/budget | ✓ | Bütçe planı oluştur |
| GET | /api/itineraries/{id}/budget | ✓ | Bütçe planı görüntüle |
| PUT | /api/itineraries/{id}/budget | ✓ | Bütçe planı güncelle |
| POST | /api/reviews | ✓ | Yorum yaz |
| GET | /api/reviews | — | Yorumları listele |
| DELETE | /api/reviews/{id} | ✓ | Yorumu sil |
| GET | /api/restaurants | — | Restoran listesi |
| GET | /api/festivals | — | Festival listesi (tarih filtreli) |
| POST | /api/festivals | — | Yeni festival ekle |
| GET | /api/tags | — | Etiketler |
| GET | /api/categories | — | Kategoriler |
| POST | /api/activities/{id}/tags | — | Aktiviteye etiket ekle |
| GET | /api/categories/{id}/activities | — | Kategoriye göre aktiviteler |
| GET | /api/seasons | — | Sezonlar |

---

## 5. Prompt Mühendisliği Yaklaşımı

Bu projede AI araçları (Google Antigravity, Claude) şu şekillerde kullanılmıştır:

**Mimari Tasarım**: Varlık ilişki diyagramı ve Cypher sorgu optimizasyonu için Claude ile iteratif diyalog. Graf şemasının seyahat domainini doğal modellediğini doğrulamak için birden fazla revizyon yapıldı.

**Kod Üretimi**: Antigravity ile Pydantic model şablonları, FastAPI router iskeletleri ve React component'leri üretildi. Her üretimde proje bağlamı ve teknoloji kısıtları prompt'a eklendi.

**Prompt Kalitesi**: Şu teknikler uygulandı:
- **Bağlam verme**: Proje adı, teknoloji yığını, mevcut dosya yapısı her prompt'ta belirtildi
- **Kısıt belirtme**: "Pydantic v2 syntax kullan", "f-string Cypher sorgusu yazma" gibi açık kısıtlar
- **Çıktı formatı**: "Yalnızca şu dosyayı oluştur" ile kapsam sınırlandırması
- **Few-shot**: Mevcut kod örnekleri gösterilerek tutarlılık sağlandı

---

## 6. Ekip ve Sorumluluklar

Detaylı dağılım için `responsibilities/` klasörüne bakınız.

| Üye | Rol | Ana Sorumluluk |
|-----|-----|---------------|
| Yağız Efe Gökçe | Mimar & Backend | FalkorDB, FastAPI core, Auth, Öneri motoru |
| Berfin Aksoy | Frontend | React sayfaları, UI/UX, API entegrasyonu |
| Emirhan Polat | Feature & Dokümantasyon | Restaurant/Festival/BudgetPlan, Seed, Raporlama |

---

## 7. Kurulum

Bkz. [README.md](./README.md)

---

## 8. Sonuç

TravelGraph, modern web teknolojilerini (FastAPI, React, FalkorDB) gerçek bir iş problemi etrafında birleştiren üretim kalitesinde bir SaaS prototipidir. Graf veritabanı seçimi rastgele değil; seyahat verisinin doğasından kaynaklanan ilişki-yoğun yapıya verilen bilinçli bir yanıttır. 14 entity, 15+ edge tipi ve M:N ilişkilerle modellenen bu yapı; bütçe-duyarlı, mevsim-bilinçli ve davranış tabanlı öneri sorgularını tek bir Cypher traversal ile çözebilmektedir.
