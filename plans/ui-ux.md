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
| `Navbar` | App.tsx | Working |
| `ProtectedRoute` | **Nowhere** | **Dead code** |
| `DestinationCard` | ExplorePage, HomePage | Working |
| `ReviewForm` | DestinationDetailPage | Working |
| `LoadingSpinner` | **Nowhere** | **Dead code** |
| `ErrorMessage` | **Nowhere** | **Dead code** |
| `StarRating` | ReviewForm, DestinationDetailPage | Working |
| `AccommodationCard` | **Nowhere** | **Dead code** |
| `ActivityCard` | **Nowhere** | **Dead code** |
| `FestivalCard` | **Nowhere** | **Dead code** |
| `RestaurantCard` | **Nowhere** | **Dead code** |
| `ReviewCard` | **Nowhere** | **Dead code** |
| `BudgetBreakdown` | **Nowhere** | **Dead code** |
| `CategoryBadge` | **Nowhere** | **Dead code** |
| `TagBadge` | **Nowhere** | **Dead code** |
| `SeasonBadge` | **Nowhere** | **Dead code** |

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
| Home | `/` | Working | Hardcoded stats, demo badge |
| Explore | `/explore` | Working | None major |
| Destination Detail | `/destinations/:id` | Working | Fragile `Promise.all`, no 404 |
| Festivals | `/festivals` | Working | "Add to route" button is fake |
| Planner | `/planner` | Mostly works | Search bar fake, hardcoded stats |
| Budget Planner | `/planner/:id/budget` | **100% broken** | No API calls, Save button no-op |
| Login | `/login` | Partially works | Not a real `form`, no email regex |
| Register | `/register` | Partially works | Not a real `form` |
| Profile | `/profile` | Working | Currency local state only |

## Accessibility Issues

| Issue | Severity | Fix |
|-------|----------|-----|
| No mobile hamburger menu | **High** | Add responsive drawer |
| Modals lack `role="dialog"`, focus trap, Escape handling | **High** | Use proper dialog element or library |
| Icon buttons lack `aria-label` | Medium | Add labels to all icon-only buttons |
| No `aria-current="page"` on nav links | Medium | Add to active `Link` |
| No skip-to-content link | Low | Add `sr-only` skip link |
| Star ratings as raw text characters | Low | Add `aria-label` with numeric value |

## Known Broken UI Features

| Feature | Status | Evidence |
|---------|--------|----------|
| Budget Planner | **100% fake** | No API integration, Save button no `onClick` |
| Search in Planner | **Decorative** | Input with no state/filter |
| "Add to route" on Festivals | **Decorative** | Button with no handler |
| Recommendations UI | **Not connected** | `useRecommendations` hook never used |
| Lunch Recommendation | **Hardcoded** | Static text regardless of data |
| Currency Preference | **Local only** | Not persisted |
| AI Insight Slider | **Placebo** | Changes nothing |
| Graph Analysis | **Hardcoded** | `"Countries", 1` always |

## Performance Issues

| Issue | Severity | Fix |
|-------|----------|-----|
| No code splitting | **High** | Use `React.lazy` + `Suspense` |
| No image lazy loading | Medium | Add `loading="lazy"` |
| Google Fonts sync `@import` | Low | Add `display=swap` |
| Hero image without dimensions | Low | Add `width`/`height` |

## Responsive Design

**Current:** Navbar hides links on mobile (`hidden md:flex`). No hamburger menu means mobile users cannot navigate.
**Required:** Implement mobile drawer with hamburger icon.
