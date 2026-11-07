import os
import unittest
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from backend.app.core.dependencies import get_db
from backend.app.main import app

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
POSTGRES_TESTS_ENABLED = bool(TEST_DATABASE_URL and TEST_DATABASE_URL.startswith("postgresql"))


@unittest.skipUnless(POSTGRES_TESTS_ENABLED, "Set TEST_DATABASE_URL to a migrated PostgreSQL test database")
class PostgreSQLAuthenticationIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        assert TEST_DATABASE_URL is not None
        cls.engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
        with cls.engine.connect() as connection:
            revision = connection.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
        if revision != "0002_revocable_auth_sessions":
            raise RuntimeError("Run `alembic upgrade head` against TEST_DATABASE_URL before these tests")

    @classmethod
    def tearDownClass(cls) -> None:
        if hasattr(cls, "engine"):
            cls.engine.dispose()

    def setUp(self) -> None:
        self.connection = self.engine.connect()
        self.transaction = self.connection.begin()

        def override_get_db():
            with Session(bind=self.connection, join_transaction_mode="create_savepoint") as session:
                yield session

        self.previous_overrides = app.dependency_overrides.copy()
        app.dependency_overrides[get_db] = override_get_db
        self.client = TestClient(app)

    def tearDown(self) -> None:
        self.client.close()
        app.dependency_overrides.clear()
        app.dependency_overrides.update(self.previous_overrides)
        self.transaction.rollback()
        self.connection.close()

    def test_registration_login_workspace_profile_and_logout(self) -> None:
        email = f"owner-{uuid4()}@example.com"
        registration = self.client.post(
            "/api/auth/register",
            json={
                "email": email,
                "password": "correct-horse-battery",
                "organization_name": "PostgreSQL workspace",
            },
        )
        self.assertEqual(registration.status_code, 201, registration.text)
        workspace = self.client.get("/api/organizations").json()[0]
        profile_payload = {
            "business_name": "PostgreSQL Studio",
            "description": "A test business profile",
            "industry": "Design",
            "website": "https://example.com",
            "location": "London",
            "products_and_services": "Design services",
            "target_market": "Small businesses",
            "unique_value_proposition": "Practical design",
            "communication_style": "Professional",
        }
        saved = self.client.put(
            "/api/business-profile",
            headers={"X-Organization-ID": workspace["id"]},
            json=profile_payload,
        )
        self.assertEqual(saved.status_code, 200, saved.text)
        self.assertEqual(
            self.client.get(
                "/api/business-profile", headers={"X-Organization-ID": workspace["id"]}
            ).json()["business_name"],
            "PostgreSQL Studio",
        )

        self.client.post("/api/auth/logout")
        login = self.client.post(
            "/api/auth/login",
            json={"email": email, "password": "correct-horse-battery"},
        )
        self.assertEqual(login.status_code, 200, login.text)
        self.assertEqual(
            self.client.get(
                "/api/business-profile", headers={"X-Organization-ID": workspace["id"]}
            ).json()["business_name"],
            "PostgreSQL Studio",
        )

    def test_user_cannot_access_another_tenant(self) -> None:
        first_email = f"first-{uuid4()}@example.com"
        second_email = f"second-{uuid4()}@example.com"
        for email, workspace_name in (
            (first_email, "First tenant"),
            (second_email, "Second tenant"),
        ):
            response = self.client.post(
                "/api/auth/register",
                json={
                    "email": email,
                    "password": "correct-horse-battery",
                    "organization_name": workspace_name,
                },
            )
            self.assertEqual(response.status_code, 201, response.text)
            if email == first_email:
                first_workspace_id = self.client.get("/api/organizations").json()[0]["id"]

        denied = self.client.get(
            "/api/business-profile", headers={"X-Organization-ID": first_workspace_id}
        )
        self.assertEqual(denied.status_code, 403)
        self.assertEqual(
            [item["name"] for item in self.client.get("/api/organizations").json()],
            ["Second tenant"],
        )


if __name__ == "__main__":
    unittest.main()