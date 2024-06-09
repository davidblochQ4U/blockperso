from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ml_model_service import MLModelService

router = APIRouter()

class TransactionData(BaseModel):
    input_data: dict

@router.post("/predict_fee")
def get_predicted_fee(transaction_data: TransactionData):
    try:
        ml_service = MLModelService()
        prediction = ml_service.predict_transaction_fee(transaction_data.input_data)
        return {"predicted_fee": prediction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))