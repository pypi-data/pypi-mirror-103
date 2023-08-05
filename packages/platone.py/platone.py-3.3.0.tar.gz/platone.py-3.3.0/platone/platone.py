import json
import sha3
import rlp
import copy
from platone.packages.eth_utils.hexadecimal import remove_0x_prefix
from platone.packages.platone_account import (
    Account,
)
from platone.packages.platone_account.internal.transactions import bech32_address_bytes
from platone.packages.eth_utils import (
    apply_to_return_value,
    is_checksum_address,
    is_string,
)
from hexbytes import (
    HexBytes,
)

from platone.contract import (
    Contract,
)
from platone.module import (
    Module,
)
from platone.utils.blocks import (
    select_method_for_block_identifier,
)
from platone.utils.decorators import (
    deprecated_for,
)
from platone.utils.empty import (
    empty,
)
from platone.utils.encoding import (
    to_hex,
)
from platone.utils.filters import (
    BlockFilter,
    LogFilter,
    TransactionFilter,
)
from platone.utils.toolz import (
    assoc,
    merge,
)
from platone.utils.transactions import (
    assert_valid_transaction_params,
    extract_valid_transaction_params,
    get_buffered_gas_estimate,
    get_required_transaction,
    replace_transaction,
    wait_for_transaction_receipt,
)

from platone.packages.platone_account.internal.signing import (
    to_standard_signature_bytes,
)

true = True
false = False


class Platone(Module):
    account = Account()
    defaultAccount = empty
    defaultBlock = "latest"
    defaultContractFactory = Contract
    gasPriceStrategy = None

    @deprecated_for("doing nothing at all")
    def enable_unaudited_features(self):
        pass

    def namereg(self):
        raise NotImplementedError()

    def icapNamereg(self):
        raise NotImplementedError()

    @property
    def protocolVersion(self):
        return self.web3.manager.request_blocking("platon_protocolVersion", [])

    def syncing(self, ledger=None):
        return self.web3.manager.request_blocking("platon_syncing", self.set_ledger([], ledger))

    def gasPrice(self, ledger=None):
        return self.web3.manager.request_blocking("platon_gasPrice", self.set_ledger([], ledger))

    def accounts(self, ledger=None):
        return self.web3.manager.request_blocking("platon_accounts", self.set_ledger([], ledger))

    def blockNumber(self, ledger=None):
        return self.web3.manager.request_blocking("platon_blockNumber", self.set_ledger([], ledger))

    @property
    def evidences(self, ledger=None):
        data = self.web3.manager.request_blocking("platon_evidences", self.set_ledger([], ledger))
        return json.loads(data)

    @property
    def consensusStatus(self, ledger=None):
        return self.web3.manager.request_blocking("platon_consensusStatus", self.set_ledger([], ledger))

    def getPrepareQC(self, block_number, ledger=None):
        return self.web3.manager.request_blocking("platon_getPrepareQC", self.set_ledger([block_number], ledger))

    def getBalance(self, account, block_identifier=None, ledger=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.web3.manager.request_blocking(
            "platon_getBalance",
            self.set_ledger([account, block_identifier], ledger),
        )

    def getStorageAt(self, account, position, block_identifier=None, ledger=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.web3.manager.request_blocking(
            "platon_getStorageAt",
            self.set_ledger([account, position, block_identifier], ledger)
        )

    def getCode(self, account, block_identifier=None, ledger=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.web3.manager.request_blocking(
            "platon_getCode",
            self.set_ledger([account, block_identifier], ledger),
        )

    def getBlock(self, block_identifier, full_transactions=False, ledger=None):
        """
        `platon_getBlockByHash`
        `platon_getBlockByNumber`
        """
        method = select_method_for_block_identifier(
            block_identifier,
            if_predefined='platon_getBlockByNumber',
            if_hash='platon_getBlockByHash',
            if_number='platon_getBlockByNumber',
        )

        return self.web3.manager.request_blocking(
            method,
            self.set_ledger([block_identifier, full_transactions], ledger),
        )

    def getBlockTransactionCount(self, block_identifier, ledger=None):
        """
        `platon_getBlockTransactionCountByHash`
        `platon_getBlockTransactionCountByNumber`
        """
        method = select_method_for_block_identifier(
            block_identifier,
            if_predefined='platon_getBlockTransactionCountByNumber',
            if_hash='platon_getBlockTransactionCountByHash',
            if_number='platon_getBlockTransactionCountByNumber',
        )
        return self.web3.manager.request_blocking(
            method,
            self.set_ledger([block_identifier], ledger),
        )

    def getTransaction(self, transaction_hash, ledger=None):
        return self.web3.manager.request_blocking(
            "platon_getTransactionByHash",
            self.set_ledger([transaction_hash], ledger),
        )

    def getRawTransaction(self, transaction_hash, ledger=None):
        return self.web3.manager.request_blocking(
            "platon_getRawTransactionByHash",
            self.set_ledger([transaction_hash], ledger),
        )

    @deprecated_for("w3.platone.getTransactionByBlock")
    def getTransactionFromBlock(self, block_identifier, transaction_index, ledger=None):
        """
        Alias for the method getTransactionByBlock
        Depreceated to maintain naming consistency with the json-rpc API
        """
        return self.getTransactionByBlock(block_identifier, transaction_index, ledger)

    def getTransactionByBlock(self, block_identifier, transaction_index, ledger=None):
        """
        `platon_getTransactionByBlockHashAndIndex`
        `platon_getTransactionByBlockNumberAndIndex`
        """
        method = select_method_for_block_identifier(
            block_identifier,
            if_predefined='platon_getTransactionByBlockNumberAndIndex',
            if_hash='platon_getTransactionByBlockHashAndIndex',
            if_number='platon_getTransactionByBlockNumberAndIndex',
        )
        return self.web3.manager.request_blocking(
            method,
            self.set_ledger([block_identifier, transaction_index], ledger),
        )

    def waitForTransactionReceipt(self, transaction_hash, ledger=None, timeout=120):
        return wait_for_transaction_receipt(self.web3, transaction_hash, ledger, timeout)

    def getTransactionReceipt(self, transaction_hash, ledger=None):
        return self.web3.manager.request_blocking(
            "platon_getTransactionReceipt",
            self.set_ledger([transaction_hash], ledger),
        )

    def getTransactionCount(self, account, block_identifier=None, ledger=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.web3.manager.request_blocking(
            "platon_getTransactionCount",
            self.set_ledger([account, block_identifier], ledger),
        )

    def replaceTransaction(self, transaction_hash, new_transaction, ledger=None):
        if ledger is None:
            ledger = self.web3.ledgers
        current_transaction = get_required_transaction(self.web3, transaction_hash, ledger)
        return replace_transaction(self.web3, current_transaction, new_transaction, ledger)

    def modifyTransaction(self, transaction_hash, ledger=None, **transaction_params):
        assert_valid_transaction_params(transaction_params)
        current_transaction = get_required_transaction(self.web3, transaction_hash, ledger)
        current_transaction_params = extract_valid_transaction_params(current_transaction)
        new_transaction = merge(current_transaction_params, transaction_params)
        return replace_transaction(self.web3, current_transaction, new_transaction, ledger)

    def sendTransaction(self, transaction, ledger=None):
        # TODO: move to middleware
        if 'from' not in transaction and is_checksum_address(self.defaultAccount):
            transaction = assoc(transaction, 'from', self.defaultAccount)

        # TODO: move gas estimation in middleware
        if 'gas' not in transaction:
            transaction = assoc(
                transaction,
                'gas',
                get_buffered_gas_estimate(self.web3, transaction, ledger),
            )

        return self.web3.manager.request_blocking(
            "platon_sendTransaction",
            [transaction],
        )

    def sendRawTransaction(self, raw_transaction, ledger=None):
        return self.web3.manager.request_blocking(
            "platon_sendRawTransaction",
            self.set_ledger([raw_transaction], ledger),
        )

    def sign(self, account, data=None, hexstr=None, text=None):
        message_hex = to_hex(data, hexstr=hexstr, text=text)
        return self.web3.manager.request_blocking(
            "platon_sign", [account, message_hex],
        )

    @apply_to_return_value(HexBytes)
    def call(self, transaction, block_identifier=None, ledger=None):
        # TODO: move to middleware
        if 'from' not in transaction and is_checksum_address(self.defaultAccount):
            transaction = assoc(transaction, 'from', self.defaultAccount)

        # TODO: move to middleware
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.web3.manager.request_blocking(
            "platon_call",
            self.set_ledger([transaction, block_identifier], ledger),
        )

    def estimateGas(self, transaction, ledger=None):
        # TODO: move to middleware
        if 'from' not in transaction and is_checksum_address(self.defaultAccount):
            transaction = assoc(transaction, 'from', self.defaultAccount)

        return self.web3.manager.request_blocking(
            "platon_estimateGas",
            self.set_ledger([transaction], ledger),
        )

    def filter(self, filter_params=None, filter_id=None, ledger=None):
        if filter_id and filter_params:
            raise TypeError(
                "Ambiguous invocation: provide either a `filter_params` or a `filter_id` argument. "
                "Both were supplied."
            )
        if is_string(filter_params):
            if filter_params == "latest":
                filter_id = self.web3.manager.request_blocking(
                    "platon_newBlockFilter", self.set_ledger([], ledger),
                )
                return BlockFilter(self.web3, filter_id)
            elif filter_params == "pending":
                filter_id = self.web3.manager.request_blocking(
                    "platon_newPendingTransactionFilter", self.set_ledger([], ledger),
                )
                return TransactionFilter(self.web3, filter_id)
            else:
                raise ValueError(
                    "The filter API only accepts the values of `pending` or "
                    "`latest` for string based filters"
                )
        elif isinstance(filter_params, dict):
            _filter_id = self.web3.manager.request_blocking(
                "platon_newFilter",
                self.set_ledger([filter_params], ledger),
            )
            return LogFilter(self.web3, _filter_id)
        elif filter_id and not filter_params:
            return LogFilter(self.web3, filter_id)
        else:
            raise TypeError("Must provide either filter_params as a string or "
                            "a valid filter object, or a filter_id as a string "
                            "or hex.")

    def getFilterChanges(self, filter_id, ledger=None):
        return self.web3.manager.request_blocking(
            "platon_getFilterChanges", self.set_ledger([filter_id], ledger),
        )

    def getFilterLogs(self, filter_id, ledger=None):
        return self.web3.manager.request_blocking(
            "platon_getFilterLogs", self.set_ledger([filter_id], ledger),
        )

    def getLogs(self, filter_params, ledger=None):
        return self.web3.manager.request_blocking(
            "platon_getLogs", self.set_ledger([filter_params], ledger),
        )

    def uninstallFilter(self, filter_id, ledger=None):
        return self.web3.manager.request_blocking(
            "platon_uninstallFilter", self.set_ledger([filter_id], ledger),
        )

    def wasm_type(self, abi_data):
        for i in range(len(abi_data)):
            if abi_data[i]['type'] == 'Action':
                abi_data[i]['type'] = 'function'
            if abi_data[i]['type'] == 'Event':
                abi_data[i]['type'] = 'event'
                abi_data[i]['anonymous'] = False
                if len(abi_data[i]['input']) > 0:
                    for j in range(len(abi_data[i]['input'])):
                        abi_data[i]['input'][j]['indexed'] = ((j + 1) <= abi_data[i]['topic'])
            if abi_data[i]['type'] == 'struct':
                if 'fields' in abi_data[i] and 'inputs' not in abi_data[i]:
                    abi_data[i]['inputs'] = abi_data[i].pop('fields')
                    if len(abi_data[i]['baseclass']) > 0:
                        for j in range(len(abi_data[i]['baseclass'])):
                            abi_data[i]['inputs'].insert(j, {'name': abi_data[i]['baseclass'][j], 'type': 'struct'})
                    # else :
                    #     abi_data[i]['inputs'].insert(0, {'name': abi_data[i]['baseclass'], 'type': 'struct'})
                    del abi_data[i]['baseclass']
            if abi_data[i]['name'] == 'init':
                abi_data[i]['type'] = 'constructor'
            if 'input' in abi_data[i]:
                abi_data[i]['inputs'] = abi_data[i].pop('input')
            if 'output' in abi_data[i]:
                abi_data[i]['outputs'] = {'name': "", 'type': abi_data[i]['output']}
                del abi_data[i]['output']
        return abi_data

    def contract(self, address=None, **kwargs):
        ContractFactoryClass = kwargs.pop('ContractFactoryClass', self.defaultContractFactory)
        ContractFactory = ContractFactoryClass.factory(self.web3, **kwargs)

        if address:
            return ContractFactory(address)
        else:
            return ContractFactory

    def wasmcontract(self,
                     address=None,
                     **kwargs):
        if 'vmtype' in kwargs:
            if kwargs['vmtype'] == 1:
                abi_data = copy.deepcopy(kwargs['abi'])
                kwargs['abi'] = self.wasm_type(abi_data)
            # del kwargs['vmtype']
        ContractFactoryClass = kwargs.pop('ContractFactoryClass', self.defaultContractFactory)
        # 若kwargs中有'ContractFactoryClass'这个key，则返回对应的value值，若无这个key，则返回self.defaultContractFactory
        ContractFactory = ContractFactoryClass.factory(self.web3, **kwargs)

        if address:
            return ContractFactory(address)
        else:
            return ContractFactory

    def setContractFactory(self, contractFactory):
        self.defaultContractFactory = contractFactory

    # @deprecated_in_v5
    # def getCompilers(self):
    #     return self.web3.manager.request_blocking("platon_getCompilers", [])

    # def getWork(self):
    #     return self.web3.manager.request_blocking("platon_getWork", [])

    def generateGasPrice(self, transaction_params=None):
        if self.gasPriceStrategy:
            return self.gasPriceStrategy(self.web3, transaction_params)

    def setGasPriceStrategy(self, gas_price_strategy):
        self.gasPriceStrategy = gas_price_strategy

    # add to platon
    def analyzeReceiptByHash(self, tx_hash, ledger=None):
        receipt = self.waitForTransactionReceipt(tx_hash, ledger)
        return self.analyzeReceipt(receipt)

    def analyzeReceipt(self, transaction_receipt):
        return self.web3.analyzeReceipt(transaction_receipt)

    def ecrecover(self, block_identifier):
        block = self.getBlock(block_identifier)
        extra = block.proofOfAuthorityData[0:32]
        sign = block.proofOfAuthorityData[32:]
        miner = bech32_address_bytes(remove_0x_prefix(block.miner))
        raw_data = [bytes.fromhex(remove_0x_prefix(block.parentHash.hex())),
                    miner,
                    bytes.fromhex(remove_0x_prefix(block.stateRoot.hex())),
                    bytes.fromhex(remove_0x_prefix(block.transactionsRoot.hex())),
                    bytes.fromhex(remove_0x_prefix(block.receiptsRoot.hex())),
                    bytes.fromhex(remove_0x_prefix(block.logsBloom.hex())),
                    block.number,
                    block.gasLimit,
                    block.gasUsed,
                    block.timestamp,
                    extra,
                    bytes.fromhex(remove_0x_prefix(block.nonce))
                    ]
        message_hash = sha3.keccak_256(rlp.encode(raw_data)).digest()
        hash_bytes = HexBytes(message_hash)
        signature_bytes = HexBytes(sign)
        signature_bytes_standard = to_standard_signature_bytes(signature_bytes)
        signature_obj = self.account._keys.Signature(signature_bytes=signature_bytes_standard)
        return remove_0x_prefix(signature_obj.recover_public_key_from_msg_hash(hash_bytes).to_hex())
