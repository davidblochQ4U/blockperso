"""
Bitcoin Transaction Fee Calculator

This module contains a function to calculate the transaction fee for Bitcoin
transactions based on the number of inputs and outputs. The fee is determined by the total
size of the transaction, with a given fee rate in satoshis per byte.
"""
from app.config import FEE_RATE, INPUT_SIZE, OUTPUT_SIZE, BASE_SIZE

def calculate_transaction_fee(num_inputs: int, num_outputs: int, fee_rate: int = FEE_RATE) -> int:
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

    # Calculate the total transaction size in vbytes
    weight = (num_inputs * INPUT_SIZE + num_outputs * OUTPUT_SIZE + BASE_SIZE) * 3 + num_inputs * 1
    transaction_size_vbytes = weight / 4

    # Calculate and return the transaction fee
    return int(transaction_size_vbytes * fee_rate)