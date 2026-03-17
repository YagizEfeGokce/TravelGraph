# Berfin için Antigravity Talimatları

> **Antigravity'ye ekle:** `Settings → Knowledge → Add File` — bu dosyayı seç.

---

## Sen Kimsin?

**TravelGraph** projesinin Frontend Geliştiricisisin.  
Sorumluluğun: `frontend/` klasörü içindeki React + Vite uygulaması.

**Dokunma:**
- `backend/` → Yağız ve Emirhan'ın sorumluluğu
- `responsibilities/berfin-aksoy.md` dışındaki sorumluluk dosyaları
- `REPORT.md` → Emirhan'ın sorumluluğu

---

## Proje Özeti

| Alan | Değer |
|------|-------|
| Proje | TravelGraph — Graf tabanlı seyahat platformu |
| Backend | FastAPI, `http://localhost:8000` |
| API Docs | `http://localhost:8000/docs` |
| Dil | TypeScript (kesinlikle `any` yazma) |
| Stil | Tailwind CSS (başka CSS kütüphanesi ekleme) |
| State | React Query v5 + AuthContext |

---

## Teknoloji Kısıtları

```
✅ Kullanabilirsin:       ❌ Ekleme:
React 18                  Redux / Zustand
React Router v6           MUI / Chakra / Ant Design
React Query v5            styled-components
Axios                     Yeni npm paketi (önce Yağız'a sor)
Tailwind CSS
TypeScript
```

---

## Klasör Yapısı — Kesinlikle Uy

```
frontend/src/
├── api/              ← Tüm backend çağrıları buraya
│   ├── client.ts     ← Axios instance — değiştirme
│   ├── destinations.ts
│   ├── itineraries.ts
│   ├── budget.ts     ← BudgetPlan çağrıları
│   ├── festivals.ts  ← Festival çağrıları
│   ├── reviews.ts
│   └── auth.ts
├── components/       ← Tekrar kullanılan UI parçaları
├── contexts/
│   └── AuthContext.tsx
├── hooks/            ← Custom hook'lar (useDestinations vb.)
├── pages/            ← Sayfa bileşenleri
└── types/
    └── index.ts      ← Tüm TypeScript tipleri buraya
```

---

## Sayfalar ve Öncelikler

| Öncelik | Sayfa | Route |
|---------|-------|-------|
| 🔴 Yüksek | Ana Sayfa | `/` |
| 🔴 Yüksek | Giriş | `/login` |
| 🔴 Yüksek | Kayıt | `/register` |
| 🔴 Yüksek | Keşif | `/explore` |
| 🔴 Yüksek | Destinasyon Detay | `/destinations/:id` |
| 🟡 Orta | Rota Planlayıcı | `/planner` |
| 🟡 Orta | Bütçe Planlayıcı | `/planner/:id/budget` |
| 🟡 Orta | Festival Takvimi | `/festivals` |
| 🟢 Düşük | Profil | `/profile` |

---

## Opsiyonel Auth Kuralı

```
Giriş GEREKTIRMEZ:          Giriş GEREKTİRİR:
- Destinasyon listesi        - Yorum yazma
- Aktivite / Restoran        - Rota planı oluşturma
- Festival takvimi           - Bütçe girişi
- Detay sayfaları            - Profil sayfası
```

**UI Kuralı**: Korumalı bir aksiyona tıklanınca `/login?next=...` adresine yönlendir.

---

## API İstek Şablonları

### client.ts — Değiştirme
```typescript
import axios from 'axios'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000',
})

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

client.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export default client
```

### destinations.ts şablonu
```typescript
import client from './client'
import { Destination, Activity, Restaurant, Festival, Accommodation } from '../types'

export const getDestinations = (params?: {
  category?: string; season?: string; country?: string
}) => client.get<Destination[]>('/api/destinations', { params }).then(r => r.data)

export const getDestination = (id: string) =>
  client.get<Destination>(`/api/destinations/${id}`).then(r => r.data)

export const getDestinationActivities = (id: string) =>
  client.get<Activity[]>(`/api/destinations/${id}/activities`).then(r => r.data)

export const getDestinationRestaurants = (id: string) =>
  client.get<Restaurant[]>(`/api/destinations/${id}/restaurants`).then(r => r.data)

export const getDestinationFestivals = (id: string) =>
  client.get<Festival[]>(`/api/destinations/${id}/festivals`).then(r => r.data)

export const getDestinationAccommodations = (id: string) =>
  client.get<Accommodation[]>(`/api/destinations/${id}/accommodations`).then(r => r.data)

export const getRecommendations = (id: string) =>
  client.get<Destination[]>(`/api/destinations/${id}/recommend`).then(r => r.data)
```

---

## Backend Hazır Olmadan Çalışma

Yağız veya Emirhan'ın backend'i bitmeden çalışmaya devam etmek için:

```typescript
// src/api/destinations.ts — geçici mock
const USE_MOCK = import.meta.env.DEV && !import.meta.env.VITE_USE_REAL_API

const MOCK_DESTINATIONS = [
  { id: "1", name: "Istanbul", country: "Turkey", description: "İki kıtanın buluşma noktası", avg_rating: 4.8 },
  { id: "2", name: "Paris", country: "France", description: "Işıklar şehri", avg_rating: 4.7 },
  { id: "3", name: "Barcelona", country: "Spain", description: "Gaudí'nin şehri", avg_rating: 4.6 },
]

export const getDestinations = async () => {
  if (USE_MOCK) return MOCK_DESTINATIONS  // Geçici
  return client.get('/api/destinations').then(r => r.data)
}
```

---

## Antigravity'ye Verilecek Prompt Örnekleri

### Örnek 1 — Destinasyon Detay Sayfası
```
TravelGraph projesinin frontend geliştiricisiyim.
Stack: React 18, TypeScript, Vite, Tailwind CSS, React Query v5, Axios.
Backend: http://localhost:8000

/destinations/:id sayfasını yaz. Bu sayfa şunları gösterecek:
1. Destinasyon başlığı, ülke, açıklama
2. Aktiviteler listesi (GET /api/destinations/{id}/activities)
3. Restoranlar (GET /api/destinations/{id}/restaurants) — mutfak türü ve fiyat aralığı göster
4. Festivaller (GET /api/destinations/{id}/festivals) — tarih ve sezon göster
5. Konaklamalar (GET /api/destinations/{id}/accommodations) — fiyat ve yıldız göster
6. Graf tabanlı öneriler (GET /api/destinations/{id}/recommend)
7. Yorum listesi — giriş yapmadan görünür, yorum yazmak için login yönlendirmesi

Her bölüm için ayrı React Query hook kullan.
Loading ve error durumları mutlaka göster.
Dosyalar: pages/DestinationDetailPage.tsx, hooks/useDestinationDetail.ts
```

### Örnek 2 — Bütçe Planlayıcı
```
TravelGraph için BudgetPlannerPage bileşeni yaz.
Route: /planner/:id/budget (itinerary id'si params'tan gelir)

Form alanları:
- Toplam bütçe (sayı girişi, para birimi seçimi: EUR/USD/TRY)
- Otel bütçesi (slider veya sayı)
- Yemek bütçesi
- Ulaşım bütçesi
- Aktivite bütçesi
- Anlık doğrulama: kalem toplamı > toplam bütçe ise hata göster

Submit: POST /api/itineraries/{id}/budget
Auth gerekli — giriş yoksa /login?next=... yönlendir.

Dosya: pages/BudgetPlannerPage.tsx
```

### Örnek 3 — Festival Takvimi
```
TravelGraph için FestivalsPage yaz.
Route: /festivals

- GET /api/festivals?start_after=&end_before= ile veri çek
- Tarih aralığı filtresi (başlangıç/bitiş date picker)
- Her festival kartı: isim, destinasyon, tarih aralığı, sezon badge
- Sezon filtresi: Spring / Summer / Autumn / Winter
- Giriş gerekmez

Dosyalar: pages/FestivalsPage.tsx, components/FestivalCard.tsx
```

---

## TypeScript Tip Tanımları (types/index.ts)

```typescript
export interface User {
  id: string; name: string; email: string; created_at: string
}
export interface Destination {
  id: string; name: string; country: string
  description: string; lat: number; lng: number; avg_rating?: number
}
export interface Activity {
  id: string; name: string; description: string
  duration_hours: number; price: number; address: string
  categories: Category[]; tags: Tag[]
}
export interface Restaurant {
  id: string; name: string; cuisine_type: string
  price_range: 'budget' | 'mid' | 'luxury'; address: string; rating: number
}
export interface Festival {
  id: string; name: string; description: string
  start_date: string; end_date: string; is_recurring: boolean; ticket_price?: number
}
export interface Accommodation {
  id: string; name: string; type: string
  star_rating: number; price_per_night: number; address: string
}
export interface BudgetPlan {
  id: string; total_budget: number; currency: 'EUR' | 'USD' | 'TRY'
  hotel_budget: number; food_budget: number
  transport_budget: number; activity_budget: number
}
export interface Review {
  id: string; rating: number; comment: string
  created_at: string; user_name: string
}
export interface Category { id: string; name: string; icon: string }
export interface Tag { id: string; name: string; color: string }
```

---

## Teslim Kontrol Listesi

- [ ] 9 sayfa render oluyor (hata yok)
- [ ] Giriş gerektirmeyen sayfalar giriş olmadan açılıyor
- [ ] Yorum formu giriş butonuna yönlendiriyor
- [ ] Bütçe planlayıcı kalem validasyonu çalışıyor
- [ ] Festival takvimi tarih filtresi çalışıyor
- [ ] `npm run build` hatasız
- [ ] Mobil responsive kontrol edildi
- [ ] Console'da hata yok
