import json

from platone.module import Module
from platone.utils.builtin_abis import CNS_ABI
from platone.utils.transactions import send_obj_transaction


class CNS(Module):
    ABI = CNS_ABI
    is_wait_receipt = False

    def __init__(self, web3):
        super().__init__(web3)
        self.contract = self.web3.platone.contract(address=self.web3.cns_address, abi=self.ABI,
                                           ledger=self.web3.system_ledger)

    def getAllContracts(self):
        return self.contract.functions.GetAllContracts().call()

    def getContractAddress(self, name, version):
        return self.contract.functions.GetContractAddress(name, version).call()

    def getContractsByAddress(self, address):
        return self.contract.functions.GetContractsByAddr(address).call()

    def getContractsByOwner(self, address):
        return self.contract.functions.GetContractsByOwner(address).call()

    def Register(self, name, version, address, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.Register(name, version, address).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def Unregister(self, name, version, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.Unregister(name, version).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)
