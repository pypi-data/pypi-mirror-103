from platone.module import (
    Module,
)


class TxPool(Module):
    def content(self, ledger=None):
        return self.web3.manager.request_blocking("txpool_content", self.set_ledger([], ledger=ledger))

    def inspect(self, ledger=None):
        return self.web3.manager.request_blocking("txpool_inspect", self.set_ledger([], ledger=ledger))

    def status(self, ledger=None):
        return self.web3.manager.request_blocking("txpool_status", self.set_ledger([], ledger=ledger))
