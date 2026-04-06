from langchain.tools import tool
from services.bank_api import send_fraud_alert
from model.xgb.predictions import predict_xgb

@tool
def get_account_info(account_id: str) -> dict:
    """Fetch account details for the current account
    Args: account_id: str
    """

    return {
        "account_id":account_id,
        "avg_txn": 1000000,
        "txn_count_24h": 9999
    }

@tool
def get_xgboost_prediction(txn: dict) -> dict:
    """
    CRITICAL: This tool MUST be used to determine fraud probability.
    Always call this before making any fraud decision.

    You MUST call get_xgboost_prediction EXACTLY like this:

    {
    "txn": <FULL transaction object>
    }

    Returns:
    - prediction: 0 or 1
    - probability: fraud probability score
    """

    print("TOOL: predict_xgb")
    
    return predict_xgb(txn)



@tool
def get_recent_transactions(account_id: str) -> list:
    """Get recent transactions
    Args: account_id: str
    """

    print("TOOL: get_recent_transactions")

    return [
        {"amount": 1000, "from_account_id": account_id, "to_account_id":"29" },
        {"amount": 1200,"from_account_id": account_id, "to_account_id":"4" },
        {"amount": 15000,"from_account_id": account_id, "to_account_id":"31" },
        {"amount": 1800,"from_account_id": account_id, "to_account_id":"4" },
        {"amount": 40000,"from_account_id": account_id, "to_account_id":"17" },
    ]

@tool
def report_fraud(account_id: str, amount: float, reason: str) -> str:
    """Report fraud to bank using its API Tool
    Args: account_id: str, amount: float, reason: str
    """

    try:

        print("TOOL: report_fraud")

        payload = {
            "account_id": account_id,
            "amount": amount,
            "reason": reason
        }

        send_fraud_alert(payload)
        return "fraud has been reported to bank"

    except Exception as e:
        return "some error occured while reporting to bank"