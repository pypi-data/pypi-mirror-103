import json
from platone.module import Module
from platone.utils.builtin_abis import NODE_MANAGER_ABI
from platone.utils.transactions import send_obj_transaction


class Node(Module):
    ABI = NODE_MANAGER_ABI
    is_wait_receipt = False

    def __init__(self, web3):
        super().__init__(web3)
        self.contract = self.web3.platone.contract(address=self.web3.node_manager_address, abi=self.ABI,
                                                   ledger=self.web3.system_ledger)

    def listAll(self):
        return self.contract.functions.ListAll().call()

    def listByHostAddress(self, host_address):
        return self.contract.functions.ListByHostAddress(host_address).call()

    def listByOwner(self, owner):
        return self.contract.functions.ListByOwner(owner).call()

    def listByStat(self, status):
        return self.contract.functions.ListByStat(status).call()

    def listByType(self, node_type):
        return self.contract.functions.ListByType(node_type).call()

    def getByName(self, name):
        return self.contract.functions.GetByName(name).call()

    def getByPublicKey(self, pubkey):
        return self.contract.functions.GetByPublicKey(pubkey).call()

    def add(self, name, owner, desc, pubkey, bls_pubkey, host_address, rpc_port, p2p_port, private_key,
            tx_cfg: dict = None):
        txn = self.contract.functions.Add(name, owner, desc, pubkey, bls_pubkey, host_address, rpc_port,
                                          p2p_port).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def delete(self, name, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.Delete(name).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def apply(self, name, desc, pubkey, bls_pubkey, host_address, rpc_port, p2p_port, private_key,
              tx_cfg: dict = None):
        txn = self.contract.functions.Apply(name, desc, pubkey, bls_pubkey, host_address, rpc_port,
                                            p2p_port).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def audit(self, name, audit_stat, audit_reason, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.Audit(name, audit_stat, audit_reason).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def update(self, name, host_address, rpc_port, p2p_port, desc, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.Update(name, host_address, rpc_port, p2p_port, desc).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def updateType(self, name, node_type, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.UpdateType(name, node_type).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def enable(self, name, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.Enable(name).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def disable(self, name, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.Disable(name).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)
