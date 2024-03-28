import pytest
from fee_calculator import calculate_transaction_fee

def test_calculate_transaction_fee():
    # Test with positive numbers of inputs and outputs
    assert calculate_transaction_fee(1, 2) == ((1 * 146) + (2 * 34) + 10) * 20
    assert calculate_transaction_fee(3, 1) == ((3 * 146) + (1 * 34) + 10) * 20

def test_calculate_transaction_fee_with_custom_fee_rate():
    # Test with a custom fee rate
    assert calculate_transaction_fee(1, 1, fee_rate=10) == ((1 * 146) + (1 * 34) + 10) * 10

def test_calculate_transaction_fee_with_negative_values():
    # Test with negative values for inputs and outputs to ensure it raises a ValueError
    with pytest.raises(ValueError):
        calculate_transaction_fee(-1, 1)
    with pytest.raises(ValueError):
        calculate_transaction_fee(1, -1)
    with pytest.raises(ValueError):
        calculate_transaction_fee(-1, -1)
