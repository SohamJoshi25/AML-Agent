import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database.postgres import Base


class Record(Base):
    __tablename__ = "record_tb"

    transactionId = Column(UUID(as_uuid=True), primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    data = Column(String, nullable=True)