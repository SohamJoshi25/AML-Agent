from langchain.tools import tool
from agent.state import AgentState
from services.bank_api import send_fraud_alert

@tool
def get_account_info(account_id: str) -> dict:
    """Fetch account details for the current account
    Args: account_id: str
    """

    return {
        "account_id":account_id,
        "avg_txn": 2000,
        "txn_count_24h": 10,
        "risk_flag": False
    }

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

    print("TOOL: report_fraud")

    payload = {
        "account_id": account_id,
        "amount": amount,
        "reason": reason
    }

    send_fraud_alert(payload)
    return "fraud has been reported to bank"