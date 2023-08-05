from platone.module import (
    Module,
)


class Net(Module):
    @property
    def listening(self):
        return self.web3.manager.request_blocking("net_listening", [])

    @property
    def peerCount(self):
        return self.web3.manager.request_blocking("net_peerCount", [])

    @property
    def version(self):
        return self.web3.manager.request_blocking("net_version", [])
