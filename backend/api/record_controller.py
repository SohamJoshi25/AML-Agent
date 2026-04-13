import json

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database.postgres import get_db
from dto.record import RecordSchema
from schema.record import Record
from core.queue import event_queue

import json
from datetime import datetime

router = APIRouter(
    prefix="/api/records",
    tags=["Records"]
)

@router.get("/", response_model=list[RecordSchema])
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
            yield f"data: {safe_data}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")



def save_transaction(txn, result):
    db_gen = get_db()
    db = next(db_gen)

    try:
        record = Record(
            transactionId=txn["transactionId"],
            timestamp=datetime.fromisoformat(txn["timestamp"]),
            data=str(result)  # ✅ full result stored
        )

        db.add(record)
        db.commit()

    except Exception as e:
        db.rollback()
        print("❌ DB Save Failed:", e)

    finally:
        db.close()