import pytest
from fee_calculator import calculate_transaction_fee

# Test with default fee rate
def test_calculate_transaction_fee_default_rate():
    # Test a transaction with 1 input and 2 outputs
    assert calculate_transaction_fee(1, 2) == ((1 * 146) + (2 * 34) + 10) * 20
    # Test with multiple inputs and outputs
    assert calculate_transaction_fee(2, 3) == ((2 * 146) + (3 * 34) + 10) * 20

# Test with specific fee rate
def test_calculate_transaction_fee_specific_rate():
    # Test a transaction with a specific fee rate
    assert calculate_transaction_fee(1, 1, fee_rate=10) == ((1 * 146) + (1 * 34) + 10) * 10
    # Test with zero inputs, which is technically invalid but should still calculate
    assert calculate_transaction_fee(0, 1, fee_rate=10) == ((0 * 146) + (1 * 34) + 10) * 10

# Test edge cases
def test_calculate_transaction_fee_edge_cases():
    # Test with zero inputs and outputs
    assert calculate_transaction_fee(0, 0) == 10 * 20  # Only base size affects fee
    # Test with a high number of inputs and outputs
    assert calculate_transaction_fee(100, 100) == ((100 * 146) + (100 * 34) + 10) * 20

# Test with negative inputs and outputs, expecting logical but technically nonsensical results
@pytest.mark.parametrize("num_inputs, num_outputs", [(-1, 2), (2, -1), (-1, -1)])
def test_calculate_transaction_fee_negative_values(num_inputs, num_outputs):
    with pytest.raises(ValueError):
        calculate_transaction_fee(num_inputs, num_outputs)
