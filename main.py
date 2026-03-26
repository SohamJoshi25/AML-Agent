from kafka import KafkaConsumer
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import json

from agent.graph import build_graph
from config.settings import KAFKA_TOPIC, KAFKA_BOOTSTRAP
from dotenv import load_dotenv

load_dotenv()
app = build_graph()



def process_transaction(txn):
    print(f"Transaction: {txn}")
    result = app.invoke({
        "transaction": txn,
        "messages":[]
    })

    last_ai = None
    messages = result.get("messages", [])
    
    for msg in messages:
        if isinstance(msg, AIMessage):
            last_ai = msg

    if last_ai:
        print(last_ai.content.strip())
    else:
        print(messages[-1])


def start_consumer():
    print(f"Consumer started on {KAFKA_BOOTSTRAP} for topic: {KAFKA_TOPIC}")
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    for message in consumer:
        txn = message.value
        process_transaction(txn)


if __name__ == "__main__":
    start_consumer()
   # process_transaction({"account_id":"1","amount":1000000})