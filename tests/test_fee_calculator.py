import pytest
from app.services.fee_calculator import calculate_transaction_fee

def test_calculate_transaction_fee_basic():
    assert calculate_transaction_fee(1, 2) == 3395
    assert calculate_transaction_fee(3, 1) == 7335

def test_calculate_transaction_fee_custom_rate():
    assert calculate_transaction_fee(1, 2, fee_rate=10) == 1697
    assert calculate_transaction_fee(2, 3, fee_rate=15) == 4597

def test_calculate_transaction_fee_zero_inputs_outputs():
    assert calculate_transaction_fee(0, 0) == 150
    assert calculate_transaction_fee(0, 2) == 1170
    assert calculate_transaction_fee(2, 0) == 4600  # Adjusted value

def test_calculate_transaction_fee_negative_inputs():
    with pytest.raises(ValueError, match="Number of inputs and outputs must be non-negative"):
        calculate_transaction_fee(-1, 1)

def test_calculate_transaction_fee_negative_outputs():
    with pytest.raises(ValueError, match="Number of inputs and outputs must be non-negative"):
        calculate_transaction_fee(1, -1)

def test_calculate_transaction_fee_no_fee_rate_provided():
    assert calculate_transaction_fee(1, 1) == 2885
