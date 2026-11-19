# Mock Microsoft Graph / SharePoint

Questo servizio locale simula la parte SharePoint di Microsoft Graph per testare l'esempio senza un tenant reale.

## Endpoints

- `GET /health`
- `POST /v1.0/sites/{site_id}/drive/root:/{path:path}:/content`
- `POST /v1.0/sites/{site_id}/lists/{list_id}/items`

## Avvio

```bash
cd /home/thimoty/git/python-base/examples/integration/mock-microsoft-graph
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8090
```

## Uso atteso

Il flow Mule può puntare a questo mock quando non hai ancora un tenant Microsoft Graph disponibile.
