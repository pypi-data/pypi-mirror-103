import json
from platone.module import Module
from platone.utils.builtin_abis import LEDGER_NODE_MANAGER_ABI
from platone.utils.transactions import send_obj_transaction


class LedgerNode(Module):
    ABI = LEDGER_NODE_MANAGER_ABI
    is_wait_receipt = False

    def __init__(self, web3):
        super().__init__(web3)
        self.contract = self.web3.platone.contract(address=self.web3.ledger_node_manager_address, abi=self.ABI,
                                                   ledger=self.web3.system_ledger)

    def list(self):
        return self.contract.functions.List().call()

    def add(self, pubkey, bls_pubkey, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.Add(pubkey, bls_pubkey).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def grantPerm(self, address, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.GrantPerm(address).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def remove(self, pubkey, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.Remove(pubkey).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def revokePerm(self, address, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.RevokePerm(address).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def updateNodeType(self, pubkey, node_type, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.UpdateNodeType(pubkey, node_type).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

