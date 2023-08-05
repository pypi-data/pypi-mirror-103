import json
from platone.module import Module
from platone.utils.builtin_abis import LEDGER_MANAGER_ABI
from platone.utils.transactions import send_obj_transaction


class Ledger(Module):
    ABI = LEDGER_MANAGER_ABI
    is_wait_receipt = False

    def __init__(self, web3):
        super().__init__(web3)
        self.contract = self.web3.platone.contract(address=self.web3.ledger_manager_address, abi=self.ABI,
                                                   ledger=self.web3.system_ledger)

    def getAllLedgers(self):
        return self.contract.functions.GetAllLedgers().call()

    def createLedger(self, ledger_json, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.CreateLedger(json.dumps(ledger_json)).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def joinLedger(self, ledger_name, node_id, bls_pubKey, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.JoinLedger(ledger_name, node_id, bls_pubKey).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def joinLedgers(self, node_id, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.JoinedLedgers(node_id).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def quitLedger(self, ledger_name, node_id, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.QuitLedger(ledger_name, node_id).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def terminateLedger(self, ledger_name, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.TerminateLedger(ledger_name).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)
