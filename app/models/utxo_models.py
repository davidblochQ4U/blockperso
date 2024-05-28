"""
UTXO Models Module

This module defines the data models used for representing Unspent Transaction Outputs (UTXOs) and transactions within a cryptocurrency wallet context. It includes models for individual UTXOs, transaction requests, and the wallet itself, leveraging Pydantic for data validation.
"""


from pydantic import BaseModel
from typing import List

class UTXO:
    """
   Represents an Unspent Transaction Output (UTXO).

   Attributes:
       value (float): The value of the UTXO.
   """
    def __init__(self, value):
        self.value = value

class UTXOModel(BaseModel):
    """
    Pydantic model for UTXO data validation.

    Attributes:
        value (float): The value of the UTXO.
    """
    value: float

class TransactionRequest(BaseModel):
    """
    Pydantic model for a transaction request.

    Attributes:
        utxos (List[UTXOModel]): A list of UTXO models representing the available UTXOs for the transaction.
        target (float): The target amount for the transaction.
    """
    utxos: List[UTXOModel]
    target: float

class Wallet:
    """
    Represents a cryptocurrency wallet, which manages a collection of UTXOs.

    Attributes:
        utxos (List[UTXO]): A list of UTXOs in the wallet.
    """
    def __init__(self, utxos=[]):
        self.utxos = utxos if utxos is not None else []

    def add_utxo(self, utxo):
        """
        Adds a UTXO to the wallet.

        Parameters:
            utxo (UTXO): The UTXO to be added.
        """
        self.utxos.append(utxo)

    def remove_utxo(self, utxo_to_remove):
        """
        Removes specified UTXOs from the wallet.

        Parameters:
            utxos_to_remove (List[UTXO]): The UTXOs to be removed.
        """
        self.utxos.remove(utxo_to_remove)

    def get_balance(self):
        """
        Calculates the total balance of the wallet based on its UTXOs.

        Returns:
            float: The total value of all UTXOs in the wallet.
        """
        return sum(utxo.value for utxo in self.utxos)
