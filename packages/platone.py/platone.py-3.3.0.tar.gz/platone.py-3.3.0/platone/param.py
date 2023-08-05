import json
from platone.module import Module
from platone.utils.builtin_abis import PARAM_MANAGER_ABI
from platone.utils.transactions import send_obj_transaction


class Param(Module):
    ABI = PARAM_MANAGER_ABI
    is_wait_receipt = False

    def __init__(self, web3):
        super().__init__(web3)
        self.contract = self.web3.platone.contract(address=self.web3.param_manager_address, abi=self.ABI,
                                                   ledger=self.web3.system_ledger)

    def getSystemParameter(self):
        return self.contract.functions.GetSystemParameter().call()

    def enableDeploy(self, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.EnableDeploy().buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def disableDeploy(self, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.DisableDeploy().buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def updateBlockGasLimit(self, block_gas_limit, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.UpdateBlockGasLimit(block_gas_limit).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def updateIsProduceEmptyBlock(self, is_produce_empty_block, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.UpdateIsProduceEmptyBlock(is_produce_empty_block).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def updateIsTxUseGas(self, is_tx_use_gas, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.UpdateIsTxUseGas(is_tx_use_gas).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def updateTxGasLimit(self, tx_gas_limit, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.UpdateTxGasLimit(tx_gas_limit).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

    def updateSystemParameter(self, block_gas_limit, tx_gas_limit, is_tx_use_gas, is_produce_empty_block, enable_deploy,
                              private_key, tx_cfg: dict = None):
        txn = self.contract.functions.UpdateSystemParameter(block_gas_limit, tx_gas_limit, is_tx_use_gas,
                                                            is_produce_empty_block, enable_deploy).buildTransaction(
            tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)
