from typing import Any, Dict, Union
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct
    
def create_hash(**kwargs) -> bytes:
    """ 챌린지 해시를 생성합니다 """
    data_string = ''.join(f'{key}:{value}' for key, value in sorted(kwargs.items()))
    data_bytes = data_string.encode('utf-8')
    return to_bytes32(Web3.keccak(data_bytes))


def create_signature(signer: Account, hash_value: bytes) -> bytes:
    """ 챌린지 해시에 서명합니다. """
    message = encode_defunct(hash_value)
    return signer.sign_message(message).signature


def verify_signature(
    signer_address: str, 
    signature: bytes, 
    hash_value: bytes
) -> bool:
    """ 서명을 검증합니다 """
    message = encode_defunct(hash_value)
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
