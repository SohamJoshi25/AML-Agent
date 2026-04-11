import requests
from config.settings import BANK_API_URL

def send_fraud_alert(payload: dict):
    response = requests.post(BANK_API_URL+"/api/account/filter/", json=payload)
    return response.status_code

def get_account_detail(account_id: str):
    response = requests.get(BANK_API_URL+f"/api/account/{account_id}")
    return response.json()

def get_previous_account_transactions(account_id: str, last: int = 10):
    response = requests.get(
        f"{BANK_API_URL}/api/transactions/last/{account_id}",
        params={"limit": last}
    )
    return response.json()