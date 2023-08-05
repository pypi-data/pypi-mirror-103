from platone.module import Module
from platone.utils.builtin_abis import RE_ENC_ABI
from platone.utils.transactions import send_obj_transaction


class ReEnc(Module):
    ABI = RE_ENC_ABI
    is_wait_receipt = False

    def __init__(self, web3):
        super().__init__(web3)
        self.contract = self.web3.platone.contract(address=self.web3.re_enc_address, abi=self.ABI,
                                                   ledger=self.web3.system_ledger)

    def reEncrypt(self, cipher, ownerPk1, reEncryptKey, private_key, tx_cfg: dict = None):
        txn = self.contract.functions.ReEncrypt(cipher, ownerPk1, reEncryptKey).buildTransaction(tx_cfg)
        return send_obj_transaction(self, txn, private_key, ledger=self.web3.system_ledger)

