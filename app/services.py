from sqlalchemy import select
from app.models import Account, Alert, Customer, Transaction
from app.risk_engine import evaluate_transaction

def import_transactions(db, items):
    imported_ids, skipped = [], 0
    # Chronological processing makes frequency checks reproducible.
    ordered = sorted(items, key=lambda item: item.transaction_datetime)
    for item in ordered:
        if db.scalar(select(Transaction).where(Transaction.external_id == item.external_id)):
            skipped += 1
            continue
        customer = db.scalar(select(Customer).where(Customer.customer_code == item.customer_code))
        if customer is None:
            customer = Customer(customer_code=item.customer_code)
            db.add(customer)
            db.flush()
        account = db.scalar(select(Account).where(Account.account_code == item.account_code))
        if account is None:
            account = Account(account_code=item.account_code, customer_id=customer.customer_id)
            db.add(account)
            db.flush()
        elif account.customer_id != customer.customer_id:
            raise ValueError(f"Account '{item.account_code}' is already associated with another customer.")
        tx = Transaction(
            external_id=item.external_id, account_id=account.account_id,
            transaction_datetime=item.transaction_datetime, amount=item.amount,
            transaction_type=item.transaction_type, channel=item.channel, region=item.region
        )
        db.add(tx)
        db.flush()
        hits = evaluate_transaction(db, tx)
        if hits:
            score = min(100, sum(hit["risk_score"] for hit in hits))
            for hit in hits:
                db.add(Alert(transaction_id=tx.transaction_id, rule_name=hit["rule_name"],
                             risk_score=score, reason=hit["reason"], review_status="pending"))
        imported_ids.append(tx.transaction_id)
    db.commit()
    return {"imported": len(imported_ids), "skipped_duplicates": skipped, "transaction_ids": imported_ids}
