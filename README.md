# GetClient MVP Foundation

This project contains the initial monorepo foundation for GetClient, based on the product requirements document in this folder.

## Stack

- Frontend: React + TypeScript + Vite
- Backend: Python + FastAPI
- Database: PostgreSQL with Alembic-managed schema migrations
- Cache / jobs: Redis (planned)

## Quick start

### 1) Backend

```bash
cd /home/bigpandaweb3/Documents/GetClient
python3 -m venv .venv
. .venv/bin/activate
pip install -r backend/requirements.txt
alembic upgrade head
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Set `DATABASE_URL` to override the local PostgreSQL connection. The development token secret has a built-in value; deployments must set a unique `AUTH_TOKEN_SECRET` of at least 32 bytes. Never use the development secret in production.

Create a reviewed migration after changing SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe schema change"
alembic upgrade head
```

### Authentication and tenant scope

- `POST /api/auth/register` creates a user, an organisation, and the user's owner membership.
- `POST /api/auth/login` sets an expiring, HTTP-only access cookie; `POST /api/auth/logout` revokes the server-side session and clears the cookie.
- `GET /api/organizations` lists only the authenticated user's workspaces. `GET` and `PATCH /api/organization` operate on a membership-validated selected workspace; only owners and admins can rename it.
- `GET` and `PUT /api/business-profile` require an authenticated session. The organisation is resolved from the user's membership; clients cannot provide `organization_id` in the profile body.
- For users with multiple memberships, `X-Organization-ID` may select a workspace only when a matching membership exists. Unknown or non-member organisation IDs are rejected.

Install the test client and run the local API suite:

```bash
pip install -r backend/test-requirements.txt
PYTHONPATH=. python -m unittest discover -s backend/tests -v
```

Run the PostgreSQL integration tests against a dedicated test database after applying migrations:

```bash
export TEST_DATABASE_URL='postgresql+psycopg://postgres:postgres@localhost:5432/getclient_test'
DATABASE_URL="$TEST_DATABASE_URL" alembic upgrade head
PYTHONPATH=. python -m unittest backend.tests.test_postgres_integration -v
```

### 2) Frontend

```bash
cd /home/bigpandaweb3/Documents/GetClient/frontend
npm install
npm run dev -- --host 0.0.0.0
```

### 3) Optional local services

```bash
docker-compose up -d postgres redis
```

## Current MVP foundation includes

- FastAPI auth endpoints with revocable HTTP-only sessions and membership-scoped organisation/profile APIs
- Alembic migrations for the tenant schema and revocable auth sessions
- React registration, login, workspace selection, and business profile management flow
- Project structure aligned to the PRD
- Docker setup for Postgres and Redis

## Next implementation steps

1. Add email verification, password reset, and account settings
2. Build ICP and prospect discovery APIs
3. Implement lead scoring and research report generation
4. Create message review workflow and approval UI
5. Connect integrations and usage-tracking modules
# GetClient
