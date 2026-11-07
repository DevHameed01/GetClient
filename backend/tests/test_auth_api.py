import unittest
from uuid import UUID, uuid4

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from backend.app.core.dependencies import ACCESS_COOKIE_NAME, get_db
from backend.app.database import Base
from backend.app.main import app
from backend.app.core.security import hash_password
from backend.app.models.tenant import AuthSession, Membership, Organization, User


class AuthenticationApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(self.engine)

        def override_get_db():
            with Session(self.engine) as session:
                yield session

        self.previous_overrides = app.dependency_overrides.copy()
        app.dependency_overrides[get_db] = override_get_db
        self.client = TestClient(app)

    def tearDown(self) -> None:
        self.client.close()
        app.dependency_overrides.clear()
        app.dependency_overrides.update(self.previous_overrides)
        self.engine.dispose()

    @staticmethod
    def registration_payload(email: str, organization_name: str) -> dict[str, str]:
        return {
            "email": email,
            "password": "correct-horse-battery",
            "organization_name": organization_name,
        }

    @staticmethod
    def profile_payload(business_name: str) -> dict[str, str]:
        return {
            "business_name": business_name,
            "description": f"{business_name} provides design services",
            "industry": "Design",
            "website": "https://example.com",
            "location": "London",
            "products_and_services": "Brand and web design",
            "target_market": "Growing businesses",
            "unique_value_proposition": "Clear, useful design",
            "communication_style": "Professional",
        }

    def register(self, email: str, organization_name: str) -> str:
        response = self.client.post(
            "/api/auth/register",
            json=self.registration_payload(email, organization_name),
        )
        self.assertEqual(response.status_code, 201, response.text)
        self.assertTrue(response.json()["authenticated"])
        self.assertTrue(response.cookies.get(ACCESS_COOKIE_NAME))
        self.assertIn("httponly", response.headers["set-cookie"].lower())
        return response.json()["user_id"]

    def test_registration_login_profile_persistence_and_logout(self) -> None:
        self.register("owner@example.com", "Owner workspace")
        organizations_response = self.client.get("/api/organizations")
        self.assertEqual(organizations_response.status_code, 200)
        organization = organizations_response.json()[0]
        self.assertEqual(organization["name"], "Owner workspace")
        self.assertEqual(organization["role"], "owner")

        profile_payload = self.profile_payload("Northstar Studio")
        saved = self.client.put(
            "/api/business-profile",
            headers={"X-Organization-ID": organization["id"]},
            json=profile_payload,
        )
        self.assertEqual(saved.status_code, 200, saved.text)
        self.assertEqual(saved.json()["business_name"], "Northstar Studio")
        self.assertNotIn("organization_id", saved.json())

        loaded = self.client.get(
            "/api/business-profile", headers={"X-Organization-ID": organization["id"]}
        )
        self.assertEqual(loaded.status_code, 200)
        self.assertEqual(loaded.json()["products_and_services"], "Brand and web design")

        token = self.client.cookies.get(ACCESS_COOKIE_NAME)
        logout = self.client.post("/api/auth/logout")
        self.assertEqual(logout.status_code, 204)
        self.assertIsNone(self.client.cookies.get(ACCESS_COOKIE_NAME))
        revoked = self.client.get(
            "/api/auth/session", headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(revoked.status_code, 401)

        login = self.client.post(
            "/api/auth/login",
            json={"email": "owner@example.com", "password": "correct-horse-battery"},
        )
        self.assertEqual(login.status_code, 200, login.text)
        persisted = self.client.get(
            "/api/business-profile", headers={"X-Organization-ID": organization["id"]}
        )
        self.assertEqual(persisted.status_code, 200)
        self.assertEqual(persisted.json()["business_name"], "Northstar Studio")

    def test_cross_tenant_access_and_untrusted_workspace_ids_are_denied(self) -> None:
        self.register("first@example.com", "First workspace")
        first_organization = self.client.get("/api/organizations").json()[0]

        self.register("second@example.com", "Second workspace")
        second_organizations = self.client.get("/api/organizations").json()
        self.assertEqual([item["name"] for item in second_organizations], ["Second workspace"])

        denied_read = self.client.get(
            "/api/business-profile", headers={"X-Organization-ID": first_organization["id"]}
        )
        self.assertEqual(denied_read.status_code, 403)
        denied_write = self.client.put(
            "/api/business-profile",
            headers={"X-Organization-ID": first_organization["id"]},
            json=self.profile_payload("Intruding profile"),
        )
        self.assertEqual(denied_write.status_code, 403)
        self.assertEqual(self.client.get("/api/business-profile").status_code, 404)

    def test_expired_session_is_rejected(self) -> None:
        self.register("expired@example.com", "Expired workspace")
        with Session(self.engine) as session:
            auth_session = session.query(AuthSession).one()
            from datetime import datetime, timedelta, timezone

            auth_session.expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
            session.commit()
        response = self.client.get("/api/auth/session")
        self.assertEqual(response.status_code, 401)

    def test_duplicate_registration_and_invalid_login_are_rejected(self) -> None:
        self.register("duplicate@example.com", "First workspace")
        duplicate = self.client.post(
            "/api/auth/register",
            json=self.registration_payload("duplicate@example.com", "Duplicate workspace"),
        )
        self.assertEqual(duplicate.status_code, 409)
        invalid_login = self.client.post(
            "/api/auth/login",
            json={"email": "duplicate@example.com", "password": "not-the-password"},
        )
        self.assertEqual(invalid_login.status_code, 401)

    def test_invalid_workspace_identifier_is_rejected(self) -> None:
        self.register("workspace@example.com", "Workspace")
        response = self.client.get("/api/organization", headers={"X-Organization-ID": str(uuid4())})
        self.assertEqual(response.status_code, 403)

    def test_multiple_workspaces_require_a_membership_checked_selection(self) -> None:
        self.register("multi@example.com", "First workspace")
        with Session(self.engine) as session:
            from backend.app.models.tenant import Membership, Organization, User

            user = session.query(User).filter_by(email="multi@example.com").one()
            second = Organization(name="Second workspace")
            session.add(second)
            session.flush()
            session.add(Membership(user_id=user.id, organization_id=second.id, role="member"))
            session.commit()
            second_id = str(second.id)

        ambiguous = self.client.get("/api/organization")
        self.assertEqual(ambiguous.status_code, 409)
        selected = self.client.get("/api/organization", headers={"X-Organization-ID": second_id})
        self.assertEqual(selected.status_code, 200)
        self.assertEqual(selected.json()["name"], "Second workspace")

    def test_member_can_read_but_cannot_rename_workspace(self) -> None:
        self.register("workspace-owner@example.com", "Role Test Workspace")
        workspace_id = UUID(self.client.get("/api/organizations").json()[0]["id"])
        with Session(self.engine) as session:
            member = User(email="workspace-member@example.com", password_hash=hash_password("correct-horse-battery"))
            session.add(member)
            session.flush()
            session.add(Membership(user_id=member.id, organization_id=workspace_id, role="member"))
            session.commit()

        self.client.post("/api/auth/logout")
        login = self.client.post(
            "/api/auth/login",
            json={"email": "workspace-member@example.com", "password": "correct-horse-battery"},
        )
        self.assertEqual(login.status_code, 200)
        readable = self.client.get("/api/organization", headers={"X-Organization-ID": str(workspace_id)})
        self.assertEqual(readable.status_code, 200)
        denied = self.client.patch(
            "/api/organization",
            headers={"X-Organization-ID": str(workspace_id)},
            json={"name": "Unauthorized rename"},
        )
        self.assertEqual(denied.status_code, 403)


if __name__ == "__main__":
    unittest.main()