"""
Bitcoin Transaction Fee Calculator

This module contains a function to calculate the transaction fee for Bitcoin
transactions based on the number of inputs and outputs. The fee is determined by the total
size of the transaction, with a given fee rate in satoshis per byte.
"""


def calculate_transaction_fee(num_inputs: int, num_outputs: int, fee_rate: int = 20) -> int:
    """
    Calculates the fee for a Bitcoin transaction.

    The fee is based on the total size of the transaction, which is a function of the number
    of inputs and outputs, as well as a base transaction size. Each input and output adds to the
    total size of the transaction, thereby increasing the fee.

    Parameters:
    - num_inputs (int): The number of inputs in the transaction.
    - num_outputs (int): The number of outputs in the transaction.
    - fee_rate (int, optional): The fee rate in satoshis per byte. Default is 20 satoshis/byte.

    Returns:
    - int: The calculated transaction fee in satoshis.
    """
    if num_inputs < 0 or num_outputs < 0:
        raise ValueError("Number of inputs and outputs must be non-negative")

    # Average sizes in bytes for transaction components
    input_size = 146  # bytes
    output_size = 34  # bytes
    base_size = 10  # bytes

    # Calculate the total transaction size
    transaction_size = num_inputs * input_size + num_outputs * output_size + base_size

    # Calculate and return the transaction fee
    return transaction_size * fee_rate