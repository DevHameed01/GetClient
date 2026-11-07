import binascii
import base64
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from jwt.exceptions import InvalidTokenError


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=64, maxmem=64 * 1024 * 1024
    )
    return f"scrypt${_encode(salt)}${_encode(digest)}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, salt_value, digest_value = password_hash.split("$")
        if algorithm != "scrypt":
            return False
        salt = _decode(salt_value)
        expected_digest = _decode(digest_value)
        actual_digest = hashlib.scrypt(
            password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=64, maxmem=64 * 1024 * 1024
        )
        return hmac.compare_digest(actual_digest, expected_digest)
    except (ValueError, TypeError, binascii.Error):
        return False


def _encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode()


def _decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def create_access_token(user_id: UUID, session_id: UUID, secret: str, expires_in_minutes: int) -> str:
    payload = {
        "sub": str(user_id),
        "sid": str(session_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes),
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def decode_access_token(token: str, secret: str) -> tuple[UUID, UUID]:
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        if (
            not isinstance(payload, dict)
            or not isinstance(payload.get("sub"), str)
            or not isinstance(payload.get("sid"), str)
        ):
            raise ValueError("Invalid token payload")
        return UUID(payload["sub"]), UUID(payload["sid"])
    except (InvalidTokenError, KeyError, TypeError, ValueError) as error:
        raise ValueError("Invalid access token") from error