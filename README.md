# Financial Risk Analysis and Rule-Based Fraud Detection System

A portfolio project using **synthetic transactions** to calculate transparent risk scores and create alerts for manual review. Alerts are not confirmed fraud.

## Stack
- Python, FastAPI, SQLAlchemy
- SQLite by default; MySQL supported
- Pandas, NumPy, Matplotlib
- Pytest, Git/GitHub

## Setup (Windows PowerShell)
```powershell
cd financial-risk-fraud-detection
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```
If activation is blocked, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in the same PowerShell window, then activate again.

Open `http://127.0.0.1:8000/docs` for interactive API documentation.

## Generate and import synthetic data
In a second terminal:
```powershell
python scripts/generate_synthetic_data.py
python scripts/import_sample_data.py
```
Create charts and CSV reports:
```powershell
python scripts/create_reports.py
```
Run tests:
```powershell
pytest
```

## MySQL setup
Create a database named `financial_risk_db` in MySQL, then set this in `.env`:
```dotenv
DATABASE_URL=mysql+pymysql://risk_user:YOUR_URL_ENCODED_PASSWORD@localhost:3306/financial_risk_db
```
URL-encode special characters in the password. Restart the API. This learning version creates tables automatically; use Alembic migrations for production.

## API endpoints
- `GET /health`
- `POST /api/v1/transactions/import`
- `GET /api/v1/transactions`
- `GET /api/v1/transactions/{transaction_id}`
- `GET /api/v1/alerts`
- `PATCH /api/v1/alerts/{alert_id}/review`
- `GET /api/v1/reports/summary`
- `GET /api/v1/reports/risk-distribution`
- `GET /api/v1/reports/alert-trends`
- `GET /api/v1/audit-logs`

Example import body:
```json
{
  "transactions": [{
    "external_id": "SYN-001",
    "customer_code": "CUST-001",
    "account_code": "ACC-001",
    "transaction_datetime": "2026-10-21T09:00:00",
    "amount": 1250,
    "transaction_type": "payment",
    "channel": "mobile",
    "region": "Hyderabad"
  }]
}
```

Review an alert with `PATCH /api/v1/alerts/1/review` and body:
```json
{"review_status":"dismissed","reviewer":"student","review_note":"Reviewed synthetic example."}
```

## Rules and limitations
- High amount: amount meets/exceeds configured threshold.
- High frequency: account reaches a configured transaction count within a rolling time window.
- Region change: current region differs from the most recent earlier region if both exist.
- Each alert record has a reason and score. Scores are rule weights, **not fraud probabilities**.
- False positives and false negatives are possible. Synthetic data is not representative of real banking activity.
- Use synthetic data only. Never commit `.env`, credentials, database files, or real customer data.

## GitHub
```powershell
git init
git add .
git status
git commit -m "Build rule-based financial risk analysis API"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/financial-risk-fraud-detection.git
git push -u origin main
```
Create an empty GitHub repository first and replace the URL with your own. `.env` and database files are ignored by `.gitignore`.
