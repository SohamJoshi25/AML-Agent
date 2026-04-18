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

    related_ids: List[str]

    fraud_score: float
    risk_level: str
    is_fraud: bool

    class Config:
        from_attributes = True