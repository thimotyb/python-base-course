from __future__ import annotations

from datetime import datetime, timezone

from fastapi import FastAPI, Path
from pydantic import BaseModel


app = FastAPI(title="Mock Microsoft Graph / SharePoint")


class UploadResponse(BaseModel):
    id: str
    name: str
    webUrl: str
    lastModifiedDateTime: str
    size: int
    source: str


class ListItemFields(BaseModel):
    title: str
    order_id: int
    customer: str
    order_date: str
    status: str
    total_rows: int


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1.0/sites/{site_id}/drive/root:/{path:path}:/content", response_model=UploadResponse)
def upload_document(
    site_id: str = Path(..., min_length=1),
    path: str = Path(..., min_length=1),
) -> UploadResponse:
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    filename = path.rsplit("/", 1)[-1] or "document.html"
    return UploadResponse(
        id=f"mock-{site_id}-{filename}",
        name=filename,
        webUrl=f"http://127.0.0.1:8090/mock/{site_id}/{path}",
        lastModifiedDateTime=now,
        size=0,
        source="mock-microsoft-graph",
    )


@app.post("/v1.0/sites/{site_id}/lists/{list_id}/items")
def create_list_item(
    site_id: str,
    list_id: str,
    payload: ListItemFields,
) -> dict[str, object]:
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return {
        "id": f"mock-{site_id}-{list_id}-{payload.order_id}",
        "createdDateTime": now,
        "lastModifiedDateTime": now,
        "fields": payload.model_dump(),
        "source": "mock-microsoft-graph",
    }
