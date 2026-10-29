import json, random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(21)
out = Path(__file__).resolve().parents[1] / "data" / "synthetic_transactions.json"
out.parent.mkdir(parents=True, exist_ok=True)
regions = ["Hyderabad", "Bengaluru", "Chennai", "Pune"]
channels = ["mobile", "web", "card", "atm"]
rows = []
start = datetime(2026, 10, 20, 9, 0)
for i in range(1, 61):
    account = (i % 8) + 1
    rows.append({
        "external_id": f"SYN-{i:04d}", "customer_code": f"CUST-{account:04d}",
        "account_code": f"ACC-{account:04d}",
        "transaction_datetime": (start + timedelta(minutes=i*17)).isoformat(),
        "amount": round(random.uniform(100, 12000), 2),
        "transaction_type": random.choice(["payment", "transfer", "withdrawal"]),
        "channel": random.choice(channels), "region": random.choice(regions)
    })
special = [
    ("SYN-HIGH-1","CUST-9001","ACC-9001",start+timedelta(days=1),90000,"payment","web","Hyderabad"),
    ("SYN-FREQ-1","CUST-9002","ACC-9002",start+timedelta(days=1,hours=1),400,"payment","mobile","Hyderabad"),
    ("SYN-FREQ-2","CUST-9002","ACC-9002",start+timedelta(days=1,hours=1,minutes=1),500,"payment","mobile","Hyderabad"),
    ("SYN-FREQ-3","CUST-9002","ACC-9002",start+timedelta(days=1,hours=1,minutes=2),600,"payment","mobile","Hyderabad"),
    ("SYN-FREQ-4","CUST-9002","ACC-9002",start+timedelta(days=1,hours=1,minutes=3),700,"payment","mobile","Hyderabad"),
    ("SYN-FREQ-5","CUST-9002","ACC-9002",start+timedelta(days=1,hours=1,minutes=4),800,"payment","mobile","Hyderabad"),
    ("SYN-REGION-1","CUST-9003","ACC-9003",start+timedelta(days=1,hours=2),1000,"payment","mobile","Chennai"),
    ("SYN-REGION-2","CUST-9003","ACC-9003",start+timedelta(days=1,hours=3),1100,"payment","mobile","Pune")
]
for ext,cust,acct,dt,amount,typ,channel,region in special:
    rows.append({"external_id":ext,"customer_code":cust,"account_code":acct,
                 "transaction_datetime":dt.isoformat(),"amount":amount,"transaction_type":typ,
                 "channel":channel,"region":region})
out.write_text(json.dumps({"transactions":rows}, indent=2), encoding="utf-8")
print(f"Wrote {len(rows)} synthetic transactions to {out}")
