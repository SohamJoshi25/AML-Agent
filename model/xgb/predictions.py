import os
import sys

import joblib
import pandas as pd
from services.model_preprocesser import TimeFeaturesExtractor,normalize_txn

sys.modules['__main__'].TimeFeaturesExtractor = TimeFeaturesExtractor

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "xgb_pipeline.pkl")

model = joblib.load(MODEL_PATH)

def predict_xgb(txn: dict) -> dict:
    df = pd.DataFrame([normalize_txn(txn)])
    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1]
    return {"prediction":pred,"probability":prob}