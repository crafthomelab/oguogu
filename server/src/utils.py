from typing import Any, Dict, Union
from hexbytes import HexBytes
from web3 import Web3, AsyncWeb3
from eth_account import Account
from eth_account.messages import encode_defunct
from web3.contract.contract import ContractFunction
from web3.types import TxReceipt

    
def create_hash(**kwargs) -> bytes:
    """ 챌린지 해시를 생성합니다 """
    data_string = ''.join(f'{key}:{value}' for key, value in sorted(kwargs.items()))
    data_bytes = data_string.encode('utf-8')
    return to_bytes32(Web3.keccak(data_bytes))


def create_signature(signer: Account, hash_value: Union[bytes, str]) -> HexBytes:
    """ 챌린지 해시에 서명합니다. """
    if isinstance(hash_value, str):
        message = encode_defunct(hexstr=hash_value)
    else:
        message = encode_defunct(hash_value)
    return signer.sign_message(message).signature


def verify_signature(
    signer_address: str, 
    signature: bytes, 
    hash_value: bytes
) -> bool:
    """ 서명을 검증합니다 """
    message = encode_defunct(hash_value)
    if isinstance(signature, str):
        signature = HexBytes(signature)
    recovered_address = Account.recover_message(message, signature=signature)
    return Web3.to_checksum_address(recovered_address) == Web3.to_checksum_address(signer_address)


def verify_hash(challenge_data: Dict[str, Any], hash: bytes) -> bool:
    """ 챌린지 해시를 검증합니다 """    
    return create_hash(**challenge_data) == hash


def to_bytes32(value: Union[Dict, str, int, bytes]) -> bytes:
    """ bytes32 타입으로 변환합니다 """
    if isinstance(value, str):
        return value.encode("utf-8").ljust(32, b"\0")
    elif isinstance(value, int):
        return value.to_bytes(32, byteorder='big')
    elif isinstance(value, bytes):
        return value.ljust(32, b"\0")
    else:
        raise ValueError(f"Invalid type: {type(value)}")



def send_transaction(
    web3: Web3, 
    account: Account, 
    func: ContractFunction
) -> TxReceipt:
    nonce = web3.eth.get_transaction_count(account.address)
    tx = func.build_transaction({'from': account.address, 'nonce': nonce})
    signed_txn = account.sign_transaction(tx)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
    
    if tx_receipt.status != 1:
        raise Exception(f"Failed to send transaction.. status: {tx_receipt.status} tx_hash: {txn_hash}")
    
    return tx_receipt
    
    
async def asend_transaction(
    web3: AsyncWeb3, 
    account: Account, 
    func: ContractFunction
) -> TxReceipt:
    nonce = await web3.eth.get_transaction_count(account.address)
    tx = func.build_transaction({ 'from': account.address, 'nonce': nonce })
    signed_txn = account.sign_transaction(tx)
    txn_hash = await web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = await web3.eth.wait_for_transaction_receipt(txn_hash)
    
    if tx_receipt.status != 1:
        raise Exception(f"Failed to send transaction.. status: {tx_receipt.status} tx_hash: {txn_hash}")
    
    return tx_receipt
