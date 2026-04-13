import asyncio
from contextlib import asynccontextmanager
import threading

from fastapi import FastAPI
from sqlalchemy import text
from database.postgres import get_db, engine, Base
from schema.record import Record   
from consumer.kafka import start_consumer
from api.record_controller import router as record_router

from core.runtime import main_loop as _main_loop
import core.runtime as runtime


@asynccontextmanager
async def lifespan(app: FastAPI):
    runtime.main_loop = asyncio.get_running_loop() 

    try:
        db_generator = get_db()
        db = next(db_generator)

        db.execute(text("SELECT 1"))

        print("✅ Database Connected Successfully")

    except Exception as e:
        print("❌ Database Connection Failed")
        print(e)

    finally:
        db.close()
    
    thread = threading.Thread(target=start_consumer, daemon=True)
    thread.start()

    print("✅ Kafka consumer started")

    yield  # 🚀 App runs here

    # 🔻 SHUTDOWN LOGIC (optional)
    print("🛑 Application shutting down")

Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=lifespan)

app.include_router(record_router)

@app.get("/")
def home():
    return {"message": "Agentic AI Server Running"}