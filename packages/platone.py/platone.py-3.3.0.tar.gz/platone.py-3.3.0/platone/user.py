import json
from platone.module import Module
from platone.utils.builtin_abis import USER_MANAGER_ABI
from platone.utils.transactions import send_obj_transaction


class User(Module):
    ABI = USER_MANAGER_ABI
    is_wait_receipt = False

    def __init__(self, web3):
        super().__init__(web3)
        self.contract = self.web3.platone.contract(address=self.web3.user_manager_address, abi=self.ABI,
                                                   ledger=self.web3.system_ledger)

    def getByAddress(self, address):
        return self.contract.functions.GetByAddr(address).call()

    def getByName(self, name):
        return self.contract.functions.GetByName(name).call()

    def hasRoles(self, address, roles):
        return self.contract.functions.HasRoles(address, roles).call()

    def pageAll(self, page_num, page_size):
        return self.contract.functions.PageAll(page_num, page_size).call()

    def pageByRoles(self, roles, page_num, page_size):
        return self.contract.functions.PageByRoles(roles, page_num, page_size).call()

    def pageByStat(self, status, page_num, page_size):
        return self.contract.functions.PageByStat(status, page_num, page_size).call()

    def add(self, address, name, mobile, email, desc, roles, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.Add(address, name, mobile, email, desc, roles).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def update(self, address, mobile, email, desc, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.Update(address, mobile, email, desc).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def delete(self, address, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.Delete(address).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def addRoles(self, address, roles, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.AddRoles(address, roles).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def setRoles(self, address, roles, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.SetRoles(address, roles).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def removeRoles(self, address, roles, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.RemoveRoles(address, roles).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def audit(self, address, audit_stat, audit_reason, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.Audit(address, audit_stat, audit_reason).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def register(self, name, mobile, email, desc, roles, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.Register(name, mobile, email, desc, roles).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def enable(self, address, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.Enable(address).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def disable(self, address, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.Disable(address).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)
