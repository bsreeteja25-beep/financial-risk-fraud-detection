from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import select, desc, func
from sqlalchemy.orm import Session
from app.audit import log_action
from app.config import settings
from app.database import Base, engine, get_db
from app.models import Alert, AuditLog, Transaction
from app.schemas import AlertOut, ImportResult, ReviewIn, TransactionBatchIn, TransactionOut
from app.security import require_api_key
from app.services import import_transactions

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title=settings.app_name,
    description="Synthetic-data demonstration. Alerts require human review and do not confirm fraud.",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "message": "Risk analysis API is running"}

@app.post("/api/v1/transactions/import", response_model=ImportResult,
          dependencies=[Depends(require_api_key)], tags=["transactions"])
def import_batch(payload: TransactionBatchIn, db: Session = Depends(get_db)):
    try:
        result = import_transactions(db, payload.transactions)
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    log_action(db, "transactions_imported", "transaction_batch",
               details=f"imported={result['imported']}; skipped_duplicates={result['skipped_duplicates']}")
    db.commit()
    return result

@app.get("/api/v1/transactions", response_model=list[TransactionOut],
         dependencies=[Depends(require_api_key)], tags=["transactions"])
def list_transactions(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0),
                      db: Session = Depends(get_db)):
    return db.scalars(select(Transaction).order_by(desc(Transaction.transaction_datetime))
                      .offset(offset).limit(limit)).all()

@app.get("/api/v1/transactions/{transaction_id}", response_model=TransactionOut,
         dependencies=[Depends(require_api_key)], tags=["transactions"])
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    tx = db.get(Transaction, transaction_id)
    if tx is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx

@app.get("/api/v1/alerts", response_model=list[AlertOut],
         dependencies=[Depends(require_api_key)], tags=["alerts"])
def list_alerts(review_status: str | None = Query(None, pattern="^(pending|approved|dismissed)$"),
                min_score: int = Query(0, ge=0, le=100), limit: int = Query(100, ge=1, le=1000),
                offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    query = select(Alert).where(Alert.risk_score >= min_score)
    if review_status:
        query = query.where(Alert.review_status == review_status)
    return db.scalars(query.order_by(desc(Alert.created_at)).offset(offset).limit(limit)).all()

@app.patch("/api/v1/alerts/{alert_id}/review", response_model=AlertOut,
           dependencies=[Depends(require_api_key)], tags=["alerts"])
def review_alert(alert_id: int, payload: ReviewIn, db: Session = Depends(get_db)):
    alert = db.get(Alert, alert_id)
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.review_status = payload.review_status
    alert.reviewer = payload.reviewer
    alert.review_note = payload.review_note
    alert.reviewed_at = datetime.utcnow()
    log_action(db, "alert_reviewed", "alert", alert_id, actor=payload.reviewer,
               details=f"review_status={payload.review_status}")
    db.commit()
    db.refresh(alert)
    return alert

@app.get("/api/v1/reports/summary", dependencies=[Depends(require_api_key)], tags=["reports"])
def report_summary(db: Session = Depends(get_db)):
    total = db.scalar(select(func.count(Transaction.transaction_id))) or 0
    alerts = db.scalar(select(func.count(Alert.alert_id))) or 0
    pending = db.scalar(select(func.count(Alert.alert_id)).where(Alert.review_status == "pending")) or 0
    return {"transaction_count": total, "alert_count": alerts, "pending_alert_count": pending,
            "note": "Alerts are rule triggers for manual review, not confirmed fraud."}

@app.get("/api/v1/reports/risk-distribution", dependencies=[Depends(require_api_key)], tags=["reports"])
def risk_distribution(db: Session = Depends(get_db)):
    rows = db.execute(select(Alert.risk_score, func.count(Alert.alert_id))
                      .group_by(Alert.risk_score).order_by(Alert.risk_score)).all()
    return {"distribution": [{"risk_score": score, "count": count} for score, count in rows]}

@app.get("/api/v1/reports/alert-trends", dependencies=[Depends(require_api_key)], tags=["reports"])
def alert_trends(db: Session = Depends(get_db)):
    rows = db.execute(select(func.date(Alert.created_at), func.count(Alert.alert_id))
                      .group_by(func.date(Alert.created_at)).order_by(func.date(Alert.created_at))).all()
    return {"daily_alerts": [{"date": str(day), "count": count} for day, count in rows]}

@app.get("/api/v1/audit-logs", dependencies=[Depends(require_api_key)], tags=["audit"])
def audit_logs(limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    rows = db.scalars(select(AuditLog).order_by(desc(AuditLog.created_at)).limit(limit)).all()
    return [{"audit_id": r.audit_id, "action": r.action, "resource_type": r.resource_type,
             "resource_id": r.resource_id, "actor": r.actor, "details": r.details,
             "created_at": r.created_at} for r in rows]
