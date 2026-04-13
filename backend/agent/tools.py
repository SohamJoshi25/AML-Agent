from langchain.tools import tool
from services.bank_api import send_fraud_alert, get_account_detail, get_previous_account_transactions
from model.xgb.predictions import predict_xgb

@tool
def get_account_info(account_id: str) -> dict:
    """Fetch account details for the current account
    Args: account_id: str
    """

    return get_account_detail(account_id)

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
def get_recent_transactions(account_id: str, last: int = 10) -> list:
    """Get recent transactions
    Args: account_id: str, last: Fetch last 'N' transactions(int)

    Do not use 'fromBank' or 'toBank'. 
    Only use proper AccountID in format 'fromAccount' or 'toAccount'
    """

    print("TOOL: get_recent_transactions")

    return get_previous_account_transactions(account_id,last)


@tool
def report_fraud(account_id: str, blacklist_level: str, reason: str) -> str:
    """Report fraud account and block it in bank using its API Tool.
    Args: account_id: str, blacklist_level: str("BLACK" = if Very Suspecious / "GREY" if urgent attention not resquired) only, reason: str
    Note: blacklist_level must be decided on based of all data collected and the models scores.
    """

    try:

        print("TOOL: report_fraud")

        payload = {
            "accountId": account_id,
            "level": blacklist_level,
            "reason": reason
        }

        send_fraud_alert(payload)
        return "fraud has been reported to bank"

    except Exception as e:
        return "some error occured while reporting to bank"
