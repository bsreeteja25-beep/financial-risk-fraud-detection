from datetime import timedelta
from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
from app.config import settings
from app.models import Transaction

def evaluate_transaction(db: Session, tx: Transaction) -> list[dict]:
    hits = []
    if tx.amount >= settings.high_amount_threshold:
        hits.append({
            "rule_name": "high_amount",
            "risk_score": settings.high_amount_risk,
            "reason": f"Amount {tx.amount:.2f} meets/exceeds threshold {settings.high_amount_threshold:.2f}."
        })

    start = tx.transaction_datetime - timedelta(minutes=settings.frequency_window_minutes)
    count = db.scalar(select(func.count(Transaction.transaction_id)).where(
        Transaction.account_id == tx.account_id,
        Transaction.transaction_datetime >= start,
        Transaction.transaction_datetime <= tx.transaction_datetime
    )) or 0
    if count >= settings.frequency_count_threshold:
        hits.append({
            "rule_name": "high_frequency",
            "risk_score": settings.frequency_risk,
            "reason": f"{count} transactions for this account occurred within {settings.frequency_window_minutes} minutes; threshold is {settings.frequency_count_threshold}."
        })

    if tx.region:
        previous = db.scalar(select(Transaction).where(
            Transaction.account_id == tx.account_id,
            Transaction.transaction_id != tx.transaction_id,
            Transaction.transaction_datetime < tx.transaction_datetime,
            Transaction.region.is_not(None)
        ).order_by(desc(Transaction.transaction_datetime)).limit(1))
        if previous and previous.region and previous.region.casefold() != tx.region.casefold():
            hits.append({
                "rule_name": "region_change",
                "risk_score": settings.region_change_risk,
                "reason": f"Region changed from '{previous.region}' to '{tx.region}' compared with the most recent earlier transaction."
            })

    score = min(100, sum(hit["risk_score"] for hit in hits))
    return hits if score >= settings.alert_score_threshold else []
