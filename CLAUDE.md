# CLAUDE.md — AI Agent Guidance for Job Application Tracker

## Purpose
This file defines rules and constraints for AI agents working on this codebase.
These rules protect system integrity and must never be violated.

## Non-Negotiable Rules

### State Machine
- The `VALID_TRANSITIONS` map in `application_service.py` is the single source of truth.
- Never add a new stage without updating `VALID_TRANSITIONS`.
- Never bypass transition validation — not even in tests.
- Stage changes must ONLY go through the `/stage` endpoint, never through `PATCH /applications/:id`.

### Ownership
- Every data-fetching query on applications and notes MUST filter by `user_id`.
- Never return data without confirming it belongs to the authenticated user.
- Ownership check must live in the service layer, not just the route.

### Validation
- All input validation must use Marshmallow schemas.
- Never manually parse or trust raw request data without schema validation.
- Schema files are in `app/schemas/` — do not inline validation logic in routes.

### Tests
- Every new endpoint must have at least one corresponding test.
- Stage transition tests must be updated when transitions change.
- Never delete existing tests — fix them instead.

### No Clever Code
- Prefer readable, explicit code over clever one-liners.
- No dynamic attribute access (`getattr` with string) unless unavoidable.
- No global state outside of Flask extensions.

## Conventions
- Routes only handle HTTP concerns (parse input, call service, return response).
- Services handle all business logic.
- Models are plain SQLAlchemy models — no business logic in models.
- UUIDs for all primary keys — no integer IDs.
- All datetimes stored as UTC.

## Adding Features
Before adding a feature:
1. Identify which service file it belongs in.
2. Check if a new schema is needed.
3. Write the test first (TDD preferred).
4. Do not modify the state machine without explicit instruction.

## What Not To Do
- Do not add new libraries without checking if existing ones cover the need.
- Do not expose stack traces in API error responses.
- Do not store plaintext passwords anywhere, ever.
- Do not add CORS wildcard (`*`) in production config.
