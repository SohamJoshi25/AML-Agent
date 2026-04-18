from sqlalchemy import JSON, Column, String, Boolean, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Record(Base):
    __tablename__ = "record_tb"

    transactionId = Column(UUID(as_uuid=True), primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)

    diagram = Column(String, nullable=True)
    reason = Column(String, nullable=False)
    pattern = Column(String, nullable=True)

    related_ids = Column(JSON, nullable=True) 

    fraud_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)

    is_fraud = Column(Boolean, nullable=False)