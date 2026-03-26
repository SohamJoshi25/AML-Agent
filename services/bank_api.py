import requests
from agent.state import AgentState
from config.settings import BANK_API_URL

def send_fraud_alert(payload: dict):
    response = requests.post(BANK_API_URL, json=payload)
    return response.status_code