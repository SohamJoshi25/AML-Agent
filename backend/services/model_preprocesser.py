from sklearn.base import BaseEstimator, TransformerMixin
from dto.transaction_dto import TransactionDTO
import pandas as pd

import sklearn
print(sklearn.__version__)
class TimeFeaturesExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()

        if 'Timestamp' in X.columns:
            X['Timestamp'] = pd.to_datetime(
                X['Timestamp'],
                format='%Y/%m/%d %H:%M',
                errors='coerce'
            )

            if X['Timestamp'].isnull().any():
                X['Timestamp'] = pd.to_datetime(X['Timestamp'], errors='coerce')

            X['Year'] = X['Timestamp'].dt.year
            X['Month'] = X['Timestamp'].dt.month
            X['Day'] = X['Timestamp'].dt.day
            X['Hour'] = X['Timestamp'].dt.hour
            X['Minute'] = X['Timestamp'].dt.minute
            X['DayOfWeek'] = X['Timestamp'].dt.dayofweek

            X = X.drop(columns=['Timestamp'])

        X = X.drop(columns=['Account', 'Account.1'], errors='ignore')

        return X

def normalize_txn(txn: TransactionDTO):
    return {
        "Timestamp": txn.get("timestamp"),
        
        "From Bank": txn.get("fromBank"),
        "Account": txn.get("fromAccount"),
        
        "To Bank": txn.get("toBank"),
        "Account": txn.get("toAccount"),

        "Amount Paid": txn.get("amountPaid"),
        "Receiving Currency": txn.get("receivingCurrency"),

        "Amount Received": txn.get("amountReceived"),
        "Payment Currency": txn.get("paymentCurrency"),

        "Payment Format": txn.get("paymentFormat"),
    }