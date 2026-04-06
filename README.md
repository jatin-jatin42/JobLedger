# JobLedger — Job Application Tracker

A production-quality full-stack web application for tracking job applications through a structured state machine pipeline.

## Project Overview

JobLedger lets each registered user manage their own job applications as they progress through stages: Applied → Screening → Interview → Offer (or Rejected/Withdrawn at any point). The application enforces a strict state machine at the API level so no stage can be skipped or reversed.

## Setup Instructions

### Prerequisites
- Docker & Docker Compose installed

### Run with Docker Compose

```bash
# 1. Copy environment variables
cp .env.example .env

# 2. Build and start all services in detached mode
docker compose up -d --build

# 3. Initialize database migrations (first time only)
docker compose exec backend flask db init
docker compose exec backend flask db migrate -m "Initial migration"
docker compose exec backend flask db upgrade

# 4. Seed database with sample data (optional)
# This will create 3 users with 10 applications each.
docker compose exec backend python seed.py
```

- **Frontend App**: http://localhost:3000
- **Backend API**: http://localhost:5001 *(Note: Changed from 5000 to prevent macOS AirPlay Receiver port conflicts)*

### Running Tests

```bash
docker compose exec backend pytest -v
```

---

## Key Technical Decisions

### State Machine in Service Layer, Not the Model
The `VALID_TRANSITIONS` map and all transition logic live in `application_service.py`, not in the `Application` model. Models are kept as plain data containers (SQLAlchemy columns only). This separation keeps business logic testable, explicit, and independent of the ORM.

### Marshmallow for Validation
Marshmallow provides declarative, schema-based validation with field-level error messages. It cleanly separates validation from route logic, and integrates with SQLAlchemy via `marshmallow-sqlalchemy`. Raw request data is never trusted without passing through a schema first.

### UUID Primary Keys
All tables use UUID PKs instead of integer sequences. This avoids enumeration attacks, makes IDs safe to expose in URLs, and supports future distributed/multi-DB setups without ID collision risk.

### Single Role (No Admin)
The spec requires a single-user-per-account tracker with no admin panel. Adding roles would introduce complexity (permission checks, role middleware, admin UI) that provides no value for this use case. Every user owns exactly their own data — enforced at the query level in every service method.

---

## Architecture Overview

| Layer | Responsibility |
|-------|---------------|
| **PostgreSQL 17** | Persistent data storage with FK constraints and indexes |
| **Flask (Python 3.12)** | REST API — auth, CRUD, state machine enforcement |
| **React 18 + TypeScript** | SPA frontend — pages, routing, API calls |
| **Docker Compose** | Orchestrates all 3 services with health checks |

**Backend structure**: Routes → Services → Models (strict layering, no skipping)

---

## Known Limitations / Tradeoffs

- **No pagination**: All results returned at once with a `total` count. Acceptable for a single-user tracker but would need cursor/offset pagination at scale.
- **SQLite for tests**: Tests use an in-memory SQLite DB for speed. A small number of PostgreSQL-specific features (e.g., `gen_random_uuid()`) aren't tested at the DB level.
- **JWT only (no refresh tokens)**: Access tokens expire in 24h. In production, a refresh token flow would improve UX.

---

## How to Extend

- **Add email notifications**: Create `notification_service.py`, use Flask-Mail. Hook into `application_service.update_stage()` to send emails on stage change.
- **Add resume uploads**: Integrate with an S3-compatible store (e.g., boto3). Add a `resume_url` field to the `applications` table via a new migration.
- **Add pagination**: Add `page` and `per_page` query params to `GET /api/applications`. Return `{ data, total, page, per_page, pages }`.
