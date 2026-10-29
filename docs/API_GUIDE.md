# API Guide

Base URL: `http://127.0.0.1:8000`. If `API_KEY` is set, send `X-API-Key`.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/api/v1/transactions/import` | Import synthetic transactions |
| GET | `/api/v1/transactions` | List transactions |
| GET | `/api/v1/transactions/{id}` | Retrieve one transaction |
| GET | `/api/v1/alerts` | List/filter alerts |
| PATCH | `/api/v1/alerts/{id}/review` | Update human review status |
| GET | `/api/v1/reports/summary` | Counts |
| GET | `/api/v1/reports/risk-distribution` | Scores distribution |
| GET | `/api/v1/reports/alert-trends` | Daily alert trend |
| GET | `/api/v1/audit-logs` | Recent audit events |

Review body:
```json
{"review_status":"dismissed","reviewer":"student","review_note":"Reviewed synthetic example."}
```
Review status accepts `pending`, `approved`, or `dismissed`. These workflow labels do not establish fraud.
