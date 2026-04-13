from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class RecordSchema(BaseModel):
    transactionId: UUID
    timestamp: datetime
    data: str

    class Config:
        from_attributes = True 