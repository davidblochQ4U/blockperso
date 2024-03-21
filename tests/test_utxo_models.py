import pytest
from utxo_models import UTXO, UTXOModel, TransactionRequest, Wallet

def test_utxo_initialization():
    utxo = UTXO(value=10.5)
    assert utxo.value == 10.5

def test_utxo_model_validation():
    utxo_model = UTXOModel(value=5.5)
    assert utxo_model.value == 5.5
    # Test validation error
    with pytest.raises(ValueError):
        UTXOModel(value="invalid")

def test_transaction_request_validation():
    utxo_models = [UTXOModel(value=1), UTXOModel(value=2)]
    transaction_request = TransactionRequest(utxos=utxo_models, target=3)
    assert transaction_request.target == 3
    assert len(transaction_request.utxos) == 2

def test_wallet_initialization():
    utxos = [UTXO(value=1), UTXO(value=2)]
    wallet = Wallet(utxos=utxos)
    assert len(wallet.utxos) == 2
    assert wallet.get_balance() == 3

def test_wallet_add_utxo():
    wallet = Wallet()
    utxo = UTXO(value=5)
    wallet.add_utxo(utxo)
    assert len(wallet.utxos) == 1
    assert wallet.get_balance() == 5

def test_wallet_remove_utxos():
    utxo1 = UTXO(value=1)
    utxo2 = UTXO(value=2)
    wallet = Wallet(utxos=[utxo1, utxo2])
    wallet.remove_utxos([utxo1])
    assert len(wallet.utxos) == 1
    assert wallet.get_balance() == 2

def test_wallet_get_balance():
    utxos = [UTXO(value=1.5), UTXO(value=2.5)]
    wallet = Wallet(utxos=utxos)
    assert wallet.get_balance() == 4.0
