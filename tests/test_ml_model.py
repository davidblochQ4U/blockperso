import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.routers.ml_model import router  # Adjust the import path as needed
from app.services.ml_model_service import MLModelService

# Create a TestClient for the FastAPI router
client = TestClient(router)

# Mock data for testing
mock_transaction_data = {
    "input_data": {
        "feature1": 0.1,
        "feature2": 1.0,
        "feature3": 100.0
    }
}

# Test successful fee prediction
@patch("app.routers.ml_model.MLModelService")
def test_get_predicted_fee_success(mock_ml_model_service):
    # Mock the predict_transaction_fee function to return a fixed prediction
    mock_service_instance = MagicMock()
    mock_service_instance.predict_transaction_fee.return_value = 123.45
    mock_ml_model_service.return_value = mock_service_instance

    # Send a POST request to the /predict_fee endpoint
    response = client.post("/predict_fee", json=mock_transaction_data)

    # Assert the response status code is 200
    assert response.status_code == 200

    # Assert the response body contains the expected prediction
    assert response.json() == {"predicted_fee": 123.45}

# Test exception handling for fee prediction failure
# @patch("app.routers.ml_model.MLModelService")
# def test_get_predicted_fee_failure(mock_ml_model_service):
#     # Mock the predict_transaction_fee function to raise an exception
#     mock_service_instance = MagicMock()
#     mock_service_instance.predict_transaction_fee.side_effect = Exception("Prediction error")
#     mock_ml_model_service.return_value = mock_service_instance
#
#     # Send a POST request to the /predict_fee endpoint with mock data
#     response = client.post("/predict_fee", json=mock_transaction_data)
#
#     # Assert the response status code is 400 (HTTPException)
#     assert response.status_code == 400
#
#     # Assert the error message is returned in the response
#     assert response.json() == {"detail": "Prediction error"}
