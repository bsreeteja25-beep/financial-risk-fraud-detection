def sample_tx(**overrides):
    data = {"external_id":"TEST-1","customer_code":"CUST-T1","account_code":"ACC-T1",
            "transaction_datetime":"2026-10-21T10:00:00","amount":100.0,
            "transaction_type":"payment","channel":"mobile","region":"Hyderabad"}
    data.update(overrides)
    return data

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_import_and_retrieve(client):
    response = client.post("/api/v1/transactions/import", json={"transactions":[sample_tx()]})
    assert response.status_code == 200 and response.json()["imported"] == 1
    listing = client.get("/api/v1/transactions")
    assert listing.status_code == 200 and len(listing.json()) == 1

def test_duplicate_external_id_skipped(client):
    body = {"transactions":[sample_tx()]}
    assert client.post("/api/v1/transactions/import", json=body).json()["imported"] == 1
    assert client.post("/api/v1/transactions/import", json=body).json()["skipped_duplicates"] == 1

def test_high_amount_creates_pending_alert(client):
    response = client.post("/api/v1/transactions/import",
                           json={"transactions":[sample_tx(external_id="HIGH-1", amount=90000)]})
    assert response.status_code == 200
    alerts = client.get("/api/v1/alerts").json()
    assert any(a["rule_name"] == "high_amount" for a in alerts)
    assert all(a["review_status"] == "pending" for a in alerts)

def test_review_alert(client):
    client.post("/api/v1/transactions/import",
                json={"transactions":[sample_tx(external_id="HIGH-2", amount=90000)]})
    alert = client.get("/api/v1/alerts").json()[0]
    response = client.patch(f"/api/v1/alerts/{alert['alert_id']}/review",
                            json={"review_status":"dismissed","reviewer":"tester",
                                  "review_note":"Reviewed synthetic example."})
    assert response.status_code == 200
    assert response.json()["review_status"] == "dismissed"

def test_summary_report(client):
    client.post("/api/v1/transactions/import",
                json={"transactions":[sample_tx(external_id="RPT-1", amount=90000)]})
    summary = client.get("/api/v1/reports/summary").json()
    assert summary["transaction_count"] == 1
    assert summary["alert_count"] >= 1
