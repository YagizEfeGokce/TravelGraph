---
version: 1.0.0
last_updated: 2026-05-20
domain: meta
scope: root
---

# TravelGraph Plans

This directory contains domain-specific implementation and documentation plans for the TravelGraph project.

## Plan Structure

| File | Covers |
|------|--------|
| `roadmap.md` | Completed, in-progress, and pending work |
| `architecture.md` | System components, data flow, tech stack |
| `api.md` | Endpoints, request/response contracts, auth |
| `business-logic.md` | Domain rules, workflows, state machines |
| `data-model.md` | FalkorDB schema, indexing, migrations |
| `security.md` | Auth, threat model, vulnerabilities, fixes |
| `ui-ux.md` | Design system, components, accessibility |
| `deployment.md` | Infrastructure, pipelines, env strategy |
| `testing.md` | Test pyramid, coverage, fixtures, CI/CD |
| `modules/backend/` | Backend-specific overrides |
| `modules/frontend/` | Frontend-specific overrides |

## Module Plan Override Rule

Root plans define project-wide defaults. Module plans override for their scope:
- `modules/backend/api.md` overrides root `api.md` for backend-specific endpoint details.
- `modules/frontend/ui-ux.md` overrides root `ui-ux.md` for frontend-specific component rules.

If a module plan does not exist for a domain, the root plan applies.

## Plan Query

When implementing, query the relevant plan before coding:

```
plan_query("<domain>:<question>")
```

Example: `plan_query("security:what is the JWT token storage requirement?")`

Resolution order:
1. Check module plan for the current scope.
2. Fall back to root plan.
3. If ambiguous, ask the human.

## Updating Plans

When specs change or audits reveal new issues:
1. Update the relevant domain plan.
2. Update `roadmap.md` status.
3. Do NOT duplicate plan content in code comments.
