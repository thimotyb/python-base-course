from fastapi import Depends, FastAPI, Header, HTTPException, status

from .auth import decode_access_token

app = FastAPI(title="M3 Keycloak JWT Demo")


def require_bearer_token(authorization: str = Header(default="")) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return decode_access_token(token)


@app.get("/")
def root() -> dict:
    return {"message": "M3 Keycloak JWT demo"}


@app.get("/protected")
def protected(payload: dict = Depends(require_bearer_token)) -> dict:
    return {
        "message": "Access granted",
        "client": payload.get("azp"),
        "issuer": payload.get("iss"),
        "subject": payload.get("sub"),
        "scopes": payload.get("scope", ""),
    }

