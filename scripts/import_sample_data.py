import os, urllib.request, urllib.error
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = root / "data" / "synthetic_transactions.json"
if not data.exists():
    raise SystemExit("Run python scripts/generate_synthetic_data.py first.")
base = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
headers = {"Content-Type": "application/json"}
if os.getenv("API_KEY"):
    headers["X-API-Key"] = os.getenv("API_KEY")
req = urllib.request.Request(f"{base}/api/v1/transactions/import", data=data.read_bytes(),
                             headers=headers, method="POST")
try:
    with urllib.request.urlopen(req, timeout=30) as response:
        print(response.read().decode())
except urllib.error.URLError as exc:
    raise SystemExit(f"Start the API first with 'uvicorn app.main:app --reload'. Details: {exc}")
