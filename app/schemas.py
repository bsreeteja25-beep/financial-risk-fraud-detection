from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

class TransactionIn(BaseModel):
    external_id: str = Field(min_length=1, max_length=150)
    customer_code: str = Field(min_length=1, max_length=64)
    account_code: str = Field(min_length=1, max_length=64)
    transaction_datetime: datetime
    amount: float = Field(gt=0, le=1_000_000_000)
    transaction_type: str = Field(min_length=1, max_length=32)
    channel: str = Field(min_length=1, max_length=32)
    region: str | None = Field(default=None, max_length=100)

class TransactionBatchIn(BaseModel):
    transactions: list[TransactionIn] = Field(min_length=1, max_length=5000)

class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    transaction_id: int
    external_id: str
    account_id: int
    transaction_datetime: datetime
    amount: float
    transaction_type: str
    channel: str
    region: str | None

class ImportResult(BaseModel):
    imported: int
    skipped_duplicates: int
    transaction_ids: list[int]

class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    alert_id: int
    transaction_id: int
    rule_name: str
    risk_score: int
    reason: str
    review_status: str
    reviewer: str | None
    review_note: str | None
    created_at: datetime
    reviewed_at: datetime | None

class ReviewIn(BaseModel):
    review_status: Literal["approved", "dismissed", "pending"]
    reviewer: str = Field(min_length=1, max_length=100)
    review_note: str | None = Field(default=None, max_length=2000)
