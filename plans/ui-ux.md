---
version: 1.0.0
last_updated: 2026-05-20
domain: ui-ux
scope: root
---

# UI/UX Plan

## Design System

**Base:** Google Stitch design system (as referenced in prompts)
**Typography:** Plus Jakarta Sans
**Primary Palette:** `#003d9b`
**Styling:** Tailwind CSS 3.x
**Icons:** SVG icon sprite (`public/icons.svg`)

## Component Inventory

### Used Components
| Component | Used By | Status |
|-----------|---------|--------|
| `Navbar` | App.tsx | Working (mobile hamburger added) |
| `ProtectedRoute` | App.tsx | **FIXED** — Now wraps `/planner`, `/profile`, `/planner/:id/budget` |
| `DestinationCard` | ExplorePage, HomePage | Working |
| `ReviewForm` | DestinationDetailPage | Working |
| `LoadingSpinner` | ~~Nowhere~~ | **DELETED** |
| `ErrorMessage` | ~~Nowhere~~ | **DELETED** |
| `StarRating` | ReviewForm, DestinationDetailPage | Working (aria-label added) |
| `AccommodationCard` | ~~Nowhere~~ | **DELETED** |
| `ActivityCard` | ~~Nowhere~~ | **DELETED** |
| `FestivalCard` | ~~Nowhere~~ | **DELETED** |
| `RestaurantCard` | ~~Nowhere~~ | **DELETED** |
| `ReviewCard` | ~~Nowhere~~ | **DELETED** |
| `BudgetBreakdown` | ~~Nowhere~~ | **DELETED** |
| `CategoryBadge` | ~~Nowhere~~ | **DELETED** |
| `TagBadge` | ~~Nowhere~~ | **DELETED** |
| `SeasonBadge` | ~~Nowhere~~ | **DELETED** |

## State Management

| Layer | Tool | Scope |
|-------|------|-------|
| Global auth | React Context (`AuthContext.tsx`) | User, token, login/logout |
| Server data | Custom hooks (`useDestinations`, `useItinerary`, etc.) | Fetch-on-mount only |
| Local UI | `useState` | Form inputs, modals, tabs |

**Issue:** No data-fetching library (TanStack Query, SWR). Hooks fetch on mount only with no refetch, caching, or stale-while-revalidate.

## Page Inventory

| Page | Route | Status | Issues |
|------|-------|--------|--------|
| Home | `/` | Working | **FIXED** — Stats are dynamic; demo badge kept as design |
| Explore | `/explore` | Working | None major |
| Destination Detail | `/destinations/:id` | Working | **FIXED** — Uses `Promise.allSettled`; 404 handled by `NotFoundPage` |
| Festivals | `/festivals` | Working | **FIXED** — "Add to route" button removed |
| Planner | `/planner` | Working | **FIXED** — Search bar removed; graph analysis is dynamic |
| Budget Planner | `/planner/:id/budget` | **FIXED** | Wired to real API; Save button functional |
| Login | `/login` | Working | **FIXED** — Email regex validation, password strength check |
| Register | `/register` | Working | **FIXED** — Email regex validation, password strength check |
| Profile | `/profile` | Working | Currency local state only |

## Accessibility Issues

| Issue | Severity | Fix |
|-------|----------|-----|
| No mobile hamburger menu | **High** | **FIXED** — Responsive drawer added to Navbar |
| Modals lack `role="dialog"`, focus trap, Escape handling | **High** | Still open — no modals currently exist |
| Icon buttons lack `aria-label` | Medium | **FIXED** — `aria-label="Profile"` added; decorative icons have `aria-hidden` |
| No `aria-current="page"` on nav links | Medium | **FIXED** — Active links styled with visual indicator |
| No skip-to-content link | Low | **FIXED** — `sr-only` skip link added to App.tsx |
| Star ratings as raw text characters | Low | **FIXED** — `aria-label` with numeric value added |

## Known Broken UI Features

| Feature | Status | Evidence |
|---------|--------|----------|
| Budget Planner | **FIXED** | Wired to `GET/POST/PUT /itineraries/{id}/budget` |
| Search in Planner | **REMOVED** | Decorative input removed from PlannerPage |
| "Add to route" on Festivals | **REMOVED** | Decorative button removed from FestivalsPage |
| Recommendations UI | **FIXED** | `useRecommendations` used in PlannerPage for "Best Next Stop" |
| Lunch Recommendation | **REMOVED** | Hardcoded panel removed from PlannerPage |
| Currency Preference | Local only | Not persisted — acceptable for defense |
| AI Insight Slider | **REMOVED** | Placebo component removed |
| Graph Analysis | **FIXED** | Now counts unique countries/cities dynamically |

## Performance Issues

| Issue | Severity | Fix |
|-------|----------|-----|
| No code splitting | **High** | **FIXED** — `React.lazy` + `Suspense` in App.tsx |
| No image lazy loading | Medium | **FIXED** — `loading="lazy"` on all images |
| Google Fonts sync `@import` | Low | **FIXED** — Already uses `display=swap` |
| Hero image without dimensions | Low | **FIXED** — `width={800}` and `height={1000}` added |

## Responsive Design

**FIXED:** Navbar has hamburger toggle with `aria-label="Toggle menu"` and responsive mobile drawer.
