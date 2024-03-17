def calculate_transaction_fee(num_inputs: int, num_outputs: int, fee_rate: int = 20) -> int:
    input_size = 146  # bytes
    output_size = 34  # bytes
    base_size = 10  # bytes
    transaction_size = num_inputs * input_size + num_outputs * output_size + base_size
    return transaction_size * fee_rate