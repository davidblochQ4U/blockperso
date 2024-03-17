from pydantic import BaseModel
from typing import List

class UTXO:
    def __init__(self, value):
        self.value = value

class UTXOModel(BaseModel):
    value: float

class TransactionRequest(BaseModel):
    utxos: List[UTXOModel]
    target: float

class Wallet:
    def __init__(self, utxos=[]):
        self.utxos = utxos

    def add_utxo(self, utxo):
        self.utxos.append(utxo)

    def remove_utxos(self, utxos_to_remove):
        self.utxos = [utxo for utxo in self.utxos if utxo not in utxos_to_remove]

    def get_balance(self):
        return sum(utxo.value for utxo in self.utxos)
