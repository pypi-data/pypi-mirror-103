from platone.packages.eth_utils import (
    apply_to_return_value,
    add_0x_prefix,
    from_wei,
    is_address,
    # is_checksum_address,
    keccak,
    remove_0x_prefix,
    # to_checksum_address,
    to_wei,
)
from platone.packages.platone_keys.utils.address import MIANNETHRP, TESTNETHRP

from platone.packages.ens import ENS

from platone.admin import Admin
from platone.platone import Platone
from platone.miner import Miner
from platone.net import Net
from platone.personal import Personal
from platone.txpool import TxPool
from platone.debug import Debug

from platone.providers.eth_tester import (
    EthereumTesterProvider,
)
from platone.providers.ipc import (
    IPCProvider,
)
from platone.providers.rpc import (
    HTTPProvider,
)
from platone.providers.tester import (
    TestRPCProvider,
)
from platone.providers.websocket import (
    WebsocketProvider
)

from platone.manager import (
    RequestManager,
)

from platone.utils.abi import (
    map_abi_data,
)
from hexbytes import (
    HexBytes,
)
from platone.utils.decorators import (
    combomethod,
)
from platone.utils.empty import empty
from platone.utils.encoding import (
    hex_encode_abi_type,
    to_bytes,
    to_int,
    to_hex,
    to_text,
    analyze,
)
from platone.utils.normalizers import (
    abi_ens_resolver,
)


def get_default_modules():
    return {
        "platone": Platone,
        "net": Net,
        "personal": Personal,
        "txpool": TxPool,
        "miner": Miner,
        "admin": Admin,
        "debug": Debug
    }


def default_address(mainnet, testnet):
    return {MIANNETHRP: mainnet, TESTNETHRP: testnet}


NODE_MANAGER = default_address("lat1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqp7pn3ep",
                               "lax1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqp3yp7hw")
USER_MANAGER = default_address("lat1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzsjx8h7",
                               "lax1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzlh5ge3")
PARAM_MANAGER = default_address("lat1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqrdyjj2v",
                                "lax1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqrzpqayr")
CNS = default_address("lat1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqyva9ztf", "lax1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqyrchd9x")
LEDGER_MANAGER = default_address("lat1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq93t3hkm",
                                 "lax1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq97wrcc5")
LEDGER_NODE_MANAGER = default_address("lat1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqxlcypcy",
                                      "lax1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqxsakwkt")
RE_ENC = default_address("lat1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq8zws59k", "lax1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq8dtzmte")


def to_checksum_address(val):
    return val


def is_checksum_address(val):
    return True


class Web3:
    # Providers
    HTTPProvider = HTTPProvider
    IPCProvider = IPCProvider
    TestRPCProvider = TestRPCProvider
    EthereumTesterProvider = EthereumTesterProvider
    WebsocketProvider = WebsocketProvider

    # Managers
    RequestManager = RequestManager

    # Encoding and Decoding
    toBytes = staticmethod(to_bytes)
    toInt = staticmethod(to_int)
    toHex = staticmethod(to_hex)
    toText = staticmethod(to_text)

    # Currency Utility
    toWei = staticmethod(to_wei)
    fromWei = staticmethod(from_wei)
    analyzeReceipt = staticmethod(analyze)

    # Address Utility
    isAddress = staticmethod(is_address)
    isChecksumAddress = staticmethod(is_checksum_address)
    toChecksumAddress = staticmethod(to_checksum_address)

    def __init__(self, providers=empty, middlewares=None, modules=None, ens=empty, chain_id=100,
                 multi_ledger: bool = False, encryption_mode='SM'):
        self.manager = RequestManager(self, providers, middlewares)

        if modules is None:
            modules = get_default_modules()
        for module_name, module_class in modules.items():
            module_class.attach(self, module_name)

        self.ens = ens

        self.chain_id = chain_id
        if chain_id == 100:
            self.net_type = MIANNETHRP
        else:
            self.net_type = TESTNETHRP

        self.system_ledger = None
        self.current_ledger = None
        self.ledgers = None
        if multi_ledger is True:
            self.system_ledger = 'sys'
            self.current_ledger = self.system_ledger
            self.ledgers = [self.system_ledger]

        self.encryption_mode = encryption_mode

        # built-in contract address
        self.node_manager_address = NODE_MANAGER[self.net_type]
        self.user_manager_address = USER_MANAGER[self.net_type]
        self.param_manager_address = PARAM_MANAGER[self.net_type]
        self.cns_address = CNS[self.net_type]
        self.ledger_manager_address = LEDGER_MANAGER[self.net_type]
        self.ledger_node_manager_address = LEDGER_NODE_MANAGER[self.net_type]
        self.re_enc_address = RE_ENC[self.net_type]

    @property
    def currentLedger(self):
        return self.current_ledger

    @currentLedger.setter
    def currentLedger(self, ledger):
        self.current_ledger = ledger
        if ledger not in self.ledgers:
            self.ledgers.append(ledger)

    @property
    def chainId(self):
        return self.chain_id

    @chainId.setter
    def chainId(self, chain_id):
        self.chain_id = chain_id

    @property
    def middleware_stack(self):
        return self.manager.middleware_stack

    @property
    def providers(self):
        return self.manager.providers

    @providers.setter
    def providers(self, providers):
        self.manager.providers = providers

    @staticmethod
    @apply_to_return_value(HexBytes)
    def sha3(primitive=None, text=None, hexstr=None):
        if isinstance(primitive, (bytes, int, type(None))):
            input_bytes = to_bytes(primitive, hexstr=hexstr, text=text)
            return keccak(input_bytes)

        raise TypeError(
            "You called sha3 with first arg %r and keywords %r. You must call it with one of "
            "these approaches: sha3(text='txt'), sha3(hexstr='0x747874'), "
            "sha3(b'\\x74\\x78\\x74'), or sha3(0x747874)." % (
                primitive,
                {'text': text, 'hexstr': hexstr}
            )
        )

    @combomethod
    def soliditySha3(cls, abi_types, values):
        """
        Executes sha3 (keccak256) exactly as Solidity does.
        Takes list of abi_types as inputs -- `[uint24, int8[], bool]`
        and list of corresponding values  -- `[20, [-1, 5, 0], True]`
        """
        if len(abi_types) != len(values):
            raise ValueError(
                "Length mismatch between provided abi types and values.  Got "
                "{0} types and {1} values.".format(len(abi_types), len(values))
            )

        if isinstance(cls, type):
            w3 = None
        else:
            w3 = cls
        normalized_values = map_abi_data([abi_ens_resolver(w3)], abi_types, values)

        hex_string = add_0x_prefix(''.join(
            remove_0x_prefix(hex_encode_abi_type(abi_type, value))
            for abi_type, value
            in zip(abi_types, normalized_values)
        ))
        return cls.sha3(hexstr=hex_string)

    def isConnected(self):
        for provider in self.providers:
            if provider.isConnected():
                return True
        else:
            return False

    @property
    def ens(self):
        if self._ens is empty:
            return ENS.fromWeb3(self)
        else:
            return self._ens

    @ens.setter
    def ens(self, new_ens):
        self._ens = new_ens

    def pubkey_to_address(self, pubkey):
        addr_dict = {MIANNETHRP: pubkey.to_bech32_address(),
                     TESTNETHRP: pubkey.to_bech32_test_address()}
        return addr_dict[self.net_type]
