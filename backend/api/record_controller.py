import json

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database.postgres import get_db
from dto.record_dto import RecordDTO
from schema.record import Record
from core.queue import event_queue
import json
from datetime import datetime

router = APIRouter(
    prefix="/api/records",
    tags=["Records"]
)

@router.get("/", response_model=list[RecordDTO])
def getAllRecords(limit: int = Query(30, ge=1), db: Session = Depends(get_db)):
    return db.query(Record).order_by(
        Record.timestamp.desc()
    ).limit(limit).all()


@router.get("/events")
async def stream_events():

    async def event_generator():
        while True:
            data = await event_queue.get()
            safe_data = str(data) 
            yield f"data: {json.dumps(data, default=str)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "http://localhost:5173", # 👈 important
        },
    )


def save_transaction(data: dict):
    db_gen = get_db()
    db = next(db_gen)

    try:
        record = Record(
            transactionId=data["transactionId"],
            timestamp=data["timestamp"] if isinstance(data["timestamp"], datetime)
                     else datetime.fromisoformat(data["timestamp"]),

            diagram=data.get("diagram"),
            reason=data.get("reason"),
            pattern=data.get("pattern"),

            related_ids=data.get("related_ids", []),

            fraud_score=data.get("fraud_score"),
            risk_level=data.get("risk_level"),

            is_fraud=data.get("is_fraud", True)
        )

        db.add(record)
        db.commit()

    except Exception as e:
        db.rollback()
        print("❌ DB Save Failed:", e)

    finally:
        db.close()