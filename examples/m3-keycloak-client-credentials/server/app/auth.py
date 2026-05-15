import os
from functools import lru_cache

import jwt
import requests
from fastapi import HTTPException, status
from jwt import PyJWKClient


@lru_cache(maxsize=1)
def get_settings() -> dict[str, str]:
    return {
        "issuer": os.getenv("KEYCLOAK_ISSUER", "http://localhost:8080/realms/m3-jwt"),
        "jwks_url": os.getenv(
            "KEYCLOAK_JWKS_URL",
            "http://localhost:8080/realms/m3-jwt/protocol/openid-connect/certs",
        ),
        "expected_azp": os.getenv("KEYCLOAK_EXPECTED_AZP", "m3-fastapi-client"),
    }


@lru_cache(maxsize=1)
def get_jwk_client() -> PyJWKClient:
    return PyJWKClient(get_settings()["jwks_url"])


def decode_access_token(token: str) -> dict:
    settings = get_settings()
    jwk_client = get_jwk_client()
    signing_key = jwk_client.get_signing_key_from_jwt(token)

    try:
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=settings["issuer"],
            options={"verify_aud": False},
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    if payload.get("azp") != settings["expected_azp"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token was not issued for the expected client",
        )

    return payload


def fetch_token(token_url: str, client_id: str, client_secret: str) -> dict:
    response = requests.post(
        token_url,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
