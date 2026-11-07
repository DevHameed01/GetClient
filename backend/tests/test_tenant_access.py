import unittest
from http.cookies import SimpleCookie
from uuid import uuid4
from unittest.mock import patch

from fastapi import HTTPException, Response
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.app.api.auth import login, register
from backend.app.core.dependencies import ACCESS_COOKIE_NAME, AuthenticatedUser, get_current_membership, get_db
from backend.app.database import Base
from backend.app.models.tenant import AuthSession, Membership, Organization, User
from backend.app.schemas.auth import LoginRequest, RegisterRequest
from backend.app.config import settings
from backend.app.config import Settings
from backend.app.schemas.business import BusinessProfileInput
from backend.app.core.security import create_access_token, decode_access_token, hash_password, verify_password


class TenantAccessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.db = Session(self.engine, expire_on_commit=False)
        self.user = User(email="member@example.com", password_hash="unused")
        self.organization = Organization(name="Member workspace")
        self.db.add_all([self.user, self.organization])
        self.db.flush()
        self.db.add(Membership(user_id=self.user.id, organization_id=self.organization.id, role="owner"))
        self.db.commit()

    def tearDown(self) -> None:
        self.db.close()
        self.engine.dispose()

    def test_tenant_context_comes_from_membership(self) -> None:
        principal = AuthenticatedUser(id=self.user.id, session_id=uuid4(), user=self.user)
        membership = get_current_membership(current_user=principal, db=self.db)
        self.assertEqual(membership.organization_id, self.organization.id)

    def test_database_dependency_rolls_back_and_closes_sessions(self) -> None:
        class TrackingSession(Session):
            was_closed = False

            def close(self) -> None:
                self.was_closed = True
                super().close()

        factory = sessionmaker(bind=self.engine, class_=TrackingSession, expire_on_commit=False)
        with patch("backend.app.core.dependencies.SessionLocal", factory):
            dependency = get_db()
            session = next(dependency)
            organization = session.get(Organization, self.organization.id)
            organization.name = "Uncommitted change"
            with self.assertRaises(RuntimeError):
                dependency.throw(RuntimeError("request failed"))

        with Session(self.engine) as verification_session:
            organization = verification_session.get(Organization, self.organization.id)
            self.assertEqual(organization.name, "Member workspace")
        self.assertTrue(session.was_closed)
        self.assertFalse(session.in_transaction())

    def test_multiple_memberships_require_server_validated_selection(self) -> None:
        other_organization = Organization(name="Other workspace")
        self.db.add(other_organization)
        self.db.flush()
        self.db.add(Membership(user_id=self.user.id, organization_id=other_organization.id, role="member"))
        self.db.commit()
        principal = AuthenticatedUser(id=self.user.id, session_id=uuid4(), user=self.user)

        with self.assertRaises(HTTPException) as raised:
            get_current_membership(current_user=principal, db=self.db)
        self.assertEqual(raised.exception.status_code, 409)

        selected_membership = get_current_membership(
            current_user=principal, db=self.db, organization_id=other_organization.id
        )
        self.assertEqual(selected_membership.organization_id, other_organization.id)

        with self.assertRaises(HTTPException) as denied:
            get_current_membership(current_user=principal, db=self.db, organization_id=uuid4())
        self.assertEqual(denied.exception.status_code, 403)

    def test_business_profile_input_rejects_client_tenant_id(self) -> None:
        values = {
            "business_name": "Example",
            "description": "Example business",
            "industry": "Design",
            "website": "https://example.com",
            "location": "London",
            "products_and_services": "Design services",
            "target_market": "Small businesses",
            "unique_value_proposition": "Useful design",
            "communication_style": "Professional",
            "organization_id": str(uuid4()),
        }
        with self.assertRaises(ValidationError):
            BusinessProfileInput.model_validate(values)

    def test_registration_creates_owner_membership_and_maps_duplicate_email(self) -> None:
        payload = RegisterRequest(
            email="new-user@example.com",
            password="long-test-password",
            organization_name="New workspace",
        )
        response = register(payload, response=Response(), db=self.db)
        self.assertTrue(response.authenticated)
        created_user = self.db.query(User).filter_by(email="new-user@example.com").one()
        membership = self.db.query(Membership).filter_by(user_id=created_user.id).one()
        self.assertEqual(membership.role, "owner")
        login_http_response = Response()
        login_response = login(
            LoginRequest(email="new-user@example.com", password="long-test-password"),
            response=login_http_response,
            db=self.db,
        )
        self.assertEqual(login_response.user_id, created_user.id)
        cookie = SimpleCookie()
        cookie.load(login_http_response.headers["set-cookie"])
        token_user_id, token_session_id = decode_access_token(
            cookie[ACCESS_COOKIE_NAME].value, settings.auth_token_secret.get_secret_value()
        )
        self.assertEqual(token_user_id, created_user.id)
        self.assertIsNotNone(self.db.get(AuthSession, token_session_id))
        with self.assertRaises(HTTPException) as bad_login:
            login(
                LoginRequest(email="new-user@example.com", password="incorrect-password"),
                response=Response(),
                db=self.db,
            )
        self.assertEqual(bad_login.exception.status_code, 401)

        with self.assertRaises(HTTPException) as raised:
            register(payload, response=Response(), db=self.db)
        self.assertEqual(raised.exception.status_code, 409)

    def test_access_token_and_password_verification(self) -> None:
        secret = "test-secret-with-more-than-thirty-two-bytes"
        token = create_access_token(self.user.id, uuid4(), secret, 5)
        self.assertEqual(decode_access_token(token, secret)[0], self.user.id)
        with self.assertRaises(ValueError):
            decode_access_token("not-a-valid-token.%", secret)
        with self.assertRaises(ValueError):
            decode_access_token(create_access_token(self.user.id, uuid4(), secret, -1), secret)
        with self.assertRaises(ValueError):
            decode_access_token(token + "tampered", secret)
        self.assertTrue(verify_password("long-test-password", hash_password("long-test-password")))
        self.assertFalse(verify_password("wrong-password", hash_password("long-test-password")))
        self.assertFalse(verify_password("any-password", "scrypt$%%%$%%%"))

    def test_auth_settings_reject_invalid_token_lifetimes_and_production_secret(self) -> None:
        with self.assertRaises(ValueError):
            Settings(_env_file=None, access_token_expire_minutes=0)
        with self.assertRaises(ValueError):
            Settings(_env_file=None, environment="production")


if __name__ == "__main__":
    unittest.main()