import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

root = Path(__file__).resolve().parents[1]
load_dotenv(root / ".env")
url = os.getenv("DATABASE_URL", "sqlite:///./data/risk_analysis.db")
if url.startswith("sqlite:///./"):
    url = "sqlite:///" + str((root / url.replace("sqlite:///./", "", 1)).resolve()).replace("\\", "/")
engine = create_engine(url, pool_pre_ping=True)
out = root / "reports"
out.mkdir(exist_ok=True)
with engine.connect() as conn:
    alerts = pd.read_sql(text("SELECT alert_id, transaction_id, rule_name, risk_score, review_status, created_at FROM alerts"), conn)
if alerts.empty:
    print("No alerts yet. Start the API and import sample data first.")
else:
    alerts["created_at"] = pd.to_datetime(alerts["created_at"])
    ax = alerts.groupby("risk_score").size().sort_index().plot(kind="bar", title="Alert Risk Score Distribution")
    ax.set_xlabel("Risk score"); ax.set_ylabel("Alert records")
    plt.tight_layout(); plt.savefig(out / "risk_score_distribution.png", dpi=150); plt.close()
    ax = alerts.set_index("created_at").resample("D").size().plot(kind="line", marker="o", title="Daily Alert Trend")
    ax.set_xlabel("Date"); ax.set_ylabel("Alert records")
    plt.tight_layout(); plt.savefig(out / "daily_alert_trends.png", dpi=150); plt.close()
    alerts.to_csv(out / "alerts_export.csv", index=False)
    print(f"Reports saved to {out}")
