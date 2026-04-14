from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List


class RecordDTO(BaseModel):
    transactionId: UUID
    timestamp: datetime

    diagram: str | None
    reason: str
    pattern: str | None

    related_ids: dict

    fraud_score: float
    risk_level: str
    isFraud: bool

    class Config:
        from_attributes = True