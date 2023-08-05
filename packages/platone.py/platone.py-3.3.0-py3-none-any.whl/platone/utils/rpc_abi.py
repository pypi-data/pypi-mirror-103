from platone.packages.eth_utils import (
    to_dict,
)

from platone.utils.abi import (
    map_abi_data,
)
from platone.utils.formatters import (
    apply_formatter_at_index,
)
from platone.utils.toolz import (
    curry,
)

TRANSACTION_PARAMS_ABIS = {
    'data': 'bytes',
    'from': 'address',
    'gas': 'uint',
    'gasPrice': 'uint',
    'nonce': 'uint',
    'to': 'address',
    'value': 'uint',
}

FILTER_PARAMS_ABIS = {
    'to': 'address',
    'address': 'address[]',
}

TRACE_PARAMS_ABIS = {
    'to': 'address',
    'from': 'address',
}

RPC_ABIS = {
    # platon
    # 'platon_call': ['ledger', TRANSACTION_PARAMS_ABIS],
    # 'platon_estimateGas': ['ledger', TRANSACTION_PARAMS_ABIS],
    'platon_getBalance': ['ledger', 'address', None],
    'platon_getBlockByHash': ['ledger', 'bytes32', 'bool'],
    'platon_getBlockTransactionCountByHash': ['ledger', 'bytes32'],
    'platon_getCode': ['ledger', 'address', None],
    'platon_getLogs': ['ledger', FILTER_PARAMS_ABIS],
    'platon_getStorageAt': ['ledger', 'address', 'uint', None],
    'platon_getTransactionByBlockHashAndIndex': ['ledger', 'bytes32', 'uint'],
    'platon_getTransactionByHash': ['ledger', 'bytes32'],
    'platon_getTransactionCount': ['ledger', 'address', None],
    'platon_getTransactionReceipt': ['ledger', 'bytes32'],
    'platon_getUncleCountByBlockHash': ['ledger', 'bytes32'],
    'platon_newFilter': ['ledger', FILTER_PARAMS_ABIS],
    'platon_sendRawTransaction': ['ledger', 'bytes'],
    'platon_sendTransaction': ['ledger', TRANSACTION_PARAMS_ABIS],
    'platon_sign': ['ledger', 'address', 'bytes'],
    # personal
    'personal_sendTransaction': ['ledger', TRANSACTION_PARAMS_ABIS],
    'personal_lockAccount': ['ledger', 'address'],
    'personal_unlockAccount': ['ledger', 'address', None, None],
    'personal_sign': ['ledger', None, 'address', None],
    'trace_call': ['ledger', TRACE_PARAMS_ABIS],
}


@curry
def apply_abi_formatters_to_dict(normalizers, abi_dict, data):
    fields = list(set(abi_dict.keys()) & set(data.keys()))
    formatted_values = map_abi_data(
        normalizers,
        [abi_dict[field] for field in fields],
        [data[field] for field in fields],
    )
    formatted_dict = dict(zip(fields, formatted_values))
    return dict(data, **formatted_dict)


@to_dict
def abi_request_formatters(normalizers, abis):
    for method, abi_types in abis.items():
        if isinstance(abi_types, list):
            yield method, map_abi_data(normalizers, abi_types)
        elif isinstance(abi_types, dict):
            single_dict_formatter = apply_abi_formatters_to_dict(normalizers, abi_types)
            yield method, apply_formatter_at_index(single_dict_formatter, 0)
        else:
            raise TypeError("ABI definitions must be a list or dictionary, got %r" % abi_types)
