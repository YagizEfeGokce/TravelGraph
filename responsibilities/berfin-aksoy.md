# Berfin Aksoy — Sorumluluk Raporu

## Rol: Frontend Geliştirici

---

## Üstlenilen Görevler

### 1. Proje Kurulumu
- `npm create vite@latest frontend -- --template react-ts`
- Tailwind CSS, React Router v6, React Query v5, Axios kurulumu
- `src/api/client.ts`: Axios instance, token interceptor, 401 yönetimi
- `src/contexts/AuthContext.tsx`: Global auth state

### 2. Sayfalar

| Sayfa | Route | Açıklama |
|-------|-------|---------|
| Ana Sayfa | `/` | Hero + arama + öne çıkan destinasyonlar |
| Keşif | `/explore` | Destinasyon grid, filtre (kategori, sezon, ülke) |
| Destinasyon Detay | `/destinations/:id` | Tüm bilgiler (aktivite, otel, restoran, festival) |
| Rota Planlayıcı | `/planner` | Sürükle-bırak durak sıralama |
| Bütçe Planlayıcı | `/planner/:id/budget` | Kalem kalem bütçe girişi |
| Festival Takvimi | `/festivals` | Tarih filtreli etkinlik listesi |
| Profil | `/profile` | Geçmiş seyahatler, planlar, yorumlar |
| Giriş / Kayıt | `/login`, `/register` | Auth formları |

### 3. Bileşenler
- `Navbar`: Gezinme, auth durumu (giriş/çıkış)
- `DestinationCard`: Destinasyon kart bileşeni
- `AccommodationCard`: Otel kartı (fiyat, yıldız)
- `RestaurantCard`: Restoran kartı (mutfak türü, fiyat aralığı)
- `FestivalCard`: Festival kartı (tarih, sezon)
- `ActivityCard`: Aktivite kartı (süre, fiyat, kategori)
- `BudgetBreakdown`: Harcama kalemi görselleştirme
- `ReviewCard` + `ReviewForm`: Yorum gösterimi ve girişi (auth gerekli)
- `StarRating`: Puan gösterimi/girişi
- `SeasonBadge`, `TagBadge`, `CategoryBadge`: Etiket bileşenleri
- `ProtectedRoute`: Giriş gerektiren sayfaları sarar
- `LoadingSpinner`, `ErrorMessage`: Durum bileşenleri

### 4. API Katmanı (`src/api/`)
- `destinations.ts`: Destinasyon CRUD, öneri, aktivite/otel/restoran/festival alt sorguları
- `itineraries.ts`: Plan oluşturma, durak yönetimi
- `budget.ts`: Bütçe planı oluşturma ve görüntüleme
- `festivals.ts`: Festival listesi, tarih filtresi
- `reviews.ts`: Yorum oluşturma ve listeleme
- `auth.ts`: Giriş, kayıt, token yenileme

### 5. Custom Hook'lar (`src/hooks/`)
- `useDestinations.ts`: Filtreli destinasyon listesi
- `useDestinationDetail.ts`: Tek destinasyon + alt kaynaklar
- `useItinerary.ts`: Plan yönetimi
- `useFestivals.ts`: Tarih filtreli festival listesi
- `useRecommendations.ts`: Graf tabanlı öneri sonuçları

---

## Teslim Edilen Çıktılar

- [ ] 8 sayfa hatasız render oluyor
- [ ] Giriş yapmadan destinasyon, aktivite, restoran, festival görünüyor
- [ ] Yorum formu giriş gerektiriyor (yönlendirme var)
- [ ] Bütçe planlayıcı kalem kalem giriş + toplam gösteriyor
- [ ] Festival takvimi tarih filtresi çalışıyor
- [ ] `npm run build` hatasız tamamlanıyor
- [ ] Mobil responsive (sm/md/lg breakpoint'ler kontrol edildi)

---

## Kullanılan Teknolojiler

`React 18` · `Vite 5` · `TypeScript` · `React Router v6` · `React Query v5` · `Axios` · `Tailwind CSS`
