"""
Transaction Simulation Module

This module provides functionality to simulate transactions between wallets using various coin selection algorithms. It is designed to test the efficiency and effectiveness of these algorithms in a controlled environment.
"""

from app.models.utxo_models import Wallet


def simulate_transaction(sender: Wallet, receiver: Wallet, amount: int, selection_method):
    """
    Simulates a cryptocurrency transaction from a sender to a receiver using a specified coin selection method.

    Parameters:
    - sender (Wallet): The wallet from which funds are to be sent.
    - receiver (Wallet): The wallet to which funds are to be sent.
    - amount (int): The amount of cryptocurrency to be transferred.
    - selection_method (function): The coin selection algorithm to use for the transaction.

    Returns:
    - bool: True if the transaction was successful, False otherwise (e.g., insufficient funds).
    """

    selected_utxos, change = selection_method(sender.utxos, amount)
    if not selected_utxos:
        return False  # Insufficient funds

    # Remove selected UTXOs from sender
    for utxo in selected_utxos:
        sender.remove_utxo(utxo)

    # Add the amount to receiver's UTXOs
    receiver.add_utxo(amount)

    # Handle change if any
    if change:
        sender.add_utxo(change)

    return True