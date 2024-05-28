from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ml_model_service import predict_transaction_fee

router = APIRouter()

class TransactionData(BaseModel):
    input_data: dict

@router.post("/predict_fee")
def get_predicted_fee(transaction_data: TransactionData):
    try:
        prediction = predict_transaction_fee(transaction_data.input_data)
        return {"predicted_fee": prediction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
