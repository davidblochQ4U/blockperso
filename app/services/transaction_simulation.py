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

    selected_utxos, _ = selection_method(sender.utxos, amount)
    if not selected_utxos:
        # Transaction failed due to insufficient funds.
        return False

    # Remove selected UTXOs from the sender's wallet and add the net amount to the receiver's wallet.
    sender.remove_utxos(selected_utxos)
    receiver.add_utxo(sum(utxo.value for utxo in selected_utxos) - amount)  # Simplified

    # The transaction is deemed successful.
    return True