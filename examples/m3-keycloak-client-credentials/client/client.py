import os
import sys

import requests


TOKEN_URL = os.getenv(
    "TOKEN_URL",
    "http://localhost:8080/realms/m3-jwt/protocol/openid-connect/token",
)
API_URL = os.getenv("API_URL", "http://localhost:8001/protected")
CLIENT_ID = os.getenv("CLIENT_ID", "m3-fastapi-client")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "m3-fastapi-secret")


def get_token() -> str:
    response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["access_token"]


def call_api(access_token: str) -> dict:
    response = requests.get(
        API_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def main() -> int:
    access_token = get_token()
    payload = call_api(access_token)
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

