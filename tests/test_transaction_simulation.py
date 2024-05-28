import pytest
from unittest.mock import MagicMock
from app.models.utxo_models import Wallet
from app.services.transaction_simulation import simulate_transaction

@pytest.fixture
def setup_wallets():
    sender = Wallet(utxos=[5, 10])  # Example UTXOs
    receiver = Wallet(utxos=[])
    return sender, receiver

def test_simulate_transaction_success(setup_wallets):
    sender, receiver = setup_wallets
    # Mock the selection method to always return the first UTXO
    mock_selection_method = MagicMock(return_value=([sender.utxos[0]], None))
    success = simulate_transaction(sender, receiver, 5, mock_selection_method)
    assert success is True
    assert len(sender.utxos) == 1  # One UTXO should be removed
    assert sender.utxos == [10]  # Ensure correct UTXO remains
    assert receiver.utxos == [5]  # Receiver should gain UTXO value

def test_simulate_transaction_insufficient_funds(setup_wallets):
    sender, receiver = setup_wallets
    # Mock the selection method to return empty list, indicating insufficient funds
    mock_selection_method = MagicMock(return_value=([], None))
    success = simulate_transaction(sender, receiver, 50, mock_selection_method)  # Request more than available
    assert success is False
    assert len(sender.utxos) == 2  # No UTXOs should be removed from sender
    assert len(receiver.utxos) == 0  # Receiver should not gain any UTXOs

