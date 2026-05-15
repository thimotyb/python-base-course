#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs
from urllib.request import Request, urlopen

import jwt
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from jwt.algorithms import RSAAlgorithm


ROOT = Path(__file__).resolve().parents[2]
EXAMPLE_DIR = ROOT / "examples" / "m3-keycloak-client-credentials"
SERVER_DIR = EXAMPLE_DIR / "server"
CLIENT_DIR = EXAMPLE_DIR / "client"
CLIENT_SCRIPT = CLIENT_DIR / "client.py"

REALM = "m3-jwt"
CLIENT_ID = "m3-fastapi-client"
CLIENT_SECRET = "m3-fastapi-secret"
KID = "m3-keycloak-smoke-key"


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def wait_for_http(url: str, timeout: float = 30.0) -> None:
    deadline = time.time() + timeout
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            with urlopen(url, timeout=2) as response:
                if 200 <= response.status < 500:
                    return
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            time.sleep(0.5)
    raise RuntimeError(f"Timed out waiting for {url}") from last_error


@dataclass
class DemoAuthState:
    issuer: str
    token_path: str
    jwks_path: str
    private_key: rsa.RSAPrivateKey
    public_jwk: dict[str, Any]

    def mint_token(self, client_id: str) -> str:
        now = int(time.time())
        payload = {
            "iss": self.issuer,
            "sub": f"service-account-{client_id}",
            "azp": client_id,
            "scope": "openid profile email",
            "iat": now,
            "exp": now + 300,
        }
        token = jwt.encode(
            payload,
            self.private_key,
            algorithm="RS256",
            headers={"kid": KID, "typ": "JWT"},
        )
        if isinstance(token, bytes):
            return token.decode("utf-8")
        return token


def build_auth_state(base_url: str) -> DemoAuthState:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    jwk = json.loads(RSAAlgorithm.to_jwk(public_key))
    jwk.update({"kid": KID, "use": "sig", "alg": "RS256"})
    return DemoAuthState(
        issuer=f"{base_url}/realms/{REALM}",
        token_path=f"/realms/{REALM}/protocol/openid-connect/token",
        jwks_path=f"/realms/{REALM}/protocol/openid-connect/certs",
        private_key=private_key,
        public_jwk=jwk,
    )


def make_handler(state: DemoAuthState):
    class DemoHandler(BaseHTTPRequestHandler):
        server_version = "DemoKeycloak/1.0"

        def _send_json(self, status: int, payload: dict[str, Any]) -> None:
            body = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802
            if self.path == state.jwks_path:
                self._send_json(200, {"keys": [state.public_jwk]})
                return
            if self.path == "/health":
                self._send_json(200, {"status": "ok"})
                return
            self._send_json(404, {"error": "not_found"})

        def do_POST(self) -> None:  # noqa: N802
            if self.path != state.token_path:
                self._send_json(404, {"error": "not_found"})
                return

            content_length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(content_length).decode("utf-8")
            params = {key: values[0] for key, values in parse_qs(body).items()}

            if params.get("grant_type") != "client_credentials":
                self._send_json(400, {"error": "unsupported_grant_type"})
                return
            if params.get("client_id") != CLIENT_ID or params.get("client_secret") != CLIENT_SECRET:
                self._send_json(401, {"error": "invalid_client"})
                return

            token = state.mint_token(params["client_id"])
            self._send_json(
                200,
                {
                    "access_token": token,
                    "token_type": "Bearer",
                    "expires_in": 300,
                },
            )

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
            return

    return DemoHandler


def start_fake_keycloak() -> tuple[ThreadingHTTPServer, threading.Thread, str, DemoAuthState]:
    port = free_port()
    base_url = f"http://127.0.0.1:{port}"
    state = build_auth_state(base_url)
    handler = make_handler(state)
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    wait_for_http(f"{base_url}/health")
    return server, thread, base_url, state


def start_fastapi_server(keycloak_base_url: str, jwks_url: str) -> subprocess.Popen[str]:
    port = free_port()
    candidate_pythons = [
        EXAMPLE_DIR / ".venv" / "bin" / "python",
        ROOT / ".venv" / "bin" / "python",
        Path(sys.executable),
    ]
    server_python = next((path for path in candidate_pythons if path.exists()), Path(sys.executable))
    env = os.environ.copy()
    env.update(
        {
            "KEYCLOAK_ISSUER": f"{keycloak_base_url}/realms/{REALM}",
            "KEYCLOAK_JWKS_URL": jwks_url,
            "KEYCLOAK_EXPECTED_AZP": CLIENT_ID,
            "PYTHONUNBUFFERED": "1",
        }
    )
    proc = subprocess.Popen(
        [
            str(server_python),
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        cwd=SERVER_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    api_base_url = f"http://127.0.0.1:{port}"
    try:
        wait_for_http(f"{api_base_url}/")
    except Exception:
        stdout, stderr = proc.communicate(timeout=5)
        raise RuntimeError(
            "FastAPI server failed to start.\n"
            f"stdout:\n{stdout}\n"
            f"stderr:\n{stderr}"
        )
    return proc, api_base_url


def stop_process(proc: subprocess.Popen[str]) -> None:
    if proc.poll() is not None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=10)


def call_token_endpoint(token_url: str) -> dict[str, Any]:
    response = requests.post(
        token_url,
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def call_protected_endpoint(api_url: str, access_token: str) -> dict[str, Any]:
    response = requests.get(
        f"{api_url}/protected",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def assert_unauthorized(api_url: str) -> None:
    request = Request(f"{api_url}/protected")
    try:
        with urlopen(request, timeout=30):
            raise AssertionError("Protected endpoint should reject missing bearer token")
    except HTTPError as exc:
        if exc.code != 401:
            raise AssertionError(f"Expected 401, got {exc.code}") from exc


def run_client_script(token_url: str, api_url: str) -> str:
    env = os.environ.copy()
    env.update(
        {
            "TOKEN_URL": token_url,
            "API_URL": api_url + "/protected",
            "CLIENT_ID": CLIENT_ID,
            "CLIENT_SECRET": CLIENT_SECRET,
        }
    )
    completed = subprocess.run(
        [sys.executable, str(CLIENT_SCRIPT)],
        cwd=CLIENT_DIR,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "Client script failed.\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}"
        )
    return completed.stdout.strip()


def main() -> int:
    fake_keycloak_server: ThreadingHTTPServer | None = None
    fake_keycloak_thread: threading.Thread | None = None
    fastapi_proc: subprocess.Popen[str] | None = None
    try:
        fake_keycloak_server, fake_keycloak_thread, keycloak_base_url, state = start_fake_keycloak()
        token_url = f"{keycloak_base_url}{state.token_path}"
        jwks_url = f"{keycloak_base_url}{state.jwks_path}"
        fastapi_proc, api_base_url = start_fastapi_server(keycloak_base_url, jwks_url)

        assert_unauthorized(api_base_url)

        token_data = call_token_endpoint(token_url)
        if token_data.get("token_type") != "Bearer":
            raise AssertionError(f"Unexpected token_type: {token_data.get('token_type')}")

        access_token = token_data["access_token"]
        protected_data = call_protected_endpoint(api_base_url, access_token)
        if protected_data.get("client") != CLIENT_ID:
            raise AssertionError(f"Unexpected client in protected payload: {protected_data}")
        if protected_data.get("issuer") != f"{keycloak_base_url}/realms/{REALM}":
            raise AssertionError(f"Unexpected issuer in protected payload: {protected_data}")

        client_output = run_client_script(token_url, api_base_url)
        if "Access granted" not in client_output and "client" not in client_output:
            raise AssertionError(f"Client script did not print a success payload: {client_output}")

        print("[ok] Keycloak token endpoint, FastAPI validation and client script all passed")
        print(f"[ok] Token URL: {token_url}")
        print(f"[ok] API URL: {api_base_url}/protected")
        return 0
    finally:
        if fastapi_proc is not None:
            stop_process(fastapi_proc)
        if fake_keycloak_server is not None:
            fake_keycloak_server.shutdown()
            fake_keycloak_server.server_close()
        if fake_keycloak_thread is not None and fake_keycloak_thread.is_alive():
            fake_keycloak_thread.join(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
