import math

from platone.module import Module
from platone.utils.error_code import ERROR_INFO
from platone.utils.threads import (
    Timeout,
)
from platone.utils.toolz import (
    assoc,
    curry,
    merge,
)

from hexbytes import HexBytes

from platone.packages.platone_account.account import Account
from platone.packages.platone_keys.datatypes import PrivateKey

VALID_TRANSACTION_PARAMS = [
    'from',
    'to',
    'gas',
    'gasPrice',
    'value',
    'data',
    'nonce',
    'chainId',
]

TRANSACTION_DEFAULTS = {
    'value': 0,
    'data': b'',
    'gas': lambda web3, tx, ledger: web3.platone.estimateGas(tx, ledger),
    'gasPrice': lambda web3, tx, ledger: web3.platone.generateGasPrice(tx) or web3.platone.gasPrice(ledger),
    'chainId': lambda web3, tx, ledger: web3.chainId,
}


def call_obj(obj, from_address, to_address, data):
    # to_address = obj.web3.toChecksumAddress(to_address)
    if from_address is None:
        return obj.web3.platon.call({"to": to_address, "data": data})
    # from_address = obj.web3.toChecksumAddress(from_address)
    return obj.web3.platon.call({"from": from_address, "to": to_address, "data": data})


def send_obj_transaction(obj: Module, txn, private_key, ledger=None):
    if txn.get('nonce') is None:
        from_address = Account.privateKeyToAccount(private_key, obj.web3.net_type, obj.web3.encryption_mode).address
        txn['from'] = from_address
        txn['nonce'] = obj.web3.platone.getTransactionCount(from_address, ledger=ledger)
    signed_transaction_dict = obj.web3.platone.account.signTransaction(
        txn, private_key, net_type=obj.web3.net_type, mode=obj.web3.encryption_mode
    )
    signed_data = signed_transaction_dict.rawTransaction
    tx_hash = HexBytes(obj.web3.platone.sendRawTransaction(signed_data, ledger=ledger)).hex()
    if hasattr(obj, 'is_wait_receipt') and obj.is_wait_receipt:
        code = obj.web3.platone.analyzeReceiptByHash(tx_hash, ledger=ledger)
        code_info = ERROR_INFO.get(code, 'Unknown code info')
        return {'hash': tx_hash, 'code': code, 'code_info': code_info}
    return {'hash': tx_hash, 'code': None, 'code_info': None}


@curry
def fill_nonce(web3, transaction):
    if 'from' in transaction and 'nonce' not in transaction:
        return assoc(
            transaction,
            'nonce',
            web3.platone.getTransactionCount(
                transaction['from'],
                block_identifier='pending'))
    else:
        return transaction


@curry
def fill_transaction_defaults(web3, transaction, ledger=None):
    '''
    if web3 is None, fill as much as possible while offline
    '''
    defaults = {}
    for key, default_getter in TRANSACTION_DEFAULTS.items():
        if key not in transaction:
            if callable(default_getter):
                if web3 is not None:
                    default_val = default_getter(web3, transaction, ledger)
                else:
                    raise ValueError("You must specify %s in the transaction" % key)
            else:
                default_val = default_getter
            defaults[key] = default_val
    return merge(defaults, transaction)


def wait_for_transaction_receipt(web3, txn_hash, ledger=None, timeout=120, poll_latency=0.1):
    with Timeout(timeout) as _timeout:
        while True:
            txn_receipt = web3.platone.getTransactionReceipt(txn_hash, ledger)
            if txn_receipt is not None:
                break
            _timeout.sleep(poll_latency)
    return txn_receipt


def get_block_gas_limit(web3, block_identifier=None, ledger=None):
    if block_identifier is None:
        block_identifier = web3.platone.blockNumber(ledger)
    block = web3.platone.getBlock(block_identifier, ledger=ledger)
    return block['gasLimit']


def get_buffered_gas_estimate(web3, transaction, ledger=None, gas_buffer=100000):
    gas_estimate_transaction = dict(**transaction)

    gas_estimate = web3.platone.estimateGas(gas_estimate_transaction, ledger)

    gas_limit = get_block_gas_limit(web3, ledger=ledger)

    if gas_estimate > gas_limit:
        raise ValueError(
            "Contract does not appear to be deployable within the "
            "current network gas limits.  Estimated: {0}. Current gas "
            "limit: {1}".format(gas_estimate, gas_limit)
        )

    return min(gas_limit, gas_estimate + gas_buffer)


def get_required_transaction(web3, transaction_hash, ledger=None):
    current_transaction = web3.platone.getTransaction(transaction_hash, ledger=None)
    if not current_transaction:
        raise ValueError('Supplied transaction with hash {} does not exist'
                         .format(transaction_hash))
    return current_transaction


def extract_valid_transaction_params(transaction_params):
    extracted_params = {key: transaction_params[key]
                        for key in VALID_TRANSACTION_PARAMS if key in transaction_params}

    if extracted_params.get('data') is not None:
        if transaction_params.get('input') is not None:
            if extracted_params['data'] != transaction_params['input']:
                msg = 'failure to handle this transaction due to both "input: {}" and'
                msg += ' "data: {}" are populated. You need to resolve this conflict.'
                err_vals = (transaction_params['input'], extracted_params['data'])
                raise AttributeError(msg.format(*err_vals))
            else:
                return extracted_params
        else:
            return extracted_params
    elif extracted_params.get('data') is None:
        if transaction_params.get('input') is not None:
            return assoc(extracted_params, 'data', transaction_params['input'])
        else:
            return extracted_params
    else:
        raise Exception("Unreachable path: transaction's 'data' is either set or not set")


def assert_valid_transaction_params(transaction_params):
    for param in transaction_params:
        if param not in VALID_TRANSACTION_PARAMS:
            raise ValueError('{} is not a valid transaction parameter'.format(param))


def prepare_replacement_transaction(web3, current_transaction, new_transaction):
    if current_transaction['blockHash'] != HexBytes(
            '0x0000000000000000000000000000000000000000000000000000000000000000'):
        raise ValueError('Supplied transaction with hash {} has already been mined'
                         .format(current_transaction['hash']))

    if 'nonce' in new_transaction:
        if isinstance(new_transaction['nonce'], int):
            if new_transaction['nonce'] != int(current_transaction['nonce'], 16):
                raise ValueError('Supplied nonce in new_transaction must match the pending transaction')
        else:
            if '0x' in new_transaction['nonce']:
                if int(new_transaction['nonce'], 16) != int(current_transaction['nonce'], 16):
                    raise ValueError('Supplied nonce in new_transaction must match the pending transaction')

    if 'nonce' not in new_transaction:
        new_transaction = assoc(new_transaction, 'nonce', current_transaction['nonce'])

    if 'gasPrice' in new_transaction:
        if new_transaction['gasPrice'] <= current_transaction['gasPrice']:
            raise ValueError('Supplied gas price must exceed existing transaction gas price')
    else:
        generated_gas_price = web3.platone.generateGasPrice(new_transaction)
        minimum_gas_price = int(current_transaction['gasPrice'] * 1.1)
        if generated_gas_price and generated_gas_price > minimum_gas_price:
            new_transaction = assoc(new_transaction, 'gasPrice', generated_gas_price)
        else:
            new_transaction = assoc(new_transaction, 'gasPrice', minimum_gas_price)

    return new_transaction


def replace_transaction(web3, current_transaction, new_transaction, ledger=None):
    new_transaction = prepare_replacement_transaction(web3, current_transaction, new_transaction)
    return web3.platone.sendTransaction(new_transaction, ledger)
