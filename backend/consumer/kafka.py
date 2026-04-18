import asyncio

from kafka import KafkaConsumer
from core.queue import event_queue
import json
from agent.graph import build_graph
from config.settings import KAFKA_TOPIC, KAFKA_BOOTSTRAP
from dotenv import load_dotenv
import core.runtime as runtime

from api.record_controller import save_transaction

load_dotenv()
app = build_graph()


async def process_transaction(txn):
    print(f"Transaction: {txn}")

    # 🚀 offload blocking graph computation
    result = await asyncio.to_thread(
        app.invoke,
        {
            "transaction": txn,
            "messages": []
        }
    )

    txn_id = txn.get("transactionId")
    timestamp = txn["timestamp"]

    diagram = result.get("diagram", "")
    reason = result.get("reason", "")
    pattern = result.get("pattern","")
    related_transactions = result.get("related_transactions", [])

    related_ids = [t.get("transactionId") for t in related_transactions]

    fraud_score = result.get("fraud_score", -1)
    is_fraud = result.get("is_fraud", False)
    risk_level = result.get("risk_level", -1)

    data = {
        "transactionId": txn_id,
        "timestamp": timestamp,
        "diagram": diagram,
        "reason": reason,
        "pattern": pattern,
        "related_ids": related_ids,
        "fraud_score": fraud_score,
        "risk_level": risk_level,
        "is_fraud": is_fraud
    }

    print(data)

    # 🚀 offload DB write
    await asyncio.to_thread(save_transaction, data)

    await event_queue.put(data)

    
def start_consumer():
    print(f"Consumer started on {KAFKA_BOOTSTRAP} for topic: {KAFKA_TOPIC}")
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )


    for message in consumer:
        txn = message.value

        if runtime.main_loop is None:
            print("❌ Main loop not ready")
            continue

        asyncio.run_coroutine_threadsafe(
            process_transaction(txn),
            runtime.main_loop
        )

async def main():

    txn = {
        "transactionId": "a1f3c9d2-7b6e-4d1a-9c3f-2e5b7a8d1001",
        "timestamp": "2022-09-04T14:59:00",
        "fromBank": "0048309",
        "fromAccount": "811C599A0",
        "toBank": "0119",
        "toAccount": "811C597B0",
        "amountReceived": 64379.45,
        "receivingCurrency": "Saudi Riyal",
        "amountPaid": 64379.45,
        "paymentCurrency": "Saudi Riyal",
        "paymentFormat": "ACH"
    }

    await process_transaction(txn)
     


if __name__ == "__main__":
    asyncio.run(main())