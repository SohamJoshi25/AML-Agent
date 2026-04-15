from langchain.tools import tool
from services.bank_api import send_fraud_alert, get_account_detail, get_previous_account_transactions
from model.xgb.predictions import predict_xgb

@tool
def get_account_info(account_id: str) -> dict:
    """Fetch account details for the current account
    Args: account_id: str
    """

    # account = MOCK_ACCOUNTS.get(account_id)

    # if not account:
    #     return {
    #         "accountId": account_id,
    #         "status": "UNKNOWN",
    #         "risk": "unknown"
    #     }
    # return account
    

    return get_account_detail(account_id)

@tool
def get_recent_transactions(account_id: str, last: int = 10) -> list:
    """Get recent transactionss
    Args: account_id: str, last: Fetch last 'N' transactions(int)

    Do not use 'fromBank' or 'toBank'. 
    Only use proper AccountID in format 'fromAccount' or 'toAccount'
    """

    print("TOOL: get_recent_transactions")

    # filtered = [
    #     txn for txn in MOCK_TXNS
    #     if txn["fromAccount"] == account_id or txn["toAccount"] == account_id
    # ]

    # # Optional: sort by timestamp (realistic behavior)
    # filtered.sort(key=lambda x: x["timestamp"], reverse=True)

    # return filtered

    val = get_previous_account_transactions(account_id,last)
    return val

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



MOCK_ACCOUNTS = {
    "811B83280": {
        "accountId": "811B83280",
        "bankId": "222",
        "entityId": "800F128A0",
        "entityName": "Corporation #36630",
        "bankName": "Saudi Arabia Bank #5"
    },
    "811C599A0": {
        "accountId": "811C599A0",
        "bankId": "48309",
        "entityId": "800F2F200",
        "entityName": "Sole Proprietorship #979",
        "bankName": "Saudi Arabia Bank #24"
    },
    "811C597B0": {
        "accountId": "811C597B0",
        "bankId": "119",
        "entityId": "800F224C0",
        "entityName": "Partnership #3715",
        "bankName": "Israel Bank #6"
    },
    "812D22980": {
        "accountId": "812D22980",
        "bankId": "150240",
        "entityId": "800F52090",
        "entityName": "Corporation #5724",
        "bankName": "Saudi Arabia Bank #68"
    }
}


MOCK_TXNS = [
    {
        "transactionId": "gs-1",
        "timestamp": "2022-09-01T00:04:00",
        "fromBank": "0119",
        "fromAccount": "811C597B0",
        "toBank": "0048309",
        "toAccount": "811C599A0",
        "amountReceived": 34254.65,
        "receivingCurrency": "Saudi Riyal",
        "amountPaid": 34254.65,
        "paymentCurrency": "Saudi Riyal",
        "paymentFormat": "ACH"
    },
    {
        "transactionId": "gs-2",
        "timestamp": "2022-09-01T19:27:00",
        "fromBank": "0150240",
        "fromAccount": "812D22980",
        "toBank": "0048309",
        "toAccount": "811C599A0",
        "amountReceived": 5971.98,
        "receivingCurrency": "Saudi Riyal",
        "amountPaid": 5971.98,
        "paymentCurrency": "Saudi Riyal",
        "paymentFormat": "ACH"
    },
    {
        "transactionId": "gs-3",
        "timestamp": "2022-09-04T05:06:00",
        "fromBank": "0222",
        "fromAccount": "811B83280",
        "toBank": "0048309",
        "toAccount": "811C599A0",
        "amountReceived": 50445.58,
        "receivingCurrency": "Saudi Riyal",
        "amountPaid": 50445.58,
        "paymentCurrency": "Saudi Riyal",
        "paymentFormat": "ACH"
    },
    {
        "transactionId": "gs-4",
        "timestamp": "2022-09-04T05:03:00",
        "fromBank": "0048309",
        "fromAccount": "811C599A0",
        "toBank": "0048309",
        "toAccount": "811C599A0",
        "amountReceived": 48649.42,
        "receivingCurrency": "Saudi Riyal",
        "amountPaid": 48649.42,
        "paymentCurrency": "Saudi Riyal",
        "paymentFormat": "ACH"
    },
    {
        "transactionId": "gs-5",
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
]
