from utxo_models import Wallet
from coin_selection_algorithms import greedy_coin_selection

def simulate_transaction(sender: Wallet, receiver: Wallet, amount: int, selection_method):
    selected_utxos, _ = selection_method(sender.utxos, amount)
    if not selected_utxos:
        return False  # Transaction failed due to insufficient funds
    sender.remove_utxos(selected_utxos)
    receiver.add_utxo(sum(utxo.value for utxo in selected_utxos) - amount)  # Simplified
    return True