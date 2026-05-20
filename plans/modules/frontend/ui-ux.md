---
version: 1.0.0
last_updated: 2026-05-20
domain: ui-ux
scope: module
module: frontend
---

# Frontend UI/UX Module Plan

## Frontend-Specific Broken Features

### BudgetPlannerPage — 100% Fake
- Ignores `:id` URL parameter entirely
- Never calls `getBudget` or `createBudget` API functions
- "Save Budget" button has **zero `onClick` handler**
- All state is local and lost on refresh
- **Required fix:** Wire to actual API endpoints

### ProtectedRoute — Unused
- Component defined in `components/ProtectedRoute.tsx`
- **Never imported** in `App.tsx`
- `/planner` and `/profile` are accessible without login via direct URL
- **Required fix:** Import and wrap protected routes

### AuthContext — Missing Loading State
- No `isLoading` during token restoration from localStorage
- Navbar flashes "Login/Register" before showing user name on every refresh
- **Required fix:** Add `isLoading` state; render skeleton/loading until restore completes

### Token Refresh — Completely Missing
- Login response includes `refresh_token`
- `client.ts` stores it in localStorage
- **Never used** — no interceptor, no refresh logic
- Access token expires after 60 min; session dies silently
- **Required fix:** Add response interceptor for 401 → attempt refresh → redirect on failure

### All Custom Hooks — Error Suppression
- Every hook uses `.catch(() => {})` — errors silently swallowed
- No `error` state returned
- No loading state management
- **Required fix:** Return `{ data, loading, error }` triplet from all hooks

### Search Bar — Decorative
- PlannerPage has `<input placeholder="Search destinations..." />`
- No `onChange`, no state, no filtering logic
- **Required fix:** Implement search/filter or remove the input

### "Add to route" Button — Decorative
- FestivalsPage has button with `title="Add to route"`
- No `onClick` handler
- **Required fix:** Implement add-to-itinerary flow or remove button

### Hardcoded Data Throughout

| Location | Hardcoded Value | Should Be |
|----------|-----------------|-----------|
| HomePage stats | `"10"`, `"14"`, `"FalkorDB"`, `"10+"` | API counts |
| Planner graph analysis | `"Countries", 1` | Computed from stops |
| Lunch recommendation | `"Local cuisine · Highly rated"` | API call or remove |
| Route total | `stops.length * 1500` | Real cost calculation |

### Form Validation Issues

| Form | Issue | Fix |
|------|-------|-----|
| Login | Not wrapped in `<form>` | Wrap in `<form onSubmit={...}>` |
| Register | Not wrapped in `<form>` | Wrap in `<form onSubmit={...}>` |
| Register | No email regex validation | Add email format check |
| Planner (new plan) | No date validation | Ensure end_date > start_date |
| Planner (stop) | No max day_number validation | Validate against trip duration |
| Review form | No `maxLength` on textarea | Add `maxLength={1000}` |

### TypeScript Issues

- All hooks use `any[]` — define proper domain types in `types/` directory
- `client.ts` casts `config.headers as any` — use proper Axios typing
- `catch (err: any)` in LoginPage and RegisterPage — use `unknown` + narrowing
- `(destination as any).image_url` in HomePage — add to type definition

### Dead Components (Never Imported)

- `AccommodationCard.tsx`
- `ActivityCard.tsx`
- `BudgetBreakdown.tsx`
- `CategoryBadge.tsx`
- `ErrorMessage.tsx`
- `FestivalCard.tsx`
- `LoadingSpinner.tsx`
- `RestaurantCard.tsx`
- `ReviewCard.tsx`
- `SeasonBadge.tsx`
- `TagBadge.tsx`

**Decision:** Either import and use them, or remove them.
