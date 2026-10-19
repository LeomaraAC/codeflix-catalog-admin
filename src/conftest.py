from datetime import datetime, timedelta, timezone

import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from rest_framework.test import APIClient


@pytest.fixture(scope="session")
def rsa_key_pair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode()
    return private_key, public_key_pem


@pytest.fixture
def token_factory(rsa_key_pair, monkeypatch):
    private_key, public_key_pem = rsa_key_pair
    public_key_body = "".join(public_key_pem.splitlines()[1:-1])
    monkeypatch.setenv("AUTH_PUBLIC_KEY", public_key_body)

    def create_token():
        now = datetime.now(timezone.utc)
        payload = {
            "sub": "test-user",
            "aud": "account",
            "iat": now,
            "exp": now + timedelta(minutes=5),
            "realm_access": {"roles": ["offline_access","admin", "uma_authorization", "default-roles-codeflix"] },
        }
        return jwt.encode(payload, private_key, algorithm="RS256")

    return create_token


@pytest.fixture
def authenticated_client(token_factory):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_factory()}")
    return client
