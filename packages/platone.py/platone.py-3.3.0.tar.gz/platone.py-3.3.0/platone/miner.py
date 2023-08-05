from platone.module import (
    Module,
)


class Miner(Module):

    # todo： coding
    def setGasPrice(self, gas_price, ledger=None):
        return self.web3.manager.request_blocking(
            "miner_setGasPrice", self.set_ledger([gas_price], ledger),
        )